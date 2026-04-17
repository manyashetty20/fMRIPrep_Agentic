#!/usr/bin/env python3
"""
scripts/compare.py
==================
Visual comparison of raw vs preprocessed T1w images.

Saves a side-by-side PNG to the output directory.

Usage
-----
python scripts/compare.py
python scripts/compare.py --participant sub-02 --slice 80 --output myplot.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from config_loader import Config


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Before / after T1w comparison plot.")
    p.add_argument("--config",      metavar="PATH")
    p.add_argument("--bids-dir",    metavar="PATH")
    p.add_argument("--output-dir",  metavar="PATH")
    p.add_argument("--participant", metavar="ID")
    p.add_argument(
        "--slice", type=int, default=None, metavar="IDX",
        help="Axial slice index to display (default: middle slice).",
    )
    p.add_argument(
        "--output", metavar="PATH", default=None,
        help="Where to save the PNG (default: <output_dir>/visual_proof.png).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    overrides: dict = {}
    if args.bids_dir:
        overrides["paths.bids_dir"] = args.bids_dir
    if args.output_dir:
        overrides["paths.output_dir"] = args.output_dir
    if args.participant:
        pid = args.participant
        if not pid.startswith("sub-"):
            pid = f"sub-{pid}"
        overrides["subject.participant_id"] = pid

    cfg = Config(yaml_path=args.config, overrides=overrides)
    pid = cfg.participant_id

    raw_path  = cfg.bids_dir  / pid / "anat" / f"{pid}_T1w.nii.gz"
    proc_path = (
        cfg.output_dir / "fmriprep" / pid / "anat" /
        f"{pid}_desc-preproc_T1w.nii.gz"
    )

    save_path = Path(args.output) if args.output else cfg.output_dir / "visual_proof.png"
    save_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import matplotlib
        matplotlib.use("Agg")   # non-interactive backend – safe for headless servers
        import matplotlib.pyplot as plt
        import nibabel as nib
    except ImportError as exc:
        print(f"❌  Missing dependency: {exc}\n   Install with: pip install nibabel matplotlib")
        sys.exit(1)

    # ------------------------------------------------------------------ #
    #  Load raw image
    # ------------------------------------------------------------------ #
    if not raw_path.exists():
        print(f"❌  Raw T1w not found: {raw_path}")
        sys.exit(1)

    raw_data = nib.load(str(raw_path)).get_fdata()
    slice_idx = args.slice if args.slice is not None else raw_data.shape[2] // 2

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("#111111")

    # --- Before ---
    axes[0].imshow(raw_data[:, :, slice_idx].T, cmap="gray", origin="lower")
    axes[0].set_title(
        f"BEFORE: Raw T1w  |  {pid}  |  slice z={slice_idx}",
        color="white", fontsize=11,
    )
    axes[0].axis("off")

    # --- After ---
    if proc_path.exists():
        proc_data = nib.load(str(proc_path)).get_fdata()
        proc_slice_idx = min(slice_idx, proc_data.shape[2] - 1)
        axes[1].imshow(proc_data[:, :, proc_slice_idx].T, cmap="gray", origin="lower")
        axes[1].set_title(
            "AFTER: Skull-stripped  |  MNI-normalised",
            color="white", fontsize=11,
        )
    else:
        axes[1].set_facecolor("#1a1a1a")
        axes[1].text(
            0.5, 0.5,
            f"Preprocessed image not yet available.\n\nExpected:\n{proc_path}",
            ha="center", va="center", color="#aaaaaa", fontsize=9,
            transform=axes[1].transAxes, wrap=True,
        )
        axes[1].set_title("AFTER: (fMRIPrep output)", color="white", fontsize=11)

    axes[1].axis("off")

    plt.tight_layout(pad=1.5)
    plt.savefig(str(save_path), dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()

    print(f"✅  Comparison plot saved → {save_path}")


if __name__ == "__main__":
    main()