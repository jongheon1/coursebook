"""Tangled design: all pricing knowledge is smeared across one module.

Deliberate smells (see chapter §2.2):
- pricing constants appear in several places (computation AND a second function)
- validation, pricing, surcharge and receipt formatting are interleaved in
  one function (procedural cohesion at best)
- total_fare() re-implements the fare arithmetic for the daily ops report
  ("written later by another developer") — duplicated knowledge
"""

import math


def quote(duration_seconds, start_hour, membership="NONE"):
    """Return (total_fare, receipt_text) for one ride."""
    # ---- validation (FR-5, FR-7) ----
    if duration_seconds <= 0:
        raise ValueError("duration must be positive")
    if not 0 <= start_hour <= 23:
        raise ValueError("start_hour out of range")
    if membership not in ("NONE", "BASIC", "PLUS"):
        raise ValueError("unknown membership")

    minutes = math.ceil(duration_seconds / 60)  # FR-1

    lines = []
    total = 0

    # ---- unlock fee (FR-2; FR-7: PLUS waives it) ----
    if membership != "PLUS":
        total += 1000
        lines.append(f"{'unlock':<14}{1000:>8}")

    # ---- time charge (FR-2) ----
    ride_amount = minutes * 180
    total += ride_amount
    lines.append(f"{'ride %d min' % minutes:<14}{ride_amount:>8}")

    # ---- membership discount (FR-7: on the time charge) ----
    if membership == "BASIC":
        discount = ride_amount * 10 // 100
        total -= discount
        ride_amount -= discount
        lines.append(f"{'basic -10%':<14}{-discount:>8}")
    elif membership == "PLUS":
        discount = ride_amount * 30 // 100
        total -= discount
        ride_amount -= discount
        lines.append(f"{'plus -30%':<14}{-discount:>8}")

    # ---- night surcharge (FR-3'): 20% of discounted time charge only ----
    if start_hour < 6:
        surcharge = ride_amount * 20 // 100
        total += surcharge
        lines.append(f"{'night +20%':<14}{surcharge:>8}")

    # ---- rounding (FR-4) + receipt footer (FR-6) ----
    total = total - total % 10
    lines.append("-" * 22)
    lines.append(f"{'TOTAL':<14}{total:>8}")
    return total, "\n".join(lines)


def total_fare(duration_seconds, start_hour, membership="NONE"):
    """Fare only, for the daily ops report.

    Re-implements the arithmetic instead of reusing quote() — the constants
    and rules live here a second time.
    """
    if duration_seconds <= 0:
        raise ValueError("duration must be positive")
    if not 0 <= start_hour <= 23:
        raise ValueError("start_hour out of range")
    if membership not in ("NONE", "BASIC", "PLUS"):
        raise ValueError("unknown membership")
    minutes = -(-duration_seconds // 60)  # ceil, written another way
    ride = minutes * 180
    if membership == "BASIC":
        ride -= ride * 10 // 100
    elif membership == "PLUS":
        ride -= ride * 30 // 100
    fare = ride if membership == "PLUS" else 1000 + ride
    if start_hour < 6:
        fare += ride * 20 // 100
    return fare - fare % 10
