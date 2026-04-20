"""
bids_discovery.py
=================
Discover BIDS subjects under a dataset root without hardcoding dataset-specific IDs.
Supports both flat (sub-X/anat/) and session-based (sub-X/ses-Y/anat/) layouts.
"""
from __future__ import annotations
import re
from pathlib import Path

_SUB_RE = re.compile(r"^sub-[a-zA-Z0-9]+$")
_SES_RE = re.compile(r"^ses-[a-zA-Z0-9]+$")


def list_bids_participants(
    bids_dir: Path,
    *,
    require_anat_t1w: bool = True,
) -> list[str]:
    """
    Return sorted `sub-*` labels present under ``bids_dir``.

    Parameters
    ----------
    bids_dir :
        Root of a BIDS dataset (contains ``dataset_description.json`` or at least ``sub-*`` dirs).
    require_anat_t1w :
        If True, only include subjects that have a ``*_T1w.nii.gz`` somewhere under anat/,
        either flat (sub-X/anat/) or session-based (sub-X/ses-Y/anat/).
    """
    if not bids_dir.is_dir():
        return []

    subjects: list[str] = []
    for child in sorted(bids_dir.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        if not _SUB_RE.match(name):
            continue

        if require_anat_t1w:
            if _has_t1w(child, name):
                subjects.append(name)
        else:
            subjects.append(name)

    return subjects


def _has_t1w(sub_dir: Path, sub_name: str) -> bool:
    """Check for T1w in flat or session-based layout."""
    # Flat layout: sub-X/anat/*_T1w.nii.gz
    flat_anat = sub_dir / "anat"
    if flat_anat.is_dir() and any(flat_anat.glob("*_T1w.nii.gz")):
        return True

    # Session layout: sub-X/ses-Y/anat/*_T1w.nii.gz
    for ses_dir in sorted(sub_dir.iterdir()):
        if not ses_dir.is_dir():
            continue
        if not _SES_RE.match(ses_dir.name):
            continue
        ses_anat = ses_dir / "anat"
        if ses_anat.is_dir() and any(ses_anat.glob("*_T1w.nii.gz")):
            return True

    return False


def is_all_participants_token(raw: str | None) -> bool:
    """True when the CLI/config value means «run every discovered subject»."""
    if raw is None:
        return False
    s = str(raw).strip().lower()
    return s in {"all", "*", "every", "everyone"}