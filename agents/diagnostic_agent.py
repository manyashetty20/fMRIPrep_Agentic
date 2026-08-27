"""
agents/diagnostic_agent.py
===========================
Diagnostic Agent – reads fMRIPrep error logs and identifies root causes.

The LLM provider and model are taken from the central Config object.
Falls back to a regex-based heuristic engine if no LLM is available.

Metrics (inspectable)
---------------------
``diagnose_crash`` emits ``diagnosis_completed`` via ``metrics_logger.emit`` with
root cause, detection method (``regex_heuristic`` vs ``llm_fallback``), timing,
and LLM token usage when available.
"""

from __future__ import annotations

import logging
import re
import time

from config_loader import Config
from metrics_logger import emit, estimate_llm_cost_usd, extract_llm_usage

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
#  Heuristic rules for common fMRIPrep failures
#  Each entry: (priority, regex_pattern, human_label, suggested_fixes)
# --------------------------------------------------------------------------- #
_HEURISTICS: list[tuple[int, str, str, list[str]]] = [
    (100, r"(?i)(Missing readout time information|Unknown total-readout time specification|missing.*TotalReadoutTime)",
     "Missing readout timing metadata",
     ["--fallback-total-readout-time", "add TotalReadoutTime or EffectiveEchoSpacing metadata"]),

    (95, r"(?i)(out of memory|oom|exit code 137|killed)",
     "OUT-OF-MEMORY crash",
     ["--low-mem", "--mem_mb", "--nprocs 1"]),

    (90, r"(?i)(repetition.?time|RepetitionTime|missing.*TR|TR.*missing)",
     "Missing RepetitionTime in BIDS metadata",
     ["BIDS_FIX: inject RepetitionTime into task JSON sidecar"]),

    (85, r"(?i)(PhaseEncodingDirection.*absent|fieldmap-less.*PhaseEncoding|SyN.*PhaseEncoding)",
     "SyN SDC requires PhaseEncodingDirection which is absent",
     ["remove --use-syn-sdc", "--ignore fieldmaps"]),

    (80, r"(?i)(fieldmap|field.?map|fmap|SDC|susceptibility)",
     "Fieldmap / distortion-correction error",
     ["--use-syn-sdc", "--ignore fieldmaps"]),

    (70, r"(?i)(no such file.*license|license.*not found|license file .* not found|freesurfer license)",
     "FreeSurfer license or binary missing",
     ["--fs-no-reconall", "verify license.txt path"]),

    (60, r"(?i)(naming conflict|already exists|FileExists|file.*exist)",
     "Output filesystem naming conflict",
     ["verify --output-spaces matches your configured output space",
      "FreeSurfer flags: -nogcareg -nocanorm"]),

    (50, r"(?i)(docker:.*cannot connect|docker:.*permission denied|cannot connect to the docker daemon|docker daemon)",
     "Docker daemon / permissions error",
     ["check Docker is running", "run with sudo if required"]),
]


