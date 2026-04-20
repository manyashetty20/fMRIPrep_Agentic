"""
evaluation_export.py
====================
Shared evaluation row construction and CSV/JSONL export for agentic and baseline runs.

Field names are stable and listed explicitly so publication tables stay comparable across runs.
"""

from __future__ import annotations

import csv
import datetime
import json
import logging
from pathlib import Path
from typing import Any

from config_loader import Config

logger = logging.getLogger(__name__)

# Ordered columns for CSV (extras still appended if missing from older rows).
EVALUATION_FIELDNAMES: list[str] = [
    "run_mode",
    "timestamp",
    "dataset_id",
    "participant",
    "output_dir",
    "initial_status",
    "final_status",
    "attempt_count",
    "max_recovery_attempts",
    "recovery_applied",
    "successful_recovery",
    "recovery_enabled",
    "diagnosis_enabled",
    "vision_enabled",
    "batch_index",
    "batch_total",
    "participant_scope",
    "initial_failure_type",
    "initial_failure_evidence",
    "first_exit_code",
    "last_exit_code",
    "qa_summary",
    "qa_status",
    "qa_warn_count",
    "qa_fail_count",
    "report_found",
    "output_found",
    "mni_found",
    "brain_mask_found",
    "raw_nonzero_voxels",
    "preprocessed_nonzero_voxels",
    "brain_mask_nonzero_voxels",
    "brain_mask_retention_ratio",
    "skull_strip_reduction",
    "total_runtime_seconds",
    "wall_clock_seconds",
    "history_entries",
    "qa_threshold_preset",
    "qa_literature_reference_note",
    "manual_intervention_count",
    "injected_failure_mode",
    "baseline_requires_manual_steps",
]


