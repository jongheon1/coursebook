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
DISCOUNT_PCT = {"BASIC": 10, "PLUS": 30}  # FR-7: off the time charge


def line_items(ride):
    """Fare breakdown as [(label, amount), ...] (FR-1, FR-2, FR-3', FR-7)."""
    minutes = math.ceil(ride.duration_seconds / 60)  # FR-1
    items = []
    if ride.membership != "PLUS":  # FR-7: PLUS waives the unlock fee
        items.append(("unlock", UNLOCK_FEE))
    ride_amount = minutes * PER_MINUTE
    items.append(("ride %d min" % minutes, ride_amount))
    if ride.membership in DISCOUNT_PCT:  # FR-7: discount on time charge
        pct = DISCOUNT_PCT[ride.membership]
        discount = ride_amount * pct // 100
        items.append(("%s -%d%%" % (ride.membership.lower(), pct), -discount))
        ride_amount -= discount
    if ride.start_hour < NIGHT_END_HOUR:  # FR-3': 20% of discounted time charge only
        items.append(("night +20%", ride_amount * NIGHT_RATE_PCT // 100))
    return items


def round_fare(amount):
    """FR-4: floor to 10 KRW."""
    return amount - amount % 10
