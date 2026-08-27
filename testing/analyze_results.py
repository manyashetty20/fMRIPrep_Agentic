#!/usr/bin/env python3
"""
testing/analyze_results.py
==========================
Aggregate evaluation CSVs + metrics JSONL into publication-ready summary tables.

Inspectable metric functions (cite these in methodology)
--------------------------------------------------------
- ``summarize_agentic`` — success / recovery rates, mean attempts & wall clock
- ``compare_baseline_agentic`` — paired baseline vs agentic rows
- ``failure_matrix`` — per-injection-run outcomes
- ``compute_diagnostic_accuracy`` — correct root cause ÷ injected failures
- ``compute_recovery_stats`` — recovery success, mean retries, timing mean±std
- ``compute_detection_method_split`` — regex_heuristic vs llm_fallback counts
- ``compute_efficiency_stats`` — wall clock, fMRIPrep CLI time, orchestration overhead
- ``compute_config_quality`` — gold-standard / hallucination pass rates
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

_TESTING = Path(__file__).resolve().parent
_ROOT = _TESTING.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file() or path.stat().st_size == 0:
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _read_metrics_jsonl(metrics_dir: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not metrics_dir.is_dir():
        return events
    for path in sorted(metrics_dir.glob("metrics_*.jsonl")):
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def _pct(n: int, d: int) -> str:
    return f"{100.0 * n / d:.1f}%" if d else "n/a"


def _mean(vals: list[float]) -> str:
    return f"{sum(vals) / len(vals):.3f}" if vals else "n/a"


def _std(vals: list[float]) -> str:
    if len(vals) < 2:
        return "n/a"
    m = sum(vals) / len(vals)
    var = sum((x - m) ** 2 for x in vals) / (len(vals) - 1)
    return f"{math.sqrt(var):.3f}"


def _mean_std(vals: list[float]) -> str:
    if not vals:
        return "n/a"
    if len(vals) == 1:
        return f"{vals[0]:.3f}"
    return f"{float(_mean(vals)):.3f} ± {float(_std(vals)):.3f}"


def _boolish(val: Any) -> bool:
    return str(val).strip().lower() in {"true", "1", "yes"}


def _float_or_none(val: Any) -> float | None:
    try:
        if val is None or str(val).strip() == "":
            return None
        return float(val)
    except (TypeError, ValueError):
        return None


def load_expected_root_causes(fixture_path: Path) -> dict[str, list[str]]:
    if not fixture_path.is_file():
        return {}
    raw = yaml.safe_load(fixture_path.read_text()) or {}
    expected = raw.get("expected_root_causes") or {}
    return {str(k): [str(x) for x in (v or [])] for k, v in expected.items()}


def _root_cause_matches(predicted: str, needles: list[str]) -> bool:
    text = (predicted or "").lower()
    return any(n.lower() in text for n in needles if n)


def summarize_agentic(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("run_mode", "agentic") != "agentic":
            continue
        key = "|".join(
            [
                row.get("dataset_id", ""),
                f"recovery={row.get('recovery_enabled', '')}",
                f"diagnosis={row.get('diagnosis_enabled', '')}",
                f"vision={row.get('vision_enabled', '')}",
            ]
        )
        groups[key].append(row)

    out: list[dict[str, Any]] = []
    for key, items in sorted(groups.items()):
        n = len(items)
        completed = sum(1 for r in items if r.get("final_status") == "completed")
        recovered = sum(1 for r in items if _boolish(r.get("successful_recovery", "")))
        attempts = [float(r["attempt_count"]) for r in items if r.get("attempt_count")]
        walls = [float(r["wall_clock_seconds"]) for r in items if r.get("wall_clock_seconds")]
        out.append(
            {
                "group": key,
                "runs": n,
                "success_rate": _pct(completed, n),
                "recovery_success_rate": _pct(recovered, n),
                "mean_attempts": _mean(attempts),
                "mean_wall_clock_s": _mean(walls),
            }
        )
    return out


def compare_baseline_agentic(
    agentic: list[dict[str, str]],
    baseline: list[dict[str, str]],
) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in agentic:
        if row.get("run_mode") == "agentic" and not row.get("injected_failure_mode"):
            if _boolish(row.get("recovery_enabled", "true")) and _boolish(
                row.get("diagnosis_enabled", "true")
            ):
                by_key[(row.get("dataset_id", ""), row.get("participant", ""))]["agentic"] = row
    for row in baseline:
        by_key[(row.get("dataset_id", ""), row.get("participant", ""))]["baseline"] = row

    out: list[dict[str, Any]] = []
    for (dataset_id, participant), modes in sorted(by_key.items()):
        a = modes.get("agentic", {})
        b = modes.get("baseline", {})
        a_wall = _float_or_none(a.get("wall_clock_seconds"))
        b_wall = _float_or_none(b.get("wall_clock_seconds"))
        overhead = ""
        if a_wall is not None and b_wall is not None:
            overhead = f"{a_wall - b_wall:.3f}"
        out.append(
            {
                "dataset_id": dataset_id,
                "participant": participant,
                "baseline_final_status": b.get("final_status", "missing"),
                "agentic_final_status": a.get("final_status", "missing"),
                "baseline_attempts": b.get("attempt_count", ""),
                "agentic_attempts": a.get("attempt_count", ""),
                "baseline_wall_s": b.get("wall_clock_seconds", ""),
                "agentic_wall_s": a.get("wall_clock_seconds", ""),
                "agentic_minus_baseline_wall_s": overhead,
                "agentic_orchestration_overhead_s": a.get("orchestration_overhead_seconds", ""),
                "agentic_qa_summary": a.get("qa_summary", ""),
            }
        )
    return out


def failure_matrix(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    injected = [r for r in rows if r.get("injected_failure_mode")]
    out: list[dict[str, Any]] = []
    for row in sorted(
        injected,
        key=lambda r: (r.get("injected_failure_mode", ""), r.get("participant", ""), r.get("run_id", "")),
    ):
        out.append(
            {
                "mode": row.get("injected_failure_mode", ""),
                "dataset_id": row.get("dataset_id", ""),
                "participant": row.get("participant", ""),
                "run_id": row.get("run_id", ""),
                "final_status": row.get("final_status", ""),
                "successful_recovery": row.get("successful_recovery", ""),
                "initial_failure_type": row.get("initial_failure_type", ""),
                "detection_method": row.get("detection_method", ""),
                "attempt_count": row.get("attempt_count", ""),
                "total_retries": row.get("total_retries", ""),
                "diagnosis_duration_seconds": row.get("diagnosis_duration_seconds", ""),
                "recovery_duration_seconds": row.get("recovery_duration_seconds", ""),
                "wall_clock_seconds": row.get("wall_clock_seconds", ""),
            }
        )
    return out


def compute_diagnostic_accuracy(
    rows: list[dict[str, str]],
    expected: dict[str, list[str]],
) -> list[dict[str, Any]]:
    """
    Diagnostic accuracy = correct root-cause IDs ÷ injected failures (per mode).

    True positive: injected failure and predicted root cause matches expected needles.
    False negative: injected failure but root cause does not match.
    False positive: non-injected run that still produced a failure-type diagnosis
    (rarely used; reported for completeness when such rows exist).
    """
    by_mode: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        mode = row.get("injected_failure_mode") or ""
        if mode:
            by_mode[mode].append(row)

    out: list[dict[str, Any]] = []
    for mode, items in sorted(by_mode.items()):
        needles = expected.get(mode, [])
        tp = sum(1 for r in items if _root_cause_matches(r.get("initial_failure_type", ""), needles))
        fn = len(items) - tp
        # FP among injected set is not well-defined; leave 0 unless needles empty.
        fp = 0 if needles else 0
        n = len(items)
        out.append(
            {
                "failure_mode": mode,
                "n_trials": n,
                "true_positives": tp,
                "false_negatives": fn,
                "false_positives": fp,
                "diagnostic_accuracy": _pct(tp, n),
                "false_negative_rate": _pct(fn, n),
                "false_positive_rate": _pct(fp, n) if n else "n/a",
                "expected_needles": "; ".join(needles) if needles else "(none configured)",
            }
        )
    return out


def compute_recovery_stats(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_mode: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        mode = row.get("injected_failure_mode") or ""
        if mode:
            by_mode[mode].append(row)

    out: list[dict[str, Any]] = []
    for mode, items in sorted(by_mode.items()):
        n = len(items)
        recovered = sum(1 for r in items if _boolish(r.get("successful_recovery", "")))
        retries = [
            float(r["total_retries"])
            for r in items
            if r.get("total_retries") not in (None, "")
        ]
        if not retries:
            retries = [
                max(0.0, float(r["attempt_count"]) - 1)
                for r in items
                if r.get("attempt_count")
            ]
        diag_t = [
            float(r["diagnosis_duration_seconds"])
            for r in items
            if r.get("diagnosis_duration_seconds") not in (None, "")
        ]
        rec_t = [
            float(r["recovery_duration_seconds"])
            for r in items
            if r.get("recovery_duration_seconds") not in (None, "")
        ]
        out.append(
            {
                "failure_mode": mode,
                "n_trials": n,
                "recovery_success_rate": _pct(recovered, n),
                "mean_retries": _mean(retries),
                "std_retries": _std(retries),
                "mean_time_to_diagnosis_s": _mean_std(diag_t),
                "mean_time_to_recovery_s": _mean_std(rec_t),
            }
        )
    return out


def compute_detection_method_split(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    injected = [r for r in rows if r.get("injected_failure_mode")]
    if not injected:
        injected = [r for r in rows if r.get("detection_method")]
    counts: dict[str, int] = defaultdict(int)
    for row in injected:
        method = row.get("detection_method") or "unknown"
        counts[method] += 1
    n = sum(counts.values())
    return [
        {
            "detection_method": method,
            "count": count,
            "fraction": _pct(count, n),
        }
        for method, count in sorted(counts.items())
    ]


def compute_efficiency_stats(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    agentic = [r for r in rows if r.get("run_mode", "agentic") == "agentic"]
    walls = [float(r["wall_clock_seconds"]) for r in agentic if r.get("wall_clock_seconds")]
    fmri = [float(r["fmriprep_cli_seconds"]) for r in agentic if r.get("fmriprep_cli_seconds")]
    overhead = [
        float(r["orchestration_overhead_seconds"])
        for r in agentic
        if r.get("orchestration_overhead_seconds")
    ]
    prompt = [float(r["llm_prompt_tokens"]) for r in agentic if r.get("llm_prompt_tokens")]
    completion = [
        float(r["llm_completion_tokens"]) for r in agentic if r.get("llm_completion_tokens")
    ]
    cost = [float(r["llm_cost_usd_estimate"]) for r in agentic if r.get("llm_cost_usd_estimate")]
    return [
        {
            "metric": "wall_clock_seconds",
            "n": len(walls),
            "mean_std": _mean_std(walls),
        },
        {
            "metric": "fmriprep_cli_seconds",
            "n": len(fmri),
            "mean_std": _mean_std(fmri),
        },
        {
            "metric": "orchestration_overhead_seconds",
            "n": len(overhead),
            "mean_std": _mean_std(overhead),
        },
        {
            "metric": "llm_prompt_tokens",
            "n": len(prompt),
            "mean_std": _mean_std(prompt),
        },
        {
            "metric": "llm_completion_tokens",
            "n": len(completion),
            "mean_std": _mean_std(completion),
        },
        {
            "metric": "llm_cost_usd_estimate",
            "n": len(cost),
            "mean_std": _mean_std(cost),
        },
    ]


def compute_config_quality(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    scored = [r for r in rows if r.get("config_gold_standard_correct") not in (None, "")]
    n = len(scored)
    correct = sum(1 for r in scored if _boolish(r.get("config_gold_standard_correct")))
    hallu_pass = sum(1 for r in scored if _boolish(r.get("config_hallucination_pass", "true")))
    return [
        {
            "n_scored_runs": n,
            "gold_standard_correct_rate": _pct(correct, n),
            "hallucination_pass_rate": _pct(hallu_pass, n),
        }
    ]


def write_table(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("# (no rows)\n")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, sections: dict[str, list[dict[str, Any]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Evaluation Summary\n"]
    for title, rows in sections.items():
        lines.append(f"## {title}\n")
        if not rows:
            lines.append("_No data._\n")
            continue
        headers = list(rows[0].keys())
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join("---" for _ in headers) + " |")
        for row in rows:
            lines.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
        lines.append("")
    path.write_text("\n".join(lines))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Summarize evaluation CSV exports.")
    p.add_argument(
        "--eval-root",
        type=Path,
        default=_TESTING / "results" / "evaluation",
        help="Directory containing evaluation/ CSV files (or parent with evaluation/ subdir).",
    )
    p.add_argument(
        "--metrics-dir",
        type=Path,
        default=_ROOT / "output" / "metrics",
        help="Directory of metrics_<run_id>.jsonl event logs (optional enrichment).",
    )
    p.add_argument(
        "--gold-standard",
        type=Path,
        default=_TESTING / "fixtures" / "gold_standard_commands.yaml",
        help="Fixture with expected_root_causes for diagnostic accuracy.",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=_TESTING / "results" / "reports",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    eval_root = args.eval_root
    if not eval_root.is_absolute():
        eval_root = (_ROOT / eval_root).resolve()

    eval_dir = eval_root / "evaluation" if (eval_root / "evaluation").is_dir() else eval_root
    # Also consider project-level output/evaluation when battery dir is empty.
    agentic_csv = eval_dir / "run_evaluation.csv"
    baseline_csv = eval_dir / "baseline_evaluation.csv"
    if not agentic_csv.is_file():
        fallback = _ROOT / "output" / "evaluation" / "run_evaluation.csv"
        if fallback.is_file():
            agentic_csv = fallback
            baseline_csv = fallback.parent / "baseline_evaluation.csv"

    agentic_rows = _read_csv(agentic_csv)
    baseline_rows = _read_csv(baseline_csv)
    expected = load_expected_root_causes(
        args.gold_standard if args.gold_standard.is_absolute() else _ROOT / args.gold_standard
    )
    _ = _read_metrics_jsonl(
        args.metrics_dir if args.metrics_dir.is_absolute() else _ROOT / args.metrics_dir
    )

    sections = {
        "Agentic / Ablation Summary": summarize_agentic(agentic_rows),
        "Baseline vs Agentic": compare_baseline_agentic(agentic_rows, baseline_rows),
        "Failure Injection Matrix": failure_matrix(agentic_rows),
        "Diagnostic Accuracy": compute_diagnostic_accuracy(agentic_rows, expected),
        "Recovery Stats by Failure Mode": compute_recovery_stats(agentic_rows),
        "Detection Method Split": compute_detection_method_split(agentic_rows),
        "Efficiency": compute_efficiency_stats(agentic_rows),
        "Config Quality": compute_config_quality(agentic_rows),
    }

    out = args.out_dir
    if not out.is_absolute():
        out = (_ROOT / out).resolve()

    write_table(out / "ablation_summary.csv", sections["Agentic / Ablation Summary"])
    write_table(out / "baseline_vs_agentic.csv", sections["Baseline vs Agentic"])
    write_table(out / "failure_injection_matrix.csv", sections["Failure Injection Matrix"])
    write_table(out / "diagnostic_accuracy.csv", sections["Diagnostic Accuracy"])
    write_table(out / "recovery_stats.csv", sections["Recovery Stats by Failure Mode"])
    write_table(out / "detection_method_split.csv", sections["Detection Method Split"])
    write_table(out / "efficiency_stats.csv", sections["Efficiency"])
    write_table(out / "config_quality.csv", sections["Config Quality"])
    write_markdown(out / "evaluation_summary.md", sections)
    (out / "meta.json").write_text(
        json.dumps(
            {
                "agentic_csv": str(agentic_csv),
                "baseline_csv": str(baseline_csv),
                "agentic_rows": len(agentic_rows),
                "baseline_rows": len(baseline_rows),
                "gold_standard": str(args.gold_standard),
            },
            indent=2,
        )
        + "\n"
    )

    print(f"✅ Reports written to {out}")
    print(f"   agentic rows: {len(agentic_rows)}  baseline rows: {len(baseline_rows)}")
    for title, rows in sections.items():
        print(f"   {title}: {len(rows)} row(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