class DiagnosticAgent:
    """
    Analyses an fMRIPrep error log and returns a structured diagnosis report.

    Strategy
    --------
    1. Try LLM-based diagnosis (full context, natural language).
    2. If LLM unavailable, fall back to heuristic regex matching.
    3. If nothing matches, return a generic report.
    """

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self._llm = None  # lazy

    # ---------------------------------------------------------------------- #
    #  Public API
    # ---------------------------------------------------------------------- #

    def diagnose_crash(self, error_log: str) -> str:
        """
        Return a plain-text diagnosis report for the given error log.

        Parameters
        ----------
        error_log : str
            Captured stderr / exception text from the failed fMRIPrep run.

        Returns
        -------
        str
            Human-readable report including cause and suggested fixes.
        """
        t0 = time.perf_counter()
        detection_method = "none"
        llm_usage: dict = {}
        report = "No error log captured. Cannot diagnose."

        if not error_log or not error_log.strip():
            elapsed = time.perf_counter() - t0
            emit(
                "diagnostic_agent",
                "diagnosis_completed",
                log_excerpt="",
                root_cause="No error log captured",
                detection_method="none",
                duration_seconds=round(elapsed, 4),
                report=report,
            )
            return report

        # Prefer heuristics first for deterministic eval metrics; still try LLM
        # when available and record which path produced the returned report.
        # Historical behaviour: try LLM first, fall back to heuristics.
        try:
            llm = self._get_llm()
            if llm is not None:
                report, llm_usage = self._llm_diagnose(llm, error_log)
                detection_method = "llm_fallback"
            else:
                report = self._heuristic_diagnose(error_log)
                detection_method = "regex_heuristic"
        except Exception as exc:
            logger.warning("LLM diagnosis failed (%s) – falling back to heuristics.", exc)
            report = self._heuristic_diagnose(error_log)
            detection_method = "regex_heuristic"

        root_cause = self._parse_root_cause(report)
        elapsed = time.perf_counter() - t0
        cost = estimate_llm_cost_usd(
            llm_usage.get("prompt_tokens"),
            llm_usage.get("completion_tokens"),
            input_rate_per_m=self.cfg.llm_cost_per_million_input_tokens,
            output_rate_per_m=self.cfg.llm_cost_per_million_output_tokens,
        )
        emit(
            "diagnostic_agent",
            "diagnosis_completed",
            log_excerpt=(error_log or "")[:2000],
            root_cause=root_cause,
            detection_method=detection_method,
            duration_seconds=round(elapsed, 4),
            report=report,
            llm_usage=llm_usage,
            llm_cost_usd_estimate=cost,
        )
        return report

    # ---------------------------------------------------------------------- #
    #  Internal helpers
    # ---------------------------------------------------------------------- #

    @staticmethod
    def _parse_root_cause(report: str) -> str:
        for line in (report or "").splitlines():
            if line.startswith("ROOT CAUSE:"):
                return line.replace("ROOT CAUSE:", "", 1).strip()
        return (report or "").splitlines()[0] if report else ""

    def _llm_diagnose(self, llm, error_log: str) -> tuple[str, dict]:
        from langchain_core.prompts import ChatPromptTemplate

        template = ChatPromptTemplate.from_messages([
            (
                "system",
                (
                    "You are an expert Neuroimaging Data Engineer specialising in "
                    "fMRIPrep, FreeSurfer, and Docker. "
                    "Your task is to analyse an error log and return a structured "
                    "diagnosis in the following format:\n\n"
                    "ROOT CAUSE: <one sentence>\n"
                    "EVIDENCE: <quoted snippet from log>\n"
                    "RECOMMENDED FIXES:\n"
                    "  1. <fix>\n"
                    "  2. <fix (if applicable)>\n"
                    "SEVERITY: LOW | MEDIUM | HIGH"
                ),
            ),
            ("user", "Error log:\n{log_text}"),
        ])
        chain = template | llm
        result = chain.invoke({"log_text": error_log[:6000]})  # trim very long logs
        usage = extract_llm_usage(result)
        text = result.content if hasattr(result, "content") else str(result)
        return text, usage

    def _heuristic_diagnose(self, error_log: str) -> str:
        best_match: tuple[int, str, list[str], str] | None = None
        for priority, pattern, label, fixes in _HEURISTICS:
            if re.search(pattern, error_log):
                match_obj = re.search(pattern, error_log)
                evidence = match_obj.group(0).strip() if match_obj else "(pattern matched)"
                if best_match is None or priority > best_match[0]:
                    best_match = (priority, label, fixes, evidence)

        if best_match is None:
            return (
                "ROOT CAUSE: Unknown – no recognised pattern found in log.\n"
                "EVIDENCE: (see full log)\n"
                "RECOMMENDED FIXES:\n"
                "  1. Inspect the full error output manually.\n"
                "  2. Try adding --verbose to fMRIPrep for more detail.\n"
                "SEVERITY: UNKNOWN"
            )

        _, label, fixes, evidence = best_match
        lines = [
            f"ROOT CAUSE: {label}",
            f"EVIDENCE: {evidence}",
            "RECOMMENDED FIXES:",
        ]
        for i, fix in enumerate(fixes, 1):
            lines.append(f"  {i}. {fix}")
        lines.append("SEVERITY: HIGH")
        return "\n".join(lines)

    def _get_llm(self):
        """Lazily build and cache the LLM instance."""
        if self._llm is not None:
            return self._llm

        provider = self.cfg.llm_provider
        model = self.cfg.llm_model
        temp = self.cfg.llm_temperature

        try:
            if provider == "groq":
                from langchain_groq import ChatGroq
                self._llm = ChatGroq(model_name=model, temperature=temp)
            elif provider == "openai":
                from langchain_openai import ChatOpenAI
                self._llm = ChatOpenAI(model_name=model, temperature=temp)
            elif provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                self._llm = ChatAnthropic(model_name=model, temperature=temp)
            else:
                logger.warning("Unknown LLM provider '%s'.", provider)
                return None
        except Exception as exc:
            logger.warning("LLM initialisation failed (%s).", exc)
            return None

        return self._llm
