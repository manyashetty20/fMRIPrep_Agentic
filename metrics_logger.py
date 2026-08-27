"""
metrics_logger.py
=================
Central structured metrics logger for Agentic fMRIPrep.

Every agent emits timestamped JSON events to a single JSONL file per run.
Events are also kept in-memory so ``evaluation_export.build_evaluation_row``
and ``testing/analyze_results.py`` can aggregate them after the run.

Canonical inspectable API
-------------------------
- ``MetricsLogger.emit`` — write one event (used by all agents)
- ``MetricsLogger.flush`` — persist any buffered events and close the run
- ``get_logger`` / ``init_run`` — process-wide singleton bound to ``run_id``
"""

from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_lock = threading.Lock()
_INSTANCE: "MetricsLogger | None" = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_run_id() -> str:
    """Return a short unique run identifier (YYYYMMDDTHHMMSSZ_<hex>)."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}_{uuid.uuid4().hex[:8]}"


class MetricsLogger:
    """
    Append-only JSONL metrics sink for one pipeline run.

    Each event must include at least:
    ``timestamp``, ``agent_name``, ``event_type``, ``subject_id``, ``run_id``.
    """

    def __init__(
        self,
        *,
        run_id: str,
        subject_id: str,
        metrics_dir: Path,
        dataset_id: str = "",
    ) -> None:
        self.run_id = run_id
        self.subject_id = subject_id
        self.dataset_id = dataset_id
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.metrics_dir / f"metrics_{run_id}.jsonl"
        self._events: list[dict[str, Any]] = []

    def emit(
        self,
        agent_name: str,
        event_type: str,
        **fields: Any,
    ) -> dict[str, Any]:
        """Append one structured event to memory and to the JSONL file."""
        event: dict[str, Any] = {
            "timestamp": _utc_now(),
            "agent_name": agent_name,
            "event_type": event_type,
            "subject_id": self.subject_id,
            "run_id": self.run_id,
            "dataset_id": self.dataset_id,
        }
        event.update(fields)
        with _lock:
            self._events.append(event)
            with self.path.open("a") as f:
                f.write(json.dumps(event, sort_keys=True, default=str) + "\n")
        return event

    @property
    def events(self) -> list[dict[str, Any]]:
        return list(self._events)

    def events_of_type(self, event_type: str) -> list[dict[str, Any]]:
        return [e for e in self._events if e.get("event_type") == event_type]

    def flush(self) -> Path:
        """Ensure the JSONL file exists (even if empty) and return its path."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()
        return self.path


def init_run(
    *,
    subject_id: str,
    metrics_dir: Path | str,
    dataset_id: str = "",
    run_id: str | None = None,
) -> MetricsLogger:
    """Create (or replace) the process-wide metrics logger for this run."""
    global _INSTANCE
    logger = MetricsLogger(
        run_id=run_id or new_run_id(),
        subject_id=subject_id,
        metrics_dir=Path(metrics_dir),
        dataset_id=dataset_id,
    )
    with _lock:
        _INSTANCE = logger
    return logger


def get_logger() -> MetricsLogger | None:
    """Return the current run's logger, or None if ``init_run`` was never called."""
    return _INSTANCE


def emit(agent_name: str, event_type: str, **fields: Any) -> dict[str, Any] | None:
    """Convenience wrapper: emit if a run logger exists; otherwise no-op."""
    logger = get_logger()
    if logger is None:
        return None
    return logger.emit(agent_name, event_type, **fields)


def reset() -> None:
    """Clear the process-wide logger (tests / multi-subject batch loops)."""
    global _INSTANCE
    with _lock:
        _INSTANCE = None


def extract_llm_usage(response: Any) -> dict[str, Any]:
    """
    Best-effort token usage from a LangChain / Groq response object.

    Inspectable path for paper metrics: call sites in ``config_agent`` /
    ``diagnostic_agent`` pass the raw LLM response here, then ``emit`` the result.
    """
    usage: dict[str, Any] = {
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
        "model_name": None,
    }
    if response is None:
        return usage

    meta = getattr(response, "response_metadata", None) or {}
    if isinstance(meta, dict):
        usage["model_name"] = meta.get("model_name") or meta.get("model")
        token_usage = meta.get("token_usage") or meta.get("usage") or {}
        if isinstance(token_usage, dict):
            usage["prompt_tokens"] = token_usage.get("prompt_tokens") or token_usage.get(
                "input_tokens"
            )
            usage["completion_tokens"] = token_usage.get("completion_tokens") or token_usage.get(
                "output_tokens"
            )
            usage["total_tokens"] = token_usage.get("total_tokens") or (
                (usage["prompt_tokens"] or 0) + (usage["completion_tokens"] or 0)
                if usage["prompt_tokens"] is not None or usage["completion_tokens"] is not None
                else None
            )

    um = getattr(response, "usage_metadata", None)
    if isinstance(um, dict):
        usage["prompt_tokens"] = usage["prompt_tokens"] or um.get("input_tokens")
        usage["completion_tokens"] = usage["completion_tokens"] or um.get("output_tokens")
        usage["total_tokens"] = usage["total_tokens"] or um.get("total_tokens")

    return usage


def estimate_llm_cost_usd(
    prompt_tokens: int | None,
    completion_tokens: int | None,
    *,
    input_rate_per_m: float,
    output_rate_per_m: float,
) -> float | None:
    """Estimate USD cost from token counts and configured per-million rates."""
    if prompt_tokens is None and completion_tokens is None:
        return None
    pin = int(prompt_tokens or 0)
    cout = int(completion_tokens or 0)
    return (pin / 1_000_000.0) * input_rate_per_m + (cout / 1_000_000.0) * output_rate_per_m
