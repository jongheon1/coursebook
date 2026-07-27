"""Fare computation: sums whatever items the policy defines. Knows no prices."""

from . import policy


def compute(ride):
    """Return (line_items, rounded_total) for a ride."""
    items = policy.line_items(ride)
    total = policy.round_fare(sum(amount for _, amount in items))
    return items, total
