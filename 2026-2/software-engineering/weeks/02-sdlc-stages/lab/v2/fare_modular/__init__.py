"""Modular design: pricing knowledge lives in exactly one module (policy)."""

from . import calculator, receipt
from .model import Ride


def quote(duration_seconds, start_hour, membership="NONE"):
    """Return (total_fare, receipt_text) for one ride."""
    ride = Ride(duration_seconds, start_hour, membership)
    items, total = calculator.compute(ride)
    return total, receipt.render(items, total)


def total_fare(duration_seconds, start_hour, membership="NONE"):
    """Fare only, for the daily ops report. Delegates — no second copy of rules."""
    return quote(duration_seconds, start_hour, membership)[0]
