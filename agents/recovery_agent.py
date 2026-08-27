"""
agents/recovery_agent.py
=========================
Recovery Agent – parses a diagnosis report and applies surgical fixes
to the fMRIPrep Docker command.

No hardcoded paths or values – everything is derived from the diagnosis
text and the central Config.

Metrics (inspectable)
---------------------
``apply_fix`` emits ``recovery_applied`` via ``metrics_logger.emit`` with
root cause received, repair actions, command diff, retry attempt, and timing.
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path

import nibabel as nib

from config_loader import Config
from metrics_logger import emit

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
#  Fix rules
#  Each entry maps a regex on the DIAGNOSIS TEXT → a function that
#  modifies the command list in-place.
# --------------------------------------------------------------------------- #


def _ensure_flag(parts: list[str], flag: str) -> None:
    """Add `flag` to parts if it isn't already present."""
    if not any(p.startswith(flag.split()[0]) for p in parts):
        parts.extend(flag.split())


def _replace_flag(parts: list[str], flag: str, value: str) -> None:
    """Replace or add a --flag value pair and deduplicate existing occurrences."""
    stem = flag.strip().split()[0].rstrip("=")
    filtered: list[str] = []
    i = 0

    while i < len(parts):
        token = parts[i]

        # Match both split form (--flag VALUE) and equals form (--flag=VALUE).
        if token == stem:
            i += 2
            continue
        if token.startswith(f"{stem}="):
            i += 1
            continue

        filtered.append(token)
        i += 1

    filtered.extend([stem, value])
    parts[:] = filtered


def _remove_flag(parts: list[str], flag: str) -> None:
    """Remove a flag in either split (--flag VALUE) or equals (--flag=VALUE) form."""
    stem = flag.strip().split()[0].rstrip("=")
    filtered: list[str] = []
    i = 0
    while i < len(parts):
        token = parts[i]
        if token == stem:
            i += 1
            continue
        if token.startswith(f"{stem}="):
            i += 1
            continue
        filtered.append(token)
        i += 1
    parts[:] = filtered


def _fix_generic_fieldmap(parts: list[str], cfg: Config) -> None:
    if "--ignore" not in parts:
        _ensure_flag(parts, "--use-syn-sdc")
    _ensure_flag(parts, "--ignore fieldmaps")


def _repair_missing_tr(parts: list[str], cfg) -> None:
    bids_dir: Path | None = None
    participant_label: str | None = None

    i = 0
    while i < len(parts):
        token = parts[i]
        if token == "-v" and i + 1 < len(parts):
            mount = parts[i + 1]
            if mount.endswith(":/data:ro"):
                host_path = mount[: -len(":/data:ro")]
                bids_dir = Path(host_path)
            i += 2
            continue
        if token == "--participant-label" and i + 1 < len(parts):
            participant_label = parts[i + 1]
            i += 2
            continue
        i += 1

    if bids_dir is None or participant_label is None:
        _ensure_flag(parts, "--skip-bids-validation")
        return

    participant = participant_label if participant_label.startswith("sub-") else f"sub-{participant_label}"
    subject_dir = bids_dir / participant
    nii_files = sorted(subject_dir.glob("ses-*/func/*_bold.nii.gz"))
    nii_files.extend(sorted((subject_dir / "func").glob("*_bold.nii.gz")))

    for nii in nii_files:
        sidecar = nii.with_name(nii.name[:-7] + ".json")
        if sidecar.exists():
            try:
                data = json.loads(sidecar.read_text())
            except Exception:
                data = {}
        else:
            data = {}
        tr = float(nib.load(str(nii)).header.get_zooms()[3])
        data["RepetitionTime"] = tr
        sidecar.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")

    _remove_flag(parts, "--skip-bids-validation")
    _ensure_flag(parts, "--skip-bids-validation")


