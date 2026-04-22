#!/usr/bin/env python3
"""
scripts/inject_failures.py
==========================
Create an **isolated copy** of BIDS data with a controlled defect for recovery experiments.

The mutated tree is written to ``--work-dir``; the original dataset is never modified.

Modes
-----
- ``missing_tr`` — remove ``RepetitionTime`` from one ``*_bold.json`` sidecar.
- ``missing_fmap`` — hide ``<sub>/fmap`` by renaming it (dataset acts as if fieldmaps are absent).
- ``bad_readout`` — remove ``TotalReadoutTime`` and ``EffectiveEchoSpacing`` from ``*_bold.json``.
- ``oom`` — does **not** change files; prints how to pair with ``scripts/mock_docker.py`` and
  ``FMRIPREP_MOCK_FORCE_EXIT137=1`` for a repeatable exit 137.

No OpenNeuro IDs or paths are hardcoded: all inputs come from CLI flags.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import nibabel as nib

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from bids_discovery import list_bids_participants

FAILURE_MODES = frozenset({"oom", "missing_tr", "missing_fmap", "bad_readout"})
DEFAULT_TOTAL_READOUT_TIME = 0.05
DEFAULT_EFFECTIVE_ECHO_SPACING = 0.0005


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Inject controlled BIDS defects for recovery evaluation.")
    p.add_argument("--bids-dir", required=True, type=Path, help="Source BIDS root (read-only).")
    p.add_argument(
        "--work-dir",
        required=True,
        type=Path,
        help="Writable copy of the dataset with the selected failure applied.",
    )
    p.add_argument(
        "--mode",
        required=True,
        choices=sorted(FAILURE_MODES),
        help="Failure injection mode.",
    )
    p.add_argument(
        "--participant",
        default=None,
        help="Limit sidecar edits to this subject (sub-XX). Default: first subject with func data.",
    )
    return p.parse_args()


def _ensure_sub(participant: str | None, bids: Path) -> str:
    if participant:
        return participant if participant.startswith("sub-") else f"sub-{participant}"
    candidates = list_bids_participants(bids, require_anat_t1w=False)
    with_func = [p for p in candidates if _resolve_func_dirs(bids / p)]
    if with_func:
        return with_func[0]
    if candidates:
        return candidates[0]
    raise FileNotFoundError(f"No sub-* directories found under {bids}")


def _session_sort_key(path: Path) -> tuple[int, str]:
    ses = path.parent.name if path.parent.name.startswith("ses-") else path.name
    is_retest = "retest" in ses.lower()
    return (1 if is_retest else 0, str(path))


def _resolve_func_dirs(subject_dir: Path) -> list[Path]:
    """
    Return candidate func directories for a subject.
    Flat layout is checked first; session layout is then sorted with non-retest sessions first.
    """
    dirs: list[Path] = []
    flat = subject_dir / "func"
    if flat.is_dir():
        dirs.append(flat)

    session_dirs = sorted([p for p in subject_dir.glob("ses-*/func") if p.is_dir()], key=_session_sort_key)
    dirs.extend(session_dirs)
    return dirs


def _resolve_fmap_dirs(subject_dir: Path) -> list[Path]:
    """
    Return candidate fmap directories for a subject.
    Flat layout is checked first; session layout is then sorted with non-retest sessions first.
    """
    dirs: list[Path] = []
    flat = subject_dir / "fmap"
    if flat.is_dir():
        dirs.append(flat)

    session_dirs = sorted([p for p in subject_dir.glob("ses-*/fmap") if p.is_dir()], key=_session_sort_key)
    dirs.extend(session_dirs)
    return dirs


def _pick_bold_json(subject_dir: Path) -> Path:
    for func_dir in _resolve_func_dirs(subject_dir):
        jsons = sorted(func_dir.glob("*_bold.json"))
        if jsons:
            return jsons[0]

    nii_path = _pick_bold_nifti(subject_dir)
    tr = _extract_tr_from_header(nii_path)
    sidecar = _sidecar_path_for_nifti(nii_path)
    sidecar_data = {
        "RepetitionTime": tr,
        "TotalReadoutTime": DEFAULT_TOTAL_READOUT_TIME,
        "EffectiveEchoSpacing": DEFAULT_EFFECTIVE_ECHO_SPACING,
    }
    sidecar.write_text(json.dumps(sidecar_data, indent=2, sort_keys=False) + "\n")
    return sidecar


def _pick_all_bold_jsons(subject_dir: Path) -> list[Path]:
    sidecars: list[Path] = []
    for func_dir in _resolve_func_dirs(subject_dir):
        jsons = sorted(func_dir.glob("*_bold.json"))
        if jsons:
            sidecars.extend(jsons)
            continue

        niis = sorted(func_dir.glob("*_bold.nii.gz"))
        if not niis:
            niis = sorted(func_dir.glob("*_bold.nii"))
        if not niis:
            raise FileNotFoundError(f"No *_bold.nii[.gz] under {func_dir}; cannot create sidecar.")

        nii_path = niis[0]
        tr = _extract_tr_from_header(nii_path)
        sidecar = _sidecar_path_for_nifti(nii_path)
        sidecar_data = {
            "RepetitionTime": tr,
            "TotalReadoutTime": DEFAULT_TOTAL_READOUT_TIME,
            "EffectiveEchoSpacing": DEFAULT_EFFECTIVE_ECHO_SPACING,
        }
        sidecar.write_text(json.dumps(sidecar_data, indent=2, sort_keys=False) + "\n")
        sidecars.append(sidecar)

    if sidecars:
        return sidecars
    return [_pick_bold_json(subject_dir)]


def _pick_bold_nifti(subject_dir: Path) -> Path:
    for func_dir in _resolve_func_dirs(subject_dir):
        niis = sorted(func_dir.glob("*_bold.nii.gz"))
        if niis:
            return niis[0]
        niis_uncompressed = sorted(func_dir.glob("*_bold.nii"))
        if niis_uncompressed:
            return niis_uncompressed[0]
    raise FileNotFoundError(f"No *_bold.nii[.gz] under {subject_dir} (flat func/ or ses-*/func/).")


def _extract_tr_from_header(nii_path: Path) -> float:
    img = nib.load(str(nii_path))
    zooms = img.header.get_zooms()
    if len(zooms) < 4:
        raise RuntimeError(f"NIfTI has no temporal axis for TR extraction: {nii_path}")
    return float(zooms[3])


def _sidecar_path_for_nifti(nii_path: Path) -> Path:
    name = nii_path.name
    if name.endswith(".nii.gz"):
        return nii_path.with_name(name[:-7] + ".json")
    if name.endswith(".nii"):
        return nii_path.with_name(name[:-4] + ".json")
    return nii_path.with_suffix(".json")


def _strip_keys(sidecar: Path, keys: set[str]) -> None:
    data = json.loads(sidecar.read_text())
    changed = False
    for k in keys:
        if k in data:
            del data[k]
            changed = True
    if not changed:
        raise RuntimeError(f"No keys {keys} present in {sidecar}; cannot inject defect.")
    sidecar.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")


def main() -> None:
    args = parse_args()
    src: Path = args.bids_dir.resolve()
    dst: Path = args.work_dir.resolve()

    if not src.is_dir():
        print(f"❌ bids-dir is not a directory: {src}", file=sys.stderr)
        sys.exit(1)

    if args.mode == "oom":
        print(
            "Mode `oom` does not modify BIDS files. For a repeatable OOM-style failure with the mock shim:\n"
            "  export FMRIPREP_MOCK_FORCE_EXIT137=1\n"
            "  # ensure PATH uses scripts/mock_docker.py as `docker` (see scripts/run_full_agent_smoke.py)\n"
            "  python main.py --bids-dir ... --output-dir ... --participant ...\n"
        )
        return

    if dst.exists():
        print(f"❌ work-dir already exists: {dst}", file=sys.stderr)
        sys.exit(1)

    try:
        shutil.copytree(src, dst)

        sub = _ensure_sub(args.participant, dst)
        subject_dir = dst / sub

        manifest: dict = {
            "mode": args.mode,
            "participant": sub,
            "source_bids": str(src),
            "mutated_bids": str(dst),
        }

        if args.mode == "missing_tr":
            sidecars = _pick_all_bold_jsons(subject_dir)
            for j in sidecars:
                _strip_keys(j, {"RepetitionTime"})
            manifest["edited_sidecars"] = [str(p) for p in sidecars]

        elif args.mode == "bad_readout":
            sidecars = _pick_all_bold_jsons(subject_dir)
            for j in sidecars:
                _strip_keys(j, {"TotalReadoutTime", "EffectiveEchoSpacing"})
            manifest["edited_sidecars"] = [str(p) for p in sidecars]

        elif args.mode == "missing_fmap":
            fmap_dirs = _resolve_fmap_dirs(subject_dir)
            if not fmap_dirs:
                raise FileNotFoundError(f"No fmap directory to hide under {subject_dir} (flat fmap/ or ses-*/fmap/).")
            target_fmap = fmap_dirs[0]
            hidden = target_fmap.parent / "_injected_fmap_backup"
            target_fmap.rename(hidden)
            manifest["hidden_fieldmap_dir"] = str(hidden)

        (dst / ".agentic_failure_injection.json").write_text(json.dumps(manifest, indent=2) + "\n")
        print(json.dumps(manifest, indent=2))
    except Exception:
        if dst.exists():
            shutil.rmtree(dst)
        raise


if __name__ == "__main__":
    main()