def build_evaluation_row(
    cfg: Config,
    final_state: dict[str, Any],
    *,
    run_mode: str = "agentic",
    wall_clock_seconds: float | None = None,
    batch_index: int | None = None,
    batch_total: int | None = None,
    participant_scope: str = "single",
    manual_intervention_count: int = 0,
    injected_failure_mode: str = "",
    baseline_requires_manual_steps: bool | None = None,
) -> dict[str, Any]:
    events = final_state.get("events", [])
    history = final_state.get("history", [])
    execution_events = [event for event in events if event.get("type") == "execution"]
    diagnosis_events = [event for event in events if event.get("type") == "diagnosis"]
    qa_event = next((event for event in reversed(events) if event.get("type") == "qa"), {})
    qa_metrics: dict[str, Any] = qa_event.get("metrics", {}) if isinstance(qa_event, dict) else {}
    qa_decision = qa_metrics.get("qa_decision", {}) if isinstance(qa_metrics, dict) else {}
    qa_checks = qa_decision.get("checks", []) if isinstance(qa_decision, dict) else []
    planning_event = next((event for event in events if event.get("type") == "planning"), {})
    first_execution = execution_events[0] if execution_events else {}
    last_execution = execution_events[-1] if execution_events else {}
    first_diagnosis = diagnosis_events[0] if diagnosis_events else {}

    recovery_applied = any(
        event.get("type") == "recovery" and event.get("changed") for event in events
    )
    successful_recovery = bool(recovery_applied and final_state.get("status") in ("success", "completed"))

    total_runtime_seconds = None
    started_at = planning_event.get("timestamp")
    ended_at = qa_event.get("timestamp") if qa_event else None
    if started_at and ended_at:
        try:
            total_runtime_seconds = (
                datetime.datetime.fromisoformat(str(ended_at))
                - datetime.datetime.fromisoformat(str(started_at))
            ).total_seconds()
        except Exception:
            total_runtime_seconds = None

    row: dict[str, Any] = {
        "run_mode": run_mode,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "dataset_id": cfg.bids_dir.name,
        "participant": cfg.participant_id,
        "output_dir": str(cfg.output_dir),
        "initial_status": first_execution.get("status", "not_run"),
        "final_status": final_state.get("status", "unknown"),
        "attempt_count": final_state.get("attempt_count", 0),
        "max_recovery_attempts": cfg.max_recovery_attempts,
        "recovery_applied": recovery_applied,
        "successful_recovery": successful_recovery,
        "recovery_enabled": cfg.recovery_enabled,
        "diagnosis_enabled": cfg.diagnosis_enabled,
        "vision_enabled": cfg.vision_enabled,
        "batch_index": batch_index if batch_index is not None else "",
        "batch_total": batch_total if batch_total is not None else "",
        "participant_scope": participant_scope,
        "initial_failure_type": (
            first_diagnosis.get("report", "").splitlines()[0].replace("ROOT CAUSE: ", "")
            if first_diagnosis
            else ""
        ),
        "initial_failure_evidence": (
            next(
                (
                    line.replace("EVIDENCE: ", "")
                    for line in str(first_diagnosis.get("report", "")).splitlines()
                    if line.startswith("EVIDENCE: ")
                ),
                "",
            )
            if first_diagnosis
            else ""
        ),
        "first_exit_code": first_execution.get("exit_code"),
        "last_exit_code": last_execution.get("exit_code"),
        "qa_summary": qa_metrics.get("qa_summary", qa_event.get("status", "")),
        "qa_status": qa_metrics.get("status", qa_event.get("status", "")),
        "qa_warn_count": sum(1 for check in qa_checks if check.get("status") == "warn"),
        "qa_fail_count": sum(1 for check in qa_checks if check.get("status") == "fail"),
        "report_found": qa_metrics.get("report_found"),
        "output_found": qa_metrics.get("output_found"),
        "mni_found": qa_metrics.get("mni_found"),
        "brain_mask_found": qa_metrics.get("brain_mask_found"),
        "raw_nonzero_voxels": qa_metrics.get("raw_nonzero_voxels"),
        "preprocessed_nonzero_voxels": qa_metrics.get("preprocessed_nonzero_voxels"),
        "brain_mask_nonzero_voxels": qa_metrics.get("brain_mask_nonzero_voxels"),
        "brain_mask_retention_ratio": qa_metrics.get("brain_mask_retention_ratio"),
        "skull_strip_reduction": qa_metrics.get("skull_strip_reduction"),
        "total_runtime_seconds": total_runtime_seconds,
        "wall_clock_seconds": wall_clock_seconds if wall_clock_seconds is not None else "",
        "history_entries": len(history),
        "qa_threshold_preset": cfg.qa_threshold_preset,
        "qa_literature_reference_note": cfg.qa_literature_reference_note,
        "manual_intervention_count": manual_intervention_count,
        "injected_failure_mode": injected_failure_mode or "",
        "baseline_requires_manual_steps": (
            baseline_requires_manual_steps if baseline_requires_manual_steps is not None else ""
        ),
    }

    for key in EVALUATION_FIELDNAMES:
        if key not in row:
            row[key] = ""

    return row


def append_evaluation_exports(
    evaluation_row: dict[str, Any],
    *,
    eval_root: Path | None = None,
    csv_name: str = "run_evaluation.csv",
    jsonl_name: str = "run_evaluation.jsonl",
) -> None:
    """Append one row to CSV and JSONL under ``<eval_root>/evaluation/`` (default: ./output/evaluation)."""
    root = eval_root if eval_root is not None else Path("output")
    eval_dir = root / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    csv_path = eval_dir / csv_name
    jsonl_path = eval_dir / jsonl_name

    fieldnames = _resolve_csv_fieldnames(csv_path, evaluation_row)

    write_header = True
    if csv_path.exists() and csv_path.stat().st_size > 0:
        write_header = False

    with csv_path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow({k: evaluation_row.get(k, "") for k in fieldnames})

    with jsonl_path.open("a") as f:
        f.write(json.dumps(evaluation_row, sort_keys=True) + "\n")


def _resolve_csv_fieldnames(csv_path: Path, new_row: dict[str, Any]) -> list[str]:
    """Union persisted header with canonical keys so new columns appear without breaking old files."""
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return list(EVALUATION_FIELDNAMES) + sorted(
            k for k in new_row if k not in EVALUATION_FIELDNAMES
        )

    with csv_path.open(newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return list(EVALUATION_FIELDNAMES)

    merged = list(dict.fromkeys(header + EVALUATION_FIELDNAMES + list(new_row.keys())))
    return merged
