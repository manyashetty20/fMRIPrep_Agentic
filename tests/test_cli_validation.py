"""
tests/test_cli_validation.py
============================
Unit tests for cli_validation.py (CLI flag verification, alias mapping, and hallucination filtering).
"""

from __future__ import annotations

import unittest
from pathlib import Path

from cli_validation import (
    canonical_flag,
    extract_flag_stems,
    load_official_flags,
    tokenize_command,
    unknown_fmriprep_flags,
    validate_flag_list,
)

OFFICIAL_FLAGS_PATH = Path(__file__).resolve().parent.parent / "data" / "fmriprep_cli_flags.txt"


class TestCLIValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.official = load_official_flags(OFFICIAL_FLAGS_PATH)
        assert len(cls.official) > 20, "Official flag list should have loaded"

    def test_tokenization_and_stem_extraction(self):
        cmd = (
            "docker run --rm -v /data:/data:ro \\\n"
            "  nipreps/fmriprep:latest /data /out participant \\\n"
            "  --participant-label 01 --low-mem --mem_mb=4000 -w /out/work"
        )
        tokens = tokenize_command(cmd)
        self.assertIn("--participant-label", tokens)
        self.assertIn("--low-mem", tokens)
        self.assertIn("--mem_mb=4000", tokens)

        stems = extract_flag_stems(cmd)
        self.assertIn("--rm", stems)
        self.assertIn("-v", stems)
        self.assertIn("--participant-label", stems)
        self.assertIn("--low-mem", stems)
        self.assertIn("--mem_mb", stems)
        self.assertIn("-w", stems)

    def test_canonical_flag_aliases(self):
        self.assertEqual(canonical_flag("--session-id"), "--session-label")
        self.assertEqual(canonical_flag("--mem-mb"), "--mem_mb")
        self.assertEqual(
            canonical_flag("--fallback-totalreadout-time"),
            "--fallback-total-readout-time",
        )
        self.assertEqual(canonical_flag("--low-mem"), "--low-mem")

    def test_unknown_flags_detection(self):
        valid_cmd = (
            "docker run --rm -v /data:/data:ro nipreps/fmriprep:latest "
            "/data /out participant --participant-label 01 --use-syn-sdc --fs-no-reconall"
        )
        unknown = unknown_fmriprep_flags(valid_cmd, self.official)
        self.assertEqual(unknown, [])

        hallucinated_cmd = (
            "docker run --rm -v /data:/data:ro nipreps/fmriprep:latest "
            "/data /out participant --session-id retest --fs-license-file /lic.txt --fake-flag"
        )
        unknown = unknown_fmriprep_flags(hallucinated_cmd, self.official)
        self.assertIn("--session-id", unknown)
        self.assertIn("--fake-flag", unknown)

    def test_validate_flag_list(self):
        proposed = ["--participant-label 01", "--session-id 01", "--bogus-flag", "--low-mem"]
        res = validate_flag_list(proposed, self.official)
        self.assertIn("--participant-label", res["valid"])
        self.assertIn("--low-mem", res["valid"])
        # --session-id is aliased to --session-label which is official, so it is valid via alias
        self.assertIn("--session-id", [a["proposed"] for a in res["aliased"]])
        self.assertIn("--bogus-flag", res["hallucinated"])
        self.assertAlmostEqual(res["valid_rate"], 3 / 4)


if __name__ == "__main__":
    unittest.main()
