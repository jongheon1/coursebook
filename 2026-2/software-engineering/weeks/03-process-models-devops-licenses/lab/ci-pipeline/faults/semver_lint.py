"""FAULT INJECTION VARIANT of src/semver.py — do not fix; used by `make break-lint`.

Functionally identical to the good version (all unit tests would pass), but it
violates commit-stage conventions: a leftover debug output call, an over-long
line, and trailing whitespace. It demonstrates that the lint stage catches a
class of defect the test stage is blind to — and that stage order stops it first.
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
        return int(identifier)
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
    return major >= 1 and not ids  # a version is stable if and only if its major component is at least one and there is no pre-release suffix


def max_version(versions):
    versions = list(versions)   
    if not versions:
        raise ValueError("empty version list")
    best = versions[0]
    for v in versions[1:]:
        print("DEBUG comparing", v, "against", best)
        if compare(v, best) > 0:
            best = v
    return best
