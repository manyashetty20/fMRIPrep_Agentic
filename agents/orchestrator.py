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
from metrics_logger import emit
from qa_verdict import decide_qa_verdict

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
    qa_verdict:       str   # PASS / WARN / FAIL / SKIPPED / NONE
    applied_repair_rule_ids: List[str]


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

    def _resolve_input_t1w() -> Path:
        """
        Resolve the subject T1w input, supporting both flat and session-based BIDS layouts.

        Priority:
          1) <bids>/sub-XX/anat/sub-XX_T1w.nii.gz
          2) <bids>/sub-XX/ses-YY/anat/sub-XX_ses-YY*_T1w.nii.gz (when session is configured)
          3) For wildcard session matches, prefer non-retest sessions first
             (e.g., ses-test before ses-retest), then alphabetical
          4) First sorted wildcard match under <bids>/sub-XX/ses-*/anat/sub-XX*_T1w.nii.gz
        """
        flat = cfg.bids_dir / cfg.participant_id / "anat" / f"{cfg.participant_id}_T1w.nii.gz"
        if flat.exists():
            return flat

        if cfg.session_id:
            ses = cfg.session_id if str(cfg.session_id).startswith("ses-") else f"ses-{cfg.session_id}"
            ses_anat = cfg.bids_dir / cfg.participant_id / ses / "anat"
            session_matches = sorted(ses_anat.glob(f"{cfg.participant_id}_{ses}*_T1w.nii.gz"))
            if session_matches:
                return session_matches[0]

        wildcard_matches = sorted(
            (cfg.bids_dir / cfg.participant_id).glob(f"ses-*/anat/{cfg.participant_id}*_T1w.nii.gz")
        )
        if wildcard_matches:
            def _session_sort_key(path: Path) -> tuple[int, str]:
                ses = next((part for part in path.parts if part.startswith("ses-")), "")
                is_retest = "retest" in ses.lower()
                return (1 if is_retest else 0, str(path))

            wildcard_matches = sorted(wildcard_matches, key=_session_sort_key)

        if wildcard_matches:
            return wildcard_matches[0]

        # Fall back to the canonical flat path for downstream warnings/messages.
        return flat

    def _resolve_subject_report_path() -> Path:
        """
        Resolve the subject HTML report path across common fMRIPrep output layouts.
        """
        candidates = [
            cfg.output_dir / f"{cfg.participant_id}.html",
            cfg.output_dir / "fmriprep" / f"{cfg.participant_id}.html",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return candidates[0]

    def _persist_qa_results(report: str, metrics: dict) -> None:
        qa_dir = cfg.output_dir / "agentic_results" / cfg.participant_id
        qa_dir.mkdir(parents=True, exist_ok=True)
        (qa_dir / "qa_report.txt").write_text(report + "\n")
        (qa_dir / "qa_metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
        qa_decision = metrics.get("qa_decision")
        if isinstance(qa_decision, dict):
            (qa_dir / "qa_decision.json").write_text(json.dumps(qa_decision, indent=2, sort_keys=True) + "\n")

    def _tokenize_command(cmd: str) -> list[str]:
        """Compare commands by shell tokens, ignoring formatting-only differences."""
        normalised = re.sub(r"\\\s*\n\s*", " ", cmd).strip()
        return shlex.split(normalised)

    # ------------------------------------------------------------------ #
    #  Node functions
    # ------------------------------------------------------------------ #

    def planning_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Planning Phase ---")
        emit(
            "orchestrator",
            "state_transition",
            from_state=state.get("status", "planning"),
            to_state="planning",
            attempt_count=state.get("attempt_count", 0),
        )
        cmd = config_agent.generate_command()
        emit(
            "orchestrator",
            "state_transition",
            from_state="planning",
            to_state="executing",
            attempt_count=0,
        )
        return {
            "command": cmd,
            "status": "executing",
            "attempt_count": 0,
            "recovery_changed": True,
            "applied_repair_rule_ids": [],
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
        t0 = datetime.now(timezone.utc)

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            duration = (datetime.now(timezone.utc) - t0).total_seconds()
            logger.info("Execution succeeded.\n%s", result.stdout[-2000:])
            emit(
                "orchestrator",
                "execution_completed",
                attempt=attempt,
                status="success",
                exit_code=0,
                duration_seconds=round(duration, 4),
                fmriprep_duration_seconds=round(duration, 4),
                command=cmd,
            )
            emit(
                "orchestrator",
                "state_transition",
                from_state="executing",
                to_state="success",
                attempt_count=attempt,
            )
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
                    "duration_seconds": round(duration, 4),
                    "stdout_tail": result.stdout[-2000:],
                }],
            }

        except subprocess.CalledProcessError as exc:
            error_text = (exc.stderr or "") + (exc.stdout or "")
            duration = (datetime.now(timezone.utc) - t0).total_seconds()
            logger.error("Execution failed (exit %d):\n%s", exc.returncode, error_text[-2000:])
            emit(
                "orchestrator",
                "execution_completed",
                attempt=attempt,
                status="failed",
                exit_code=exc.returncode,
                duration_seconds=round(duration, 4),
                fmriprep_duration_seconds=round(duration, 4),
                command=cmd,
                log_tail=error_text[-2000:],
            )
            emit(
                "orchestrator",
                "state_transition",
                from_state="executing",
                to_state="diagnosing",
                attempt_count=attempt,
                failure_detected=True,
            )
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
                    "duration_seconds": round(duration, 4),
                    "log_tail": error_text[-2000:],
                }],
            }

        except Exception as exc:
            duration = (datetime.now(timezone.utc) - t0).total_seconds()
            logger.exception("Unexpected error during execution.")
            emit(
                "orchestrator",
                "execution_completed",
                attempt=attempt,
                status="failed",
                exit_code=None,
                duration_seconds=round(duration, 4),
                command=cmd,
                log_tail=str(exc),
            )
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
                    "duration_seconds": round(duration, 4),
                    "log_tail": str(exc),
                }],
            }

    def success_finalize_node(state: AgentState) -> dict:
        """Successful fMRIPrep run without voxel/HTML QA (ablation: vision disabled)."""
        logger.info("--- [GRAPH] Success finalize (Vision QA disabled) ---")
        report = "VISUAL AUDIT SKIPPED: agents.vision_enabled is false in configuration."
        metrics: dict[str, object] = {
            "status": "skipped",
            "reason": "vision_disabled",
            "qa_summary": "SKIPPED",
            "qa_decision": {
                "summary": "SKIPPED",
                "status": "skipped",
                "checks": [],
            },
        }
        qa_dir = cfg.output_dir / "agentic_results" / cfg.participant_id
        qa_dir.mkdir(parents=True, exist_ok=True)
        (qa_dir / "qa_report.txt").write_text(report + "\n")
        (qa_dir / "qa_metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
        return {
            "status": "completed",
            "history": [report],
            "events": [{
                "type": "qa",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "skipped",
                "metrics": metrics,
                "report": report,
            }],
        }

    def diagnostic_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Diagnostic Phase ---")
        emit(
            "orchestrator",
            "state_transition",
            from_state=state.get("status", "diagnosing"),
            to_state="diagnosis",
            attempt_count=state.get("attempt_count", 0),
        )
        report = diagnostic_agent.diagnose_crash(state["log"])
        logger.info("Diagnosis:\n%s", report)
        emit(
            "orchestrator",
            "state_transition",
            from_state="diagnosis",
            to_state="recovering",
            attempt_count=state.get("attempt_count", 0),
        )
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
        attempt = state.get("attempt_count", 0)
        already = list(state.get("applied_repair_rule_ids") or [])
        new_cmd = recovery_agent.apply_fix(
            state["command"],
            latest_diagnosis,
            retry_attempt=attempt,
            already_applied=already,
        )
        newly = list(recovery_agent.last_applied or [])
        merged_ids = list(dict.fromkeys(already + newly))
        logger.info("Recovered command:\n%s", new_cmd)
        changed = _tokenize_command(new_cmd) != _tokenize_command(state["command"])
        bids_data_fix = bool(re.search(r"(?i)(BIDS_FIX|RepetitionTime|missing.*TR)", latest_diagnosis))
        if not changed and not bids_data_fix:
            logger.warning("Recovery phase produced no command change.")
            emit(
                "orchestrator",
                "state_transition",
                from_state="recovering",
                to_state="unrecoverable",
                attempt_count=attempt,
            )
            return {
                "command": new_cmd,
                "status": "unrecoverable",
                "history": ["RECOVERY: no effective command change was possible."],
                "recovery_changed": False,
                "applied_repair_rule_ids": merged_ids,
                "events": [{
                    "type": "recovery",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "attempt": attempt,
                    "changed": False,
                    "command": new_cmd,
                    "repair_rule_ids": newly,
                }],
            }
        elif not changed and bids_data_fix:
            logger.info("Recovery phase wrote BIDS sidecar fix – retrying with same command.")
        emit(
            "orchestrator",
            "state_transition",
            from_state="recovering",
            to_state="relaunch",
            attempt_count=attempt,
            command_changed=changed or bids_data_fix,
        )
        return {
            "command": new_cmd,
            "status": "executing",
            "recovery_changed": True,
            "applied_repair_rule_ids": merged_ids,
            "events": [{
                "type": "recovery",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "attempt": attempt,
                "changed": True,
                "command": new_cmd,
                "repair_rule_ids": newly,
                "scientific_impacts": list(recovery_agent.last_impacts or []),
            }],
        }

    def route_after_recovery(state: AgentState) -> str:
        if state.get("status") == "unrecoverable" or not state.get("recovery_changed", True):
            logger.error("Recovery could not produce a new command – stopping retries.")
            return "vision_agent"
        return "executor"

    def route_after_diagnosis(state: AgentState) -> str:
        """Recovery agent optional (ablation): diagnosis may go straight to QA."""
        if not cfg.recovery_enabled:
            logger.info("Recovery disabled by config – skipping engineer node.")
            return "vision_agent"
        return "engineer"

    def vision_agent_node(state: AgentState) -> dict:
        logger.info("--- [GRAPH] Vision Quality Phase ---")

        if not cfg.vision_enabled:
            logger.info("Vision agent disabled by config.")
            return {"history": ["Vision QA skipped (disabled in config)."], "status": "completed"}

        if state.get("status") != "success":
            qa_decision = {
                "summary": "SKIPPED",
                "status": "skipped",
                "checks": [
                    {
                        "name": "execution_success",
                        "value": False,
                        "threshold": True,
                        "status": "fail",
                        "reason": "No successful execution was recorded.",
                    }
                ],
            }
            report = (
                "VISUAL AUDIT SKIPPED:\n"
                "  No successful execution was recorded, so output quality was not assessed."
            )
            _persist_qa_results(
                report,
                {
                    "status": "skipped",
                    "reason": "execution_not_successful",
                    "qa_summary": "SKIPPED",
                    "qa_decision": qa_decision,
                },
            )
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
        input_img   = _resolve_input_t1w()
        output_img  = subject_output_dir / "anat" / f"{cfg.participant_id}_desc-preproc_T1w.nii.gz"
        mni_img     = subject_output_dir / "anat" / f"{cfg.participant_id}_space-{cfg.output_space}_desc-preproc_T1w.nii.gz"
        brain_mask  = subject_output_dir / "anat" / f"{cfg.participant_id}_desc-brain_mask.nii.gz"
        report_html = _resolve_subject_report_path()

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
            "qa_output_space": cfg.output_space,
            "qa_thresholds": {
                "min_brain_mask_retention_ratio": cfg.min_brain_mask_retention_ratio,
                "max_brain_mask_retention_ratio": cfg.max_brain_mask_retention_ratio,
                "min_skull_strip_reduction": cfg.min_skull_strip_reduction,
                "max_skull_strip_reduction": cfg.max_skull_strip_reduction,
            },
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
                edge_fraction = 0.0
                if brain_mask.exists():
                    mask_obj = nib.load(str(brain_mask))
                    mask_data = mask_obj.get_fdata()
                    mask_nonzero = int(np.count_nonzero(mask_data))
                    
                    # Boundary clipping check: detect if brain mask is clipped at FOV edges
                    if cfg.check_boundary_clipping and mask_nonzero > 0:
                        mask_bool = mask_data > 0
                        edge_voxels = int(
                            np.count_nonzero(mask_bool[0, :, :]) +
                            np.count_nonzero(mask_bool[-1, :, :]) +
                            np.count_nonzero(mask_bool[:, 0, :]) +
                            np.count_nonzero(mask_bool[:, -1, :]) +
                            np.count_nonzero(mask_bool[:, :, 0]) +
                            np.count_nonzero(mask_bool[:, :, -1])
                        )
                        edge_fraction = float(edge_voxels / mask_nonzero)

                kept_nonzero = mask_nonzero if mask_nonzero is not None else proc_nonzero
                retention_ratio = kept_nonzero / max(proc_nonzero, 1)
                reduction = 1.0 - kept_nonzero / max(proc_nonzero, 1)

                qa_checks = [
                    {
                        "name": "output_found",
                        "value": output_img.exists(),
                        "threshold": True,
                        "status": "pass" if output_img.exists() else "fail",
                        "reason": "Expected preprocessed T1w output exists." if output_img.exists() else "Expected preprocessed T1w output is missing.",
                    },
                    {
                        "name": "report_found",
                        "value": report_html.exists(),
                        "threshold": True,
                        "status": "pass" if report_html.exists() else "warn",
                        "reason": "Subject HTML report exists." if report_html.exists() else "Subject HTML report is missing.",
                    },
                    {
                        "name": "mni_found",
                        "value": mni_img.exists(),
                        "threshold": True,
                        "status": "pass" if mni_img.exists() else "warn",
                        "reason": "MNI-space anatomical derivative exists." if mni_img.exists() else "No MNI-space anatomical derivative was found.",
                    },
                    {
                        "name": "brain_mask_found",
                        "value": brain_mask.exists(),
                        "threshold": True,
                        "status": "pass" if brain_mask.exists() else "warn",
                        "reason": "Brain mask derivative exists." if brain_mask.exists() else "Brain mask derivative is missing; voxel metrics fall back to the preprocessed image.",
                    },
                    {
                        "name": "brain_mask_retention_ratio",
                        "value": retention_ratio,
                        "threshold": {
                            "min": cfg.min_brain_mask_retention_ratio,
                            "max": cfg.max_brain_mask_retention_ratio,
                        },
                        "status": (
                            "pass"
                            if cfg.min_brain_mask_retention_ratio <= retention_ratio <= cfg.max_brain_mask_retention_ratio
                            else "fail"
                        ),
                        "reason": (
                            "Mask-vs-preprocessed retention ratio is inside the configured QA band."
                            if cfg.min_brain_mask_retention_ratio <= retention_ratio <= cfg.max_brain_mask_retention_ratio
                            else f"Mask-vs-preprocessed retention ratio ({retention_ratio:.1%}) falls outside configured band [{cfg.min_brain_mask_retention_ratio:.1%}, {cfg.max_brain_mask_retention_ratio:.1%}]."
                        ),
                    },
                    {
                        "name": "skull_strip_reduction",
                        "value": reduction,
                        "threshold": {
                            "min": cfg.min_skull_strip_reduction,
                            "max": cfg.max_skull_strip_reduction,
                        },
                        "status": (
                            "pass"
                            if cfg.min_skull_strip_reduction <= reduction <= cfg.max_skull_strip_reduction
                            else "fail"
                        ),
                        "reason": (
                            "Mask-vs-preprocessed voxel reduction is inside the configured QA band."
                            if cfg.min_skull_strip_reduction <= reduction <= cfg.max_skull_strip_reduction
                            else f"Mask-vs-preprocessed voxel reduction ({reduction:.1%}) falls outside configured band [{cfg.min_skull_strip_reduction:.1%}, {cfg.max_skull_strip_reduction:.1%}]."
                        ),
                    },
                ]

                # Boundary clipping check
                if cfg.check_boundary_clipping and mask_nonzero is not None:
                    is_clipped = edge_fraction > cfg.max_boundary_slice_fraction
                    qa_checks.append({
                        "name": "boundary_clipping",
                        "value": edge_fraction,
                        "threshold": {"max": cfg.max_boundary_slice_fraction},
                        "status": "fail" if is_clipped else "pass",
                        "reason": (
                            f"Brain mask touches FOV boundary slices ({edge_fraction:.2%} > {cfg.max_boundary_slice_fraction:.2%}), indicating potential cortex clipping or truncated scan FOV."
                            if is_clipped
                            else f"Brain mask is fully contained within FOV boundaries ({edge_fraction:.2%} edge voxels)."
                        ),
                    })

                # Tissue segmentation check (if available)
                dseg_candidates = [
                    subject_output_dir / "anat" / f"{cfg.participant_id}_dseg.nii.gz",
                    subject_output_dir / "anat" / f"{cfg.participant_id}_desc-aseg_dseg.nii.gz",
                ]
                dseg_found = any(p.exists() for p in dseg_candidates)
                if dseg_found:
                    qa_checks.append({
                        "name": "tissue_segmentation",
                        "value": True,
                        "threshold": True,
                        "status": "pass",
                        "reason": "Anatomical tissue segmentation derivative verified.",
                    })

                # SVG figure checks
                fig_dirs = [
                    subject_output_dir / "figures",
                    cfg.output_dir / "fmriprep" / cfg.participant_id / "figures",
                ]
                svg_files = []
                for fd in fig_dirs:
                    if fd.exists():
                        svg_files.extend(list(fd.glob("*.svg")))
                if svg_files:
                    qa_checks.append({
                        "name": "figures_generated",
                        "value": len(svg_files),
                        "threshold": 1,
                        "status": "pass",
                        "reason": f"Found {len(svg_files)} visual QA figure(s) for audit.",
                    })

                fail_count = sum(1 for check in qa_checks if check["status"] == "fail")
                warn_count = sum(1 for check in qa_checks if check["status"] == "warn")
                qa_summary = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
                metrics.update({
                    "raw_nonzero_voxels": raw_nonzero,
                    "preprocessed_nonzero_voxels": proc_nonzero,
                    "brain_mask_nonzero_voxels": mask_nonzero,
                    "boundary_edge_fraction": edge_fraction,
                    "skull_strip_reduction": reduction,
                    "brain_mask_retention_ratio": retention_ratio,
                    "qa_summary": qa_summary,
                    "qa_decision": {
                        "summary": qa_summary,
                        "status": "completed",
                        "checks": qa_checks,
                    },
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
                    f"  Boundary edge voxel ratio   : {edge_fraction:.2%}",
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
                qa_summary = "WARN"
            except Exception as exc:
                report_lines.append(f"  QA error: {exc}")
                metrics["status"] = "partial"
                metrics["reason"] = str(exc)
                qa_summary = "WARN"

        report = "\n".join(report_lines)
        _persist_qa_results(report, metrics)
        logger.info(report)
        thresholds = metrics.get("qa_thresholds", {})
        emit(
            "qa_node",
            "qa_completed",
            raw_nonzero_voxels=metrics.get("raw_nonzero_voxels"),
            preprocessed_nonzero_voxels=metrics.get("preprocessed_nonzero_voxels"),
            brain_mask_nonzero_voxels=metrics.get("brain_mask_nonzero_voxels"),
            brain_mask_retention_ratio=metrics.get("brain_mask_retention_ratio"),
            skull_strip_reduction_pct=(
                round(float(metrics["skull_strip_reduction"]) * 100.0, 4)
                if metrics.get("skull_strip_reduction") is not None
                else None
            ),
            non_brain_tissue_reduction_pct=(
                round(float(metrics["skull_strip_reduction"]) * 100.0, 4)
                if metrics.get("skull_strip_reduction") is not None
                else None
            ),
            mni_normalization_success=bool(metrics.get("mni_found")),
            qa_verdict=metrics.get("qa_summary", "UNKNOWN"),
            thresholds_used=thresholds,
            report_found=metrics.get("report_found"),
            output_found=metrics.get("output_found"),
            brain_mask_found=metrics.get("brain_mask_found"),
        )

        qa_summary_verdict = metrics.get("qa_summary", "PASS")
        attempt = state.get("attempt_count", 0)

        # Build QA diagnosis log text if QA checks failed
        qa_log = state.get("log", "")
        if qa_summary_verdict == "FAIL":
            failed_checks = [c for c in metrics.get("qa_decision", {}).get("checks", []) if c.get("status") == "fail"]
            failed_names = [c.get("name") for c in failed_checks]
            
            if "boundary_clipping" in failed_names or "brain_mask_retention_ratio" in failed_names:
                root_cause = "ANAT_CLIPPED_BRAIN"
                fix_hint = "--skull-strip-template OASIS30ANTs, --skull-strip-fixed-seed, --fs-no-reconall"
            elif "skull_strip_reduction" in failed_names:
                root_cause = "ANAT_OVERSEGMENTATION"
                fix_hint = "--skull-strip-template OASIS30ANTs, --skull-strip-fixed-seed"
            elif "mni_found" in failed_names:
                root_cause = "MNI_REGISTRATION_DISTORTION"
                fix_hint = "--output-spaces MNI152NLin2009cAsym:res-2"
            else:
                root_cause = "ANAT_CLIPPED_BRAIN"
                fix_hint = "--skull-strip-template OASIS30ANTs"

            evidence_items = [f"{c.get('name')}: {c.get('reason')}" for c in failed_checks]
            qa_log = (
                f"ROOT CAUSE: {root_cause}\n"
                f"EVIDENCE: QA audit failed ({len(failed_checks)} failure(s)):\n"
                + "\n".join(f"  - {e}" for e in evidence_items) + "\n"
                f"RECOMMENDED FIXES:\n"
                f"  1. {fix_hint}\n"
                f"SEVERITY: HIGH"
            )

        if (
            qa_summary_verdict == "FAIL"
            and cfg.retry_on_qa_fail
            and cfg.recovery_enabled
            and attempt < cfg.max_recovery_attempts
        ):
            new_status = "qa_failed"
            logger.warning(
                "QA detected anatomical failure (%s). Triggering recovery attempt %d/%d.",
                qa_summary_verdict,
                attempt,
                cfg.max_recovery_attempts,
            )
        else:
            new_status = "completed"

        emit(
            "orchestrator",
            "state_transition",
            from_state=state.get("status", "success"),
            to_state="qa_complete" if new_status == "completed" else "diagnosing_qa",
            attempt_count=attempt,
            final_verdict=qa_summary_verdict,
        )

        return {
            "history": [report],
            "log": qa_log if qa_summary_verdict == "FAIL" else state.get("log", ""),
            "status": new_status,
            "qa_verdict": qa_summary_verdict,
            "events": [{
                "type": "qa",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": metrics.get("status", "completed"),
                "qa_verdict": qa_summary_verdict,
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
            return "vision_agent" if cfg.vision_enabled else "success_finalize"

        if not cfg.diagnosis_enabled:
            logger.info("Diagnosis disabled – routing failed execution to QA/report.")
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

    def route_after_vision_qa(state: AgentState) -> str:
        status = state.get("status", "")
        verdict = state.get("qa_verdict", "NONE")
        attempt = state.get("attempt_count", 0)

        if (
            status == "qa_failed"
            and cfg.retry_on_qa_fail
            and cfg.recovery_enabled
            and attempt < cfg.max_recovery_attempts
        ):
            logger.info(
                "Routing QA failure (%s) to detective for autonomous repair (attempt %d/%d).",
                verdict,
                attempt,
                cfg.max_recovery_attempts,
            )
            return "detective"

        return "END"

    # ------------------------------------------------------------------ #
    #  Build the graph
    # ------------------------------------------------------------------ #

    workflow = StateGraph(AgentState)

    workflow.add_node("planner",      planning_node)
    workflow.add_node("executor",     execution_node)
    workflow.add_node("detective",    diagnostic_node)
    workflow.add_node("engineer",     recovery_node)
    workflow.add_node("vision_agent", vision_agent_node)
    workflow.add_node("success_finalize", success_finalize_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")

    workflow.add_conditional_edges(
        "executor",
        route_after_execution,
        {
            "detective":         "detective",
            "vision_agent":      "vision_agent",
            "success_finalize":  "success_finalize",
        },
    )

    workflow.add_conditional_edges(
        "detective",
        route_after_diagnosis,
        {
            "engineer":     "engineer",
            "vision_agent": "vision_agent",
        },
    )
    workflow.add_conditional_edges(
        "engineer",
        route_after_recovery,
        {
            "executor": "executor",
            "vision_agent": "vision_agent",
        },
    )
    workflow.add_conditional_edges(
        "vision_agent",
        route_after_vision_qa,
        {
            "detective": "detective",
            "END":       END,
        },
    )
    workflow.add_edge("success_finalize", END)

    return workflow.compile()