_FIX_RULES: list[tuple[str, str, object]] = [
    # Memory / OOM
    (r"(?i)(out.of.memory|oom|exit code 137|LOW-MEM|--low-mem)",
     "oom_low_mem",
     lambda parts, cfg: (
         _ensure_flag(parts, "--low-mem"),
         _replace_flag(parts, "--mem_mb ", str(cfg.mem_mb)),
         _replace_flag(parts, "--nprocs ", "1"),
     )),

    # Missing readout timing metadata
    (r"(?i)(readout time|readout timing|fallback-total-readout-time|Unknown total-readout time specification)",
     "fallback_readout_time",
     lambda parts, cfg: _replace_flag(
         parts,
         "--fallback-total-readout-time ",
         str(cfg.fallback_total_readout_time),
     )),

    # Missing TR / BIDS metadata → skip validation so fMRIPrep proceeds
    (r"(?i)(RepetitionTime|BIDS_FIX|missing.*TR)",
     "repair_missing_tr",
     _repair_missing_tr),

    # SyN SDC requires PhaseEncodingDirection; if absent, drop SyN and ignore fieldmaps.
    (r"(?i)(PhaseEncodingDirection.*absent|SyN.*PhaseEncoding|fieldmap-less.*PhaseEncoding)",
     "drop_syn_ignore_fieldmaps",
     lambda parts, cfg: (
         _remove_flag(parts, "--use-syn-sdc"),
         _ensure_flag(parts, "--ignore fieldmaps"),
     )),

    # Fieldmap errors
    (r"(?i)(fieldmap|SDC|susceptibility)",
     "generic_fieldmap_fix",
     _fix_generic_fieldmap),

    # FreeSurfer issues
    (r"(?i)(freesurfer|recon-all|fs-no-reconall)",
     "fs_no_reconall",
     lambda parts, cfg: _ensure_flag(parts, "--fs-no-reconall")),

    # Filesystem naming conflict → skip problematic FreeSurfer sub-stages
    (r"(?i)(naming conflict|FileExists|nogcareg|nocanorm)",
     "fs_naming_conflict",
     lambda parts, cfg: (
         _ensure_flag(parts, "--fs-no-reconall"),
     )),
]


class RecoveryAgent:
    """
    Applies targeted fixes to a Docker command based on a diagnosis report.

    The agent parses the diagnosis text, matches known failure patterns,
    and modifies the command accordingly.  Multiple fixes can be applied
    in a single pass if the report mentions multiple issues.
    """

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg

    # ---------------------------------------------------------------------- #
    #  Public API
    # ---------------------------------------------------------------------- #

    def apply_fix(self, command: str, diagnosis_report: str, *, retry_attempt: int = 0) -> str:
        """
        Return a modified command with fixes applied.

        Parameters
        ----------
        command : str
            The Docker command that failed (may contain shell line-continuations).
        diagnosis_report : str
            Plain-text output from DiagnosticAgent.diagnose_crash().
        retry_attempt : int
            Current orchestrator attempt count (logged for metrics).

        Returns
        -------
        str
            Updated command string, ready to pass to subprocess.
        """
        t0 = time.perf_counter()
        clean = self._normalise(command)
        parts = clean.split()
        diagnosis = diagnosis_report or ""
        original = clean

        applied: list[str] = []
        for pattern, action_name, fix_fn in _FIX_RULES:
            if re.search(pattern, diagnosis):
                fix_fn(parts, self.cfg)
                applied.append(action_name)

        if not applied:
            logger.warning(
                "RecoveryAgent: no fix rule matched the diagnosis. "
                "Returning original command."
            )
            new_cmd = clean
        else:
            logger.info("RecoveryAgent applied %d fix rule(s): %s", len(applied), applied)
            new_cmd = " ".join(parts)

        root_cause = ""
        for line in diagnosis.splitlines():
            if line.startswith("ROOT CAUSE:"):
                root_cause = line.replace("ROOT CAUSE:", "", 1).strip()
                break

        elapsed = time.perf_counter() - t0
        emit(
            "recovery_agent",
            "recovery_applied",
            root_cause_received=root_cause,
            repair_actions=applied,
            retry_attempt=retry_attempt,
            command_before=original,
            command_after=new_cmd,
            command_changed=(new_cmd.split() != original.split()),
            duration_seconds=round(elapsed, 4),
        )
        return new_cmd

    # ---------------------------------------------------------------------- #
    #  Internal helpers
    # ---------------------------------------------------------------------- #

    @staticmethod
    def _normalise(cmd: str) -> str:
        """Strip markdown code fences and merge shell line-continuations."""
        cmd = cmd.replace("```bash", "").replace("```sh", "").replace("```", "")
        # Collapse backslash-newline continuations into a single line
        cmd = re.sub(r"\\\s*\n\s*", " ", cmd)
        return cmd.strip()
