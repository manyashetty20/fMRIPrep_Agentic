"""
testing/common.py
=================
Shared helpers for publication evaluation runners.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TESTING_ROOT = Path(__file__).resolve().parent
DEFAULT_RESULTS_ROOT = TESTING_ROOT / "results"


@dataclass
class TestConfig:
    """Resolved publication-battery settings."""

    bids_dir: Path
    dataset_id: str
    participants: list[str]
    eval_root: Path
    output_root: Path
    license_file: Path
    config_yaml: Path | None
    docker_image: str | None = None
    anat_only: bool = False
    sloppy: bool = False
    low_mem: bool = True
    nprocs: int = 1
    max_participants: int | None = None
    extra_main_args: list[str] = field(default_factory=list)
    extra_baseline_args: list[str] = field(default_factory=list)

    def output_dir_for(self, suite: str, participant: str) -> Path:
        return self.output_root / suite / self.dataset_id / participant

    def eval_export_root(self) -> Path:
        return self.eval_root


def project_python() -> Path:
    venv_py = ROOT / "venv" / "bin" / "python"
    return venv_py if venv_py.exists() else Path(sys.executable)


def load_test_config(path: Path) -> TestConfig:
    raw: dict[str, Any] = yaml.safe_load(path.read_text()) or {}
    dataset = raw.get("dataset", {})
    paths = raw.get("paths", {})
    pipeline = raw.get("pipeline", {})

    bids_dir = Path(dataset.get("bids_dir", "./data/bids_input")).expanduser()
    if not bids_dir.is_absolute():
        bids_dir = (ROOT / bids_dir).resolve()

    eval_root = Path(paths.get("eval_root", "./testing/results/evaluation")).expanduser()
    if not eval_root.is_absolute():
        eval_root = (ROOT / eval_root).resolve()

    output_root = Path(paths.get("output_root", "./testing/results/outputs")).expanduser()
    if not output_root.is_absolute():
        output_root = (ROOT / output_root).resolve()

    license_file = Path(paths.get("license_file", "./license.txt")).expanduser()
    if not license_file.is_absolute():
        license_file = (ROOT / license_file).resolve()

    config_yaml = paths.get("config_yaml")
    config_path = None
    if config_yaml:
        config_path = Path(config_yaml).expanduser()
        if not config_path.is_absolute():
            config_path = (ROOT / config_path).resolve()

    participants = list(dataset.get("participants") or [])
    if not participants:
        from bids_discovery import list_bids_participants

        participants = list_bids_participants(bids_dir, require_anat_t1w=True)

    max_p = dataset.get("max_participants")
    if max_p is not None:
        participants = participants[: int(max_p)]

    return TestConfig(
        bids_dir=bids_dir,
        dataset_id=str(dataset.get("dataset_id", bids_dir.name)),
        participants=participants,
        eval_root=eval_root,
        output_root=output_root,
        license_file=license_file,
        config_yaml=config_path,
        docker_image=pipeline.get("docker_image"),
        anat_only=bool(pipeline.get("anat_only", False)),
        sloppy=bool(pipeline.get("sloppy", False)),
        low_mem=bool(pipeline.get("low_mem", True)),
        nprocs=int(pipeline.get("nprocs", 1)),
        max_participants=dataset.get("max_participants"),
        extra_main_args=list(raw.get("extra_main_args") or []),
        extra_baseline_args=list(raw.get("extra_baseline_args") or []),
    )


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_run_manifest(path: Path, payload: dict[str, Any]) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def run_command(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    dry_run: bool = False,
    log_file: Path | None = None,
) -> int:
    line = " ".join(cmd)
    print(f"\n$ {line}")
    if dry_run:
        return 0

    proc = subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        env=env,
        capture_output=log_file is not None,
        text=True,
    )
    if log_file is not None:
        ensure_parent(log_file)
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        log_file.write_text(stdout + ("\n--- STDERR ---\n" + stderr if stderr else ""))
        print(f"  log → {log_file}")
    return proc.returncode


def pipeline_flags(cfg: TestConfig) -> list[str]:
    args: list[str] = []
    if cfg.anat_only:
        args.append("--anat-only")
    else:
        args.append("--no-anat-only")
    if cfg.sloppy:
        args.append("--sloppy")
    else:
        args.append("--no-sloppy")
    if cfg.low_mem:
        args.append("--low-mem")
    else:
        args.append("--no-low-mem")
    args.extend(["--nprocs", str(cfg.nprocs)])
    if cfg.docker_image:
        args.extend(["--docker-image", cfg.docker_image])
    return args


def base_main_cmd(
    cfg: TestConfig,
    *,
    participant: str,
    output_dir: Path,
    injected_failure_mode: str = "",
    ablation_args: list[str] | None = None,
) -> list[str]:
    cmd = [
        str(project_python()),
        str(ROOT / "main.py"),
        "--bids-dir",
        str(cfg.bids_dir),
        "--output-dir",
        str(output_dir),
        "--evaluation-export-root",
        str(cfg.eval_export_root()),
        "--license",
        str(cfg.license_file),
        "--participant",
        participant,
        *pipeline_flags(cfg),
    ]
    if cfg.config_yaml:
        cmd.extend(["--config", str(cfg.config_yaml)])
    if injected_failure_mode:
        cmd.extend(["--injected-failure-mode", injected_failure_mode])
    if ablation_args:
        cmd.extend(ablation_args)
    cmd.extend(cfg.extra_main_args)
    return cmd


def base_baseline_cmd(cfg: TestConfig, *, participant: str, output_dir: Path) -> list[str]:
    cmd = [
        str(project_python()),
        str(ROOT / "scripts" / "run_baseline.py"),
        "--bids-dir",
        str(cfg.bids_dir),
        "--output-dir",
        str(output_dir),
        "--evaluation-export-root",
        str(cfg.eval_export_root()),
        "--license",
        str(cfg.license_file),
        "--participant",
        participant,
        *pipeline_flags(cfg),
    ]
    if cfg.config_yaml:
        cmd.extend(["--config", str(cfg.config_yaml)])
    cmd.extend(cfg.extra_baseline_args)
    return cmd


def validate_prerequisites(cfg: TestConfig, *, require_docker: bool = True) -> list[str]:
    """Return a list of blocking issues (empty = OK)."""
    issues: list[str] = []
    if not cfg.bids_dir.is_dir():
        hint = _suggest_bids_dir(cfg.bids_dir)
        issues.append(f"BIDS directory not found: {cfg.bids_dir}.{hint}")
    elif not (cfg.bids_dir / "dataset_description.json").is_file():
        issues.append(
            f"BIDS root missing dataset_description.json: {cfg.bids_dir} "
            "(point bids_dir at the dataset root, not a subject folder)."
        )
    if not cfg.license_file.is_file():
        issues.append(
            f"FreeSurfer license not found: {cfg.license_file} "
            "(save your license as license.txt in the project root)."
        )
    if require_docker:
        proc = subprocess.run(["docker", "info"], capture_output=True, text=True)
        if proc.returncode != 0:
            issues.append(
                "Docker is not running. Open Docker Desktop, wait until it says "
                "'Docker Desktop is running', then run `docker info` again."
            )
    if not cfg.participants:
        issues.append(f"No participants configured or discovered under {cfg.bids_dir}")
    return issues


def _suggest_bids_dir(configured: Path) -> str:
    """Offer likely local paths when the YAML still has a placeholder."""
    candidates = [
        Path("/Users/manyashetty/Desktop/ds000114"),
        ROOT / "data" / "bids_input",
    ]
    for path in candidates:
        if path.is_dir() and (path / "dataset_description.json").is_file():
            return f" Found dataset at {path} — set bids_dir in testing/config/publication_battery.yaml."
    if "/path/to/" in str(configured):
        return (
            " Edit testing/config/publication_battery.yaml and set bids_dir to your "
            "OpenNeuro download (must contain dataset_description.json)."
        )
    return ""
