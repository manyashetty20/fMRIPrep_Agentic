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

import hashlib
import logging
import re
import time

from config_loader import Config
from diagnosis_evidence import evidence_pass, report_from_evidence, strip_benign_warnings
from metrics_logger import emit, estimate_llm_cost_usd, extract_llm_usage

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
#  Heuristic rules for common fMRIPrep failures
#  Each entry: (priority, regex_pattern, human_label, suggested_fixes)
# --------------------------------------------------------------------------- #
_HEURISTICS: list[tuple[int, str, str, list[str]]] = [
    (110, r"(?i)(ANAT_CLIPPED_BRAIN|boundary.*clipping|brain.*clipped|cortex.*clipped|over-stripped|skull_strip_reduction.*high|brain_mask.*boundary)",
     "Anatomical clipping / brain over-stripped",
     ["--skull-strip-template OASIS30ANTs", "--skull-strip-fixed-seed", "--fs-no-reconall"]),

    (106, r"(?i)(JSON_INVALID|Not a valid JSON file)",
     "Invalid JSON sidecar (JSON_INVALID)",
     ["quarantine unparseable sidecar JSON; rely on BIDS inheritance"]),

    (105, r"(?i)(ANAT_OVERSEGMENTATION|skull.*retained|dura.*retained|under-stripped|skull_strip_reduction.*low)",
     "Anatomical under-stripping / non-brain tissue retained",
     ["--skull-strip-template OASIS30ANTs", "--skull-strip-fixed-seed"]),

    (100, r"(?i)(Missing readout time information|Unknown total-readout time specification|missing.*TotalReadoutTime)",
     "Missing readout timing metadata",
     ["--fallback-total-readout-time", "add TotalReadoutTime or EffectiveEchoSpacing metadata"]),

    (95, r"(?i)(out of memory|oom-?killer|exit code 137|Process killed with exit code 137|(?m:^\s*Killed\s*$))",
     "OUT-OF-MEMORY crash",
     ["--low-mem", "--mem_mb", "--nprocs 1"]),

    (92, r"(?i)(the input device is not a TTY|pseudo-tty)",
     "Docker TTY / pseudo-tty error",
     ["remove -t/-i/-ti from docker run"]),

    (90, r"(?i)(repetition.?time|RepetitionTime|missing.*TR|TR.*missing)",
     "Missing RepetitionTime in BIDS metadata",
     ["BIDS_FIX: inject RepetitionTime into task JSON sidecar"]),

    (85, r"(?i)(PhaseEncodingDirection.*absent|fieldmap-less.*PhaseEncoding|SyN.*PhaseEncoding)",
     "SyN SDC requires PhaseEncodingDirection which is absent",
     ["remove --use-syn-sdc", "--ignore fieldmaps"]),

    (80, r"(?i)(fieldmap|field.?map|fmap|SDC|susceptibility)",
     "Fieldmap / distortion-correction error",
     ["--use-syn-sdc", "--ignore fieldmaps"]),

    (75, r"(?i)(FREESURFER_SURFACE_FAILURE|recon-all.*failed|surface.*defect|euler.*number|topology.*error)",
     "FreeSurfer surface reconstruction failure",
     ["--fs-no-reconall"]),

    (72, r"(?i)(MNI_REGISTRATION_DISTORTION|normalization.*failed|registration.*distortion|MNI.*misalignment)",
     "MNI spatial normalization distortion or failure",
     ["--output-spaces MNI152NLin2009cAsym:res-2"]),

    (70, r"(?i)(no such file.*license|license.*not found|license file .* not found|valid license file is required|freesurfer license)",
     "FreeSurfer license or binary missing",
     ["verify license.txt path", "--fs-no-reconall"]),

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
        prompt_hash = ""
        evidence: dict = {}

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

        evidence = evidence_pass(error_log)
        filtered_log = evidence.get("filtered_log") or strip_benign_warnings(error_log)
        evidence_report = report_from_evidence(evidence, excerpt=filtered_log[:400])
        mode = (self.cfg.diagnosis_mode or "regex_llm_fallback").strip()

        if evidence_report and mode != "llm_only":
            report = evidence_report
            detection_method = "deterministic_evidence_pass"
        elif mode == "regex_only":
            report = self._heuristic_diagnose(filtered_log)
            detection_method = "regex_heuristic"
        elif mode == "llm_only":
            try:
                llm = self._get_llm()
                if llm is not None:
                    report, llm_usage, prompt_hash = self._llm_diagnose(llm, filtered_log)
                    detection_method = "llm_only"
                else:
                    report = self._heuristic_diagnose(filtered_log)
                    detection_method = "regex_heuristic"
            except Exception as exc:
                logger.warning("LLM diagnosis failed (%s) – falling back to heuristics.", exc)
                report = self._heuristic_diagnose(filtered_log)
                detection_method = "regex_heuristic"
        else:
            # regex_llm_fallback: evidence already handled; try regex then LLM if unknown
            report = self._heuristic_diagnose(filtered_log)
            detection_method = "regex_heuristic"
            if "Unknown – no recognised pattern" in report:
                try:
                    llm = self._get_llm()
                    if llm is not None:
                        report, llm_usage, prompt_hash = self._llm_diagnose(llm, filtered_log)
                        detection_method = "llm_fallback"
                except Exception as exc:
                    logger.warning("LLM diagnosis failed (%s) – keeping heuristics.", exc)

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
            log_excerpt=(filtered_log or "")[:2000],
            root_cause=root_cause,
            detection_method=detection_method,
            duration_seconds=round(elapsed, 4),
            report=report,
            llm_usage=llm_usage,
            llm_cost_usd_estimate=cost,
            evidence_findings=evidence.get("findings"),
            prompt_hash=prompt_hash,
            model_name=self.cfg.llm_model,
            model_provider=self.cfg.llm_provider,
            temperature=self.cfg.llm_temperature,
            llm_seed=self.cfg.llm_seed,
        )
        return report

    # ---------------------------------------------------------------------- #
    #  Internal helpers
    # ---------------------------------------------------------------------- #

    @staticmethod
    def _parse_root_cause(report: str) -> str:
        for line in (report or "").splitlines():
            stripped = line.strip().lstrip("#").lstrip("*").strip()
            if stripped.upper().startswith("ROOT CAUSE:"):
                return stripped.split(":", 1)[1].strip()
        return (report or "").splitlines()[0] if report else ""

    def _llm_diagnose(self, llm, error_log: str) -> tuple[str, dict, str]:
        from langchain_core.prompts import ChatPromptTemplate

        system = (
                    "You are an expert Neuroimaging Data Engineer specialising in "
                    "fMRIPrep, FreeSurfer, Docker, and Automated Image Quality Assurance. "
                    "Your task is to analyse an execution error log or Visual/Anatomical QA failure report "
                    "and return a structured diagnosis in the following format:\n\n"
                    "ROOT CAUSE: <one sentence, e.g. Anatomical clipping / brain over-stripped, Missing readout timing, etc.>\n"
                    "EVIDENCE: <quoted snippet from log or QA report>\n"
                    "RECOMMENDED FIXES:\n"
                    "  1. <fix, e.g. --skull-strip-template OASIS30ANTs, --fs-no-reconall, --fallback-total-readout-time, etc.>\n"
                    "  2. <fix (if applicable)>\n"
                    "SEVERITY: LOW | MEDIUM | HIGH"
        )
        template = ChatPromptTemplate.from_messages([
            ("system", system),
            ("user", "Execution log / QA Failure Report:\n{log_text}"),
        ])
        payload = {"log_text": error_log[:6000]}
        prompt_hash = hashlib.sha256((system + payload["log_text"]).encode("utf-8")).hexdigest()
        chain = template | llm
        result = chain.invoke(payload)
        usage = extract_llm_usage(result)
        usage["prompt_hash"] = prompt_hash
        usage["model_name"] = usage.get("model_name") or self.cfg.llm_model
        text = result.content if hasattr(result, "content") else str(result)
        return text, usage, prompt_hash

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
                kwargs = {"model_name": model, "temperature": temp}
                if self.cfg.llm_seed is not None:
                    kwargs["model_kwargs"] = {"seed": int(self.cfg.llm_seed)}
                self._llm = ChatGroq(**kwargs)
            elif provider == "openai":
                from langchain_openai import ChatOpenAI
                self._llm = ChatOpenAI(model_name=model, temperature=temp, seed=self.cfg.llm_seed)
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
