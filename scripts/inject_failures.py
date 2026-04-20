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

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from bids_discovery import list_bids_participants

FAILURE_MODES = frozenset({"oom", "missing_tr", "missing_fmap", "bad_readout"})


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
    with_func = [p for p in candidates if (bids / p / "func").is_dir() and any((bids / p / "func").glob("*.json"))]
    if with_func:
        return with_func[0]
    if candidates:
        return candidates[0]
    raise FileNotFoundError(f"No sub-* directories found under {bids}")


def _pick_bold_json(func_dir: Path) -> Path:
    jsons = sorted(func_dir.glob("*_bold.json"))
    if not jsons:
        raise FileNotFoundError(f"No *_bold.json under {func_dir}")
    return jsons[0]


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
        func_dir = dst / sub / "func"
        fmap_dir = dst / sub / "fmap"

        manifest: dict = {
            "mode": args.mode,
            "participant": sub,
            "source_bids": str(src),
            "mutated_bids": str(dst),
        }

        if args.mode == "missing_tr":
            j = _pick_bold_json(func_dir)
            _strip_keys(j, {"RepetitionTime"})
            manifest["edited_sidecar"] = str(j)

        elif args.mode == "bad_readout":
            j = _pick_bold_json(func_dir)
            _strip_keys(j, {"TotalReadoutTime", "EffectiveEchoSpacing"})
            manifest["edited_sidecar"] = str(j)

        elif args.mode == "missing_fmap":
            if not fmap_dir.is_dir():
                raise FileNotFoundError(f"No fmap directory to hide: {fmap_dir}")
            hidden = dst / sub / "_injected_fmap_backup"
            fmap_dir.rename(hidden)
            manifest["hidden_fieldmap_dir"] = str(hidden)

        (dst / ".agentic_failure_injection.json").write_text(json.dumps(manifest, indent=2) + "\n")
        print(json.dumps(manifest, indent=2))
    except Exception:
        if dst.exists():
            shutil.rmtree(dst)
        raise


if __name__ == "__main__":
    main()
