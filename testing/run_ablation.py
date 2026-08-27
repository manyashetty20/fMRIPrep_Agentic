#!/usr/bin/env python3
"""
testing/run_ablation.py
=======================
Run ablation conditions for publication tables.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_TESTING = Path(__file__).resolve().parent
_ROOT = _TESTING.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from testing.common import (
    DEFAULT_RESULTS_ROOT,
    base_main_cmd,
    load_test_config,
    run_command,
    validate_prerequisites,
    write_run_manifest,
)

ABLATIONS: dict[str, list[str]] = {
    "full": [],
    "no_recovery": ["--no-recovery"],
    "no_diagnosis": ["--no-diagnosis"],
    "no_vision": ["--no-vision"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ablation study runner.")
    p.add_argument(
        "--config",
        type=Path,
        default=_TESTING / "config" / "publication_battery.yaml",
    )
    p.add_argument(
        "--condition",
        choices=sorted(ABLATIONS.keys()),
        default=None,
        help="Run one ablation (default: all four).",
    )
    p.add_argument("--participant", metavar="ID")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-docker-check", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if not args.config.is_file():
        print(f"❌ Config not found: {args.config}", file=sys.stderr)
        return 1

    cfg = load_test_config(args.config)
    participants = [args.participant] if args.participant else cfg.participants
    if args.participant and not args.participant.startswith("sub-"):
        participants = [f"sub-{args.participant}"]

    issues = validate_prerequisites(
        cfg, require_docker=not args.skip_docker_check and not args.dry_run
    )
    if issues:
        for msg in issues:
            print(f"❌ {msg}", file=sys.stderr)
        return 1

    conditions = [args.condition] if args.condition else sorted(ABLATIONS.keys())
    codes: list[int] = []

    for cond in conditions:
        ablation_args = ABLATIONS[cond]
        for pid in participants:
            out_dir = cfg.output_dir_for(f"ablation_{cond}", pid)
            out_dir.mkdir(parents=True, exist_ok=True)
            cmd = base_main_cmd(
                cfg,
                participant=pid,
                output_dir=out_dir,
                ablation_args=ablation_args,
            )
            log = DEFAULT_RESULTS_ROOT / "logs" / "ablation" / cond / cfg.dataset_id / f"{pid}.log"
            rc = run_command(cmd, dry_run=args.dry_run, log_file=None if args.dry_run else log)
            write_run_manifest(
                DEFAULT_RESULTS_ROOT / "manifests" / "ablation" / cond / cfg.dataset_id / f"{pid}.json",
                {
                    "suite": "ablation",
                    "condition": cond,
                    "participant": pid,
                    "output_dir": str(out_dir),
                    "exit_code": rc,
                },
            )
            codes.append(rc)

    return 0 if all(c == 0 for c in codes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
