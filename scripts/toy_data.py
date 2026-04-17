#!/usr/bin/env python3
"""
scripts/toy_data.py
===================
Create a small "toy" brain volume from the full T1w scan.

Reduces the scan to a 64×64×64 voxel cube (~85% smaller) so the
agentic pipeline can be tested end-to-end without heavy compute.

Usage
-----
# Use defaults from config.yaml
python scripts/toy_data.py

# Override participant and bids dir on the fly
python scripts/toy_data.py --participant sub-02 --bids-dir /data/bids

Flags
-----
--restore   Put the original file back (undo toy mode).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from any directory by adding project root to path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from config_loader import Config


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create / restore toy brain volume.")
    p.add_argument("--config",      metavar="PATH", help="Path to config.yaml.")
    p.add_argument("--bids-dir",    metavar="PATH", help="Override BIDS directory.")
    p.add_argument("--participant", metavar="ID",   help="Override participant label.")
    p.add_argument(
        "--crop-start", type=int, default=50, metavar="N",
        help="Start index for the 64-voxel crop (default 50).",
    )
    p.add_argument(
        "--restore", action="store_true",
        help="Restore the original file from the .bak backup.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    overrides: dict = {}
    if args.bids_dir:
        overrides["paths.bids_dir"] = args.bids_dir
    if args.participant:
        pid = args.participant
        if not pid.startswith("sub-"):
            pid = f"sub-{pid}"
        overrides["subject.participant_id"] = pid

    cfg  = Config(yaml_path=args.config, overrides=overrides)
    pid  = cfg.participant_id
    anat_dir = cfg.bids_dir / pid / "anat"

    t1w_path = anat_dir / f"{pid}_T1w.nii.gz"
    bak_path = Path(str(t1w_path) + ".bak")

    # ------------------------------------------------------------------ #
    #  Restore mode
    # ------------------------------------------------------------------ #
    if args.restore:
        if not bak_path.exists():
            print(f"❌  No backup found at {bak_path}. Nothing to restore.")
            sys.exit(1)
        t1w_path.unlink(missing_ok=True)
        bak_path.rename(t1w_path)
        print(f"✅  Original T1w restored: {t1w_path}")
        return

    # ------------------------------------------------------------------ #
    #  Create toy brain
    # ------------------------------------------------------------------ #
    if not t1w_path.exists():
        print(f"❌  T1w image not found: {t1w_path}")
        sys.exit(1)

    try:
        import nibabel as nib
    except ImportError:
        print("❌  nibabel is required: pip install nibabel")
        sys.exit(1)

    print(f"📂  Loading: {t1w_path}")
    img  = nib.load(str(t1w_path))
    data = img.get_fdata()

    s = args.crop_start
    e = s + 64
    max_dims = data.shape
    if any(e > d for d in max_dims[:3]):
        print(
            f"⚠️   Crop window [{s}:{e}] exceeds image dimensions {max_dims}. "
            "Adjusting to centre crop."
        )
        s = min(d // 4 for d in max_dims[:3])
        e = s + 64

    toy_data = data[s:e, s:e, s:e]
    toy_img  = nib.Nifti1Image(toy_data, img.affine, img.header)

    # Backup original
    t1w_path.rename(bak_path)
    print(f"📦  Original backed up → {bak_path}")

    # Save toy
    nib.save(toy_img, str(t1w_path))

    orig_mb = bak_path.stat().st_size / 1e6
    toy_mb  = t1w_path.stat().st_size / 1e6
    reduction = (1 - toy_mb / orig_mb) * 100

    print(
        f"✅  Toy brain saved: {t1w_path}\n"
        f"    Original size : {orig_mb:.1f} MB\n"
        f"    Toy size      : {toy_mb:.1f} MB\n"
        f"    Reduction     : {reduction:.0f}%"
    )


if __name__ == "__main__":
    main()