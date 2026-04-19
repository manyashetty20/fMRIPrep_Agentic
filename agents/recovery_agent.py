"""
agents/recovery_agent.py
=========================
Recovery Agent – parses a diagnosis report and applies surgical fixes
to the fMRIPrep Docker command.

No hardcoded paths or values – everything is derived from the diagnosis
text and the central Config.
"""

from __future__ import annotations

import logging
import re

from config_loader import Config

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
    """Replace or add a flag=value pair."""
    stem = flag.rstrip("=")
    filtered: list[str] = []
    skip_next = False

    for i, token in enumerate(parts):
        if skip_next:
            skip_next = False
            continue

        if token == stem:
            skip_next = True
            continue

        if token.startswith(stem):
            continue

        filtered.append(token)

    filtered.extend(stem.split())
    filtered.append(value)
    parts[:] = filtered


_FIX_RULES: list[tuple[str, object]] = [
    # Memory / OOM
    (r"(?i)(out.of.memory|oom|exit code 137|LOW-MEM|--low-mem)",
     lambda parts, cfg: (
         _ensure_flag(parts, "--low-mem"),
         _replace_flag(parts, "--mem_mb ", str(cfg.mem_mb)),
         _replace_flag(parts, "--nprocs ", "1"),
     )),

    # Missing readout timing metadata
    (r"(?i)(readout time|readout timing|fallback-total-readout-time|Unknown total-readout time specification)",
     lambda parts, cfg: _replace_flag(
         parts,
         "--fallback-total-readout-time ",
         str(cfg.fallback_total_readout_time),
     )),

    # Missing TR / BIDS metadata → skip validation so fMRIPrep proceeds
    (r"(?i)(RepetitionTime|BIDS_FIX|missing.*TR)",
     lambda parts, cfg: _ensure_flag(parts, "--skip-bids-validation")),

    # Fieldmap errors
    (r"(?i)(fieldmap|SDC|--use-syn-sdc|susceptibility)",
     lambda parts, cfg: (
         _ensure_flag(parts, "--use-syn-sdc"),
         _ensure_flag(parts, "--ignore fieldmaps"),
     )),

    # FreeSurfer issues
    (r"(?i)(freesurfer|recon-all|fs-no-reconall)",
     lambda parts, cfg: _ensure_flag(parts, "--fs-no-reconall")),

    # Filesystem naming conflict → skip problematic FreeSurfer sub-stages
    (r"(?i)(naming conflict|FileExists|nogcareg|nocanorm)",
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

    def apply_fix(self, command: str, diagnosis_report: str) -> str:
        """
        Return a modified command with fixes applied.

        Parameters
        ----------
        command : str
            The Docker command that failed (may contain shell line-continuations).
        diagnosis_report : str
            Plain-text output from DiagnosticAgent.diagnose_crash().

        Returns
        -------
        str
            Updated command string, ready to pass to subprocess.
        """
        # Normalise the command: strip markdown fences and line continuations
        clean = self._normalise(command)
        parts = clean.split()
        diagnosis = diagnosis_report or ""

        applied: list[str] = []
        for pattern, fix_fn in _FIX_RULES:
            if re.search(pattern, diagnosis):
                fix_fn(parts, self.cfg)
                applied.append(pattern)

        if not applied:
            logger.warning(
                "RecoveryAgent: no fix rule matched the diagnosis. "
                "Returning original command."
            )
            return clean

        logger.info("RecoveryAgent applied %d fix rule(s): %s", len(applied), applied)
        return " ".join(parts)

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
