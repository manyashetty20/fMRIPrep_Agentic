#!/usr/bin/env python3
"""
testing/run_failure_injection.py
================================
Inject controlled BIDS defects, run the agentic pipeline, restore, and optionally
repeat N times per failure type for publication statistics.

Original source BIDS data is never modified: each trial copies into an isolated
work directory that is deleted after the run (unless ``--keep-mutated``).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

_TESTING = Path(__file__).resolve().parent
_ROOT = _TESTING.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from testing.common import (
    DEFAULT_RESULTS_ROOT,
    ROOT,
    base_main_cmd,
    load_test_config,
    project_python,
    run_command,
    validate_prerequisites,
    write_run_manifest,
)

INJECTION_MODES = (
    "missing_tr",
    "bad_readout",
    "missing_fmap",
    "strip_phase_encoding",
    "malformed_json",
    "truncate_json",
    "oom",
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Failure-injection evaluation suite.")
    p.add_argument(
        "--config",
        type=Path,
        default=_TESTING / "config" / "publication_battery.yaml",
    )
    p.add_argument("--mode", choices=INJECTION_MODES, required=True)
    p.add_argument("--participant", metavar="ID", required=True)
    p.add_argument(
        "--trials",
        type=int,
        default=1,
        help="Repeat inject→run→restore this many times (default: 1).",
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-docker-check", action="store_true")
    p.add_argument(
        "--force",
        action="store_true",
        help="Remove existing mutated BIDS work dir if present.",
    )
    p.add_argument(
        "--keep-mutated",
        action="store_true",
        help="Keep the mutated BIDS copy after each trial (default: delete to restore isolation).",
    )
    return p.parse_args()


def _participant_label(raw: str) -> str:
    return raw if raw.startswith("sub-") else f"sub-{raw}"


def _inject_bids(
    cfg,
    mode: str,
    participant: str,
    work_dir: Path,
    *,
    dry_run: bool,
    force: bool,
) -> int:
    if mode == "oom":
        print(
            "Mode `oom` uses mock Docker (no BIDS mutation).\n"
            "Run: python testing/run_smoke.py\n"
            "Or set FMRIPREP_MOCK_FORCE_EXIT137=1 with mock docker on PATH."
        )
        return 0

    if work_dir.exists():
        if not force:
            print(f"❌ Work dir exists: {work_dir} (use --force to replace)", file=sys.stderr)
            return 1
        shutil.rmtree(work_dir)

    cmd = [
        str(project_python()),
        str(ROOT / "scripts" / "inject_failures.py"),
        "--bids-dir",
        str(cfg.bids_dir),
        "--work-dir",
        str(work_dir),
        "--mode",
        mode,
        "--participant",
        participant,
    ]
    return run_command(cmd, dry_run=dry_run)


def _run_one_trial(
    cfg,
    *,
    mode: str,
    pid: str,
    trial_idx: int,
    dry_run: bool,
    force: bool,
    keep_mutated: bool,
) -> int:
    from dataclasses import replace

    mutated_root = (
        DEFAULT_RESULTS_ROOT
        / "bids_mutated"
        / cfg.dataset_id
        / f"{mode}_{pid}_trial{trial_idx:02d}"
    )
    rc = _inject_bids(
        cfg, mode, pid, mutated_root, dry_run=dry_run, force=force or mutated_root.exists()
    )
    if rc != 0 or dry_run:
        return rc

    run_cfg = replace(cfg, bids_dir=mutated_root, dataset_id=f"{cfg.dataset_id}_{mode}")
    out_dir = run_cfg.output_dir_for(f"failure_{mode}", f"{pid}_trial{trial_idx:02d}")
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = base_main_cmd(
        run_cfg,
        participant=pid,
        output_dir=out_dir,
        injected_failure_mode=mode,
    )
    log = (
        DEFAULT_RESULTS_ROOT
        / "logs"
        / "failure"
        / mode
        / cfg.dataset_id
        / f"{pid}_trial{trial_idx:02d}.log"
    )
    rc = run_command(cmd, dry_run=False, log_file=log)

    manifest = {
        "suite": "failure_injection",
        "mode": mode,
        "participant": pid,
        "trial_index": trial_idx,
        "source_bids": str(cfg.bids_dir),
        "mutated_bids": str(mutated_root),
        "output_dir": str(out_dir),
        "exit_code": rc,
        "restored": not keep_mutated,
    }
    inj = mutated_root / ".agentic_failure_injection.json"
    if inj.is_file():
        manifest["injection_manifest"] = json.loads(inj.read_text())

    write_run_manifest(
        DEFAULT_RESULTS_ROOT
        / "manifests"
        / "failure"
        / mode
        / cfg.dataset_id
        / f"{pid}_trial{trial_idx:02d}.json",
        manifest,
    )

    # Restore isolation: delete mutated copy so the next trial starts clean.
    if not keep_mutated and mutated_root.exists():
        shutil.rmtree(mutated_root)
        print(f"🧹 Restored (deleted mutated copy): {mutated_root}")

    return rc


def main() -> int:
    args = parse_args()

    if not args.config.is_file():
        print(f"❌ Config not found: {args.config}", file=sys.stderr)
        return 1

    if args.trials < 1:
        print("❌ --trials must be >= 1", file=sys.stderr)
        return 1

    cfg = load_test_config(args.config)
    pid = _participant_label(args.participant)

    if args.mode == "oom":
        return _inject_bids(cfg, "oom", pid, Path(), dry_run=args.dry_run, force=args.force)

    issues = validate_prerequisites(
        cfg, require_docker=not args.skip_docker_check and not args.dry_run
    )
    if issues:
        for msg in issues:
            print(f"❌ {msg}", file=sys.stderr)
        return 1

    exit_codes: list[int] = []
    for trial_idx in range(1, args.trials + 1):
        print(f"\n=== Failure injection trial {trial_idx}/{args.trials} mode={args.mode} ===")
        rc = _run_one_trial(
            cfg,
            mode=args.mode,
            pid=pid,
            trial_idx=trial_idx,
            dry_run=args.dry_run,
            force=args.force,
            keep_mutated=args.keep_mutated,
        )
        exit_codes.append(rc)
        if args.dry_run:
            break

    failures = sum(1 for c in exit_codes if c != 0)
    print(
        f"\nDone: {len(exit_codes)} trial(s), "
        f"{len(exit_codes) - failures} pipeline-success exit(s), {failures} non-zero."
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
