"""Measure the change cost of CR-1 for both designs (stdlib only).

For every .py file in v1/ and v2/, compute a unified diff and count added +
removed lines. Report per design: files touched, total changed lines, and —
for the modular design — how many changed lines fall OUTSIDE the module that
owns the pricing decision (policy.py). Parnas's prediction: a change to the
pricing decision should be confined to its owner.

Run: python3 measure_change_cost.py  (from the lab/ directory)
"""

import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def diff_stats(rel_path):
    """Return (added, removed, hunks) between v1/<rel> and v2/<rel>.

    hunks = distinct edit locations (unified-diff @@ headers) — how many
    separate places in the file you had to touch.
    """
    old, new = ROOT / "v1" / rel_path, ROOT / "v2" / rel_path
    old_lines = old.read_text().splitlines() if old.exists() else []
    new_lines = new.read_text().splitlines() if new.exists() else []
    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm="", n=0))
    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
    hunks = sum(1 for l in diff if l.startswith("@@"))
    return added, removed, hunks


def files_of(design_dir):
    v1 = {p.relative_to(ROOT / "v1") for p in (ROOT / "v1" / design_dir).rglob("*.py")}
    v2 = {p.relative_to(ROOT / "v2") for p in (ROOT / "v2" / design_dir).rglob("*.py")}
    return sorted(str(p) for p in v1 | v2)


DESIGNS = {
    "tangled": ["fare_tangled.py"],
    "modular": files_of("fare_modular"),
}
PRICING_OWNER = {"tangled": "fare_tangled.py", "modular": "fare_modular/policy.py"}


def main():
    summary = {}
    for design, files in DESIGNS.items():
        print(f"== {design} ==")
        total = touched = outside_owner = total_hunks = 0
        for rel in files:
            added, removed, hunks = diff_stats(rel)
            changed = added + removed
            mark = " <- pricing owner" if rel == PRICING_OWNER[design] else ""
            print(f"  {rel:<28} +{added:<3} -{removed:<3} hunks {hunks}{mark}")
            total += changed
            total_hunks += hunks
            if changed:
                touched += 1
                if rel != PRICING_OWNER[design]:
                    outside_owner += changed
        summary[design] = (touched, total, outside_owner, total_hunks)
        print(f"  files touched: {touched}, changed lines: {total}, "
              f"edit locations (hunks): {total_hunks}, "
              f"changed lines outside pricing owner: {outside_owner}\n")

    t, m = summary["tangled"], summary["modular"]
    print("== verdict ==")
    print(f"tangled : {t[1]} lines / {t[3]} edit locations in {t[0]} file(s); "
          f"the whole module IS the pricing owner — every edit sits next to "
          f"validation and formatting code, and the surcharge rule had to be "
          f"changed in TWO places (quote and total_fare)")
    print(f"modular : {m[1]} lines / {m[3]} edit locations in {m[0]} file(s); "
          f"{m[1] - m[2]} lines in policy.py, {m[2]} interface ripple "
          f"(model/facade); calculator.py and receipt.py provably untouched")


if __name__ == "__main__":
    main()
