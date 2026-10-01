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

    force_oom = os.environ.get("FMRIPREP_MOCK_FORCE_EXIT137", "").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    if force_oom:
        sys.stderr.write(
            "Mock docker: FMRIPREP_MOCK_FORCE_EXIT137 enabled — simulating OOM exit 137\n"
        )
        return 137

    participant_label = _flag_value(args, "--participant-label", "01") or "01"
    participant = participant_label if participant_label.startswith("sub-") else f"sub-{participant_label}"
    nprocs = int(_flag_value(args, "--nprocs", "1") or "1")
    has_low_mem = "--low-mem" in args

    bids_dir = _mounted_host(args, "/data")
    output_dir = _mounted_host(args, "/out")

    # 1. TTY check
    if any(tok in ("-t", "-i", "-ti") for tok in args):
        sys.stderr.write("the input device is not a TTY: cannot allocate pseudo-tty\n")
        return 1

    # 2. FreeSurfer License check
    license_mounted = False
    for i, tok in enumerate(args):
        if tok == "-v" and i + 1 < len(args):
            mount = args[i + 1]
            if "license" in mount.lower():
                host_file = Path(mount.split(":")[0])
                if host_file.is_file() and host_file.stat().st_size > 0:
                    license_mounted = True
    if not license_mounted and "--fs-no-reconall" not in args:
        sys.stderr.write("ERROR: a valid license file is required for FreeSurfer to run\nlicense file not found\n")
        return 1

    # Read defect manifest if present
    manifest_file = bids_dir / ".agentic_failure_injection.json"
    manifest: dict = {}
    if manifest_file.exists():
        try:
            import json as json_lib
            manifest = json_lib.loads(manifest_file.read_text())
        except Exception:
            pass
    inj_mode = manifest.get("mode", "")

    # 3. Missing TR check
    if inj_mode in ("missing_tr",):
        missing_tr = False
        import json as json_lib
        for jf in (bids_dir / participant).glob("**/*_bold.json"):
            try:
                data = json_lib.loads(jf.read_text())
                if not data.get("RepetitionTime"):
                    missing_tr = True
                    break
            except Exception:
                missing_tr = True
                break
        if missing_tr and "--skip-bids-validation" not in args:
            sys.stderr.write("BIDS validation failed: RepetitionTime is required in BIDS metadata for functional scans\n")
            return 1

    # 4. Readout timing check
    if inj_mode in ("bad_readout", "missing_total_readout_time"):
        if "--fallback-total-readout-time" not in args and "--anat-only" not in args:
            sys.stderr.write("Missing readout time information: Unknown total-readout time specification\n")
            return 1

    # 5. SyN PhaseEncoding absent check
    has_syn = "--use-syn-sdc" in args
    ignore_fmap = "--ignore" in args and "fieldmaps" in args
    if inj_mode in ("strip_phase_encoding", "missing_phase_encoding") or has_syn:
        # Check if phase encoding is missing in sidecars
        missing_ped = False
        import json as json_lib
        for jf in (bids_dir / participant).glob("**/*_bold.json"):
            try:
                data = json_lib.loads(jf.read_text())
                if not data.get("PhaseEncodingDirection"):
                    missing_ped = True
                    break
            except Exception:
                missing_ped = True
                break
        if (inj_mode in ("strip_phase_encoding", "missing_phase_encoding") or missing_ped) and has_syn and not ignore_fmap:
            sys.stderr.write("Fieldmap-less (SyN) estimation was requested, but PhaseEncodingDirection is absent\n")
            return 1

    # 6. Fieldmap inconsistency check
    if inj_mode in ("fieldmap_inconsistency", "missing_fmap"):
        if not ("--ignore" in args and "fieldmaps" in args):
            sys.stderr.write("Fieldmap / distortion-correction error: invalid fieldmap pairing or missing metadata\n")
            return 1

    # 7. FreeSurfer naming conflict check
    if inj_mode == "fs_naming_conflict":
        if "--fs-no-reconall" not in args:
            sys.stderr.write("FileExistsError: naming conflict in FreeSurfer output directory\n")
            return 1

    # 8. OOM check
    if force_oom or (inj_mode == "oom" and not has_low_mem) or (not has_low_mem) or nprocs > 1:
        sys.stderr.write(
            "fMRIPrep worker crashed: out of memory\n"
            "Process killed with exit code 137\n"
        )
        return 137

    # Find T1w image
    t1_candidates = [
        bids_dir / participant / "anat" / f"{participant}_T1w.nii.gz",
        *sorted((bids_dir / participant).glob("ses-*/anat/*_T1w.nii.gz")),
        *sorted((bids_dir / participant).glob("anat/*_T1w.nii.gz")),
    ]
    src = next((p for p in t1_candidates if p.is_file()), None)

    anat_dir = output_dir / "fmriprep" / participant / "anat"
    anat_dir.mkdir(parents=True, exist_ok=True)

    dst_preproc = anat_dir / f"{participant}_desc-preproc_T1w.nii.gz"
    dst_mni = anat_dir / f"{participant}_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz"
    dst_mask = anat_dir / f"{participant}_desc-brain_mask.nii.gz"

    simulate_anat_defect = os.environ.get("FMRIPREP_MOCK_INJECT_ANAT_FAIL", "").strip().lower() in ("1", "true")
    has_template_fix = "--skull-strip-template" in args

    try:
        import nibabel as nib
        import numpy as np

        if src and src.exists():
            img = nib.load(str(src))
            data = img.get_fdata()
            affine = img.affine
            header = img.header
        else:
            data = np.ones((64, 64, 64), dtype=np.float32) * 100.0
            affine = np.eye(4)
            header = None

        if not dst_preproc.exists():
            nib.Nifti1Image(data, affine, header).to_filename(str(dst_preproc))
        if not dst_mni.exists():
            nib.Nifti1Image(data, affine, header).to_filename(str(dst_mni))

        if simulate_anat_defect and not has_template_fix:
            bad_mask = np.zeros_like(data, dtype=np.uint8)
            bad_mask[0, :3, :3] = 1
            bad_mask[5:7, 5:7, 5:7] = 1
            nib.Nifti1Image(bad_mask, affine, header).to_filename(str(dst_mask))
        else:
            mask = np.zeros_like(data, dtype=np.uint8)
            cx, cy, cz = [s // 2 for s in data.shape[:3]]
            rx = max(1, data.shape[0] // 5)
            ry = max(1, data.shape[1] // 5)
            rz = max(1, data.shape[2] // 5)
            mask[cx - rx : cx + rx, cy - ry : cy + ry, cz - rz : cz + rz] = 1
            nib.Nifti1Image(mask, affine, header).to_filename(str(dst_mask))
    except Exception:
        if src and src.exists():
            shutil.copy2(src, dst_preproc)
            shutil.copy2(src, dst_mni)
            shutil.copy2(src, dst_mask)

    fig_dir = output_dir / "fmriprep" / participant / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    (fig_dir / f"{participant}_dseg.svg").write_text("<svg><text>Mock dseg</text></svg>")
    (fig_dir / f"{participant}_space-MNI152NLin2009cAsym_T1w.svg").write_text("<svg><text>Mock MNI</text></svg>")

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
