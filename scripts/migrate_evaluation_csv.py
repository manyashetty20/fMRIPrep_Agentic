#!/usr/bin/env python3
"""
scripts/migrate_evaluation_csv.py
==================================
Non-destructive canonical migration of run_evaluation.csv and run_evaluation.jsonl:
- Backs up old CSV as run_evaluation.legacy.csv.
- Unifies schema using EVALUATION_FIELDNAMES (including forensic audit columns).
- Standardizes retention ratio strictly to Eq. 1: mask / preprocessed.
- Preserves historical retention ratio in legacy_retention_ratio with provenance notes.
- Rebuilds QA verdicts deterministically through qa_verdict.py.
- Encodes forensic metadata from DATA_LABEL_CHECK.md section 8 (true_subject, sessions_processed, true_failure_mode, applied_rule_ids, run_class, run_source, label_note).
- Ingests testing harness runs (de-duplicated by run_id, including 20260829T175552Z_0071b161).
"""

from __future__ import annotations

import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation_export import EVALUATION_FIELDNAMES
from qa_verdict import verdict_from_metrics


def migrate() -> None:
    eval_dir = ROOT / "output" / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    csv_path = eval_dir / "run_evaluation.csv"
    legacy_csv_path = eval_dir / "run_evaluation.legacy.csv"
    jsonl_path = eval_dir / "run_evaluation.jsonl"

    # 1. Back up existing CSV if present
    if csv_path.exists() and not legacy_csv_path.exists():
        shutil.copy2(csv_path, legacy_csv_path)
        print(f"Backed up {csv_path} to {legacy_csv_path}")

    # 2. Ingest main run_evaluation.jsonl
    main_rows: list[dict] = []
    if jsonl_path.exists():
        with jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    main_rows.append(json.loads(line))
    print(f"Loaded {len(main_rows)} rows from {jsonl_path}")

    # 3. Ingest testing harness runs
    test_jsonl = ROOT / "testing" / "results" / "evaluation" / "evaluation" / "run_evaluation.jsonl"
    test_rows: list[dict] = []
    if test_jsonl.exists():
        with test_jsonl.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    test_rows.append(json.loads(line))
    print(f"Loaded {len(test_rows)} rows from testing harness {test_jsonl}")

    # Track seen run_ids to de-duplicate
    seen_run_ids = set()
    unified_rows: list[dict] = []

    # Map forensic properties for main 32 rows
    for i, r in enumerate(main_rows, 1):
        row = dict(r)
        run_id = row.get("run_id") or f"main_row_{i}"
        if run_id in seen_run_ids and row.get("run_id"):
            continue
        if row.get("run_id"):
            seen_run_ids.add(row["run_id"])

        row["run_source"] = "main"

        # Classify run_class
        if i in {1, 29, 30, 31, 32} or row.get("dataset_id") == "bids":
            row["run_class"] = "MOCK"
        else:
            row["run_class"] = "REAL_DOCKER"

        # Forensic subjects & sessions
        if i in {4, 9, 12, 28}:
            row["true_subject"] = "sub-02"
        elif i in {5, 10}:
            row["true_subject"] = "sub-03"
        else:
            row["true_subject"] = "sub-01"

        if i in {1, 29, 30, 31, 32}:
            row["sessions_processed"] = "ses-test"
        elif i == 25:
            row["sessions_processed"] = "none"
        elif i == 28:
            row["sessions_processed"] = "ses-retest"
        else:
            row["sessions_processed"] = "ses-test, ses-retest"

        # True failure modes & origins
        if i == 2:
            row["true_failure_mode"] = "missing_readout_timing_metadata"
            row["failure_origin"] = "bids_metadata_gap"
            row["label_note"] = "BIDS readout time specification missing"
        elif 3 <= i <= 10 or i in {22, 24, 27}:
            row["true_failure_mode"] = "none"
            row["failure_origin"] = "clean"
            row["label_note"] = "clean baseline execution"
        elif 11 <= i <= 14:
            row["true_failure_mode"] = "injected_failure_tolerated"
            row["failure_origin"] = "injected_metadata_tolerated"
            row["label_note"] = "injected failure tolerated by --skip-bids-validation (NOT a recovery test)"
        elif 15 <= i <= 20:
            row["true_failure_mode"] = "syn_phase_encoding_absent"
            row["failure_origin"] = "self_induced_by_config_agent"
            row["label_note"] = "failure self-induced by config agent adding --use-syn-sdc without phase encoding metadata"
        elif i in {21, 23}:
            row["true_failure_mode"] = "syn_phase_encoding_absent"
            row["failure_origin"] = "self_induced_by_config_agent"
            row["applied_rule_ids"] = "drop_syn_ignore_fieldmaps"
            row["label_note"] = "recovered: removed --use-syn-sdc, added --ignore fieldmaps"
        elif i == 25:
            row["true_failure_mode"] = "cli_invalid_flag"
            row["failure_origin"] = "llm_cli_hallucination"
            row["label_note"] = "CLI parser failure (invalid argument --session-id instead of --session-label)"
        elif i == 26:
            row["true_failure_mode"] = "oom_killed_misdiagnosed"
            row["failure_origin"] = "resource_limit_oom"
            row["label_note"] = "OOM killed at 14.6ks; LLM misdiagnosed platform warning"
        elif i == 28:
            row["true_failure_mode"] = "spatial_normalization_ants_crash"
            row["failure_origin"] = "runtime_crash_ants"
            row["label_note"] = "genuine sub-02 execution; crashed inside ANTs norm registration"
        elif i in {1, 30, 32}:
            row["true_failure_mode"] = "oom_mock_injected"
            row["failure_origin"] = "mock_test"
            row["applied_rule_ids"] = "oom_low_mem"
            row["label_note"] = "mock test injection: exit 137"
        elif i in {29, 31}:
            row["true_failure_mode"] = "clipping_mock_injected"
            row["failure_origin"] = "mock_test"
            row["applied_rule_ids"] = "fix_skull_strip_clipping"
            row["label_note"] = "mock test injection: boundary clipping"

        # Standardize retention ratio to Eq. 1
        raw_v = row.get("raw_nonzero_voxels")
        proc_v = row.get("preprocessed_nonzero_voxels")
        mask_v = row.get("brain_mask_nonzero_voxels")
        hist_ret = row.get("brain_mask_retention_ratio")
        row["legacy_retention_ratio"] = hist_ret

        if i in {4, 5, 6}:
            row["label_note"] = (row.get("label_note", "") + "; denominator changed at commit c3e0b3ca").strip("; ")

        if mask_v is not None and proc_v is not None and int(proc_v) > 0:
            recomputed = float(mask_v) / float(proc_v)
            row["retention_ratio_recomputed"] = recomputed
            row["brain_mask_retention_ratio"] = recomputed
            row["skull_strip_reduction"] = 1.0 - recomputed
        else:
            row["retention_ratio_recomputed"] = ""

        # Recompute QA verdict through qa_verdict
        if row.get("output_found") and row.get("brain_mask_found"):
            v = verdict_from_metrics(row)
            row["qa_summary"] = v["summary"]
            row["qa_status"] = v.get("display") or v["summary"]
            row["qa_warn_count"] = v.get("qa_warn_count", 0)
            row["qa_fail_count"] = v.get("qa_fail_count", 0)

        unified_rows.append(row)

    # Ingest testing harness rows
    for r in test_rows:
        row = dict(r)
        run_id = row.get("run_id")
        if not run_id or run_id in seen_run_ids:
            continue
        seen_run_ids.add(run_id)

        row["run_source"] = "testing_harness"
        row["run_class"] = "REAL_DOCKER"
        row["true_subject"] = row.get("participant") or "sub-01"
        row["sessions_processed"] = "ses-test"
        row["true_failure_mode"] = "missing_repetition_time"
        row["failure_origin"] = "injected_metadata"
        row["applied_rule_ids"] = "repair_missing_tr"
        row["label_note"] = "testing harness injection trial"

        raw_v = row.get("raw_nonzero_voxels")
        proc_v = row.get("preprocessed_nonzero_voxels")
        mask_v = row.get("brain_mask_nonzero_voxels")
        hist_ret = row.get("brain_mask_retention_ratio")
        row["legacy_retention_ratio"] = hist_ret

        if mask_v is not None and proc_v is not None and int(proc_v) > 0:
            recomputed = float(mask_v) / float(proc_v)
            row["retention_ratio_recomputed"] = recomputed
            row["brain_mask_retention_ratio"] = recomputed
            row["skull_strip_reduction"] = 1.0 - recomputed
        else:
            row["retention_ratio_recomputed"] = ""

        unified_rows.append(row)

    print(f"Total unified rows: {len(unified_rows)}")

    # Ensure every key in EVALUATION_FIELDNAMES exists in every row
    for r in unified_rows:
        for k in EVALUATION_FIELDNAMES:
            if k not in r or r[k] is None:
                r[k] = ""

    # Write unified JSONL
    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in unified_rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    print(f"Wrote {len(unified_rows)} rows to {jsonl_path}")

    # Write unified CSV
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EVALUATION_FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for r in unified_rows:
            writer.writerow({k: r.get(k, "") for k in EVALUATION_FIELDNAMES})
    print(f"Wrote {len(unified_rows)} rows to {csv_path} with {len(EVALUATION_FIELDNAMES)} columns")


if __name__ == "__main__":
    migrate()
