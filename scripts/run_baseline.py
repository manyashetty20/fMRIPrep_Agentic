#!/usr/bin/env python3
"""
scripts/run_baseline.py
=======================
Run **vanilla** fMRIPrep (Docker command from ConfigAgent rule-based builder) once — no
LLM planning, no diagnosis, no recovery loop — and log comparable evaluation fields.

Metrics are appended to ``output/evaluation/baseline_evaluation.csv`` alongside
``run_evaluation.csv`` from the agentic runs.
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import subprocess
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from bids_discovery import is_all_participants_token, list_bids_participants
from config_loader import Config
from agents.config_agent import ConfigAgent
from evaluation_export import append_evaluation_exports, build_evaluation_row

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Baseline fMRIPrep (no agentic loop).")
    p.add_argument("--config", metavar="PATH", default=None)
    p.add_argument("--bids-dir", metavar="PATH")
    p.add_argument("--output-dir", metavar="PATH")
    p.add_argument("--evaluation-export-root", metavar="PATH", default=None)
    p.add_argument("--license", metavar="PATH")
    p.add_argument("--participant", metavar="ID")
    p.add_argument("--session", metavar="ID")
    p.add_argument("--all-participants", action="store_true")
    p.add_argument("--max-participants", type=int, default=None, metavar="N")
    p.add_argument("--dry-run", action="store_true", help="Print command only; do not execute.")
    return p.parse_args()


def _overrides_from_args(args: argparse.Namespace) -> dict:
    o: dict = {}
    if args.bids_dir:
        o["paths.bids_dir"] = args.bids_dir
    if args.output_dir:
        o["paths.output_dir"] = args.output_dir
    if args.evaluation_export_root:
        o["paths.evaluation_export_root"] = args.evaluation_export_root
    if args.license:
        o["paths.license_file"] = args.license
    if args.participant:
        pid = args.participant
        if not str(pid).startswith("sub-") and not is_all_participants_token(str(pid)):
            pid = f"sub-{pid}"
        o["subject.participant_id"] = pid
    if args.session:
        o["subject.session_id"] = args.session
    return o


def _minimal_state_for_baseline(cmd: str, exit_code: int, wall_s: float) -> dict:
    """Synthetic graph-like state so ``build_evaluation_row`` stays uniform."""
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    ok = exit_code == 0
    return {
        "status": "completed" if ok else "failed",
        "command": cmd,
        "attempt_count": 1,
        "history": [],
        "events": [
            {
                "type": "planning",
                "timestamp": ts,
                "command": cmd,
            },
            {
                "type": "execution",
                "timestamp": ts,
                "attempt": 1,
                "status": "success" if ok else "failed",
                "exit_code": exit_code,
                "command": cmd,
                "stdout_tail": "",
                "log_tail": "",
            },
        ],
    }


def run_one(cfg: Config, args: argparse.Namespace) -> int:
    agent = ConfigAgent(cfg)
    cmd = agent.generate_command()
    if args.dry_run:
        print(cmd)
        return 0

    t0 = time.perf_counter()
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    wall = time.perf_counter() - t0

    state = _minimal_state_for_baseline(cmd, proc.returncode, wall)
    row = build_evaluation_row(
        cfg,
        state,
        run_mode="baseline",
        wall_clock_seconds=wall,
        baseline_requires_manual_steps=False,
    )
    out = cfg.output_dir / "agentic_results" / cfg.participant_id / "baseline_run.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "command": cmd,
                "exit_code": proc.returncode,
                "wall_clock_seconds": wall,
                "stdout_tail": proc.stdout[-4000:] if proc.stdout else "",
                "stderr_tail": proc.stderr[-4000:] if proc.stderr else "",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    (out.parent / "baseline_evaluation_row.json").write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")
    append_evaluation_exports(
        row,
        eval_root=cfg.evaluation_export_root,
        csv_name="baseline_evaluation.csv",
        jsonl_name="baseline_evaluation.jsonl",
    )

    if proc.returncode != 0:
        print(proc.stderr[-4000:] or proc.stdout[-4000:] or "(no stderr)", file=sys.stderr)
    return proc.returncode


def main() -> None:
    args = parse_args()
    overrides = _overrides_from_args(args)
    if args.all_participants:
        overrides["subject.participant_id"] = "all"

    cfg0 = Config(yaml_path=args.config, overrides=overrides)
    try:
        cfg0.validate()
    except FileNotFoundError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        sys.exit(1)

    if is_all_participants_token(str(cfg0.participant_id)):
        pids = list_bids_participants(cfg0.bids_dir, require_anat_t1w=True)
        if not pids:
            print(f"❌ No subjects found under {cfg0.bids_dir}", file=sys.stderr)
            sys.exit(1)
        if args.max_participants is not None:
            pids = pids[: max(0, args.max_participants)]
        codes: list[int] = []
        for pid in pids:
            try:
                o = dict(overrides)
                o["subject.participant_id"] = pid
                cfg = Config(yaml_path=args.config, overrides=o)
                codes.append(run_one(cfg, args))
            except Exception as exc:
                logger.exception(
                    "Baseline run for %s failed with an unexpected error; continuing batch.",
                    pid,
                )
                print(
                    f"\n⚠️  {pid}: unexpected error (logged above). Continuing.\n",
                    file=sys.stderr,
                )
                codes.append(1)
        sys.exit(0 if all(c == 0 for c in codes) else 1)

    sys.exit(run_one(cfg0, args))


if __name__ == "__main__":
    main()
