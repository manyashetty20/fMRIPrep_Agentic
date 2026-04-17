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

# Point to a different config file
python main.py --config /path/to/my_config.yaml

# Full anatomy run (not toy / sloppy mode)
python main.py --no-sloppy --no-low-mem --nprocs 4
"""

from __future__ import annotations

import argparse
import datetime
import logging
import sys

from config_loader import Config
from agents.orchestrator import build_graph

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
    parser.add_argument("--license",     metavar="PATH", help="FreeSurfer license.txt path.")

    # --- Subject ---
    parser.add_argument(
        "--participant", metavar="ID",
        help="Participant label, e.g. sub-01 or 01.",
    )
    parser.add_argument("--session", metavar="ID", help="Session label (optional).")

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

    # --- Agent behaviour ---
    parser.add_argument(
        "--max-retries", type=int, metavar="N",
        help="Maximum recovery attempts before giving up.",
    )
    parser.add_argument(
        "--no-vision", action="store_false", dest="vision_enabled",
        help="Skip the Vision QA agent.",
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
        "bids_dir":       "paths.bids_dir",
        "output_dir":     "paths.output_dir",
        "license":        "paths.license_file",
        "participant":    "subject.participant_id",
        "session":        "subject.session_id",
        "anat_only":      "pipeline.anat_only",
        "sloppy":         "pipeline.sloppy",
        "low_mem":        "pipeline.low_mem",
        "mem_mb":         "pipeline.mem_mb",
        "nprocs":         "pipeline.nprocs",
        "docker_image":   "pipeline.docker_image",
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
                val = f"sub-{val}"
            overrides[key] = val

    return overrides


# --------------------------------------------------------------------------- #
#  Main
# --------------------------------------------------------------------------- #

def main() -> None:
    args      = parse_args()
    overrides = build_overrides(args)

    # Build config (yaml → env vars → CLI overrides)
    cfg = Config(yaml_path=args.config, overrides=overrides)

    # Validate critical paths exist before doing anything
    try:
        cfg.validate()
    except FileNotFoundError as exc:
        print(f"\n❌  {exc}\n", file=sys.stderr)
        sys.exit(1)

    # Build and invoke the agentic graph
    print("\n🚀  Starting Agentic fMRIPrep Autonomous Loop …")
    print(f"    Participant : {cfg.participant_id}")
    print(f"    BIDS dir    : {cfg.bids_dir}")
    print(f"    Output dir  : {cfg.output_dir}")
    print(f"    Sloppy mode : {cfg.sloppy}")
    print(f"    LLM         : {cfg.llm_provider} / {cfg.llm_model}\n")

    app = build_graph(cfg)

    initial_state = {
        "command":       "",
        "log":           "",
        "history":       [],
        "status":        "planning",
        "attempt_count": 0,
    }

    final_state = app.invoke(initial_state)

    # ---------- Final Report ----------
    _print_report(final_state)


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

    print(f"\n{sep}")
    ok = final_state.get("status") in ("success", "completed")
    print("✅  MISSION COMPLETE: Human Intervention Not Required." if ok
          else "⚠️   Pipeline ended without full success – review logs above.")
    print(sep)


if __name__ == "__main__":
    main()