"""
Backup and restore original Docker command and mutated BIDS sidecar JSON files.

Hashes are SHA-256 of file bytes. Restore is rejected if the backup manifest
does not match the recorded hashes (tamper / incomplete backup).
"""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def backup_dir_for(output_dir: Path) -> Path:
    return Path(output_dir) / "agentic_results" / ".rollback"


def write_command_backup(output_dir: Path, command: str) -> Path:
    root = backup_dir_for(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    path = root / "original_command.txt"
    if not path.exists():
        path.write_text(command)
        (root / "original_command.sha256").write_text(sha256_text(command) + "\n")
    return path


def backup_sidecar(output_dir: Path, sidecar: Path) -> dict[str, Any]:
    """Copy sidecar to the rollback store before mutation. Idempotent per path."""
    sidecar = Path(sidecar)
    root = backup_dir_for(output_dir)
    sidecars_root = root / "sidecars"
    sidecars_root.mkdir(parents=True, exist_ok=True)
    digest = sha256_file(sidecar) if sidecar.exists() else ""
    rel_name = sidecar.name + "." + (digest[:12] if digest else "missing")
    dest = sidecars_root / rel_name
    if sidecar.exists() and not dest.exists():
        shutil.copy2(sidecar, dest)
    record = {
        "original_path": str(sidecar.resolve()),
        "backup_path": str(dest.resolve()) if dest.exists() else "",
        "sha256_before": digest,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path = root / "sidecar_manifest.jsonl"
    with manifest_path.open("a") as f:
        f.write(json.dumps(record) + "\n")
    return record


def load_manifest(output_dir: Path) -> list[dict[str, Any]]:
    path = backup_dir_for(output_dir) / "sidecar_manifest.jsonl"
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def restore(output_dir: Path) -> dict[str, Any]:
    """
    Restore original command file (informational) and every backed-up sidecar.

    Returns a report with per-file hash verification.
    """
    root = backup_dir_for(output_dir)
    report: dict[str, Any] = {"ok": True, "restored": [], "errors": []}
    cmd_path = root / "original_command.txt"
    hash_path = root / "original_command.sha256"
    if cmd_path.exists() and hash_path.exists():
        expected = hash_path.read_text().strip()
        actual = sha256_text(cmd_path.read_text())
        if actual != expected:
            report["ok"] = False
            report["errors"].append(
                {"file": str(cmd_path), "error": "command hash mismatch", "expected": expected, "actual": actual}
            )
        else:
            report["command_hash_verified"] = True
            report["original_command"] = cmd_path.read_text()

    seen: set[str] = set()
    for record in reversed(load_manifest(output_dir)):
        orig = record.get("original_path", "")
        if orig in seen:
            continue
        seen.add(orig)
        backup = Path(record.get("backup_path", ""))
        dest = Path(orig)
        expected = record.get("sha256_before", "")
        if not backup.is_file():
            report["ok"] = False
            report["errors"].append({"file": orig, "error": "backup missing"})
            continue
        actual = sha256_file(backup)
        if expected and actual != expected:
            report["ok"] = False
            report["errors"].append(
                {"file": orig, "error": "backup hash mismatch", "expected": expected, "actual": actual}
            )
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup, dest)
        after = sha256_file(dest)
        verified = after == actual
        if not verified:
            report["ok"] = False
        report["restored"].append(
            {"path": orig, "sha256": after, "hash_verified": verified}
        )
    return report


def main() -> None:
    import argparse
    import json as json_lib
    import sys

    p = argparse.ArgumentParser(description="Restore BIDS sidecars from an agentic rollback store.")
    p.add_argument("output_dir", type=Path, help="Pipeline output directory containing agentic_results/.rollback")
    args = p.parse_args()
    report = restore(args.output_dir)
    print(json_lib.dumps(report, indent=2))
    sys.exit(0 if report.get("ok") else 1)


if __name__ == "__main__":
    main()
