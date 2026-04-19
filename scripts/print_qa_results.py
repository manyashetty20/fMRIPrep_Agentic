#!/usr/bin/env python3
"""
Print QA results for an existing Agentic fMRIPrep output directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nibabel as nib
import numpy as np


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Print QA metrics from an existing output tree.")
    p.add_argument("--bids-dir", required=True, help="BIDS input directory used for the run.")
    p.add_argument("--output-dir", required=True, help="Output directory from the run.")
    p.add_argument("--participant", default="sub-01", help="Participant label.")
    return p.parse_args()


def resolve_subject_output_dir(output_dir: Path, participant: str) -> Path:
    for candidate in (output_dir / participant, output_dir / "fmriprep" / participant):
        if candidate.exists():
            return candidate
    return output_dir / participant


def main() -> None:
    args = parse_args()
    participant = args.participant if args.participant.startswith("sub-") else f"sub-{args.participant}"
    bids_dir = Path(args.bids_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    subject_output_dir = resolve_subject_output_dir(output_dir, participant)

    input_img = bids_dir / participant / "anat" / f"{participant}_T1w.nii.gz"
    output_img = subject_output_dir / "anat" / f"{participant}_desc-preproc_T1w.nii.gz"
    mni_img = subject_output_dir / "anat" / f"{participant}_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz"
    brain_mask = subject_output_dir / "anat" / f"{participant}_desc-brain_mask.nii.gz"

    raw = nib.load(str(input_img)).get_fdata()
    proc = nib.load(str(output_img)).get_fdata()
    raw_nonzero = int(np.count_nonzero(raw))
    proc_nonzero = int(np.count_nonzero(proc))
    mask_nonzero = int(np.count_nonzero(nib.load(str(brain_mask)).get_fdata())) if brain_mask.exists() else None
    kept_nonzero = mask_nonzero if mask_nonzero is not None else proc_nonzero
    reduction = 1.0 - kept_nonzero / max(raw_nonzero, 1)
    retention_ratio = kept_nonzero / max(raw_nonzero, 1)
    qa_summary = "PASS" if output_img.exists() and mni_img.exists() and brain_mask.exists() else "WARN"

    report = [
        "VISUAL AUDIT:",
        f"  Subject output dir          : {subject_output_dir}",
        f"  Raw voxels (non-zero)       : {raw_nonzero:,}",
        f"  Preprocessed voxels (non-zero): {proc_nonzero:,}",
        (
            f"  Brain-mask voxels (non-zero): {mask_nonzero:,}"
            if mask_nonzero is not None
            else "  Brain-mask voxels (non-zero): Not available"
        ),
        f"  Brain-mask retention ratio  : {retention_ratio:.1%}",
        f"  Skull-strip reduction       : {reduction:.1%}",
        (
            "  Skull-stripping : change detected between raw volume and brain mask."
            if reduction > 0
            else "  Skull-stripping : no measurable voxel reduction detected."
        ),
        (
            "  Normalization   : MNI-space preprocessed output file detected."
            if mni_img.exists()
            else "  Normalization   : Not verified in code (no MNI-space file detected)."
        ),
        f"  QA Summary      : {qa_summary}",
    ]
    print("\n".join(report))
    print("\nJSON:")
    print(json.dumps(
        {
            "participant": participant,
            "subject_output_dir": str(subject_output_dir),
            "raw_nonzero_voxels": raw_nonzero,
            "preprocessed_nonzero_voxels": proc_nonzero,
            "brain_mask_nonzero_voxels": mask_nonzero,
            "brain_mask_retention_ratio": retention_ratio,
            "skull_strip_reduction": reduction,
            "qa_summary": qa_summary,
            "mni_found": mni_img.exists(),
        },
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
