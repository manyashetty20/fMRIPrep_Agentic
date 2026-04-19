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

import json
import logging
import os
import re
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path
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
    events:           Annotated[List[dict], operator.add]
    status:           str
    attempt_count:    int   # tracks recovery iterations
    recovery_changed: bool


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

    def _resolve_subject_output_dir() -> Path:
        """Return the subject derivatives directory for the configured output root."""
        candidates = [
            cfg.output_dir / cfg.participant_id,
            cfg.output_dir / "fmriprep" / cfg.participant_id,
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        # Prefer the current output layout if nothing exists yet.
        return candidates[0]

    def _persist_qa_results(report: str, metrics: dict) -> None:
        qa_dir = cfg.output_dir / "agentic_results" / cfg.participant_id
        qa_dir.mkdir(parents=True, exist_ok=True)
        (qa_dir / "qa_report.txt").write_text(report + "\n")
        (qa_dir / "qa_metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")

    def _tokenize_command(cmd: str) -> list[str]:
        """Compare commands by shell tokens, ignoring formatting-only differences."""
        normalised = re.sub(r"\\\s*\n\s*", " ", cmd).strip()
        return shlex.split(normalised)

    # ------------------------------------------------------------------ #
    #  Node functions
    # ------------------------------------------------------------------ #

    def planning_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Planning Phase ---")
        cmd = config_agent.generate_command()
        return {
            "command": cmd,
            "status": "executing",
            "attempt_count": 0,
            "recovery_changed": True,
            "events": [{
                "type": "planning",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "command": cmd,
            }],
        }

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
            return {
                "status": "success",
                "command": cmd,
                "attempt_count": attempt,
                "events": [{
                    "type": "execution",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "attempt": attempt,
                    "status": "success",
                    "exit_code": 0,
                    "command": cmd,
                    "stdout_tail": result.stdout[-2000:],
                }],
            }

        except subprocess.CalledProcessError as exc:
            error_text = (exc.stderr or "") + (exc.stdout or "")
            logger.error("Execution failed (exit %d):\n%s", exc.returncode, error_text[-2000:])
            return {
                "log": error_text,
                "status": "diagnosing",
                "attempt_count": attempt,
                "events": [{
                    "type": "execution",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "attempt": attempt,
                    "status": "failed",
                    "exit_code": exc.returncode,
                    "command": cmd,
                    "log_tail": error_text[-2000:],
                }],
            }

        except Exception as exc:
            logger.exception("Unexpected error during execution.")
            return {
                "log": str(exc),
                "status": "diagnosing",
                "attempt_count": attempt,
                "events": [{
                    "type": "execution",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "attempt": attempt,
                    "status": "failed",
                    "exit_code": None,
                    "command": cmd,
                    "log_tail": str(exc),
                }],
            }

    def diagnostic_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Diagnostic Phase ---")
        report = diagnostic_agent.diagnose_crash(state["log"])
        logger.info("Diagnosis:\n%s", report)
        return {
            "history": [report],
            "status": "recovering",
            "events": [{
                "type": "diagnosis",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "attempt": state.get("attempt_count", 0),
                "report": report,
            }],
        }

    def recovery_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Recovery Phase ---")
        latest_diagnosis = state["history"][-1] if state["history"] else ""
        new_cmd = recovery_agent.apply_fix(state["command"], latest_diagnosis)
        logger.info("Recovered command:\n%s", new_cmd)
        changed = _tokenize_command(new_cmd) != _tokenize_command(state["command"])
        if not changed:
            logger.warning("Recovery phase produced no command change.")
            return {
                "command": new_cmd,
                "status": "unrecoverable",
                "history": ["RECOVERY: no effective command change was possible."],
                "recovery_changed": False,
                "events": [{
                    "type": "recovery",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "attempt": state.get("attempt_count", 0),
                    "changed": False,
                    "command": new_cmd,
                }],
            }
        return {
            "command": new_cmd,
            "status": "executing",
            "recovery_changed": True,
            "events": [{
                "type": "recovery",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "attempt": state.get("attempt_count", 0),
                "changed": True,
                "command": new_cmd,
            }],
        }

    def route_after_recovery(state: AgentState) -> str:
        if state.get("status") == "unrecoverable" or not state.get("recovery_changed", True):
            logger.error("Recovery could not produce a new command – stopping retries.")
            return "vision_agent"
        return "executor"

    def vision_agent_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Vision Quality Phase ---")

        if not cfg.vision_enabled:
            logger.info("Vision agent disabled by config.")
            return {"history": ["Vision QA skipped (disabled in config)."], "status": "completed"}

        if state.get("status") != "success":
            report = (
                "VISUAL AUDIT SKIPPED:\n"
                "  No successful execution was recorded, so output quality was not assessed."
            )
            _persist_qa_results(report, {"status": "skipped", "reason": "execution_not_successful"})
            logger.info(report)
            return {
                "history": [report],
                "status": "failed",
                "events": [{
                    "type": "qa",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "skipped",
                    "report": report,
                }],
            }

        subject_output_dir = _resolve_subject_output_dir()
        input_img   = cfg.bids_dir / cfg.participant_id / "anat" / f"{cfg.participant_id}_T1w.nii.gz"
        output_img  = subject_output_dir / "anat" / f"{cfg.participant_id}_desc-preproc_T1w.nii.gz"
        mni_img     = subject_output_dir / "anat" / f"{cfg.participant_id}_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz"
        brain_mask  = subject_output_dir / "anat" / f"{cfg.participant_id}_desc-brain_mask.nii.gz"
        report_html = cfg.output_dir / f"{cfg.participant_id}.html"

        logger.info("Comparing:\n  Input : %s\n  Output: %s", input_img, output_img)

        report_lines = [
            "VISUAL AUDIT:",
            f"  Subject output dir          : {subject_output_dir}",
            f"  Subject report              : {report_html}",
        ]
        metrics: dict[str, object] = {
            "status": "completed",
            "subject_output_dir": str(subject_output_dir),
            "subject_report": str(report_html),
            "input_image": str(input_img),
            "output_image": str(output_img),
            "mni_image": str(mni_img),
            "brain_mask": str(brain_mask),
            "report_found": report_html.exists(),
            "output_found": output_img.exists(),
            "mni_found": mni_img.exists(),
            "brain_mask_found": brain_mask.exists(),
        }

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
                mask_nonzero = None
                if brain_mask.exists():
                    mask = nib.load(str(brain_mask)).get_fdata()
                    mask_nonzero = int(np.count_nonzero(mask))

                kept_nonzero = mask_nonzero if mask_nonzero is not None else proc_nonzero
                reduction    = 1.0 - kept_nonzero / max(raw_nonzero, 1)
                retention_ratio = kept_nonzero / max(raw_nonzero, 1)
                qa_summary = (
                    "PASS"
                    if output_img.exists() and mni_img.exists() and report_html.exists() and brain_mask.exists()
                    else "WARN"
                )
                metrics.update({
                    "raw_nonzero_voxels": raw_nonzero,
                    "preprocessed_nonzero_voxels": proc_nonzero,
                    "brain_mask_nonzero_voxels": mask_nonzero,
                    "skull_strip_reduction": reduction,
                    "brain_mask_retention_ratio": retention_ratio,
                    "qa_summary": qa_summary,
                })

                report_lines += [
                    f"  Raw voxels (non-zero)       : {raw_nonzero:,}",
                    f"  Preprocessed voxels (non-zero): {proc_nonzero:,}",
                    (
                        f"  Brain-mask voxels (non-zero): {mask_nonzero:,}"
                        if mask_nonzero is not None
                        else "  Brain-mask voxels (non-zero): Not available"
                    ),
                    f"  Brain-mask retention ratio  : {retention_ratio:.1%}",
                    f"  Skull-strip reduction       : {reduction:.1%}",
                    (
                        "  Skull-stripping : change detected between raw volume and brain mask."
                        if reduction > 0
                        else "  Skull-stripping : no measurable voxel reduction detected."
                    ),
                    (
                        "  Normalization   : MNI-space preprocessed output file detected."
                        if mni_img.exists()
                        else "  Normalization   : Not verified in code (no MNI-space file detected)."
                    ),
                    f"  QA Summary      : {qa_summary}",
                ]
            except ImportError:
                report_lines.append("  nibabel not installed – skipping voxel-level QA.")
                metrics["status"] = "partial"
                metrics["reason"] = "nibabel_missing"
            except Exception as exc:
                report_lines.append(f"  QA error: {exc}")
                metrics["status"] = "partial"
                metrics["reason"] = str(exc)

        report = "\n".join(report_lines)
        _persist_qa_results(report, metrics)
        logger.info(report)
        return {
            "history": [report],
            "status": "completed",
            "events": [{
                "type": "qa",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": metrics.get("status", "completed"),
                "metrics": metrics,
                "report": report,
            }],
        }

    # ------------------------------------------------------------------ #
    #  Routing logic
    # ------------------------------------------------------------------ #

    def route_after_execution(state: AgentState) -> str:
        status  = state["status"]
        attempt = state.get("attempt_count", 0)

        if status == "success":
            return "vision_agent"
        if status == "unrecoverable" or not state.get("recovery_changed", True):
            logger.error("Recovery could not produce a new command – stopping retries.")
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
    workflow.add_conditional_edges(
        "engineer",
        route_after_recovery,
        {
            "executor": "executor",
            "vision_agent": "vision_agent",
        },
    )
    workflow.add_edge("vision_agent", END)

    return workflow.compile()
