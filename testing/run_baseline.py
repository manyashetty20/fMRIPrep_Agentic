#!/usr/bin/env python3
"""
testing/run_baseline.py
=======================
Run vanilla fMRIPrep (no agentic loop) for baseline comparison tables.
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
    base_baseline_cmd,
    load_test_config,
    run_command,
    validate_prerequisites,
    write_run_manifest,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Baseline fMRIPrep evaluation suite.")
    p.add_argument(
        "--config",
        type=Path,
        default=_TESTING / "config" / "publication_battery.yaml",
        help="YAML test config (see publication_battery.example.yaml).",
    )
    p.add_argument("--participant", metavar="ID", help="Run one subject only.")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-docker-check", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if not args.config.is_file():
        print(
            f"❌ Config not found: {args.config}\n"
            f"   Copy testing/config/publication_battery.example.yaml → publication_battery.yaml",
            file=sys.stderr,
        )
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

    codes: list[int] = []
    for pid in participants:
        out_dir = cfg.output_dir_for("baseline", pid)
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = base_baseline_cmd(cfg, participant=pid, output_dir=out_dir)
        log = DEFAULT_RESULTS_ROOT / "logs" / "baseline" / cfg.dataset_id / f"{pid}.log"
        rc = run_command(cmd, dry_run=args.dry_run, log_file=None if args.dry_run else log)
        write_run_manifest(
            DEFAULT_RESULTS_ROOT / "manifests" / "baseline" / cfg.dataset_id / f"{pid}.json",
            {"suite": "baseline", "participant": pid, "output_dir": str(out_dir), "exit_code": rc},
        )
        codes.append(rc)

    return 0 if all(c == 0 for c in codes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
