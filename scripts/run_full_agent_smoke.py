#!/usr/bin/env python3
"""
Run an isolated smoke test that exercises config, diagnostic, recovery, and vision.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = ROOT / "venv" / "bin" / "python"
SMOKE_ROOT = ROOT / "tmp" / "full_agent_smoke"
SMOKE_BIDS = SMOKE_ROOT / "bids"
SMOKE_OUTPUTS = SMOKE_ROOT / "outputs"
MOCK_BIN = SMOKE_ROOT / "mock_bin"
SMOKE_LOG = SMOKE_ROOT / "smoke_run.log"


def _write_mock_docker_wrapper() -> None:
    MOCK_BIN.mkdir(parents=True, exist_ok=True)
    wrapper = MOCK_BIN / "docker"
    wrapper.write_text(
        "#!/bin/sh\n"
        f'exec "{VENV_PYTHON}" "{ROOT / "scripts" / "mock_docker.py"}" "$@"\n'
    )
    wrapper.chmod(0o755)


def main() -> int:
    if SMOKE_ROOT.exists():
        shutil.rmtree(SMOKE_ROOT)
    SMOKE_ROOT.mkdir(parents=True, exist_ok=True)

    prep_cmd = [
        str(VENV_PYTHON),
        str(ROOT / "scripts" / "prepare_smoke_dataset.py"),
        "--source-bids",
        str(ROOT / "data" / "bids_input"),
        "--dest-bids",
        str(SMOKE_BIDS),
        "--participant",
        "sub-01",
        "--bold-volumes",
        "12",
    ]
    subprocess.run(prep_cmd, check=True)

    _write_mock_docker_wrapper()

    env = os.environ.copy()
    env["PATH"] = f"{MOCK_BIN}:{env.get('PATH', '')}"

    run_cmd = [
        str(VENV_PYTHON),
        str(ROOT / "main.py"),
        "--bids-dir",
        str(SMOKE_BIDS),
        "--output-dir",
        str(SMOKE_OUTPUTS),
        "--participant",
        "sub-01",
        "--no-anat-only",
        "--no-low-mem",
        "--nprocs",
        "4",
        "--log-level",
        "INFO",
    ]

    result = subprocess.run(
        run_cmd,
        env=env,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )

    SMOKE_LOG.write_text(result.stdout + "\n--- STDERR ---\n" + result.stderr)

    print(f"Smoke test exit code: {result.returncode}")
    print(f"Smoke BIDS dir: {SMOKE_BIDS}")
    print(f"Smoke outputs: {SMOKE_OUTPUTS}")
    print(f"Smoke log: {SMOKE_LOG}")

    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        return result.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
