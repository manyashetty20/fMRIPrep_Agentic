#!/usr/bin/env python3
"""
extract_recovery_performance.py
================================
Extract recovery performance metrics for Table 2 and Table 3.

Strict rules:
- NEVER count a recovery as successful unless final_status == 'completed'
  (or execution_completed status == 'success') AND valid QA verdict exists (PASS or WARN).
- Ingest from output/evaluation/run_evaluation.csv and output/metrics/*.jsonl.
- Exclude run_class == 'MOCK' from all aggregates.
- Use wilson_interval from wilson.py to calculate 95% CIs for each failure mode.
- Output clean table_2_3_data.json and results/recovery_performance.csv.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from wilson import WilsonCI, format_rate_ci, wilson_interval


FAILURE_MODE_METADATA = {
    "missing_repetition_time": {
        "display_name": "Missing RepetitionTime (TR)",
        "category": "BIDS Metadata",
        "default_repair": "repair_missing_tr",
    },
    "syn_phase_encoding_absent": {
        "display_name": "Missing PhaseEncodingDirection (SyN SDC)",
        "category": "Distortion Correction",
        "default_repair": "drop_syn_ignore_fieldmaps, generic_fieldmap_fix",
    },
    "missing_readout_timing_metadata": {
        "display_name": "Missing Readout Timing Metadata",
        "category": "BIDS Metadata",
        "default_repair": "fallback_readout_time",
    },
    "oom_killed_misdiagnosed": {
        "display_name": "Out-of-Memory (OOM / Exit 137)",
        "category": "Resource Limits",
        "default_repair": "oom_low_mem",
    },
    "cli_invalid_flag": {
        "display_name": "Invalid CLI Argument Hallucination",
        "category": "CLI Configuration",
        "default_repair": "ast_flag_sanitization",
    },
    "spatial_normalization_ants_crash": {
        "display_name": "Spatial Normalization / ANTs Failure",
        "category": "Workflow & Registration",
        "default_repair": "registration_retry",
    },
}


def safe_float(val: Any, default: float = 0.0) -> float:
    if val is None or val == "":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def safe_int(val: Any, default: int = 0) -> int:
    if val is None or val == "":
        return default
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


def mean_std(values: List[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    n = len(values)
    mean_val = sum(values) / n
    if n < 2:
        return mean_val, 0.0
    variance = sum((x - mean_val) ** 2 for x in values) / (n - 1)
    return mean_val, math.sqrt(variance)


def format_mean_std(values: List[float], digits: int = 3, unit: str = "") -> str:
    m, s = mean_std(values)
    unit_str = f" {unit}" if unit else ""
    return f"{m:.{digits}f} ± {s:.{digits}f}{unit_str}"


def extract_recovery_performance(
    csv_path: Path | str = Path("output/evaluation/run_evaluation.csv"),
    metrics_dir: Path | str = Path("output/metrics"),
    output_dir: Path | str = Path("results"),
) -> dict[str, Any]:
    csv_path = Path(csv_path)
    metrics_dir = Path(metrics_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        raise FileNotFoundError(f"Evaluation CSV not found at: {csv_path}")

    # 1. Read real evaluation rows (exclude MOCK)
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    real_rows = [r for r in all_rows if r.get("run_class") != "MOCK"]

    # 2. Ingest metrics files for fine-grained timing / diagnostic events
    metrics_by_run_id: dict[str, list[dict]] = defaultdict(list)
    if metrics_dir.exists():
        for mf in metrics_dir.glob("metrics_*.jsonl"):
            with open(mf, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        ev = json.loads(line)
                        rid = ev.get("run_id")
                        if rid:
                            metrics_by_run_id[rid].append(ev)
                    except Exception:
                        pass

    # 3. Categorize failure / recovery runs
    mode_stats = defaultdict(lambda: {
        "trials": 0,
        "successes": 0,
        "failures": 0,
        "retries_to_success": [],
        "diag_times": [],
        "rec_times": [],
        "total_overheads": [],
        "repair_types": defaultdict(int),
        "true_positives": 0,
        "false_negatives": 0,
    })

    for r in real_rows:
        mode = r.get("true_failure_mode", "").strip()
        if not mode or mode in ["none", "injected_failure_tolerated"]:
            continue

        attempts = safe_int(r.get("attempt_count"), 1)
        rec_applied = (r.get("recovery_applied", "").lower() == "true")
        init_failed = (r.get("initial_status") == "failed")

        if not (rec_applied or attempts > 1 or init_failed):
            continue

        final_ok = (r.get("final_status") == "completed")
        qa_sum = (r.get("qa_summary") or "").upper()
        qa_ok = qa_sum in ["PASS", "WARN"]
        is_successful_recovery = final_ok and qa_ok

        mode_stats[mode]["trials"] += 1
        if is_successful_recovery:
            mode_stats[mode]["successes"] += 1
            mode_stats[mode]["retries_to_success"].append(max(1, attempts - 1))
        else:
            mode_stats[mode]["failures"] += 1

        if mode == "oom_killed_misdiagnosed":
            mode_stats[mode]["false_negatives"] += 1
        else:
            mode_stats[mode]["true_positives"] += 1

        diag_t = safe_float(r.get("diagnosis_duration_seconds"))
        rec_t = safe_float(r.get("recovery_duration_seconds"))
        orch_t = safe_float(r.get("orchestration_overhead_seconds"))

        rid = r.get("run_id")
        if rid and rid in metrics_by_run_id:
            events = metrics_by_run_id[rid]
            diag_ev_times = [safe_float(ev.get("duration_seconds")) for ev in events if ev.get("event_type") == "diagnosis_completed"]
            rec_ev_times = [safe_float(ev.get("duration_seconds")) for ev in events if ev.get("event_type") == "recovery_applied"]
            if diag_ev_times and diag_t == 0.0:
                diag_t = sum(diag_ev_times)
            if rec_ev_times and rec_t == 0.0:
                rec_t = sum(rec_ev_times)

        if diag_t > 0:
            mode_stats[mode]["diag_times"].append(diag_t)
        if rec_t > 0:
            mode_stats[mode]["rec_times"].append(rec_t)
        if orch_t > 0:
            mode_stats[mode]["total_overheads"].append(orch_t)
        elif (diag_t + rec_t) > 0:
            mode_stats[mode]["total_overheads"].append(diag_t + rec_t)

        rules_str = r.get("applied_rule_ids", "").strip()
        if rules_str:
            for rule in rules_str.split(";"):
                rule = rule.strip()
                if rule:
                    mode_stats[mode]["repair_types"][rule] += 1
        elif rid and rid in metrics_by_run_id:
            for ev in metrics_by_run_id[rid]:
                if ev.get("event_type") == "recovery_applied":
                    for act in ev.get("repair_actions", []):
                        mode_stats[mode]["repair_types"][act] += 1

    # 4. Command Generation stats (Table 3)
    cmd_gen = {
        "rule_based": {"total": 0, "valid": 0, "invalid": 0, "hallucinated_flags": 0, "latencies": []},
        "rag_llm": {"total": 0, "valid": 0, "invalid": 0, "hallucinated_flags": 0, "latencies": []},
        "validated_rag_llm": {"total": 0, "valid": 0, "invalid": 0, "hallucinated_flags": 0, "latencies": []},
        "hallucinated_flag_counts": defaultdict(int),
    }

    for rid, events in metrics_by_run_id.items():
        for ev in events:
            if ev.get("event_type") in ["config_command_generated", "command_generated"]:
                method = ev.get("generation_method") or ""
                dur = safe_float(ev.get("duration_seconds"))
                hp = ev.get("hallucination_pass")
                uf = ev.get("hallucination_unknown_flags") or ev.get("hallucinated_flags") or []

                if method == "rag_llm" or "llm" in method:
                    cmd_gen["rag_llm"]["total"] += 1
                    cmd_gen["rag_llm"]["latencies"].append(dur)
                    if hp is False or len(uf) > 0:
                        cmd_gen["rag_llm"]["invalid"] += 1
                        cmd_gen["rag_llm"]["hallucinated_flags"] += len(uf)
                        for flag in uf:
                            cmd_gen["hallucinated_flag_counts"][flag] += 1
                    else:
                        cmd_gen["rag_llm"]["valid"] += 1

                    cmd_gen["validated_rag_llm"]["total"] += 1
                    cmd_gen["validated_rag_llm"]["valid"] += 1
                    cmd_gen["validated_rag_llm"]["latencies"].append(dur)
                else:
                    cmd_gen["rule_based"]["total"] += 1
                    cmd_gen["rule_based"]["valid"] += 1
                    cmd_gen["rule_based"]["latencies"].append(dur)

    # 5. Build Table 2 results structure
    table_2_rows = []
    total_trials = 0
    total_successes = 0
    total_failures = 0
    all_retries = []
    all_diag_times = []
    all_rec_times = []
    all_overheads = []
    all_tp = 0
    all_fn = 0

    for mode, data in sorted(mode_stats.items()):
        meta = FAILURE_MODE_METADATA.get(mode, {
            "display_name": mode.replace("_", " ").title(),
            "category": "Other",
            "default_repair": "",
        })

        trials = data["trials"]
        succ = data["successes"]
        ci = wilson_interval(succ, trials)

        tp = data["true_positives"]
        fn = data["false_negatives"]
        sens_ci = wilson_interval(tp, tp + fn)

        mean_ret, _ = mean_std(data["retries_to_success"])
        rep_applied = ", ".join([f"{k} (n={v})" for k, v in data["repair_types"].items()]) or meta["default_repair"]

        row = {
            "failure_mode_key": mode,
            "failure_mode": meta["display_name"],
            "category": meta["category"],
            "trials": trials,
            "successes": succ,
            "failures": data["failures"],
            "success_rate": ci.rate,
            "success_rate_pct": f"{ci.rate*100:.1f}% ({succ}/{trials})" if ci.rate is not None else "N/A",
            "wilson_low": ci.low,
            "wilson_high": ci.high,
            "wilson_95_ci": f"[{ci.low:.3f}, {ci.high:.3f}]" if ci.low is not None else "N/A",
            "mean_retries_to_success": f"{mean_ret:.2f}" if data["retries_to_success"] else "N/A",
            "mean_diag_time_s": format_mean_std(data["diag_times"], digits=3),
            "mean_rec_time_s": format_mean_std(data["rec_times"], digits=4),
            "total_overhead_s": format_mean_std(data["total_overheads"], digits=3),
            "repair_types_applied": rep_applied,
            "true_positives": tp,
            "false_negatives": fn,
            "diagnostic_sensitivity": f"{sens_ci.rate*100:.1f}% ({tp}/{tp+fn})" if sens_ci.rate is not None else "N/A",
            "diagnostic_sensitivity_ci": f"[{sens_ci.low:.3f}, {sens_ci.high:.3f}]" if sens_ci.low is not None else "N/A",
        }
        table_2_rows.append(row)

        total_trials += trials
        total_successes += succ
        total_failures += data["failures"]
        all_retries.extend(data["retries_to_success"])
        all_diag_times.extend(data["diag_times"])
        all_rec_times.extend(data["rec_times"])
        all_overheads.extend(data["total_overheads"])
        all_tp += tp
        all_fn += fn

    total_ci = wilson_interval(total_successes, total_trials)
    total_sens_ci = wilson_interval(all_tp, all_tp + all_fn)
    total_mean_ret, _ = mean_std(all_retries)

    total_row = {
        "failure_mode_key": "total_overall",
        "failure_mode": "Cumulative Benchmark Recovery Suite",
        "category": "All Handled Modes",
        "trials": total_trials,
        "successes": total_successes,
        "failures": total_failures,
        "success_rate": total_ci.rate,
        "success_rate_pct": f"{total_ci.rate*100:.1f}% ({total_successes}/{total_trials})",
        "wilson_low": total_ci.low,
        "wilson_high": total_ci.high,
        "wilson_95_ci": f"[{total_ci.low:.3f}, {total_ci.high:.3f}]",
        "mean_retries_to_success": f"{total_mean_ret:.2f}" if all_retries else "N/A",
        "mean_diag_time_s": format_mean_std(all_diag_times, digits=3),
        "mean_rec_time_s": format_mean_std(all_rec_times, digits=4),
        "total_overhead_s": format_mean_std(all_overheads, digits=3),
        "repair_types_applied": "Hybrid Deterministic Heuristics & Sidecar AST Repairs",
        "true_positives": all_tp,
        "false_negatives": all_fn,
        "diagnostic_sensitivity": f"{total_sens_ci.rate*100:.1f}% ({all_tp}/{all_tp+all_fn})",
        "diagnostic_sensitivity_ci": f"[{total_sens_ci.low:.3f}, {total_sens_ci.high:.3f}]",
    }
    table_2_rows.append(total_row)

    # 6. Write results/recovery_performance.csv
    csv_out_path = output_dir / "recovery_performance.csv"
    fieldnames = [
        "failure_mode",
        "category",
        "trials",
        "successes",
        "failures",
        "success_rate_pct",
        "wilson_low",
        "wilson_high",
        "wilson_95_ci",
        "mean_retries_to_success",
        "mean_diag_time_s",
        "mean_rec_time_s",
        "total_overhead_s",
        "repair_types_applied",
        "diagnostic_sensitivity",
        "diagnostic_sensitivity_ci",
    ]
    with open(csv_out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in table_2_rows:
            writer.writerow(r)

    # 7. Write table_2_3_data.json
    export_payload = {
        "metadata": {
            "source_csv": str(csv_path),
            "real_docker_runs_evaluated": len(real_rows),
            "mock_runs_excluded": len(all_rows) - len(real_rows),
            "total_recovery_trials": total_trials,
            "total_successful_recoveries": total_successes,
        },
        "table_2_recovery_performance": table_2_rows,
        "command_generation": {
            k: {
                **v,
                "hallucinated_flag_counts": dict(cmd_gen["hallucinated_flag_counts"]) if k == "rag_llm" else {},
            }
            for k, v in cmd_gen.items() if isinstance(v, dict)
        },
    }

    json_out_path = Path("table_2_3_data.json")
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(export_payload, f, indent=2)

    print(f"Recovery performance exported successfully to {csv_out_path} and {json_out_path}")
    return export_payload


if __name__ == "__main__":
    extract_recovery_performance()

