"""
tests/test_wilson.py
====================
Unit tests for wilson.py (Wilson 95% binomial confidence intervals).
"""

from __future__ import annotations

import unittest
from wilson import wilson_interval, format_rate_ci, WilsonCI


class TestWilsonInterval(unittest.TestCase):
    def test_zero_sample_size(self):
        """When n=0, rate and bounds must be None."""
        ci = wilson_interval(0, 0)
        self.assertEqual(ci.n, 0)
        self.assertEqual(ci.k, 0)
        self.assertIsNone(ci.rate)
        self.assertIsNone(ci.low)
        self.assertIsNone(ci.high)
        self.assertIn("undefined", format_rate_ci(ci))

    def test_negative_sample_size(self):
        ci = wilson_interval(0, -5)
        self.assertIsNone(ci.rate)
        self.assertIsNone(ci.low)
        self.assertIsNone(ci.high)

    def test_fifty_percent_rate(self):
        """For k=5, n=10, rate is 0.50, interval is symmetric around center."""
        ci = wilson_interval(5, 10)
        self.assertAlmostEqual(ci.rate, 0.5, places=4)
        self.assertTrue(0.0 <= ci.low < 0.5 < ci.high <= 1.0)
        # Wilson interval for 5/10 with z=1.96 is approx [0.2366, 0.7634]
        self.assertAlmostEqual(ci.low, 0.2366, places=3)
        self.assertAlmostEqual(ci.high, 0.7634, places=3)

    def test_zero_successes_clipped(self):
        """For k=0, n=20, low bound must be non-negative (clipped to 0.0)."""
        ci = wilson_interval(0, 20)
        self.assertEqual(ci.rate, 0.0)
        self.assertGreaterEqual(ci.low, 0.0)
        self.assertAlmostEqual(ci.low, 0.0, places=4)
        self.assertGreater(ci.high, 0.0)
        self.assertLessEqual(ci.high, 1.0)

    def test_perfect_success_rate_clipped(self):
        """For k=20, n=20, high bound must be <= 1.0 (clipped to 1.0)."""
        ci = wilson_interval(20, 20)
        self.assertEqual(ci.rate, 1.0)
        self.assertGreater(ci.low, 0.0)
        self.assertLessEqual(ci.high, 1.0)
        self.assertAlmostEqual(ci.high, 1.0, places=4)

    def test_as_dict(self):
        ci = wilson_interval(7, 10)
        d = ci.as_dict()
        self.assertEqual(d["n"], 10)
        self.assertEqual(d["k"], 7)
        self.assertAlmostEqual(d["rate"], 0.7)
        self.assertIn("wilson_low", d)
        self.assertIn("wilson_high", d)


if __name__ == "__main__":
    unittest.main()
