#!/usr/bin/env python3
"""
testing/run_publication_battery.py
==================================
Master runner for publication evaluation (sequential suites).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_TESTING = Path(__file__).resolve().parent
_ROOT = _TESTING.parent


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run the full publication evaluation battery.")
    p.add_argument(
        "--config",
        type=Path,
        default=_TESTING / "config" / "publication_battery.yaml",
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-docker-check", action="store_true")
    p.add_argument("--skip-smoke", action="store_true")
    p.add_argument("--skip-baseline", action="store_true")
    p.add_argument("--skip-ablation", action="store_true")
    p.add_argument("--skip-failure", action="store_true")
    p.add_argument(
        "--failure-participant",
        default="sub-01",
        help="Subject used for failure-injection runs.",
    )
    return p.parse_args()


def _run(script: str, extra: list[str]) -> int:
    cmd = [sys.executable, str(_TESTING / script), *extra]
    print(f"\n{'=' * 60}\n▶ {script}\n{'=' * 60}")
    return subprocess.run(cmd, cwd=str(_ROOT)).returncode


def main() -> int:
    args = parse_args()
    common = ["--config", str(args.config)]
    if args.dry_run:
        common.append("--dry-run")
    if args.skip_docker_check:
        common.append("--skip-docker-check")

    codes: list[int] = []

    if not args.skip_smoke:
        codes.append(_run("run_smoke.py", ["--dry-run"] if args.dry_run else []))

    codes.append(_run("run_baseline.py", common))
    codes.append(_run("run_agentic.py", common))

    if not args.skip_ablation:
        codes.append(_run("run_ablation.py", common))

    if not args.skip_failure:
        for mode in ("missing_tr", "bad_readout", "missing_fmap"):
            extra = common + [
                "--mode",
                mode,
                "--participant",
                args.failure_participant,
                "--force",
            ]
            codes.append(_run("run_failure_injection.py", extra))

    codes.append(_run("analyze_results.py", ["--eval-root", "./testing/results/evaluation"]))

    failed = sum(1 for c in codes if c != 0)
    print(f"\nPublication battery finished: {len(codes) - failed}/{len(codes)} suites OK.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
