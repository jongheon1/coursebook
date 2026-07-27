#!/usr/bin/env python3
"""Tiny stand-in for a real linter (flake8/ruff), dependency-free.

Commit-stage checks, in the spirit of "fast, code-local, fixable by the
committer": syntax, line length, tab indentation, trailing whitespace,
and leftover debug print() calls in library code.

Usage: python3 tools/lint.py <dir> [<dir> ...]
Exit code: 0 = clean, 1 = findings (the build must fail).
"""

import pathlib
import re
import sys

MAX_LINE = 100
DEBUG_CALL = re.compile(r"(^|[^.\w])print\(")


def lint_file(path):
    findings = []
    text = path.read_text(encoding="utf-8")
    try:
        compile(text, str(path), "exec")
    except SyntaxError as e:
        findings.append((e.lineno or 0, "E9 syntax error: %s" % e.msg))
        return findings  # nothing else is meaningful past a syntax error
    for no, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_LINE:
            findings.append((no, "E501 line too long (%d > %d)" % (len(line), MAX_LINE)))
        if line[: len(line) - len(line.lstrip())].count("\t"):
            findings.append((no, "W191 tab in indentation"))
        if line != line.rstrip():
            findings.append((no, "W291 trailing whitespace"))
        stripped = line.strip()
        if DEBUG_CALL.search(line) and not stripped.startswith("#"):
            findings.append((no, "T201 print() call in library code"))
    return findings


def main(argv):
    if not argv:
        sys.stderr.write("usage: lint.py <dir> [<dir> ...]\n")
        return 2
    total = 0
    for d in argv:
        for path in sorted(pathlib.Path(d).rglob("*.py")):
            for no, msg in lint_file(path):
                sys.stderr.write("%s:%d: %s\n" % (path, no, msg))
                total += 1
    if total:
        sys.stderr.write("lint: %d finding(s)\n" % total)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
