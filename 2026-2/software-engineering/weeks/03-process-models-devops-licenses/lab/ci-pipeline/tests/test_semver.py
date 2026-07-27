import unittest

from src.semver import InvalidVersion, compare, is_stable, max_version, parse


class ParseTest(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(parse("1.2.3"), (1, 2, 3, ()))

    def test_prerelease_and_build(self):
        self.assertEqual(parse("1.0.0-alpha.1+build.5"), (1, 0, 0, ("alpha", 1)))

    def test_build_only(self):
        self.assertEqual(parse("2.0.0+exp.sha.5114f85"), (2, 0, 0, ()))

    def test_rejects_garbage(self):
        for bad in ("1.2", "v1.2.3", "1.02.3", "1.2.3-01", ""):
            with self.assertRaises(InvalidVersion, msg=bad):
                parse(bad)


class CompareTest(unittest.TestCase):
    def test_core_numeric_order(self):
        # numeric, not lexicographic: 1.10.0 > 1.9.0
        self.assertEqual(compare("1.10.0", "1.9.0"), 1)

    def test_prerelease_lower_than_release(self):
        self.assertEqual(compare("1.0.0-alpha", "1.0.0"), -1)

    def test_prerelease_numeric_order(self):
        # spec 11.4.1: numeric identifiers compare numerically -> 10 > 9
        self.assertEqual(compare("1.0.0-alpha.10", "1.0.0-alpha.9"), 1)

    def test_numeric_before_alphanumeric(self):
        # spec 11.4.3: numeric identifiers sort before alphanumeric
        self.assertEqual(compare("1.0.0-1", "1.0.0-alpha"), -1)

    def test_more_ids_higher(self):
        self.assertEqual(compare("1.0.0-alpha.1", "1.0.0-alpha"), 1)

    def test_build_metadata_ignored(self):
        self.assertEqual(compare("1.0.0+a", "1.0.0+b"), 0)

    def test_spec_example_chain(self):
        chain = [
            "1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta",
            "1.0.0-beta", "1.0.0-beta.2", "1.0.0-beta.11",
            "1.0.0-rc.1", "1.0.0",
        ]
        for lo, hi in zip(chain, chain[1:]):
            self.assertEqual(compare(lo, hi), -1, "%s < %s" % (lo, hi))


class HelperTest(unittest.TestCase):
    def test_is_stable(self):
        self.assertTrue(is_stable("1.0.0"))
        self.assertFalse(is_stable("0.9.9"))
        self.assertFalse(is_stable("1.0.0-rc.1"))

    def test_max_version(self):
        self.assertEqual(
            max_version(["1.0.0-rc.1", "0.9.0", "1.0.0", "1.0.0-beta.11"]),
            "1.0.0",
        )

    def test_max_version_empty(self):
        with self.assertRaises(ValueError):
            max_version([])


if __name__ == "__main__":
    unittest.main()
