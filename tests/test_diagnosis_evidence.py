"""
tests/test_diagnosis_evidence.py
================================
Unit tests for diagnosis_evidence.py (benign warning filtering and hard evidence extraction).
"""

from __future__ import annotations

import unittest

from diagnosis_evidence import (
    evidence_pass,
    strip_benign_warnings,
)


class TestDiagnosisEvidence(unittest.TestCase):
    def test_strip_benign_warnings(self):
        log = (
            "WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested\n"
            "You are using fMRIPrep-25.2.3, and a newer version of fMRIPrep is available: 25.2.5.\n"
            "CRITICAL: Real error occurred here.\n"
            "experimental features notice: do not use in production."
        )
        cleaned = strip_benign_warnings(log)
        self.assertNotIn("image's platform", cleaned)
        self.assertNotIn("experimental features", cleaned)
        self.assertIn("CRITICAL: Real error occurred here.", cleaned)
        self.assertIn("fMRIPrep-25.2.3", cleaned)

    def test_extract_oom_evidence(self):
        # Case 1: exit code 137
        res1 = evidence_pass("Process crashed with exit code 137 after 5 minutes.")
        self.assertEqual(res1.get("primary"), "oom")
        self.assertTrue(res1.get("exit_137"))

        # Case 2: Out of memory killer
        res2 = evidence_pass("Kernel: Out of memory: Kill process 1234 (fmriprep).")
        self.assertEqual(res2.get("primary"), "oom")

        # Case 3: Subprocess Killed with short runtime
        res3 = evidence_pass("makeIsotropic WARNING: not different enough!\nKilled\nSome error", runtime_seconds=20)
        self.assertEqual(res3.get("primary"), "oom")

    def test_extract_license_evidence(self):
        res = evidence_pass("ERROR: a valid license file is required to run FreeSurfer.")
        self.assertEqual(res.get("primary"), "missing_fs_license")

    def test_extract_syn_ped_evidence(self):
        res = evidence_pass(
            "ValueError: Fieldmap-less (SyN) estimation was requested, but PhaseEncodingDirection information appears to be absent."
        )
        self.assertEqual(res.get("primary"), "missing_phase_encoding")

    def test_extract_readout_evidence(self):
        res = evidence_pass("Exception: Unknown total-readout time specification for bold data.")
        self.assertEqual(res.get("primary"), "missing_total_readout_time")

    def test_extract_tty_evidence(self):
        res = evidence_pass("the input device is not a TTY")
        self.assertEqual(res.get("primary"), "tty")

    def test_benign_stripped_flag(self):
        raw_log = (
            "WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8)\n"
            "Normal processing line\n"
            "ValueError: Fieldmap-less (SyN) estimation was requested, but PhaseEncodingDirection information appears to be absent.\n"
        )
        res = evidence_pass(raw_log)
        self.assertTrue(res["benign_stripped"])
        self.assertNotIn("image's platform", res["filtered_log"])
        self.assertEqual(res["primary"], "missing_phase_encoding")


if __name__ == "__main__":
    unittest.main()
