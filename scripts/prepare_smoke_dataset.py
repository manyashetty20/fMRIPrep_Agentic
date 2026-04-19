#!/usr/bin/env python3
"""
Prepare a small BIDS-like smoke-test dataset in an isolated directory.

This copies subject-level files from an existing BIDS tree, then shrinks:
  - T1w: central 64x64x64 crop
  - BOLD: first N volumes (default 12)
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import nibabel as nib
import numpy as np


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prepare an isolated toy BIDS dataset.")
    p.add_argument("--source-bids", required=True, help="Source BIDS directory.")
    p.add_argument("--dest-bids", required=True, help="Destination BIDS directory.")
    p.add_argument("--participant", default="sub-01", help="Participant label.")
    p.add_argument("--bold-volumes", type=int, default=12, help="Number of BOLD volumes to keep.")
    return p.parse_args()


def _center_crop_3d(data: np.ndarray, size: int = 64) -> np.ndarray:
    starts = [max((dim - size) // 2, 0) for dim in data.shape[:3]]
    slices = tuple(slice(start, min(start + size, dim)) for start, dim in zip(starts, data.shape[:3]))
    return data[slices]


def _copy_text_files(src: Path, dst: Path) -> None:
    for path in src.rglob("*"):
        if not path.is_file() or path.suffix in {".nii", ".gz"}:
            continue
        rel = path.relative_to(src)
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, out)


def _copy_dataset_description(src_root: Path, dst_root: Path) -> None:
    for name in ("dataset_description.json", "participants.tsv", "participants.json", "README"):
        src = src_root / name
        if src.exists():
            dst = dst_root / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def main() -> None:
    args = parse_args()
    source_root = Path(args.source_bids).resolve()
    dest_root = Path(args.dest_bids).resolve()
    participant = args.participant if args.participant.startswith("sub-") else f"sub-{args.participant}"

    src_subject = source_root / participant
    dst_subject = dest_root / participant

    if not src_subject.exists():
        raise FileNotFoundError(f"Participant not found: {src_subject}")

    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    _copy_dataset_description(source_root, dest_root)
    _copy_text_files(src_subject, dst_subject)

    src_t1w = src_subject / "anat" / f"{participant}_T1w.nii.gz"
    dst_t1w = dst_subject / "anat" / f"{participant}_T1w.nii.gz"
    dst_t1w.parent.mkdir(parents=True, exist_ok=True)
    t1w_img = nib.load(str(src_t1w))
    t1w_data = t1w_img.get_fdata()
    toy_t1w = _center_crop_3d(t1w_data, size=64)
    nib.save(nib.Nifti1Image(toy_t1w, t1w_img.affine, t1w_img.header), str(dst_t1w))

    for src_bold in sorted((src_subject / "func").glob("*_bold.nii.gz")):
        dst_bold = dst_subject / "func" / src_bold.name
        dst_bold.parent.mkdir(parents=True, exist_ok=True)
        bold_img = nib.load(str(src_bold))
        bold_data = bold_img.get_fdata()
        if bold_data.ndim != 4:
            raise ValueError(f"Expected 4D BOLD image, got shape {bold_data.shape} for {src_bold}")
        toy_bold = bold_data[:, :, :, : args.bold_volumes]
        nib.save(nib.Nifti1Image(toy_bold, bold_img.affine, bold_img.header), str(dst_bold))

    print(f"Prepared smoke dataset at {dest_root}")


if __name__ == "__main__":
    main()
