#!/usr/bin/env python3
"""
Local docker shim for smoke-testing the agent graph.

Behavior:
  - If the command lacks --low-mem or sets --nprocs > 1, emit an OOM-like error and exit 137.
  - Otherwise, create the expected fMRIPrep-like anatomical outputs and exit 0.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def _mounted_host(args: list[str], container_path: str) -> Path:
    for i, token in enumerate(args):
        if token == "-v" and i + 1 < len(args):
            mount = args[i + 1]
            parts = mount.split(":")
            if len(parts) >= 2 and parts[1] == container_path:
                return Path(parts[0]).resolve()
    raise RuntimeError(f"Could not find mount for {container_path}")


def _flag_value(args: list[str], flag: str, default: str | None = None) -> str | None:
    value = default
    for i, token in enumerate(args):
        if token == flag and i + 1 < len(args):
            value = args[i + 1]
    return value


def main() -> int:
    args = sys.argv[1:]

    participant_label = _flag_value(args, "--participant-label", "01") or "01"
    participant = participant_label if participant_label.startswith("sub-") else f"sub-{participant_label}"
    nprocs = int(_flag_value(args, "--nprocs", "1") or "1")
    has_low_mem = "--low-mem" in args

    bids_dir = _mounted_host(args, "/data")
    output_dir = _mounted_host(args, "/out")

    if (not has_low_mem) or nprocs > 1:
        sys.stderr.write(
            "fMRIPrep worker crashed: out of memory\n"
            "Process killed with exit code 137\n"
        )
        return 137

    src = bids_dir / participant / "anat" / f"{participant}_T1w.nii.gz"
    anat_dir = output_dir / "fmriprep" / participant / "anat"
    anat_dir.mkdir(parents=True, exist_ok=True)

    dst_preproc = anat_dir / f"{participant}_desc-preproc_T1w.nii.gz"
    dst_mni = anat_dir / f"{participant}_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz"
    shutil.copy2(src, dst_preproc)
    shutil.copy2(src, dst_mni)

    report = output_dir / "fmriprep" / f"{participant}.html"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("<html><body><h1>Mock fMRIPrep report</h1></body></html>")

    sys.stdout.write(
        f"Mock docker succeeded for {participant}\n"
        f"Output written to {output_dir}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
