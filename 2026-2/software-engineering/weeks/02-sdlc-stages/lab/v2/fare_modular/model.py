"""Ride model. Owns input validation (FR-5) and nothing about money."""

from dataclasses import dataclass

MEMBERSHIPS = ("NONE", "BASIC", "PLUS")


@dataclass(frozen=True)
class Ride:
    duration_seconds: int
    start_hour: int
    membership: str = "NONE"  # FR-7

    def __post_init__(self):
        if self.duration_seconds <= 0:
            raise ValueError("duration must be positive")
        if not 0 <= self.start_hour <= 23:
            raise ValueError("start_hour out of range")
        if self.membership not in MEMBERSHIPS:
            raise ValueError("unknown membership")
