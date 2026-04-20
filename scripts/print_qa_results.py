#!/usr/bin/env python3
"""
Print saved QA results for an existing Agentic fMRIPrep output directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Print saved QA metrics from an existing output tree.")
    p.add_argument("--bids-dir", required=False, help="BIDS input directory (used to resolve raw T1w path).")
    p.add_argument("--output-dir", required=True, help="Output directory from the run.")
    p.add_argument("--participant", default="sub-01", help="Participant label.")
    p.add_argument(
        "--output-space",
        default="MNI152NLin2009cAsym",
        help="Expected output space label for MNI preprocessed T1w filename.",
    )
    return p.parse_args()


def _resolve_subject_output_dir(output_dir: Path, participant: str) -> Path:
    candidates = [
        output_dir / participant,
        output_dir / "fmriprep" / participant,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _resolve_subject_report_path(output_dir: Path, participant: str) -> Path:
    candidates = [
        output_dir / f"{participant}.html",
        output_dir / "fmriprep" / f"{participant}.html",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _resolve_input_t1w(bids_dir: Path, participant: str) -> Path:
    """
    Resolve subject T1w path for both flat and session-based BIDS layouts.
    Prefer non-retest sessions when multiple session matches exist.
    """
    flat = bids_dir / participant / "anat" / f"{participant}_T1w.nii.gz"
    if flat.exists():
        return flat

    session_matches = sorted((bids_dir / participant).glob(f"ses-*/anat/{participant}*_T1w.nii.gz"))
    if session_matches:
        def _session_sort_key(path: Path) -> tuple[int, str]:
            ses = next((part for part in path.parts if part.startswith("ses-")), "")
            is_retest = "retest" in ses.lower()
            return (1 if is_retest else 0, str(path))

        session_matches = sorted(session_matches, key=_session_sort_key)
        return session_matches[0]

    return flat


def _compute_voxel_metrics(raw_t1w: Path, preproc_t1w: Path, brain_mask: Path) -> dict | None:
    """
    Compute QA voxel metrics using the same definitions as orchestrator:
      - retention_ratio = mask_nonzero / preproc_nonzero
      - reduction       = 1 - (mask_nonzero / preproc_nonzero)
    Raw voxels are reported for context only.
    """
    if not raw_t1w.exists() or not preproc_t1w.exists():
        return None

    try:
        import nibabel as nib
        import numpy as np
    except ImportError:
        return None

    raw = nib.load(str(raw_t1w)).get_fdata()
    proc = nib.load(str(preproc_t1w)).get_fdata()
    raw_nonzero = int(np.count_nonzero(raw))
    proc_nonzero = int(np.count_nonzero(proc))
    mask_nonzero = None
    if brain_mask.exists():
        mask = nib.load(str(brain_mask)).get_fdata()
        mask_nonzero = int(np.count_nonzero(mask))

    kept_nonzero = mask_nonzero if mask_nonzero is not None else proc_nonzero
    retention_ratio = kept_nonzero / max(proc_nonzero, 1)
    reduction = 1.0 - kept_nonzero / max(proc_nonzero, 1)
    return {
        "raw_nonzero_voxels": raw_nonzero,
        "preprocessed_nonzero_voxels": proc_nonzero,
        "brain_mask_nonzero_voxels": mask_nonzero,
        "brain_mask_retention_ratio": retention_ratio,
        "skull_strip_reduction": reduction,
    }


def main() -> None:
    args = parse_args()
    participant = args.participant if args.participant.startswith("sub-") else f"sub-{args.participant}"
    bids_dir = Path(args.bids_dir).resolve() if args.bids_dir else None
    output_dir = Path(args.output_dir).resolve()
    subject_output_dir = _resolve_subject_output_dir(output_dir, participant)
    qa_dir = output_dir / "agentic_results" / participant
    qa_report_path = qa_dir / "qa_report.txt"
    qa_metrics_path = qa_dir / "qa_metrics.json"
    qa_decision_path = qa_dir / "qa_decision.json"
    report_html = _resolve_subject_report_path(output_dir, participant)
    preproc_t1w = subject_output_dir / "anat" / f"{participant}_desc-preproc_T1w.nii.gz"
    brain_mask = subject_output_dir / "anat" / f"{participant}_desc-brain_mask.nii.gz"
    mni_t1w = subject_output_dir / "anat" / f"{participant}_space-{args.output_space}_desc-preproc_T1w.nii.gz"
    input_t1w = _resolve_input_t1w(bids_dir, participant) if bids_dir else None

    if qa_report_path.exists():
        print(qa_report_path.read_text().rstrip())
    else:
        print(
            f"WARNING: QA report not found at {qa_report_path}. "
            "Run the pipeline first or use an output directory with agentic_results."
        )

    if qa_metrics_path.exists():
        print("\nJSON:")
        print(json.dumps(json.loads(qa_metrics_path.read_text()), indent=2, sort_keys=True))
    else:
        print(f"\nWARNING: QA metrics JSON not found at {qa_metrics_path}")

    if qa_decision_path.exists():
        print("\nDECISION:")
        print(json.dumps(json.loads(qa_decision_path.read_text()), indent=2, sort_keys=True))

    print("\nKEY OUTPUT FILES:")
    print(f"  HTML report     : {report_html}")
    print(f"  Preprocessed T1w: {preproc_t1w}")
    print(f"  Brain mask      : {brain_mask}")
    print(f"  MNI T1w         : {mni_t1w}")
    print(f"  QA report       : {qa_report_path}")
    if input_t1w is not None:
        print(f"  Raw input T1w   : {input_t1w}")

    if input_t1w is not None:
        live_metrics = _compute_voxel_metrics(input_t1w, preproc_t1w, brain_mask)
        if live_metrics is not None:
            print("\nLIVE VOXEL METRICS (mask vs preprocessed):")
            print(json.dumps(live_metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
