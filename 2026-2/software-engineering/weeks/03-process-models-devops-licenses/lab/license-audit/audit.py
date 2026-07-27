#!/usr/bin/env python3
"""Dependency license audit: classify SPDX licenses and decide copyleft
obligations for a given distribution scenario.

Usage:
    python3 audit.py --requirements requirements-sample.txt \
                     --db licenses.json --scenario scenario-binary.json

Inputs:
    requirements  pip-style lines "name==version" (comments/blank lines ok)
    db            JSON {package: "SPDX license expression"}
    scenario      JSON {"name": str,
                        "distribution": "internal" | "saas" | "binary",
                        "linking": {package: "import"|"static"|"dynamic"|"process"},
                        "modified": [package, ...]}
                  linking defaults to "import" (in-process combination).

Exit code: 0 = no violations, 1 = at least one VIOLATION or UNKNOWN license.

Model (deliberately simplified — this is a teaching tool, not legal advice):
  - copyleft triggers on conveying (distribution="binary"); running internally
    or as SaaS is not conveying.
  - AGPL section 13 adds a network trigger for *modified* versions; combining
    an AGPL library in-process with proprietary code that serves users over a
    network is treated as a violation under the conservative FSF reading.
  - LGPL allows proprietary in-process use if the user can relink (dynamic
    linking, or object files when statically linked).
  - "X WITH Classpath-exception-2.0" carves linking out of GPL copyleft, so
    for linking purposes it is classified as weak copyleft.
  - SPDX operator precedence: WITH binds tightest, then AND, then OR.
    Parentheses are not supported.
"""

import argparse
import json
import pathlib
import re
import sys

# ---------------------------------------------------------------- categories

PERMISSIVE, WEAK, STRONG, NETWORK, UNKNOWN = range(5)
CATEGORY_NAMES = {
    PERMISSIVE: "permissive",
    WEAK: "weak-copyleft",
    STRONG: "strong-copyleft",
    NETWORK: "network-copyleft",
    UNKNOWN: "UNKNOWN",
}

_PREFIX_TABLE = [
    ("AGPL-3.0", NETWORK),
    ("SSPL", NETWORK),          # not OSI-approved; strictest bucket
    ("GPL-2.0", STRONG),
    ("GPL-3.0", STRONG),
    ("LGPL-2.1", WEAK),
    ("LGPL-3.0", WEAK),
    ("MPL-2.0", WEAK),
    ("EPL-1.0", WEAK),
    ("EPL-2.0", WEAK),
    ("MIT", PERMISSIVE),
    ("BSD-2-Clause", PERMISSIVE),
    ("BSD-3-Clause", PERMISSIVE),
    ("Apache-2.0", PERMISSIVE),
    ("ISC", PERMISSIVE),
    ("Zlib", PERMISSIVE),
    ("Unlicense", PERMISSIVE),
    ("Python-2.0", PERMISSIVE),
    ("PSF-2.0", PERMISSIVE),
]

# exceptions that carve linking out of copyleft -> weak for linking purposes
_LINKING_EXCEPTIONS = {"Classpath-exception-2.0", "GCC-exception-3.1", "LLVM-exception"}


def classify_id(license_id):
    """Category of a single SPDX id, optionally 'ID WITH exception'."""
    license_id = license_id.strip()
    if " WITH " in license_id:
        base, exc = (s.strip() for s in license_id.split(" WITH ", 1))
        cat = classify_id(base)
        if exc in _LINKING_EXCEPTIONS and cat in (STRONG, NETWORK):
            return WEAK
        return cat  # unknown exception: keep the conservative base category
    for prefix, cat in _PREFIX_TABLE:
        if license_id == prefix or license_id.startswith(prefix + "-") \
                or license_id.startswith(prefix + "+"):
            return cat
    return UNKNOWN


def classify_expression(expr):
    """Category of an SPDX expression (no parentheses).

    OR  = recipient chooses  -> take the weakest (most permissive) branch.
    AND = all parts apply    -> take the strongest part.
    """
    alternatives = []
    for branch in re.split(r"\s+OR\s+", expr.strip()):
        parts = [classify_id(p) for p in re.split(r"\s+AND\s+", branch)]
        known = [c for c in parts if c is not UNKNOWN]
        alternatives.append(max(parts) if len(known) == len(parts) else UNKNOWN)
    known = [c for c in alternatives if c is not UNKNOWN]
    return min(known) if known else UNKNOWN


