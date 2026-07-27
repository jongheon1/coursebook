"""Receipt rendering (FR-6): formats ANY breakdown. Knows no pricing rules."""

LABEL_WIDTH = 14
AMOUNT_WIDTH = 8


def render(items, total):
    lines = [f"{label:<{LABEL_WIDTH}}{amount:>{AMOUNT_WIDTH}}" for label, amount in items]
    lines.append("-" * (LABEL_WIDTH + AMOUNT_WIDTH))
    lines.append(f"{'TOTAL':<{LABEL_WIDTH}}{total:>{AMOUNT_WIDTH}}")
    return "\n".join(lines)
