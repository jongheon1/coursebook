"""Minimal Semantic Versioning 2.0.0 parser and comparator.

Implements the precedence rules of https://semver.org/ (spec item 11):
- compare major, minor, patch numerically
- a pre-release version has lower precedence than the normal version
- pre-release identifiers: numeric ones compare numerically, alphanumeric
  ones lexically; numeric < alphanumeric; more identifiers > fewer (when
  all preceding identifiers are equal)
- build metadata (after '+') is ignored for precedence
"""

import re

_SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)"
    r"\.(?P<minor>0|[1-9]\d*)"
    r"\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>[0-9A-Za-z.-]+))?"
    r"(?:\+(?P<build>[0-9A-Za-z.-]+))?$"
)


class InvalidVersion(ValueError):
    pass


def parse(version):
    """Parse a version string into (major, minor, patch, prerelease_ids).

    prerelease_ids is a tuple of str/int identifiers ('' pre-release -> ()).
    Raises InvalidVersion on malformed input.
    """
    m = _SEMVER_RE.match(version)
    if m is None:
        raise InvalidVersion("not a semver string: %r" % (version,))
    major = int(m.group("major"))
    minor = int(m.group("minor"))
    patch = int(m.group("patch"))
    pre = m.group("prerelease")
    ids = tuple(_coerce(i) for i in pre.split(".")) if pre else ()
    return (major, minor, patch, ids)


def _coerce(identifier):
    """Numeric identifiers are compared numerically (spec 11.4.1)."""
    if identifier.isdigit():
        if len(identifier) > 1 and identifier[0] == "0":
            raise InvalidVersion("numeric identifier with leading zero")
        return int(identifier)
    return identifier


def _cmp_ids(a, b):
    for x, y in zip(a, b):
        if x == y:
            continue
        x_num, y_num = isinstance(x, int), isinstance(y, int)
        if x_num and y_num:
            return -1 if x < y else 1
        if x_num != y_num:  # numeric identifiers sort before alphanumeric
            return -1 if x_num else 1
        return -1 if x < y else 1
    if len(a) != len(b):  # larger set of fields has higher precedence
        return -1 if len(a) < len(b) else 1
    return 0


def compare(v1, v2):
    """Return -1, 0, or 1 as v1 <, ==, > v2 by semver precedence."""
    a, b = parse(v1), parse(v2)
    if a[:3] != b[:3]:
        return -1 if a[:3] < b[:3] else 1
    pa, pb = a[3], b[3]
    if pa and not pb:  # pre-release < release
        return -1
    if pb and not pa:
        return 1
    return _cmp_ids(pa, pb)


def is_stable(version):
    """A version is stable iff major >= 1 and it has no pre-release part."""
    major, _minor, _patch, ids = parse(version)
    return major >= 1 and not ids


def max_version(versions):
    """Return the highest-precedence version in a non-empty iterable."""
    versions = list(versions)
    if not versions:
        raise ValueError("empty version list")
    best = versions[0]
    for v in versions[1:]:
        if compare(v, best) > 0:
            best = v
    return best
