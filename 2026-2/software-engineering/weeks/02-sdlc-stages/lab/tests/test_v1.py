"""Spec tests for SRS-lite v1.0 — run against BOTH implementations.

Test-first: these encode the SRS (srs-lite.md), not any implementation.
Run: python3 tests/test_v1.py  (from the lab/ directory)
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "v1"))

import fare_modular  # noqa: E402
import fare_tangled  # noqa: E402

IMPLS = [("tangled", fare_tangled), ("modular", fare_modular)]


def receipt_total(receipt_text):
    return int(receipt_text.splitlines()[-1].split()[-1])


def receipt_item_amounts(receipt_text):
    lines = receipt_text.splitlines()
    return [int(line.split()[-1]) for line in lines[:-2]]  # drop separator + TOTAL


class TestV1Spec(unittest.TestCase):
    def test_fr1_fr2_base_fare_day(self):
        """FR-1/FR-2: 600s @ 14h -> 1000 + 10*180 = 2800."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                self.assertEqual(impl.quote(600, 14)[0], 2800)

    def test_fr1_minutes_round_up(self):
        """FR-1: 61s counts as 2 minutes -> 1000 + 360 = 1360."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                self.assertEqual(impl.quote(61, 14)[0], 1360)

    def test_fr3_night_surcharge_on_total(self):
        """FR-3 (v1): 20% on the whole fare. 2800 * 1.2 = 3360."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                total, receipt = impl.quote(600, 3)
                self.assertEqual(total, 3360)
                self.assertIn("night +20%", receipt)

    def test_fr4_floor_to_ten(self):
        """FR-4: 70s @ 3h -> base 1360, surcharge 272, 1632 -> 1630."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                self.assertEqual(impl.quote(70, 3)[0], 1630)

    def test_fr5_validation(self):
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                for args in [(0, 14), (-5, 3), (600, 24), (600, -1)]:
                    with self.assertRaises(ValueError):
                        impl.quote(*args)

    def test_fr6_receipt_consistency(self):
        """FR-6: floor10(sum of item lines) == TOTAL line."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                for args in [(600, 14), (61, 14), (600, 3), (70, 3)]:
                    total, receipt = impl.quote(*args)
                    items_sum = sum(receipt_item_amounts(receipt))
                    self.assertEqual(items_sum - items_sum % 10, receipt_total(receipt))
                    self.assertEqual(total, receipt_total(receipt))

    def test_ops_report_agrees_with_quote(self):
        """total_fare() (ops report API) must agree with quote()."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                for args in [(600, 14), (61, 14), (600, 3), (70, 3), (3600, 0)]:
                    self.assertEqual(impl.total_fare(*args), impl.quote(*args)[0])

    def test_nfr2_deterministic(self):
        """NFR-2: same input, same output."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                self.assertEqual(impl.quote(600, 3), impl.quote(600, 3))


if __name__ == "__main__":
    unittest.main(verbosity=2)