# ------------------------------------------------------------------ verdicts

OK, WARN, VIOLATION, FLAG_UNKNOWN = "OK", "WARN", "VIOLATION", "UNKNOWN"
IN_PROCESS = {"import", "static", "dynamic"}


def decide(category, linking, modified, distribution):
    """Return (verdict, note) for one dependency in one scenario."""
    if category is UNKNOWN:
        return FLAG_UNKNOWN, "license unresolved — must be identified before any use"

    if distribution == "internal":
        return OK, "no conveying: copyleft not triggered (internal use only)"

    if distribution == "saas":
        if category is NETWORK:
            if modified:
                return VIOLATION, ("AGPL s13: network users must be offered the "
                                   "modified version's Corresponding Source")
            if linking in IN_PROCESS:
                return VIOLATION, ("in-process combination with AGPL code served over "
                                   "a network — conservative reading treats the combined "
                                   "work as a modified version; disclose, isolate, or remove")
            return OK, "unmodified, separate process at arm's length: s13 not triggered"
        if category is STRONG and linking in IN_PROCESS:
            return WARN, ("no conveying now, but latent: any future distribution "
                          "requires releasing the combined work under the GPL")
        return OK, "no conveying: copyleft not triggered"

    if distribution == "binary":
        if category is PERMISSIVE:
            return OK, ("compliance only: ship license text and notices "
                        "(Apache-2.0: NOTICE file, state changes)")
        if category is WEAK:
            if modified:
                return WARN, "modifications to the library itself must be released"
            if linking == "static":
                return WARN, ("LGPL relink condition: provide object files "
                              "or switch to dynamic linking")
            return OK, ("keep the library user-replaceable (relink); "
                        "library modifications must be released")
        if category in (STRONG, NETWORK):
            if linking in IN_PROCESS:
                return VIOLATION, ("conveying a combined work with copyleft code — "
                                   "release the whole work under the license, or "
                                   "remove / replace / obtain a commercial license")
            return WARN, ("separate program at arm's length: aggregation is allowed, "
                          "but its own source must be offered and IPC intimacy is "
                          "the legal risk")

    raise ValueError("unknown distribution: %r" % (distribution,))


# ----------------------------------------------------------------------- io

def parse_requirements(path):
    pkgs = []
    for raw in pathlib.Path(path).read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        name = re.split(r"[=<>!~\[]", line, maxsplit=1)[0].strip()
        if name:
            pkgs.append(name)
    return pkgs


def run_audit(requirements, db, scenario):
    linking_map = scenario.get("linking", {})
    modified = set(scenario.get("modified", []))
    rows = []
    for pkg in requirements:
        expr = db.get(pkg)
        category = classify_expression(expr) if expr else UNKNOWN
        verdict, note = decide(category, linking_map.get(pkg, "import"),
                               pkg in modified, scenario["distribution"])
        rows.append({
            "package": pkg,
            "license": expr or "(not in db)",
            "category": CATEGORY_NAMES[category],
            "linking": linking_map.get(pkg, "import"),
            "modified": pkg in modified,
            "verdict": verdict,
            "note": note,
        })
    return rows


def print_report(rows, scenario):
    print("license audit — scenario: %s (distribution=%s)"
          % (scenario.get("name", "?"), scenario["distribution"]))
    print("-" * 100)
    fmt = "%-14s %-46s %-17s %-8s %-9s"
    print(fmt % ("PACKAGE", "LICENSE", "CATEGORY", "LINKING", "VERDICT"))
    for r in rows:
        print(fmt % (r["package"], r["license"], r["category"],
                     r["linking"], r["verdict"]))
        print("               -> %s" % r["note"])
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print("-" * 100)
    print("summary:", ", ".join("%s=%d" % kv for kv in sorted(counts.items())))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--requirements", required=True)
    ap.add_argument("--db", required=True)
    ap.add_argument("--scenario", required=True)
    args = ap.parse_args(argv)

    requirements = parse_requirements(args.requirements)
    db = json.loads(pathlib.Path(args.db).read_text())
    scenario = json.loads(pathlib.Path(args.scenario).read_text())

    rows = run_audit(requirements, db, scenario)
    print_report(rows, scenario)

    bad = [r for r in rows if r["verdict"] in (VIOLATION, FLAG_UNKNOWN)]
    if bad:
        print("AUDIT FAILED: %d blocking finding(s)" % len(bad))
        return 1
    print("AUDIT PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
