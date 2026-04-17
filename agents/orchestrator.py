"""
agents/orchestrator.py
======================
Orchestrator – builds and compiles the LangGraph state machine that drives
the full agentic fMRIPrep loop.

Graph topology
--------------

  planner  →  executor  ──(success)──►  vision_agent  →  END
                │
                └─(fail)──►  detective  →  engineer  ─►  executor (loop)

The retry loop is bounded by cfg.max_recovery_attempts to prevent infinite loops.
"""

from __future__ import annotations

import logging
import os
import subprocess
from typing import Annotated, List, TypedDict

import operator
from langgraph.graph import StateGraph, END

from config_loader import Config
from agents.config_agent import ConfigAgent
from agents.diagnostic_agent import DiagnosticAgent
from agents.recovery_agent import RecoveryAgent

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
#  Shared State definition
# --------------------------------------------------------------------------- #

class AgentState(TypedDict):
    command:          str
    log:              str
    history:          Annotated[List[str], operator.add]
    status:           str
    attempt_count:    int   # tracks recovery iterations


# --------------------------------------------------------------------------- #
#  Graph factory
# --------------------------------------------------------------------------- #

def build_graph(cfg: Config) -> object:
    """
    Instantiate all agents using `cfg` and return a compiled LangGraph app.

    Parameters
    ----------
    cfg : Config
        Fully-resolved configuration object.

    Returns
    -------
    Compiled LangGraph CompiledGraph ready to call `.invoke()` on.
    """
    config_agent    = ConfigAgent(cfg)
    diagnostic_agent = DiagnosticAgent(cfg)
    recovery_agent  = RecoveryAgent(cfg)

    # ------------------------------------------------------------------ #
    #  Node functions
    # ------------------------------------------------------------------ #

    def planning_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Planning Phase ---")
        cmd = config_agent.generate_command()
        return {"command": cmd, "status": "executing", "attempt_count": 0}

    def execution_node(state: AgentState) -> dict:
        attempt = state.get("attempt_count", 0) + 1
        logger.info("--- [GRAPH] Execution Phase (attempt %d) ---", attempt)

        cmd = state["command"]
        logger.info("Running: %s", cmd)

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            logger.info("Execution succeeded.\n%s", result.stdout[-2000:])
            return {"status": "success", "command": cmd, "attempt_count": attempt}

        except subprocess.CalledProcessError as exc:
            error_text = (exc.stderr or "") + (exc.stdout or "")
            logger.error("Execution failed (exit %d):\n%s", exc.returncode, error_text[-2000:])
            return {
                "log": error_text,
                "status": "diagnosing",
                "attempt_count": attempt,
            }

        except Exception as exc:
            logger.exception("Unexpected error during execution.")
            return {"log": str(exc), "status": "diagnosing", "attempt_count": attempt}

    def diagnostic_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Diagnostic Phase ---")
        report = diagnostic_agent.diagnose_crash(state["log"])
        logger.info("Diagnosis:\n%s", report)
        return {"history": [report], "status": "recovering"}

    def recovery_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Recovery Phase ---")
        latest_diagnosis = state["history"][-1] if state["history"] else ""
        new_cmd = recovery_agent.apply_fix(state["command"], latest_diagnosis)
        logger.info("Recovered command:\n%s", new_cmd)
        return {"command": new_cmd, "status": "executing"}

    def vision_agent_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Vision Quality Phase ---")

        if not cfg.vision_enabled:
            logger.info("Vision agent disabled by config.")
            return {"history": ["Vision QA skipped (disabled in config)."], "status": "completed"}

        input_img  = cfg.bids_dir  / cfg.participant_id / "anat" / f"{cfg.participant_id}_T1w.nii.gz"
        output_img = cfg.output_dir / "fmriprep" / cfg.participant_id / "anat" / f"{cfg.participant_id}_desc-preproc_T1w.nii.gz"

        logger.info("Comparing:\n  Input : %s\n  Output: %s", input_img, output_img)

        report_lines = ["VISUAL AUDIT:"]

        if not input_img.exists():
            report_lines.append(f"  WARNING: Input image not found at {input_img}")
        if not output_img.exists():
            report_lines.append(f"  WARNING: Output image not found at {output_img}")

        if input_img.exists() and output_img.exists():
            try:
                import nibabel as nib
                import numpy as np

                raw  = nib.load(str(input_img)).get_fdata()
                proc = nib.load(str(output_img)).get_fdata()

                # Simple sanity checks
                raw_nonzero  = int(np.count_nonzero(raw))
                proc_nonzero = int(np.count_nonzero(proc))
                reduction    = 1.0 - proc_nonzero / max(raw_nonzero, 1)

                report_lines += [
                    f"  Raw voxels (non-zero)       : {raw_nonzero:,}",
                    f"  Preprocessed voxels (non-zero): {proc_nonzero:,}",
                    f"  Skull-strip reduction       : {reduction:.1%}",
                    "  Skull-stripping : PASS (non-brain tissue removed)" if reduction > 0.05
                    else "  Skull-stripping : WARN (little reduction detected)",
                    "  Normalization   : ALIGNED to MNI152 template (assumed from fMRIPrep output).",
                    f"  Quality Score   : {min(0.5 + reduction * 2.0, 1.0):.2f}/1.0",
                ]
            except ImportError:
                report_lines.append("  nibabel not installed – skipping voxel-level QA.")
            except Exception as exc:
                report_lines.append(f"  QA error: {exc}")
        else:
            report_lines.append(
                "  Preprocessing successful (output file confirmed at expected path)."
                if output_img.exists()
                else "  Output file not yet available for QA."
            )

        report = "\n".join(report_lines)
        logger.info(report)
        return {"history": [report], "status": "completed"}

    # ------------------------------------------------------------------ #
    #  Routing logic
    # ------------------------------------------------------------------ #

    def route_after_execution(state: AgentState) -> str:
        status  = state["status"]
        attempt = state.get("attempt_count", 0)

        if status == "success":
            return "vision_agent"
        if attempt >= cfg.max_recovery_attempts:
            logger.error(
                "Max recovery attempts (%d) reached – giving up.",
                cfg.max_recovery_attempts,
            )
            return "vision_agent"   # Still run vision for partial results
        return "detective"

    # ------------------------------------------------------------------ #
    #  Build the graph
    # ------------------------------------------------------------------ #

    workflow = StateGraph(AgentState)

    workflow.add_node("planner",      planning_node)
    workflow.add_node("executor",     execution_node)
    workflow.add_node("detective",    diagnostic_node)
    workflow.add_node("engineer",     recovery_node)
    workflow.add_node("vision_agent", vision_agent_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")

    workflow.add_conditional_edges(
        "executor",
        route_after_execution,
        {
            "detective":    "detective",
            "vision_agent": "vision_agent",
        },
    )

    workflow.add_edge("detective", "engineer")
    workflow.add_edge("engineer",  "executor")
    workflow.add_edge("vision_agent", END)

    return workflow.compile()