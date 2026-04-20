#!/usr/bin/env python3
"""
main.py
=======
Entry point for the Agentic fMRIPrep pipeline.

Usage
-----
# Use defaults from config.yaml
python main.py

# Override participant and memory limit on the fly
python main.py --participant sub-02 --mem-mb 8000

# All valid BIDS subjects under a dataset (requires T1w for discovery)
python main.py --bids-dir /data/ds000114 --participant all

# Point to a different config file
python main.py --config /path/to/my_config.yaml

# Full anatomy run (not toy / sloppy mode)
python main.py --no-sloppy --no-low-mem --nprocs 4
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import sys
import time
from pathlib import Path

from bids_discovery import is_all_participants_token, list_bids_participants
from config_loader import Config
from agents.orchestrator import build_graph
from evaluation_export import append_evaluation_exports, build_evaluation_row

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
#  CLI argument parsing
# --------------------------------------------------------------------------- #

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Agentic fMRIPrep – autonomous preprocessing pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # --- Config file ---
    parser.add_argument(
        "--config", metavar="PATH",
        default=None,
        help="Path to config.yaml (auto-detected if omitted).",
    )

    # --- Paths ---
    parser.add_argument("--bids-dir",    metavar="PATH", help="BIDS input directory.")
    parser.add_argument("--output-dir",  metavar="PATH", help="Output directory.")
    parser.add_argument(
        "--evaluation-export-root",
        metavar="PATH",
        help="Root for output/evaluation CSV exports (default: ./output → <root>/evaluation/).",
    )
    parser.add_argument("--license",     metavar="PATH", help="FreeSurfer license.txt path.")

    # --- Subject ---
    parser.add_argument(
        "--participant", metavar="ID",
        help='Participant label (e.g. sub-01) or "all" / "*" to run every subject under --bids-dir.',
    )
    parser.add_argument("--session", metavar="ID", help="Session label (optional).")
    parser.add_argument(
        "--all-participants",
        action="store_true",
        help="Shorthand for --participant all (discover all subjects under --bids-dir).",
    )
    parser.add_argument(
        "--max-participants",
        type=int,
        default=None,
        metavar="N",
        help="When running all subjects, process at most N (order is sorted BIDS IDs).",
    )

    # --- Pipeline flags ---
    parser.add_argument("--anat-only",    action="store_true",  default=None)
    parser.add_argument("--no-anat-only", action="store_false", dest="anat_only")
    parser.add_argument("--sloppy",       action="store_true",  default=None)
    parser.add_argument("--no-sloppy",    action="store_false", dest="sloppy")
    parser.add_argument("--low-mem",      action="store_true",  default=None)
    parser.add_argument("--no-low-mem",   action="store_false", dest="low_mem")
    parser.add_argument("--mem-mb",       type=int, metavar="MB")
    parser.add_argument("--nprocs",       type=int, metavar="N")
    parser.add_argument("--docker-image", metavar="IMAGE")
    parser.add_argument("--fallback-total-readout-time", type=float, metavar="SECONDS")
    parser.add_argument("--output-space", metavar="SPACE", help="Expected output space label for QA and --output-spaces in fMRIPrep.")

    # --- Agent behaviour ---
    parser.add_argument(
        "--max-retries", type=int, metavar="N",
        help="Maximum recovery attempts before giving up.",
    )
    parser.add_argument(
        "--no-vision", action="store_false", dest="vision_enabled",
        help="Skip the Vision QA agent.",
    )
    parser.add_argument(
        "--no-recovery",
        action="store_true",
        help="Ablation: disable the recovery / engineer loop (diagnosis may still run).",
    )
    parser.add_argument(
        "--no-diagnosis",
        action="store_true",
        help="Ablation: disable the diagnostic agent on failures.",
    )

    # --- LLM ---
    parser.add_argument("--llm-provider", choices=["groq", "openai", "anthropic"])
    parser.add_argument("--llm-model",    metavar="NAME")

    # --- Logging ---
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=None,
    )
    parser.add_argument("--log-file", metavar="PATH")

    return parser.parse_args()


def build_overrides(args: argparse.Namespace) -> dict:
    """Convert parsed CLI args into a flat overrides dict for Config."""
    overrides: dict = {}

    mapping = {
        "bids_dir":                 "paths.bids_dir",
        "output_dir":               "paths.output_dir",
        "evaluation_export_root": "paths.evaluation_export_root",
        "license":                  "paths.license_file",
        "participant":              "subject.participant_id",
        "session":        "subject.session_id",
        "anat_only":      "pipeline.anat_only",
        "sloppy":         "pipeline.sloppy",
        "low_mem":        "pipeline.low_mem",
        "mem_mb":         "pipeline.mem_mb",
        "nprocs":         "pipeline.nprocs",
        "docker_image":   "pipeline.docker_image",
        "fallback_total_readout_time": "pipeline.fallback_total_readout_time",
        "output_space": "pipeline.output_space",
        "max_retries":    "agents.max_recovery_attempts",
        "vision_enabled": "agents.vision_enabled",
        "llm_provider":   "llm.provider",
        "llm_model":      "llm.model_name",
        "log_level":      "logging.level",
        "log_file":       "logging.log_file",
    }

    for attr, key in mapping.items():
        val = getattr(args, attr, None)
        if val is not None:
            # Normalise participant label: always include "sub-" prefix
            if attr == "participant" and not str(val).startswith("sub-"):
                if not is_all_participants_token(str(val)):
                    val = f"sub-{val}"
            overrides[key] = val

    if getattr(args, "no_recovery", False):
        overrides["agents.recovery_enabled"] = False
    if getattr(args, "no_diagnosis", False):
        overrides["agents.diagnosis_enabled"] = False

    return overrides


# --------------------------------------------------------------------------- #
#  Main
# --------------------------------------------------------------------------- #

def main() -> None:
    args = parse_args()
    overrides = build_overrides(args)

    if args.all_participants:
        overrides["subject.participant_id"] = "all"

    base_yaml = args.config
    base_cfg = Config(yaml_path=base_yaml, overrides=overrides)

    try:
        base_cfg.validate()
    except FileNotFoundError as exc:
        print(f"\n❌  {exc}\n", file=sys.stderr)
        sys.exit(1)

    bids_dir = base_cfg.bids_dir
    run_all = is_all_participants_token(str(base_cfg.participant_id))

    if run_all:
        participants = list_bids_participants(bids_dir, require_anat_t1w=True)
        if not participants:
            print(
                f"\n❌  No BIDS subjects with anat/T1w found under: {bids_dir}\n",
                file=sys.stderr,
            )
            sys.exit(1)
        if args.max_participants is not None:
            participants = participants[: max(0, args.max_participants)]

        total = len(participants)
        print(
            f"\n🚀  Batch mode: {total} participant(s) under {bids_dir}\n"
        )
        any_fail = False
        for i, pid in enumerate(participants, start=1):
            print(f"--- [{i}/{total}] {pid} ---")
            try:
                batch_overrides = dict(overrides)
                batch_overrides["subject.participant_id"] = pid
                cfg = Config(yaml_path=base_yaml, overrides=batch_overrides)
                rc = _run_one(cfg, batch_index=i, batch_total=total, participant_scope="all")
                any_fail = any_fail or (rc != 0)
            except Exception as exc:
                logger.exception(
                    "Participant %s aborted with an unexpected error; continuing batch.",
                    pid,
                )
                print(
                    f"\n⚠️  {pid}: unexpected error (logged above). Continuing with next participant.\n",
                    file=sys.stderr,
                )
                any_fail = True
        sys.exit(1 if any_fail else 0)

    # Single participant
    rc = _run_one(base_cfg, participant_scope="single")
    sys.exit(rc)


def _run_one(
    cfg: Config,
    *,
    batch_index: int | None = None,
    batch_total: int | None = None,
    participant_scope: str = "single",
) -> int:
    """Return process exit code (0 = pipeline reports success/completed)."""

    print("\n🚀  Starting Agentic fMRIPrep Autonomous Loop …")
    print(f"    Participant : {cfg.participant_id}")
    print(f"    BIDS dir    : {cfg.bids_dir}")
    print(f"    Output dir  : {cfg.output_dir}")
    print(f"    Sloppy mode : {cfg.sloppy}")
    print(f"    LLM         : {cfg.llm_provider} / {cfg.llm_model}")
    print(
        f"    Agents      : diagnosis={cfg.diagnosis_enabled} "
        f"recovery={cfg.recovery_enabled} vision={cfg.vision_enabled}\n"
    )

    t0 = time.perf_counter()
    app = build_graph(cfg)

    initial_state = {
        "command":       "",
        "log":           "",
        "history":       [],
        "events":        [],
        "status":        "planning",
        "attempt_count": 0,
        "recovery_changed": True,
    }

    final_state = app.invoke(initial_state)
    wall = time.perf_counter() - t0
    _write_publication_artifacts(
        cfg,
        final_state,
        wall_clock_seconds=wall,
        batch_index=batch_index,
        batch_total=batch_total,
        participant_scope=participant_scope,
    )

    _print_report(final_state)

    ok = final_state.get("status") in ("success", "completed")
    return 0 if ok else 1


def _write_publication_artifacts(
    cfg: Config,
    final_state: dict,
    *,
    wall_clock_seconds: float,
    batch_index: int | None,
    batch_total: int | None,
    participant_scope: str,
) -> None:
    out_dir = cfg.output_dir / "agentic_results" / cfg.participant_id
    out_dir.mkdir(parents=True, exist_ok=True)

    run_summary = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "participant": cfg.participant_id,
        "bids_dir": str(cfg.bids_dir),
        "output_dir": str(cfg.output_dir),
        "final_status": final_state.get("status"),
        "attempt_count": final_state.get("attempt_count", 0),
        "final_command": final_state.get("command", ""),
        "history": final_state.get("history", []),
        "events": final_state.get("events", []),
        "agents": {
            "recovery_enabled": cfg.recovery_enabled,
            "diagnosis_enabled": cfg.diagnosis_enabled,
            "vision_enabled": cfg.vision_enabled,
        },
    }

    config_snapshot = {
        "resolved_config": cfg.as_dict(),
        "participant": cfg.participant_id,
        "bids_dir": str(cfg.bids_dir),
        "output_dir": str(cfg.output_dir),
        "metadata_summary": {
            "has_fieldmap_dir": cfg.has_fieldmap(),
            "missing_readout_timing_metadata": cfg.missing_readout_timing_metadata(),
            "func_metadata_files": [str(p) for p in cfg.func_metadata_files()],
        },
    }

    (out_dir / "run_summary.json").write_text(json.dumps(run_summary, indent=2, sort_keys=True) + "\n")
    (out_dir / "config_snapshot.json").write_text(json.dumps(config_snapshot, indent=2, sort_keys=True) + "\n")
    evaluation_row = build_evaluation_row(
        cfg,
        final_state,
        run_mode="agentic",
        wall_clock_seconds=wall_clock_seconds,
        batch_index=batch_index,
        batch_total=batch_total,
        participant_scope=participant_scope,
    )
    (out_dir / "evaluation_row.json").write_text(json.dumps(evaluation_row, indent=2, sort_keys=True) + "\n")
    append_evaluation_exports(evaluation_row, eval_root=cfg.evaluation_export_root)


def _print_report(final_state: dict) -> None:
    sep = "═" * 55
    print(f"\n{sep}")
    print("🤖  AGENTIC fMRIPrep SYSTEM REPORT")
    print(f"    Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(sep)

    status   = final_state.get("status", "UNKNOWN").upper()
    attempts = final_state.get("attempt_count", 0)
    cmd      = final_state.get("command", "No command generated.")

    has_low_mem = "ENABLED (--low-mem)" if "--low-mem" in cmd else "STANDARD"
    fieldmap    = "SYNTHETIC (--use-syn-sdc)" if "--use-syn-sdc" in cmd else "DIRECT"

    print(f"▶  FINAL STATUS      : {status}")
    print(f"▶  TOTAL ATTEMPTS    : {attempts}")
    print(f"▶  HARDWARE OPTIM    : {has_low_mem}")
    print(f"▶  FIELD MAP TYPE    : {fieldmap}")

    print(f"\n📜  FINAL GENERATED COMMAND:\n{cmd}")

    history = final_state.get("history", [])
    if history:
        print("\n🔍  AGENT HISTORY SUMMARY:")
        for i, entry in enumerate(history, 1):
            preview = "\n".join(entry.strip().splitlines()[:5])
            print(f"  [{i}] {preview}\n      …")

    qa_report = next((entry for entry in reversed(history) if entry.startswith("VISUAL AUDIT")), None)
    if qa_report:
        print("\n📊  QA RESULTS:")
        print(qa_report)

    print(f"\n{sep}")
    ok = final_state.get("status") in ("success", "completed")
    print("✅  MISSION COMPLETE: Human Intervention Not Required." if ok
          else "⚠️   Pipeline ended without full success – review logs above.")
    print(sep)


if __name__ == "__main__":
    main()
