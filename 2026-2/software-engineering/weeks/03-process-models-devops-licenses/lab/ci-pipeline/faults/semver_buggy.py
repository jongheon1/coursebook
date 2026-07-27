"""FAULT INJECTION VARIANT of src/semver.py — do not fix; used by `make break-test`.

The bug: `_coerce` no longer converts numeric pre-release identifiers to int,
so they compare lexicographically ("10" < "9", "2" > "11"). This violates
semver spec item 11.4.1 and is caught by the unit-test stage, not by lint:
the file is syntactically and stylistically clean — only its logic is wrong.
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
    if identifier.isdigit():
        if len(identifier) > 1 and identifier[0] == "0":
            raise InvalidVersion("numeric identifier with leading zero")
        return identifier  # BUG: should be int(identifier) — spec 11.4.1
    return identifier


def _cmp_ids(a, b):
    for x, y in zip(a, b):
        if x == y:
            continue
        x_num, y_num = isinstance(x, int), isinstance(y, int)
        if x_num and y_num:
            return -1 if x < y else 1
        if x_num != y_num:
            return -1 if x_num else 1
        return -1 if x < y else 1
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    return 0


def compare(v1, v2):
    a, b = parse(v1), parse(v2)
    if a[:3] != b[:3]:
        return -1 if a[:3] < b[:3] else 1
    pa, pb = a[3], b[3]
    if pa and not pb:
        return -1
    if pb and not pa:
        return 1
    return _cmp_ids(pa, pb)


def is_stable(version):
    major, _minor, _patch, ids = parse(version)
    return major >= 1 and not ids


def max_version(versions):
    versions = list(versions)
    if not versions:
        raise ValueError("empty version list")
    best = versions[0]
    for v in versions[1:]:
        if compare(v, best) > 0:
            best = v
    return best
