"""Lab 1 — Ariane 5 Flight 501: the 64-bit float -> 16-bit int conversion, replayed.

Python stdlib only. Deterministic (no randomness).

What this simulates (per the Lions inquiry report, 1996):
- The SRI alignment function computes a horizontal-bias variable BH proportional
  to horizontal velocity. On Ariane 4 the value stayed within the 16-bit signed
  range; on Ariane 5 it did not, at ~36.7 s after H0 (approx. 30 s after
  lift-off). The simulation's t is measured from H0, like the report's times.
- The conversion was intentionally left unprotected: a decision jointly agreed
  by the project partners, based on reasoning that BH was physically limited
  (the board found no evidence trajectory data were used) plus a <=80% CPU load
  requirement — but its justification was documented neither in the source code
  nor in the spec, hiding it from external review. Ada's checked conversion then
  raised an Operand Error; the exception policy shut the processor down.
- Both SRIs ran identical software: the backup failed the same way (one 72 ms
  cycle earlier), so redundancy bought nothing (common-mode failure).

NOTE: trajectory constants below are *pedagogical* — tuned so the overflow occurs
at ~36.7 s like the real flight. They are not real telemetry.
"""

INT16_MIN, INT16_MAX = -(2**15), 2**15 - 1
DT = 0.1                 # simulation step [s]
ALIGNMENT_ACTIVE_UNTIL = 47.0  # alignment function keeps running ~50 s after
                               # flight mode starts at H0-3 s (Ariane 4 legacy)


class OperandError(Exception):
    """Ada-style constraint/operand error on a checked conversion."""


# ---------------------------------------------------------------- conversions
def to_int16_ada(x: float) -> int:
    """Ada checked conversion: raises instead of producing a wrong value."""
    v = int(x)
    if not (INT16_MIN <= v <= INT16_MAX):
        raise OperandError(f"value {v} outside int16 range")
    return v


def to_int16_wrap(x: float) -> int:
    """C-flavoured silent wraparound (two's complement). In real C, an
    out-of-range float->int conversion is *undefined behavior* (C11 6.3.1.4),
    which can be even worse than wraparound — see ariane_overflow.c."""
    return ((int(x) + 2**15) % 2**16) - 2**15


def to_int16_saturate(x: float) -> int:
    """Clamp to the representable range (bounded, but silently wrong)."""
    return max(INT16_MIN, min(INT16_MAX, int(x)))


# ---------------------------------------------------------------- trajectories
def vh_ariane4(t: float) -> float:
    """Horizontal velocity proxy, Ariane 4 profile (never overflows int16)."""
    return 20.0 * t + 1.5 * t * t


def vh_ariane5(t: float) -> float:
    """Ariane 5 profile: much higher horizontal velocity early in flight.
    Crosses the int16 limit at ~36.7 s (tuned constants)."""
    return 40.0 * t + 23.24 * t * t


# ---------------------------------------------------------------- SRI channel
class SRI:
    """One inertial reference channel. policy decides what the conversion does
    and what happens on an out-of-range value."""

    def __init__(self, name: str, policy: str):
        self.name = name
        self.policy = policy
        self.alive = True
        self.last_good = 0
        self.flagged = False   # did the channel *report* an anomaly?

    def cycle(self, t: float, vh: float):
        """One 72 ms-ish computation cycle. Returns BH_int16 or None if dead."""
        if not self.alive:
            return None
        if self.policy == "disable-after-liftoff":
            if t >= 0.0:               # the honest fix: dead requirement removed
                return self.last_good
        if t > ALIGNMENT_ACTIVE_UNTIL:  # alignment stops on its own eventually
            return self.last_good

        bh = vh  # BH proportional to horizontal velocity (proportionality = 1)
        if self.policy in ("unprotected-ada", "disable-after-liftoff"):
            try:
                self.last_good = to_int16_ada(bh)
            except OperandError:
                # actual SRI exception policy: log diagnostics, SHUT DOWN
                self.alive = False
                return None
        elif self.policy == "wraparound-c":
            self.last_good = to_int16_wrap(bh)      # garbage flows on, silently
        elif self.policy == "saturate":
            v = to_int16_saturate(bh)
            if v != int(bh):
                self.flagged = True                 # saturated: mark degraded
            self.last_good = v
        elif self.policy == "range-check-fallback":
            v = int(bh)
            if INT16_MIN <= v <= INT16_MAX:
                self.last_good = v
            else:
                self.flagged = True                 # keep last good value + flag
        else:
            raise ValueError(self.policy)
        return self.last_good


