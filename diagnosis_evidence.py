"""
Deterministic pre-LLM evidence pass over fMRIPrep / Docker logs.

Filters known-benign warnings out of the text that would otherwise be sent to
an LLM, and extracts hard evidence (OOM killer, exit 137, missing license).
"""

from __future__ import annotations

import re
from typing import Any

BENIGN_LINE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)the requested image's platform \(linux/amd64\) does not match"),
    re.compile(r"(?i)WARNING: The requested image's platform"),
    re.compile(r"(?i)experimental features"),
]

OOM_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("exit_137", re.compile(r"(?i)exit(?:ed)?(?: with)?(?: code)?\s*137")),
    ("oom_killer", re.compile(r"(?i)oom-?killer|out of memory|Killed process")),
    ("killed_after_runtime", re.compile(r"(?i)(?<!not )Killed(?! process)")),
]

LICENSE_PATTERNS = [
    re.compile(r"(?i)valid license file is required"),
    re.compile(r"(?i)no such file.*license|license.*not found"),
]

SYN_PED_PATTERNS = [
    re.compile(r"(?i)Fieldmap-less \(SyN\) estimation was requested, but PhaseEncoding"),
    re.compile(r"(?i)PhaseEncodingDirection.*absent"),
]

READOUT_PATTERNS = [
    re.compile(r"(?i)Unknown total-readout time specification"),
    re.compile(r"(?i)Missing readout time information"),
]

TR_PATTERNS = [
    re.compile(r"(?i)RepetitionTime"),
]

TTY_PATTERNS = [
    re.compile(r"(?i)the input device is not a TTY|pseudo-tty"),
]

NAMING_PATTERNS = [
    re.compile(r"(?i)naming conflict|FileExistsError|already exists"),
]

FILE_NOT_FOUND_AFTER_LONG = re.compile(r"(?i)FileNotFoundError")


def strip_benign_warnings(log_text: str) -> str:
    kept: list[str] = []
    for line in (log_text or "").splitlines():
        if any(p.search(line) for p in BENIGN_LINE_PATTERNS):
            continue
        kept.append(line)
    return "\n".join(kept)


def evidence_pass(log_text: str, *, runtime_seconds: float | None = None) -> dict[str, Any]:
    """
    Return structured evidence that can override or constrain LLM diagnosis.

    Priority: OOM/exit 137 > license > TTY > SyN/PED > readout > TR > naming.
    Generic 'killed' without 137/OOM is not treated as OOM unless runtime is long
    and FileNotFoundError is absent.
    """
    raw = log_text or ""
    filtered = strip_benign_warnings(raw)
    findings: list[str] = []

    has_137 = bool(OOM_PATTERNS[0][1].search(filtered) or "137" in filtered)
    has_oom_killer = bool(OOM_PATTERNS[1][1].search(filtered))
    has_killed = bool(re.search(r"(?i)\bKilled\b", filtered))
    has_fnf = bool(FILE_NOT_FOUND_AFTER_LONG.search(filtered))

    if has_137 or has_oom_killer:
        findings.append("oom")
    elif has_killed and not has_fnf and (runtime_seconds is None or runtime_seconds < 30):
        # Short-run "Killed" is treated as OOM-like; long-run FileNotFound is not.
        findings.append("oom")

    if any(p.search(filtered) for p in LICENSE_PATTERNS):
        findings.append("missing_fs_license")
    if any(p.search(filtered) for p in TTY_PATTERNS):
        findings.append("tty")
    if any(p.search(filtered) for p in SYN_PED_PATTERNS):
        findings.append("missing_phase_encoding")
    if any(p.search(filtered) for p in READOUT_PATTERNS):
        findings.append("missing_total_readout_time")
    if any(p.search(filtered) for p in TR_PATTERNS) and "missing_total_readout_time" not in findings:
        if re.search(r"(?i)missing.*RepetitionTime|RepetitionTime.*required", filtered):
            findings.append("missing_tr")
    if any(p.search(filtered) for p in NAMING_PATTERNS):
        findings.append("fs_naming_conflict")

    primary = findings[0] if findings else None
    return {
        "primary": primary,
        "findings": findings,
        "filtered_log": filtered,
        "benign_stripped": filtered != raw,
        "exit_137": has_137,
        "file_not_found": has_fnf,
        "runtime_seconds": runtime_seconds,
    }


EVIDENCE_TO_REPORT: dict[str, tuple[str, list[str]]] = {
    "oom": (
        "OUT-OF-MEMORY crash",
        ["--low-mem", "--mem_mb", "--nprocs 1"],
    ),
    "missing_fs_license": (
        "FreeSurfer license or binary missing",
        ["verify license.txt path", "--fs-no-reconall"],
    ),
    "tty": (
        "Docker TTY / pseudo-tty error",
        ["remove -t/-i/-ti from docker run"],
    ),
    "missing_phase_encoding": (
        "SyN SDC requires PhaseEncodingDirection which is absent",
        ["remove --use-syn-sdc", "--ignore fieldmaps"],
    ),
    "missing_total_readout_time": (
        "Missing readout timing metadata",
        ["--fallback-total-readout-time"],
    ),
    "missing_tr": (
        "Missing RepetitionTime in BIDS metadata",
        ["BIDS_FIX: inject RepetitionTime into task JSON sidecar"],
    ),
    "fs_naming_conflict": (
        "Output filesystem naming conflict",
        ["--fs-no-reconall"],
    ),
}


def report_from_evidence(evidence: dict[str, Any], excerpt: str = "") -> str | None:
    primary = evidence.get("primary")
    if not primary or primary not in EVIDENCE_TO_REPORT:
        return None
    label, fixes = EVIDENCE_TO_REPORT[primary]
    lines = [
        f"ROOT CAUSE: {label}",
        f"EVIDENCE: {excerpt.strip() or primary}",
        "RECOMMENDED FIXES:",
    ]
    for i, fix in enumerate(fixes, 1):
        lines.append(f"  {i}. {fix}")
    lines.append("SEVERITY: HIGH")
    lines.append("DETECTION: deterministic_evidence_pass")
    return "\n".join(lines)
