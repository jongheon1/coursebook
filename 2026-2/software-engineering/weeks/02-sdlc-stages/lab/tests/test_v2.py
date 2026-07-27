"""Spec tests for SRS-lite v2.0 (after CR-1) — run against BOTH implementations.

CR-1: FR-7 memberships added; FR-3' surcharge base corrected.
Run: python3 tests/test_v2.py  (from the lab/ directory)
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "v2"))

import fare_modular  # noqa: E402
import fare_tangled  # noqa: E402

IMPLS = [("tangled", fare_tangled), ("modular", fare_modular)]


def receipt_total(receipt_text):
    return int(receipt_text.splitlines()[-1].split()[-1])


def receipt_item_amounts(receipt_text):
    lines = receipt_text.splitlines()
    return [int(line.split()[-1]) for line in lines[:-2]]  # drop separator + TOTAL


class TestV2Spec(unittest.TestCase):
    def test_fr2_unchanged_day_none(self):
        """Unchanged behavior: 600s @ 14h, NONE -> 2800."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                self.assertEqual(impl.quote(600, 14)[0], 2800)

    def test_fr3p_night_surcharge_on_time_charge_only(self):
        """FR-3': 600s @ 3h, NONE -> 1000 + 1800 + 360 = 3160 (was 3360 in v1)."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                total, receipt = impl.quote(600, 3)
                self.assertEqual(total, 3160)
                self.assertIn("night +20%", receipt)

    def test_fr7_basic_discount(self):
        """FR-7: 610s @ 14h, BASIC -> 1000 + 1980 - 198 = 2782 -> 2780."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                total, receipt = impl.quote(610, 14, membership="BASIC")
                self.assertEqual(total, 2780)
                self.assertIn("basic -10%", receipt)
                self.assertIn("-198", receipt)

    def test_fr7_plus_waives_unlock_and_discounts(self):
        """FR-7 + FR-3': 610s @ 3h, PLUS -> (1980-594) + 277 = 1663 -> 1660."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                total, receipt = impl.quote(610, 3, membership="PLUS")
                self.assertEqual(total, 1660)
                self.assertIn("plus -30%", receipt)
                self.assertNotIn("unlock", receipt)

    def test_fr4_floor_to_ten(self):
        """FR-4: 70s @ 3h, NONE -> 1000 + 360 + 72 = 1432 -> 1430."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                self.assertEqual(impl.quote(70, 3)[0], 1430)

    def test_fr5_fr7_validation(self):
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                for args, kwargs in [
                    ((0, 14), {}),
                    ((600, 24), {}),
                    ((600, 14), {"membership": "GOLD"}),
                ]:
                    with self.assertRaises(ValueError):
                        impl.quote(*args, **kwargs)

    def test_fr6_receipt_consistency(self):
        """FR-6: floor10(sum of item lines) == TOTAL line, for every membership."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                for m in ("NONE", "BASIC", "PLUS"):
                    for args in [(600, 14), (61, 14), (610, 3), (70, 3)]:
                        total, receipt = impl.quote(*args, membership=m)
                        items_sum = sum(receipt_item_amounts(receipt))
                        self.assertEqual(items_sum - items_sum % 10, receipt_total(receipt))
                        self.assertEqual(total, receipt_total(receipt))

    def test_ops_report_agrees_with_quote(self):
        """total_fare() must agree with quote() — catches a stale duplicate."""
        for name, impl in IMPLS:
            with self.subTest(impl=name):
                for m in ("NONE", "BASIC", "PLUS"):
                    for args in [(600, 14), (61, 14), (610, 3), (70, 3), (3600, 0)]:
                        self.assertEqual(
                            impl.total_fare(*args, membership=m),
                            impl.quote(*args, membership=m)[0],
                        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
