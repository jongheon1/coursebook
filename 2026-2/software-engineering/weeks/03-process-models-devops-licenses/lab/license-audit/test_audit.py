import unittest

from audit import (
    NETWORK, PERMISSIVE, STRONG, UNKNOWN, WEAK,
    OK, VIOLATION, WARN, FLAG_UNKNOWN,
    classify_expression, classify_id, decide, parse_requirements,
)


class ClassifyIdTest(unittest.TestCase):
    def test_basic_buckets(self):
        self.assertEqual(classify_id("MIT"), PERMISSIVE)
        self.assertEqual(classify_id("Apache-2.0"), PERMISSIVE)
        self.assertEqual(classify_id("LGPL-3.0-only"), WEAK)
        self.assertEqual(classify_id("MPL-2.0"), WEAK)
        self.assertEqual(classify_id("GPL-2.0-only"), STRONG)
        self.assertEqual(classify_id("GPL-3.0-or-later"), STRONG)
        self.assertEqual(classify_id("AGPL-3.0-only"), NETWORK)
        self.assertEqual(classify_id("WTFPL"), UNKNOWN)

    def test_classpath_exception_downgrades_gpl_to_weak(self):
        self.assertEqual(
            classify_id("GPL-2.0-only WITH Classpath-exception-2.0"), WEAK)

    def test_unknown_exception_keeps_base_category(self):
        self.assertEqual(
            classify_id("GPL-3.0-only WITH Mystery-exception-1.0"), STRONG)


class ClassifyExpressionTest(unittest.TestCase):
    def test_or_takes_weakest_branch(self):
        # recipient's choice: pick MIT, ignore the GPL branch
        self.assertEqual(classify_expression("GPL-3.0-only OR MIT"), PERMISSIVE)

    def test_and_takes_strongest_part(self):
        self.assertEqual(classify_expression("MIT AND GPL-3.0-only"), STRONG)

    def test_with_binds_tighter_than_and(self):
        self.assertEqual(
            classify_expression("MIT AND GPL-2.0-only WITH Classpath-exception-2.0"),
            WEAK)

    def test_unknown_propagates(self):
        self.assertEqual(classify_expression("MIT AND WTFPL"), UNKNOWN)
        self.assertEqual(classify_expression("MIT OR WTFPL"), PERMISSIVE)


class DecideTest(unittest.TestCase):
    def test_internal_never_triggers_copyleft(self):
        v, _ = decide(STRONG, "import", False, "internal")
        self.assertEqual(v, OK)

    def test_saas_gpl_import_is_latent_warning(self):
        v, note = decide(STRONG, "import", False, "saas")
        self.assertEqual(v, WARN)
        self.assertIn("latent", note)

    def test_saas_unmodified_agpl_process_ok(self):
        v, _ = decide(NETWORK, "process", False, "saas")
        self.assertEqual(v, OK)

    def test_saas_modified_agpl_violates_s13(self):
        v, note = decide(NETWORK, "process", True, "saas")
        self.assertEqual(v, VIOLATION)
        self.assertIn("s13", note)

    def test_saas_agpl_in_process_conservative_violation(self):
        v, _ = decide(NETWORK, "import", False, "saas")
        self.assertEqual(v, VIOLATION)

    def test_binary_gpl_import_violates(self):
        v, _ = decide(STRONG, "import", False, "binary")
        self.assertEqual(v, VIOLATION)

    def test_binary_gpl_separate_process_is_warn_not_violation(self):
        v, _ = decide(STRONG, "process", False, "binary")
        self.assertEqual(v, WARN)

    def test_binary_lgpl_dynamic_ok_static_warn(self):
        self.assertEqual(decide(WEAK, "dynamic", False, "binary")[0], OK)
        self.assertEqual(decide(WEAK, "static", False, "binary")[0], WARN)

    def test_binary_permissive_ok(self):
        self.assertEqual(decide(PERMISSIVE, "import", False, "binary")[0], OK)

    def test_unknown_always_blocks(self):
        for dist in ("internal", "saas", "binary"):
            self.assertEqual(decide(UNKNOWN, "import", False, dist)[0],
                             FLAG_UNKNOWN)


class ParseRequirementsTest(unittest.TestCase):
    def test_sample_file(self):
        pkgs = parse_requirements("requirements-sample.txt")
        self.assertIn("flask", pkgs)
        self.assertIn("pdfengine", pkgs)
        self.assertEqual(len(pkgs), 7)


if __name__ == "__main__":
    unittest.main()
