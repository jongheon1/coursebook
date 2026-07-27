"""Pricing policy — the module that OWNS the pricing design decision.

Parnas: a module is characterized by the design decision it hides from all
others. The 'secret' here is everything about money: the constants, which
items make up a fare, what the surcharge applies to, and the rounding rule.
Other modules only ever see a list of (label, amount) items.
"""

import math

UNLOCK_FEE = 1000
PER_MINUTE = 180
NIGHT_END_HOUR = 6
NIGHT_RATE_PCT = 20


def line_items(ride):
    """Fare breakdown as [(label, amount), ...] (FR-1, FR-2, FR-3)."""
    minutes = math.ceil(ride.duration_seconds / 60)  # FR-1
    items = [
        ("unlock", UNLOCK_FEE),
        ("ride %d min" % minutes, minutes * PER_MINUTE),
    ]
    if ride.start_hour < NIGHT_END_HOUR:  # FR-3: 20% of the fare so far
        base = sum(amount for _, amount in items)
        items.append(("night +20%", base * NIGHT_RATE_PCT // 100))
    return items


def round_fare(amount):
    """FR-4: floor to 10 KRW."""
    return amount - amount % 10
