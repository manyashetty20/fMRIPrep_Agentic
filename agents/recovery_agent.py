"""
agents/recovery_agent.py
=========================
Recovery Agent – parses a diagnosis report and applies surgical fixes
to the fMRIPrep Docker command.

Free-text LLM output is never executed. Only named rule functions run.
When rule_gate is on (default), recommended flags in the diagnosis text are
ignored except as pattern matches against this catalog.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import nibabel as nib

from cli_validation import load_official_flags, validate_flag_list
from config_loader import Config
from metrics_logger import emit
from sidecar_rollback import backup_sidecar, write_command_backup

logger = logging.getLogger(__name__)


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
    takes_value = stem not in {
        "--use-syn-sdc",
        "--low-mem",
        "--sloppy",
        "--skip-bids-validation",
        "--fs-no-reconall",
        "--anat-only",
        "-t",
        "-i",
        "-ti",
        "--rm",
        "--skull-strip-fixed-seed",
    }
    filtered: list[str] = []
    i = 0
    while i < len(parts):
        token = parts[i]
        if token == stem:
            i += 1
            if takes_value and i < len(parts) and not parts[i].startswith("-"):
                i += 1
            continue
        if token.startswith(f"{stem}="):
            i += 1
            continue
        filtered.append(token)
        i += 1
    parts[:] = filtered


def _fix_generic_fieldmap(parts: list[str], cfg: Config) -> None:
    """Ignore broken fieldmaps. Never enable SyN when PhaseEncodingDirection is missing."""
    if cfg.missing_phase_encoding_direction():
        _remove_flag(parts, "--use-syn-sdc")
        _ensure_flag(parts, "--ignore fieldmaps")
        return
    if "--ignore" not in parts:
        _ensure_flag(parts, "--use-syn-sdc")
    _ensure_flag(parts, "--ignore fieldmaps")


def _fix_license_mount(parts: list[str], cfg: Config) -> None:
    """Ensure the FreeSurfer license is mounted at the correct path. Preserve all other tokens."""
    filtered: list[str] = []
    i = 0
    while i < len(parts):
        token = parts[i]
        if token == "-v" and i + 1 < len(parts):
            mount = parts[i + 1]
            if "license" in mount.lower():
                i += 2
                continue
        filtered.append(token)
        i += 1
    mount = f"{cfg.license_file}:/opt/freesurfer/license.txt:ro"
    filtered.extend(["-v", mount])
    parts[:] = filtered


def _repair_missing_tr(parts: list[str], cfg: Config) -> None:
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
        logger.warning("Could not extract bids_dir or participant_label from command, skipping TR repair")
        _ensure_flag(parts, "--skip-bids-validation")
        return

    participant = participant_label if participant_label.startswith("sub-") else f"sub-{participant_label}"
    subject_dir = bids_dir / participant

    if not subject_dir.exists():
        logger.warning("Subject directory does not exist: %s, skipping TR repair", subject_dir)
        _ensure_flag(parts, "--skip-bids-validation")
        return

    nii_files = sorted(subject_dir.glob("ses-*/func/*_bold.nii.gz"))
    nii_files.extend(sorted(subject_dir.glob("ses-*/func/*_bold.nii")))
    nii_files.extend(sorted((subject_dir / "func").glob("*_bold.nii.gz")))
    nii_files.extend(sorted((subject_dir / "func").glob("*_bold.nii")))

    if not nii_files:
        logger.warning("No NIfTI files found in %s, skipping TR repair", subject_dir)
        _ensure_flag(parts, "--skip-bids-validation")
        return

    repaired_count = 0
    for nii in nii_files:
        try:
            if nii.name.endswith(".nii.gz"):
                sidecar = nii.with_name(nii.name[:-7] + ".json")
            else:
                sidecar = nii.with_name(nii.name[:-4] + ".json")

            if sidecar.exists():
                backup_sidecar(cfg.output_dir, sidecar)
                try:
                    data = json.loads(sidecar.read_text())
                except Exception as e:
                    logger.warning("Failed to parse existing sidecar %s: %s", sidecar, e)
                    data = {}
            else:
                data = {}

            tr = float(nib.load(str(nii)).header.get_zooms()[3])
            data["RepetitionTime"] = tr
            sidecar.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")
            repaired_count += 1
        except Exception as e:
            logger.error("Failed to repair TR for %s: %s", nii, e)
            continue

    logger.info("Successfully repaired TR in %s/%s sidecar files", repaired_count, len(nii_files))
    _ensure_flag(parts, "--skip-bids-validation")


def _fix_skull_strip_clipping(parts: list[str], cfg: Config) -> None:
    templates = getattr(cfg, "skull_strip_templates", ["OASIS30ANTs", "NKI", "MNI152NLin2009cAsym"])
    current_tpl = None
    for i, tok in enumerate(parts):
        if tok == "--skull-strip-template" and i + 1 < len(parts):
            current_tpl = parts[i + 1]
            break

    next_tpl = templates[0]
    if current_tpl in templates:
        idx = templates.index(current_tpl)
        if idx + 1 < len(templates):
            next_tpl = templates[idx + 1]

    _replace_flag(parts, "--skull-strip-template ", next_tpl)
    _ensure_flag(parts, "--skull-strip-fixed-seed")
    _ensure_flag(parts, "--fs-no-reconall")


def _fix_skull_strip_oversegmentation(parts: list[str], cfg: Config) -> None:
    _replace_flag(parts, "--skull-strip-template ", "OASIS30ANTs")
    _ensure_flag(parts, "--skull-strip-fixed-seed")


def _fix_freesurfer_surface(parts: list[str], cfg: Config) -> None:
    _ensure_flag(parts, "--fs-no-reconall")


def _fix_spatial_normalization(parts: list[str], cfg: Config) -> None:
    target_space = getattr(cfg, "output_space", "MNI152NLin2009cAsym")
    if ":" not in target_space:
        _replace_flag(parts, "--output-spaces ", f"{target_space}:res-2")
    else:
        _replace_flag(parts, "--output-spaces ", target_space)


def _drop_syn(parts: list[str], cfg: Config) -> None:
    _remove_flag(parts, "--use-syn-sdc")
    _ensure_flag(parts, "--ignore fieldmaps")


def _fix_oom(parts: list[str], cfg: Config) -> None:
    _ensure_flag(parts, "--low-mem")
    _replace_flag(parts, "--mem_mb ", str(max(int(cfg.mem_mb), 8000)))
    _replace_flag(parts, "--nprocs ", "1")


def _fix_tty(parts: list[str], cfg: Config) -> None:
    _remove_flag(parts, "-ti")
    _remove_flag(parts, "-t")
    _remove_flag(parts, "-i")


def _fix_readout(parts: list[str], cfg: Config) -> None:
    _replace_flag(
        parts,
        "--fallback-total-readout-time ",
        str(cfg.fallback_total_readout_time),
    )


@dataclass(frozen=True)
class RepairRule:
    rule_id: str
    pattern: str
    scientific_impact: str
    apply: Callable[[list[str], Config], None]


# Order matters: more specific rules first. drop_syn must precede generic_fieldmap.
# generic_fieldmap is skipped in the same pass if drop_syn already ran.
def _repair_invalid_json(parts: list[str], cfg: Config) -> None:
    # Quarantine unparseable per-subject sidecars so BIDS inheritance uses the top-level task JSON.
    import shutil

    bids_dir = None
    for i, tok in enumerate(parts):
        if tok == "-v" and i + 1 < len(parts) and parts[i + 1].endswith(":/data:ro"):
            bids_dir = Path(parts[i + 1][: -len(":/data:ro")])
    if bids_dir is None or not bids_dir.exists():
        logger.warning("Could not locate BIDS dir in command; no JSON repair possible")
        return

    quarantine = Path(cfg.output_dir) / "quarantined_sidecars"
    moved = 0
    for jf in sorted(bids_dir.rglob("*.json")):
        if jf.name.startswith("."):
            continue
        try:
            json.loads(jf.read_text())
            continue
        except Exception:
            pass
        rel = jf.relative_to(bids_dir)
        if not rel.parts[0].startswith("sub-"):
            logger.warning("Invalid top-level JSON %s left untouched (would lose metadata)", jf)
            continue
        quarantine.mkdir(parents=True, exist_ok=True)
        shutil.move(str(jf), str(quarantine / jf.name))
        logger.info("Quarantined invalid sidecar %s", jf)
        moved += 1

    if moved:
        idx = parts.index("run") + 1 if "run" in parts else 1
        parts[idx:idx] = ["--label", "agentic_repair=json_quarantine"]


REPAIR_RULES: list[RepairRule] = [
    RepairRule(
        "quarantine_invalid_json",
        r"(?i)(JSON_INVALID|Not a valid JSON file|Invalid JSON sidecar)",
        "unparseable sidecar JSON quarantined (top-level task JSON inherited)",
        _repair_invalid_json,
    ),
    RepairRule(
        "fix_skull_strip_clipping",
        r"(?i)(ANAT_CLIPPED_BRAIN|boundary.*clipping|brain.*clipped|cortex.*clipped|over-stripped|skull_strip_reduction.*high|brain_mask.*boundary)",
        "skull-strip template/seed changed",
        _fix_skull_strip_clipping,
    ),
    RepairRule(
        "fix_skull_strip_oversegmentation",
        r"(?i)(ANAT_OVERSEGMENTATION|skull.*retained|dura.*retained|under-stripped|skull_strip_reduction.*low)",
        "skull-strip template/seed changed",
        _fix_skull_strip_oversegmentation,
    ),
    RepairRule(
        "remove_tty_flags",
        r"(?i)(tty|input device is not a TTY|pseudo-tty)",
        "docker TTY flags removed (no scientific impact)",
        _fix_tty,
    ),
    RepairRule(
        "fix_license_path",
        r"(?i)(license.*not found|valid license file is required|fs-license-file)",
        "license mount repaired (no scientific impact)",
        _fix_license_mount,
    ),
    RepairRule(
        "oom_low_mem",
        r"(?i)(out.of.memory|oom|exit code 137|LOW-MEM|--low-mem)",
        "memory clamped; nprocs=1",
        _fix_oom,
    ),
    RepairRule(
        "fallback_readout_time",
        r"(?i)(readout time|readout timing|fallback-total-readout-time|Unknown total-readout time specification)",
        "TotalReadoutTime fallback used (SDC timing approximated)",
        _fix_readout,
    ),
    RepairRule(
        "repair_missing_tr",
        r"(?i)(RepetitionTime|BIDS_FIX|missing.*TR)",
        "BIDS validation skipped after sidecar TR repair",
        _repair_missing_tr,
    ),
    RepairRule(
        "drop_syn_ignore_fieldmaps",
        r"(?i)(PhaseEncodingDirection.*absent|SyN.*PhaseEncoding|fieldmap-less.*PhaseEncoding)",
        "SDC dropped (SyN disabled; fieldmaps ignored)",
        _drop_syn,
    ),
    RepairRule(
        "generic_fieldmap_fix",
        r"(?i)(fieldmap|SDC|susceptibility)",
        "fieldmaps ignored (SyN only if PhaseEncodingDirection present)",
        _fix_generic_fieldmap,
    ),
    RepairRule(
        "fs_no_reconall",
        r"(?i)(FREESURFER_SURFACE_FAILURE|recon-all.*failed|surface.*defect|euler.*number|topology.*error)",
        "recon-all skipped",
        _fix_freesurfer_surface,
    ),
    RepairRule(
        "fix_spatial_normalization",
        r"(?i)(MNI_REGISTRATION_DISTORTION|normalization.*failed|registration.*distortion|MNI.*misalignment)",
        "output-spaces resolution clamped",
        _fix_spatial_normalization,
    ),
    RepairRule(
        "fs_naming_conflict",
        r"(?i)(naming conflict|FileExists|nogcareg|nocanorm)",
        "recon-all skipped due to naming conflict",
        _fix_freesurfer_surface,
    ),
]

# Keep the old name used by tests/docs.
_FIX_RULES = [(r.pattern, r.rule_id, r.apply) for r in REPAIR_RULES]


def extract_recommended_flags(diagnosis: str) -> list[str]:
    flags: list[str] = []
    for token in re.findall(r"(--[A-Za-z0-9][A-Za-z0-9_-]*)", diagnosis or ""):
        if token not in flags:
            flags.append(token)
    return flags


class RecoveryAgent:
    """
    Applies targeted fixes to a Docker command based on a diagnosis report.
    """

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.last_applied: list[str] = []
        self.last_impacts: list[str] = []
        self.last_dry_run: dict | None = None

    def apply_fix(
        self,
        command: str,
        diagnosis_report: str,
        *,
        retry_attempt: int = 0,
        already_applied: Iterable[str] | None = None,
    ) -> str:
        t0 = time.perf_counter()
        clean = self._normalise(command)
        parts = clean.split()
        diagnosis = diagnosis_report or ""
        original = clean
        applied_set = set(already_applied or [])

        write_command_backup(self.cfg.output_dir, original)

        if self.cfg.repair_dry_run and not self.cfg.rule_gate_enabled:
            official = load_official_flags(self.cfg.official_flags_file)
            proposed = extract_recommended_flags(diagnosis)
            self.last_dry_run = validate_flag_list(proposed, official)
            emit(
                "recovery_agent",
                "repair_dry_run",
                proposed_flags=proposed,
                validation=self.last_dry_run,
                retry_attempt=retry_attempt,
            )
            self.last_applied = []
            self.last_impacts = []
            return clean

        logger.info("RecoveryAgent: Starting fix application for attempt %d", retry_attempt)

        applied: list[str] = []
        impacts: list[str] = []
        for rule in REPAIR_RULES:
            if rule.rule_id in applied_set:
                continue
            if rule.rule_id == "generic_fieldmap_fix" and "drop_syn_ignore_fieldmaps" in (applied_set | set(applied)):
                continue
            if re.search(rule.pattern, diagnosis):
                logger.info("RecoveryAgent: Matched fix rule '%s'", rule.rule_id)
                try:
                    rule.apply(parts, self.cfg)
                    applied.append(rule.rule_id)
                    impacts.append(rule.scientific_impact)
                    applied_set.add(rule.rule_id)
                except Exception as e:
                    logger.error("RecoveryAgent: Failed to apply fix rule '%s': %s", rule.rule_id, e)

        if not applied:
            logger.warning("RecoveryAgent: no fix rule matched the diagnosis. Returning original command.")
            new_cmd = clean
        else:
            logger.info("RecoveryAgent applied %d fix rule(s): %s", len(applied), applied)
            new_cmd = " ".join(parts)

        root_cause = ""
        for line in diagnosis.splitlines():
            stripped = line.strip().lstrip("#").lstrip("*").strip()
            if stripped.upper().startswith("ROOT CAUSE:"):
                root_cause = stripped.split(":", 1)[1].strip()
                break

        elapsed = time.perf_counter() - t0
        self.last_applied = applied
        self.last_impacts = impacts
        emit(
            "recovery_agent",
            "recovery_applied",
            root_cause_received=root_cause,
            repair_actions=applied,
            repair_rule_ids=applied,
            scientific_impacts=impacts,
            retry_attempt=retry_attempt,
            command_before=original,
            command_after=new_cmd,
            command_changed=(new_cmd.split() != original.split()),
            duration_seconds=round(elapsed, 4),
            rule_gate_enabled=self.cfg.rule_gate_enabled,
        )
        return new_cmd

    @staticmethod
    def _normalise(cmd: str) -> str:
        cmd = cmd.replace("```bash", "").replace("```sh", "").replace("```", "")
        cmd = re.sub(r"\\\s*\n\s*", " ", cmd)
        return cmd.strip()
