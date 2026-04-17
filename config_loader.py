"""
config_loader.py
================
Single source of truth for all runtime configuration.

Priority (highest → lowest):
  1. CLI arguments (parsed in main.py, passed here)
  2. Environment variables  (FMRIPREP_BIDS_DIR, FMRIPREP_PARTICIPANT, etc.)
  3. config.yaml values
  4. Built-in defaults
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Any, Optional

import yaml

# --------------------------------------------------------------------------- #
#  Defaults – used when neither yaml nor env vars provide a value
# --------------------------------------------------------------------------- #
_DEFAULTS: dict[str, Any] = {
    "paths.bids_dir":         "./data/bids_input",
    "paths.output_dir":       "./outputs",
    "paths.work_dir":         "./outputs/work",
    "paths.license_file":     "./license.txt",
    "paths.docs_dir":         "./data/docs",
    "paths.vector_db_dir":    "./database/vector_store",

    "subject.participant_id": "sub-01",
    "subject.session_id":     None,

    "pipeline.anat_only":              True,
    "pipeline.sloppy":                 True,
    "pipeline.skip_bids_validation":   True,
    "pipeline.low_mem":                True,
    "pipeline.mem_mb":                 4000,
    "pipeline.nprocs":                 1,
    "pipeline.docker_image":           "poldracklab/fmriprep:latest",

    "llm.provider":       "groq",
    "llm.model_name":     "llama-3.3-70b-versatile",
    "llm.temperature":    0,

    "embeddings.model_name": "all-MiniLM-L6-v2",

    "agents.max_recovery_attempts": 3,
    "agents.vision_enabled":        True,

    "logging.level":    "INFO",
    "logging.log_file": None,
}

# --------------------------------------------------------------------------- #
#  Environment-variable overrides
# --------------------------------------------------------------------------- #
_ENV_MAP: dict[str, str] = {
    "FMRIPREP_BIDS_DIR":       "paths.bids_dir",
    "FMRIPREP_OUTPUT_DIR":     "paths.output_dir",
    "FMRIPREP_WORK_DIR":       "paths.work_dir",
    "FMRIPREP_LICENSE":        "paths.license_file",
    "FMRIPREP_DOCS_DIR":       "paths.docs_dir",
    "FMRIPREP_VECTOR_DB_DIR":  "paths.vector_db_dir",
    "FMRIPREP_PARTICIPANT":    "subject.participant_id",
    "FMRIPREP_SESSION":        "subject.session_id",
    "FMRIPREP_DOCKER_IMAGE":   "pipeline.docker_image",
    "FMRIPREP_MEM_MB":         "pipeline.mem_mb",
    "FMRIPREP_NPROCS":         "pipeline.nprocs",
    "GROQ_MODEL":              "llm.model_name",
    "LOG_LEVEL":               "logging.level",
}


def _flatten(d: dict, prefix: str = "") -> dict[str, Any]:
    """Recursively flatten a nested dict into dot-separated keys."""
    out: dict[str, Any] = {}
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(_flatten(v, full_key))
        else:
            out[full_key] = v
    return out


class Config:
    """
    Unified configuration object.

    Usage
    -----
    >>> cfg = Config()                          # auto-find config.yaml
    >>> cfg = Config("path/to/config.yaml")
    >>> cfg.bids_dir                            # resolved absolute Path
    >>> cfg.get("pipeline.mem_mb")              # 4000
    """

    def __init__(
        self,
        yaml_path: Optional[str | Path] = None,
        overrides: Optional[dict[str, Any]] = None,
    ) -> None:
        # Locate yaml
        if yaml_path is None:
            yaml_path = self._find_yaml()

        # Load yaml (may be None if file not found)
        raw: dict[str, Any] = {}
        if yaml_path and Path(yaml_path).exists():
            with open(yaml_path, "r") as f:
                raw = yaml.safe_load(f) or {}

        # Merge: defaults < yaml < env vars < overrides
        self._cfg: dict[str, Any] = dict(_DEFAULTS)
        self._cfg.update(_flatten(raw))

        for env_var, key in _ENV_MAP.items():
            val = os.environ.get(env_var)
            if val is not None:
                # Cast numerics
                if key in ("pipeline.mem_mb", "pipeline.nprocs", "agents.max_recovery_attempts"):
                    val = int(val)  # type: ignore[assignment]
                self._cfg[key] = val

        if overrides:
            self._cfg.update(overrides)

        # Setup logging
        self._configure_logging()

    # ---------------------------------------------------------------------- #
    #  Dot-path accessor
    # ---------------------------------------------------------------------- #

    def get(self, key: str, default: Any = None) -> Any:
        return self._cfg.get(key, default)

    # ---------------------------------------------------------------------- #
    #  Convenience properties (resolved absolute Paths where applicable)
    # ---------------------------------------------------------------------- #

    def _abs(self, key: str) -> Path:
        raw = self._cfg.get(key, "")
        return Path(raw).resolve()

    @property
    def bids_dir(self) -> Path:
        return self._abs("paths.bids_dir")

    @property
    def output_dir(self) -> Path:
        return self._abs("paths.output_dir")

    @property
    def work_dir(self) -> Path:
        return self._abs("paths.work_dir")

    @property
    def license_file(self) -> Path:
        return self._abs("paths.license_file")

    @property
    def docs_dir(self) -> Path:
        return self._abs("paths.docs_dir")

    @property
    def vector_db_dir(self) -> Path:
        return self._abs("paths.vector_db_dir")

    @property
    def participant_id(self) -> str:
        return str(self._cfg.get("subject.participant_id", "sub-01"))

    @property
    def session_id(self) -> Optional[str]:
        val = self._cfg.get("subject.session_id")
        return str(val) if val else None

    @property
    def docker_image(self) -> str:
        return str(self._cfg.get("pipeline.docker_image", "poldracklab/fmriprep:latest"))

    @property
    def anat_only(self) -> bool:
        return bool(self._cfg.get("pipeline.anat_only", True))

    @property
    def sloppy(self) -> bool:
        return bool(self._cfg.get("pipeline.sloppy", True))

    @property
    def skip_bids_validation(self) -> bool:
        return bool(self._cfg.get("pipeline.skip_bids_validation", True))

    @property
    def low_mem(self) -> bool:
        return bool(self._cfg.get("pipeline.low_mem", True))

    @property
    def mem_mb(self) -> int:
        return int(self._cfg.get("pipeline.mem_mb", 4000))

    @property
    def nprocs(self) -> int:
        return int(self._cfg.get("pipeline.nprocs", 1))

    @property
    def llm_provider(self) -> str:
        return str(self._cfg.get("llm.provider", "groq"))

    @property
    def llm_model(self) -> str:
        return str(self._cfg.get("llm.model_name", "llama-3.3-70b-versatile"))

    @property
    def llm_temperature(self) -> float:
        return float(self._cfg.get("llm.temperature", 0))

    @property
    def embedding_model(self) -> str:
        return str(self._cfg.get("embeddings.model_name", "all-MiniLM-L6-v2"))

    @property
    def max_recovery_attempts(self) -> int:
        return int(self._cfg.get("agents.max_recovery_attempts", 3))

    @property
    def vision_enabled(self) -> bool:
        return bool(self._cfg.get("agents.vision_enabled", True))

    # ---------------------------------------------------------------------- #
    #  Helpers
    # ---------------------------------------------------------------------- #

    def has_fieldmap(self) -> bool:
        """Check whether fieldmap data exists for the configured participant."""
        fmap_path = self.bids_dir / self.participant_id / "fmap"
        return fmap_path.exists() and fmap_path.is_dir() and any(fmap_path.iterdir())

    def validate(self) -> None:
        """Raise descriptive errors for missing required files/dirs."""
        errors: list[str] = []

        if not self.bids_dir.exists():
            errors.append(f"BIDS directory not found: {self.bids_dir}")

        if not self.license_file.exists():
            errors.append(
                f"FreeSurfer license not found: {self.license_file}\n"
                "  → Download from https://surfer.nmr.mgh.harvard.edu/registration.html"
            )

        if not self.docs_dir.exists():
            errors.append(f"Docs directory not found: {self.docs_dir}")

        if errors:
            raise FileNotFoundError(
                "Configuration validation failed:\n" + "\n".join(f"  • {e}" for e in errors)
            )

    def _configure_logging(self) -> None:
        level_str = str(self._cfg.get("logging.level", "INFO")).upper()
        level = getattr(logging, level_str, logging.INFO)
        log_file = self._cfg.get("logging.log_file")

        handlers: list[logging.Handler] = [logging.StreamHandler()]
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            handlers.append(logging.FileHandler(log_path))

        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
            handlers=handlers,
        )

    @staticmethod
    def _find_yaml() -> Optional[Path]:
        """Search for config.yaml starting from CWD up to repo root."""
        search = Path.cwd()
        for _ in range(4):  # walk up at most 4 levels
            candidate = search / "config.yaml"
            if candidate.exists():
                return candidate
            search = search.parent
        return None

    def __repr__(self) -> str:
        lines = [f"  {k}: {v}" for k, v in sorted(self._cfg.items())]
        return "Config(\n" + "\n".join(lines) + "\n)"