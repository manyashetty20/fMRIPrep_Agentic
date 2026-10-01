"""
tests/test_qa_verdict.py
========================
Tests verifying QA verdict determinism and regression fixes for:
- Runs 7 vs 8 (identical inputs must produce identical PASS verdicts)
- Run 3 (no voxel metrics -> WARN with voxel_metrics_unavailable)
- Run 1 (missing brain mask -> WARN with brain_mask_missing, no false 100% retention)
- Rule-based degradation qualifier
"""

from __future__ import annotations

import unittest
from qa_verdict import decide_qa_verdict, verdict_from_metrics


class TestQAVerdictDeterminism(unittest.TestCase):
    def test_determinism_identical_calls(self):
        """Verify identical inputs produce strictly identical verdicts across 20 iterations."""
        kwargs = dict(
            output_found=True,
            report_found=True,
            mni_found=True,
            brain_mask_found=True,
            retention_ratio=0.0906,
            skull_strip_reduction=0.9094,
            min_retention=0.05,
            max_retention=0.25,
            min_reduction=0.75,
            max_reduction=0.95,
            voxel_metrics_available=True,
            repair_impacts=[],
        )
        base = decide_qa_verdict(**kwargs)
        self.assertEqual(base["summary"], "PASS")
        self.assertEqual(base["qualifier"], "CLEAN")
        self.assertEqual(base["reasons"], [])

        for _ in range(20):
            res = decide_qa_verdict(**kwargs)
            self.assertEqual(res["summary"], base["summary"])
            self.assertEqual(res["qualifier"], base["qualifier"])
            self.assertEqual(res["reasons"], base["reasons"])
            self.assertEqual(res["qa_warn_count"], base["qa_warn_count"])
            self.assertEqual(res["qa_fail_count"], base["qa_fail_count"])

    def test_runs_7_vs_8_consistency(self):
        """Runs 7 and 8 have identical voxel ratios (9.06% retention, 90.94% reduction).
        Both must evaluate to PASS with zero warnings under pure deterministic logic.
        """
        metrics_run7 = {
            "output_found": True,
            "report_found": True,
            "mni_found": True,
            "brain_mask_found": True,
            "raw_nonzero_voxels": 5308353,
            "preprocessed_nonzero_voxels": 10194543,
            "brain_mask_nonzero_voxels": 923998,
            "brain_mask_retention_ratio": 0.0906365297591074,
            "skull_strip_reduction": 0.9093634702408926,
            "qa_thresholds": {
                "min_brain_mask_retention_ratio": 0.05,
                "max_brain_mask_retention_ratio": 0.25,
                "min_skull_strip_reduction": 0.75,
                "max_skull_strip_reduction": 0.95,
            },
        }
        metrics_run8 = dict(metrics_run7)

        v7 = verdict_from_metrics(metrics_run7)
        v8 = verdict_from_metrics(metrics_run8)

        self.assertEqual(v7["summary"], "PASS")
        self.assertEqual(v8["summary"], "PASS")
        self.assertEqual(v7["summary"], v8["summary"])
        self.assertEqual(v7["reasons"], v8["reasons"])
        self.assertEqual(v7["reasons"], [])

    def test_run_3_no_voxel_metrics(self):
        """Run 3 had derivatives present but no voxel metrics computed.
        Must evaluate to WARN with voxel_metrics_unavailable logged in qa_reasons.
        """
        metrics_run3 = {
            "output_found": True,
            "report_found": True,
            "mni_found": True,
            "brain_mask_found": True,
            "raw_nonzero_voxels": None,
            "preprocessed_nonzero_voxels": None,
            "brain_mask_nonzero_voxels": None,
            "brain_mask_retention_ratio": None,
            "skull_strip_reduction": None,
        }
        v3 = verdict_from_metrics(metrics_run3)
        self.assertEqual(v3["summary"], "WARN")
        self.assertIn("voxel_metrics_unavailable", v3["reasons"])

    def test_run_1_missing_brain_mask(self):
        """Run 1 had missing brain mask (brain_mask_found=False).
        Must evaluate to WARN with brain_mask_missing logged in qa_reasons.
        Retention/reduction proxies must not be treated as 100% / 0%.
        """
        metrics_run1 = {
            "output_found": True,
            "report_found": False,
            "mni_found": True,
            "brain_mask_found": False,
            "raw_nonzero_voxels": 262144,
            "preprocessed_nonzero_voxels": 262144,
            "brain_mask_nonzero_voxels": None,
            "brain_mask_retention_ratio": 1.0,
            "skull_strip_reduction": 0.0,
        }
        v1 = verdict_from_metrics(metrics_run1)
        self.assertEqual(v1["summary"], "WARN")
        self.assertIn("brain_mask_missing", v1["reasons"])
        self.assertIn("html_report_missing", v1["reasons"])
        self.assertNotIn("retention_out_of_band", v1["reasons"])

    def test_degraded_qualifier_on_repair_impact(self):
        """When repair impacts are provided, verdict qualifier must be DEGRADED and recorded in reasons."""
        res = decide_qa_verdict(
            output_found=True,
            report_found=True,
            mni_found=True,
            brain_mask_found=True,
            retention_ratio=0.10,
            skull_strip_reduction=0.90,
            min_retention=0.05,
            max_retention=0.25,
            min_reduction=0.75,
            max_reduction=0.95,
            repair_impacts=["SDC dropped"],
        )
        self.assertEqual(res["summary"], "PASS")
        self.assertEqual(res["qualifier"], "DEGRADED: SDC dropped")
        self.assertIn("repair_degraded_outputs", res["reasons"])
        self.assertEqual(res["display"], "PASS (DEGRADED: SDC dropped)")

    def test_out_of_band_causes_fail(self):
        """Extreme retention (>25%) or reduction (<75%) must trigger FAIL."""
        res = decide_qa_verdict(
            output_found=True,
            report_found=True,
            mni_found=True,
            brain_mask_found=True,
            retention_ratio=0.40,
            skull_strip_reduction=0.60,
            min_retention=0.05,
            max_retention=0.25,
            min_reduction=0.75,
            max_reduction=0.95,
        )
        self.assertEqual(res["summary"], "FAIL")
        self.assertIn("retention_out_of_band", res["reasons"])
        self.assertIn("reduction_out_of_band", res["reasons"])


if __name__ == "__main__":
    unittest.main()
