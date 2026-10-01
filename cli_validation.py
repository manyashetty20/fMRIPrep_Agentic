"""Validate command tokens against the curated official fMRIPrep CLI flag list."""

from __future__ import annotations

import re
import shlex
from pathlib import Path

DOCKER_OK = frozenset({"-v", "-e", "--rm", "--user", "-u", "--gpus", "-w", "-t", "-i", "-ti", "--name"})
# Docker-only / wrapper tokens that are not fMRIPrep flags.
NON_FMRIPREP_PREFIXES = frozenset({"docker", "run"})

# Documented aliases that appear in older papers / wrappers.
FLAG_ALIASES: dict[str, str] = {
    "--fallback-totalreadout-time": "--fallback-total-readout-time",
    "--mem-mb": "--mem_mb",
    "--session-id": "--session-label",  # hallucinated in some LLM outputs; not official
}


def load_official_flags(path: Path) -> set[str]:
    flags: set[str] = set()
    if not path.is_file():
        return flags
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        flags.add(line.split()[0])
    return flags


def tokenize_command(command: str) -> list[str]:
    normalised = re.sub(r"\\\s*\n\s*", " ", command or "").strip()
    try:
        return shlex.split(normalised)
    except ValueError:
        return normalised.split()


def extract_flag_stems(command: str) -> list[str]:
    stems: list[str] = []
    for tok in tokenize_command(command):
        if tok.startswith("-"):
            stem = tok.split("=", 1)[0]
            if stem not in stems:
                stems.append(stem)
    return stems


def unknown_fmriprep_flags(command: str, official: set[str]) -> list[str]:
    """Return flag stems that are not in the official list and not Docker-only."""
    unknown: list[str] = []
    for stem in extract_flag_stems(command):
        if stem in DOCKER_OK:
            continue
        if stem in official:
            continue
        unknown.append(stem)
    return unknown


def canonical_flag(stem: str) -> str:
    return FLAG_ALIASES.get(stem, stem)


def validate_flag_list(flags: list[str], official: set[str]) -> dict:
    """
    Validate a list of proposed repair/CLI fragments (A4 dry-run).

    Does not execute anything. Returns counts of valid vs hallucinated stems.
    """
    valid: list[str] = []
    hallucinated: list[str] = []
    aliased: list[dict[str, str]] = []
    for raw in flags:
        token = raw.strip().split()[0] if raw.strip() else ""
        if not token.startswith("-"):
            continue
        stem = token.split("=", 1)[0]
        canon = canonical_flag(stem)
        if stem != canon:
            aliased.append({"proposed": stem, "canonical": canon})
        if stem in official or canon in official or stem in DOCKER_OK:
            valid.append(stem)
        else:
            hallucinated.append(stem)
    return {
        "valid": valid,
        "hallucinated": hallucinated,
        "aliased": aliased,
        "valid_rate": (len(valid) / max(len(valid) + len(hallucinated), 1)),
    }
