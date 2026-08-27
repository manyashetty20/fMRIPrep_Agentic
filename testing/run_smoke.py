#!/usr/bin/env python3
"""
testing/run_smoke.py
====================
Fast orchestration smoke test (mock Docker, no real fMRIPrep).

Exercises: config → executor → diagnostic → recovery → QA.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_TESTING = Path(__file__).resolve().parent
_ROOT = _TESTING.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from testing.common import ROOT, run_command, write_run_manifest


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Agentic fMRIPrep smoke test (mock Docker).")
    p.add_argument("--dry-run", action="store_true", help="Print the underlying command only.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = _TESTING / "results" / "manifests" / "smoke_test.json"
    cmd = [str(ROOT / "venv" / "bin" / "python"), str(ROOT / "scripts" / "run_full_agent_smoke.py")]
    if not (ROOT / "venv" / "bin" / "python").exists():
        cmd = [sys.executable, str(ROOT / "scripts" / "run_full_agent_smoke.py")]

    rc = run_command(cmd, dry_run=args.dry_run)
    write_run_manifest(
        manifest_path,
        {
            "suite": "smoke",
            "command": cmd,
            "exit_code": rc,
            "artifacts": {
                "smoke_root": str(ROOT / "tmp" / "full_agent_smoke"),
                "smoke_log": str(ROOT / "tmp" / "full_agent_smoke" / "smoke_run.log"),
            },
        },
    )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
