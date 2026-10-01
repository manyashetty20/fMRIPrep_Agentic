"""
tests/test_sidecar_rollback.py
==============================
Unit tests for sidecar_rollback.py (cryptographic SHA-256 backup and restore).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sidecar_rollback import (
    backup_sidecar,
    restore,
    sha256_file,
    sha256_text,
    write_command_backup,
)


class TestSidecarRollback(unittest.TestCase):
    def test_sha256_helpers(self):
        text = "test-string-12345"
        digest = sha256_text(text)
        self.assertEqual(len(digest), 64)

        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            tf.write(text)
            tf.flush()
            f_path = Path(tf.name)
        try:
            self.assertEqual(sha256_file(f_path), digest)
        finally:
            f_path.unlink()

    def test_command_backup_and_verify(self):
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "outputs"
            cmd = "docker run --rm nipreps/fmriprep:latest /data /out participant"
            write_command_backup(out_dir, cmd)

            report = restore(out_dir)
            self.assertTrue(report.get("ok"))
            self.assertTrue(report.get("command_hash_verified"))
            self.assertEqual(report.get("original_command"), cmd)

    def test_command_tamper_rejection(self):
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "outputs"
            cmd = "docker run --rm nipreps/fmriprep:latest /data /out participant"
            write_command_backup(out_dir, cmd)

            # Tamper with the saved command text
            cmd_file = out_dir / "agentic_results" / ".rollback" / "original_command.txt"
            cmd_file.write_text("docker run --tampered-flag /data /out")

            report = restore(out_dir)
            self.assertFalse(report.get("ok"))
            self.assertTrue(any("command hash mismatch" in str(e) for e in report.get("errors", [])))

    def test_sidecar_roundtrip_restore(self):
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "outputs"
            bids_dir = Path(td) / "bids"
            bids_dir.mkdir(parents=True)
            sidecar = bids_dir / "sub-01_task-rest_bold.json"
            original_content = '{\n  "RepetitionTime": 2.0,\n  "TaskName": "rest"\n}'
            sidecar.write_text(original_content)

            # 1. Backup
            rec = backup_sidecar(out_dir, sidecar)
            self.assertEqual(rec["original_path"], str(sidecar.resolve()))
            self.assertEqual(rec["sha256_before"], sha256_text(original_content))

            # 2. Mutate
            mutated_content = '{\n  "RepetitionTime": 2.5,\n  "Mutated": true\n}'
            sidecar.write_text(mutated_content)
            self.assertEqual(sidecar.read_text(), mutated_content)

            # 3. Restore
            report = restore(out_dir)
            self.assertTrue(report.get("ok"))
            self.assertEqual(len(report.get("restored", [])), 1)
            self.assertTrue(report["restored"][0]["hash_verified"])
            self.assertEqual(sidecar.read_text(), original_content)

    def test_sidecar_tamper_rejection(self):
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "outputs"
            bids_dir = Path(td) / "bids"
            bids_dir.mkdir(parents=True)
            sidecar = bids_dir / "sub-01_task-rest_bold.json"
            sidecar.write_text('{"RepetitionTime": 2.0}')

            rec = backup_sidecar(out_dir, sidecar)
            backup_file = Path(rec["backup_path"])
            self.assertTrue(backup_file.exists())

            # Corrupt the backup file
            backup_file.write_text('{"Corrupted": true}')

            report = restore(out_dir)
            self.assertFalse(report.get("ok"))
            self.assertTrue(any("backup hash mismatch" in str(e) for e in report.get("errors", [])))


if __name__ == "__main__":
    unittest.main()
