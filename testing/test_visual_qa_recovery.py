#!/usr/bin/env python3
"""
testing/test_visual_qa_recovery.py
==================================
Tests closed-loop visual QA and anatomical recovery:
1. Simulates initial visual/anatomical QA defect (boundary clipping / over-stripping).
2. Verifies QA node detects defect and routes to detective.
3. Verifies recovery agent applies --skull-strip-template / --skull-strip-fixed-seed.
4. Verifies second run succeeds with QA verdict PASS.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = ROOT / "venv" / "bin" / "python"
if not VENV_PYTHON.exists():
    VENV_PYTHON = Path(sys.executable)

TEST_ROOT = ROOT / "tmp" / "test_visual_qa_recovery"
TEST_BIDS = TEST_ROOT / "bids"
TEST_OUTPUTS = TEST_ROOT / "outputs"
MOCK_BIN = TEST_ROOT / "mock_bin"
TEST_LOG = TEST_ROOT / "test_run.log"


def _write_mock_docker_wrapper() -> None:
    MOCK_BIN.mkdir(parents=True, exist_ok=True)
    wrapper = MOCK_BIN / "docker"
    wrapper.write_text(
        "#!/bin/sh\n"
        f'exec "{VENV_PYTHON}" "{ROOT / "scripts" / "mock_docker.py"}" "$@"\n'
    )
    wrapper.chmod(0o755)


def main() -> int:
    print("\n🧪 Running Closed-Loop Visual QA Recovery Test...")

    if TEST_ROOT.exists():
        shutil.rmtree(TEST_ROOT)
    TEST_ROOT.mkdir(parents=True, exist_ok=True)

    # 1. Prepare test dataset
    prep_cmd = [
        str(VENV_PYTHON),
        str(ROOT / "scripts" / "prepare_smoke_dataset.py"),
        "--source-bids",
        str(ROOT / "data" / "bids_input"),
        "--dest-bids",
        str(TEST_BIDS),
        "--participant",
        "sub-01",
        "--bold-volumes",
        "8",
    ]
    subprocess.run(prep_cmd, check=True)
    _write_mock_docker_wrapper()

    env = os.environ.copy()
    env["PATH"] = f"{MOCK_BIN}:{env.get('PATH', '')}"
    # Inject initial anatomical QA failure in mock docker
    env["FMRIPREP_MOCK_INJECT_ANAT_FAIL"] = "1"

    # 2. Run Agentic fMRIPrep
    run_cmd = [
        str(VENV_PYTHON),
        str(ROOT / "main.py"),
        "--bids-dir",
        str(TEST_BIDS),
        "--output-dir",
        str(TEST_OUTPUTS),
        "--participant",
        "sub-01",
        "--low-mem",
        "--nprocs",
        "1",
        "--max-retries",
        "3",
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

    TEST_LOG.write_text(result.stdout + "\n--- STDERR ---\n" + result.stderr)

    print(f"Test run completed with exit code: {result.returncode}")

    if result.returncode != 0:
        print("❌ Pipeline failed to exit cleanly. Log excerpt:")
        print(result.stdout[-1500:])
        print(result.stderr[-1500:])
        return 1

    # 3. Verify closed-loop recovery artifacts
    qa_results_dir = TEST_OUTPUTS / "agentic_results" / "sub-01"
    summary_file = qa_results_dir / "run_summary.json"
    qa_metrics_file = qa_results_dir / "qa_metrics.json"

    if not summary_file.exists() or not qa_metrics_file.exists():
        print("❌ Missing QA result files in agentic_results/sub-01")
        return 1

    summary = json.loads(summary_file.read_text())
    qa_metrics = json.loads(qa_metrics_file.read_text())

    attempt_count = summary.get("attempt_count", 0)
    final_cmd = summary.get("final_command", "")
    qa_verdict = qa_metrics.get("qa_summary", "")

    print(f"▶ Total Attempts: {attempt_count}")
    print(f"▶ Final QA Verdict: {qa_verdict}")
    print(f"▶ Final Command: {final_cmd}")

    # Checks
    assert attempt_count >= 2, f"Expected at least 2 attempts due to QA self-healing loop, got {attempt_count}"
    assert "--skull-strip-template" in final_cmd, "Expected --skull-strip-template to be injected by RecoveryAgent"
    assert qa_verdict == "PASS", f"Expected final QA verdict to be PASS, got {qa_verdict}"

    print("✅ Closed-loop visual QA recovery verified successfully!\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