def fly(policy: str, vh_profile, t_end: float = 60.0):
    """Fly one trajectory with a single SRI channel; report what happened."""
    sri = SRI("SRI", policy)
    first_anomaly = None
    garbage_seen = None
    t = 0.0
    while t <= t_end:
        vh = vh_profile(t)
        out = sri.cycle(t, vh)
        if out is None:                              # processor shut down
            return dict(policy=policy, outcome="PROCESSOR SHUTDOWN",
                        t=round(t, 1), detected=True, value=None)
        if first_anomaly is None:
            if sri.flagged:
                first_anomaly = t
            elif policy == "wraparound-c" and int(vh) > INT16_MAX:
                first_anomaly, garbage_seen = t, out  # wrong value, no signal
        t = round(t + DT, 10)
    if first_anomaly is None:
        return dict(policy=policy, outcome="nominal", t=None,
                    detected=False, value=sri.last_good)
    if policy == "wraparound-c":
        return dict(policy=policy, outcome="GARBAGE DATA (undetected)",
                    t=round(first_anomaly, 1), detected=False, value=garbage_seen)
    return dict(policy=policy, outcome="degraded, flagged, kept flying",
                t=round(first_anomaly, 1), detected=True, value=sri.last_good)


# ---------------------------------------------------------------- experiments
def part1():
    print("=== Part 1: same code, two rockets ===")
    for name, prof in (("Ariane 4", vh_ariane4), ("Ariane 5", vh_ariane5)):
        peak = max(prof(i * DT) for i in range(int(60.0 / DT) + 1))
        r = fly("unprotected-ada", prof)
        status = (f"OK  (max BH = {int(peak):6d}, fits int16)"
                  if r["outcome"] == "nominal" else
                  f"OPERAND ERROR at t={r['t']}s (BH = {int(prof(r['t']))} "
                  f"> {INT16_MAX}) -> {r['outcome']}")
        print(f"  {name}: {status}")
    print("  -> the code did not change; the ENVIRONMENT did. 'Proven on "
          "Ariane 4' was a claim about Ariane 4's trajectory, not the code.\n")


def part2():
    print("=== Part 2: redundancy vs common-mode failure (Ariane 5) ===")
    # (a) identical software on both channels — the actual design
    both = [SRI("SRI1 (backup)", "unprotected-ada"),
            SRI("SRI2 (active)", "unprotected-ada")]
    # (b) diverse design: same spec, different out-of-range policy
    diverse = [SRI("SRI1 (backup)", "unprotected-ada"),
               SRI("SRI2 (active)", "range-check-fallback")]
    for label, channels in (("identical software (actual design)", both),
                            ("diverse conversion policy", diverse)):
        t = 0.0
        deaths = []
        while t <= 60.0:
            for ch in channels:
                if ch.alive and ch.cycle(t, vh_ariane5(t)) is None:
                    deaths.append((ch.name, round(t, 1)))
            t = round(t + DT, 10)
        alive = [c.name for c in channels if c.alive]
        print(f"  [{label}]")
        for name, td in deaths:
            print(f"    {name} shut down at t={td}s")
        if alive:
            print(f"    surviving channel(s): {', '.join(alive)} -> OBC still "
                  "has attitude data, mission continues")
        else:
            print("    no surviving channel within one cycle -> OBC reads the "
                  "diagnostic bit pattern as flight data -> loss of mission")
    print("  -> two copies of the same design fault fail on the same input;\n"
          "     redundancy only protects against INDEPENDENT failures.\n")


def part3():
    print("=== Part 3: defense comparison on the Ariane 5 trajectory ===")
    rows = [fly(p, vh_ariane5) for p in
            ("unprotected-ada", "wraparound-c", "saturate",
             "range-check-fallback", "disable-after-liftoff")]
    print(f"  {'policy':<22} {'first anomaly':<14} {'detected':<9} outcome")
    print("  " + "-" * 72)
    for r in rows:
        t = f"t={r['t']}s" if r["t"] is not None else "-"
        det = "yes" if r["detected"] else "NO"
        extra = f" (BH reported as {r['value']})" if r["policy"] == "wraparound-c" else ""
        print(f"  {r['policy']:<22} {t:<14} {det:<9} {r['outcome']}{extra}")
    print("\n  Reading the table:")
    print("  - unprotected-ada : fails LOUDLY but the exception POLICY (shutdown)")
    print("    turns a useless computation's overflow into loss of the vehicle.")
    print("  - wraparound-c    : no crash, but attitude input is garbage and NOTHING")
    print("    signals it — silent wrong data is the worst failure mode.")
    print("  - saturate/fallback: bounded value + explicit flag; system keeps flying")
    print("    on degraded data and can report the anomaly.")
    print("  - disable-after-liftoff: the real fix — the requirement was dead on")
    print("    Ariane 5; code with no purpose cannot fail. (Remove dead requirements.)")


if __name__ == "__main__":
    part1()
    part2()
    part3()
