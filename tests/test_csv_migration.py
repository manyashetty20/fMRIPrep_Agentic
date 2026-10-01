"""
tests/test_csv_migration.py
===========================
Tests verifying the canonical CSV migration, schema consistency,
field count uniformity, and retention ratio recomputation.
"""

from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from evaluation_export import EVALUATION_FIELDNAMES, append_evaluation_exports

CSV_PATH = Path(__file__).resolve().parent.parent / "output" / "evaluation" / "run_evaluation.csv"
LEGACY_CSV_PATH = Path(__file__).resolve().parent.parent / "output" / "evaluation" / "run_evaluation.legacy.csv"
JSONL_PATH = Path(__file__).resolve().parent.parent / "output" / "evaluation" / "run_evaluation.jsonl"


class TestCSVMigration(unittest.TestCase):
    def test_legacy_backup_exists(self):
        self.assertTrue(LEGACY_CSV_PATH.exists(), "Legacy backup CSV must be preserved")
        with open(LEGACY_CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(len(header), 29, "Legacy header had 29 columns")

    def test_migrated_csv_field_uniformity(self):
        """Every single row in run_evaluation.csv must have exactly len(header) fields."""
        self.assertTrue(CSV_PATH.exists())
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(header, EVALUATION_FIELDNAMES)
            header_len = len(header)

            row_count = 0
            for idx, row in enumerate(reader, 1):
                row_count += 1
                self.assertEqual(
                    len(row),
                    header_len,
                    f"Row {idx} has {len(row)} fields, expected {header_len}",
                )
            self.assertGreaterEqual(row_count, 32, "Must contain all historical rows")

    def test_run_class_partition(self):
        """MOCK rows must be strictly identified; REAL_DOCKER must be classified."""
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        mock_rows = [r for r in rows if r["run_class"] == "MOCK"]
        real_rows = [r for r in rows if r["run_class"] == "REAL_DOCKER"]

        self.assertEqual(len(mock_rows), 5, "Exactly 5 rows must be classified as MOCK")
        self.assertGreaterEqual(len(real_rows), 27)

        # Verify all mocks have 262,144 raw voxels
        for m in mock_rows:
            self.assertEqual(m["raw_nonzero_voxels"], "262144")

    def test_retention_ratio_eq1(self):
        """Retention ratio must equal mask / preprocessed for all valid rows."""
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                mask_str = r.get("brain_mask_nonzero_voxels")
                proc_str = r.get("preprocessed_nonzero_voxels")
                ret_str = r.get("brain_mask_retention_ratio")
                if mask_str and proc_str and float(proc_str) > 0:
                    expected = float(mask_str) / float(proc_str)
                    actual = float(ret_str)
                    self.assertAlmostEqual(actual, expected, places=5)

    def test_legacy_retention_provenance(self):
        """Rows 4, 5, 6 must flag the denominator change at commit c3e0b3ca."""
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Rows 4, 5, 6 in 0-indexing are rows[3], rows[4], rows[5]
        for idx in [3, 4, 5]:
            r = rows[idx]
            self.assertIn("denominator changed at commit c3e0b3ca", r["label_note"])
            self.assertTrue(r["legacy_retention_ratio"])

    def test_dynamic_header_expansion_preserves_length(self):
        """Adding a row with an extra column rewrites the CSV without dropping old rows."""
        with tempfile.TemporaryDirectory() as td:
            eval_root = Path(td)
            # Add initial row
            row1 = {"run_mode": "agentic", "dataset_id": "ds01", "participant": "sub-01"}
            append_evaluation_exports(row1, eval_root=eval_root)

            # Add row with a novel column
            row2 = {"run_mode": "agentic", "dataset_id": "ds01", "new_future_col": "val123"}
            append_evaluation_exports(row2, eval_root=eval_root)

            csv_file = eval_root / "evaluation" / "run_evaluation.csv"
            with csv_file.open("r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader)
                self.assertIn("new_future_col", header)
                for r in reader:
                    self.assertEqual(len(r), len(header))


if __name__ == "__main__":
    unittest.main()
