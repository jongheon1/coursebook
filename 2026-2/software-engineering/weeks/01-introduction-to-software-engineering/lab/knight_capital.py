"""Lab 2 — Knight Capital (2012-08-01): flag reuse + partial deployment,
as a state machine simulation.

Python stdlib only. Deterministic (round-robin routing, fixed order flow).

What this simulates (per SEC Release No. 34-70694, 2013):
- SMARS ran on 8 servers. The new RLP feature REUSED a message flag that had
  activated 'Power Peg' — code retired in 2003 but left deployed, whose
  cumulative-fill stop condition had been silently broken by a 2005 refactor.
- Deployment was manual; 1 of 8 servers was missed. Flagged orders routed to
  that server activated Power Peg: child orders sent continuously, fills never
  counted. 212 defective parent orders -> millions of orders, ~$460M lost in
  ~45 minutes. Rolling the new code BACK off the 7 good servers made all 8
  servers defective.

Model calibration is illustrative (loss-per-execution chosen so the order of
magnitude matches the real incident), not market data.
"""

MINUTES = 45                 # incident window (09:30 - 10:15)
PARENTS_PER_MIN = 5          # flagged parent orders arriving per minute (~212 total: 5*45=225)
CHILDS_PER_MIN_RUNAWAY = 1_000  # child orders/min emitted by one runaway parent
CHILDS_PER_PARENT_OK = 10    # child orders a CORRECT execution needs
LOSS_PER_CHILD = 115         # $ per runaway child execution (illustrative)

NEW, LEGACY, HALTED = "RLP_2012", "SMARS_LEGACY", "HALTED"


class Server:
    def __init__(self, sid: int, code: str):
        self.sid = sid
        self.code = code

    def handle_parent(self, order_id: int):
        """Returns the parent-order end state for a flagged (RLP) parent order.

        state machine:  NEW -> WORKING -> FILLED          (new code)
                        NEW -> RUNAWAY (never terminates)  (legacy: Power Peg,
                                broken fill counter reads 0 forever)
                        NEW -> REJECTED                    (dead code removed)
        """
        if self.code == NEW:
            return "FILLED"          # tracks fills, completes after 10 children
        if self.code == LEGACY:
            return "RUNAWAY"         # Power Peg: sends children, never sees fills
        if self.code == "LEGACY_NO_DEADCODE":
            return "REJECTED"        # unknown flag -> hard reject + error log
        raise ValueError(self.code)


def run(scenario: str, verbose_timeline: bool = False):
    """Run one 45-minute session. Returns summary dict."""
    # --- deployment step -----------------------------------------------------
    if scenario == "full-deploy":
        servers = [Server(i, NEW) for i in range(8)]
    elif scenario in ("incident", "incident+rollback", "kill-switch"):
        servers = [Server(i, NEW) for i in range(7)] + [Server(7, LEGACY)]
    elif scenario == "deploy-verification":
        servers = [Server(i, NEW) for i in range(7)] + [Server(7, LEGACY)]
        versions = {s.code for s in servers}
        if len(versions) > 1:        # post-deploy check: versions must agree
            return dict(scenario=scenario, filled=0, runaway=0, rejected=0,
                        children=0, loss=0,
                        note="version mismatch across servers -> deployment "
                             "aborted before open, zero orders at risk")
    elif scenario == "dead-code-removed":
        servers = ([Server(i, NEW) for i in range(7)] +
                   [Server(7, "LEGACY_NO_DEADCODE")])
    else:
        raise ValueError(scenario)

    # pre-open warning e-mails (the real system sent 97 referencing
    # 'Power Peg disabled' at 08:01; nobody treated them as alerts)
    legacy_present = any(s.code == LEGACY for s in servers)
    if legacy_present and scenario != "deploy-verification":
        emails = 97
    else:
        emails = 0

    # --- market session ------------------------------------------------------
    filled = rejected = 0
    runaway_started_at = []          # activation minute of each runaway parent
    children = 0
    loss = 0
    order_id = 0
    halted_at = None
    rollback_at = 20 if scenario == "incident+rollback" else None
    loss_limit = 2_000_000 if scenario == "kill-switch" else None
    timeline = []

    for minute in range(MINUTES):
        if halted_at is not None:
            break
        if rollback_at is not None and minute == rollback_at:
            # "roll back the new code" = redeploy the OLD code on 7 servers
            for s in servers:
                if s.code == NEW:
                    s.code = LEGACY
        # runaway parents emit children continuously, fills never counted
        n_runaway = len(runaway_started_at)
        children += n_runaway * CHILDS_PER_MIN_RUNAWAY
        loss += n_runaway * CHILDS_PER_MIN_RUNAWAY * LOSS_PER_CHILD
        # new flagged parent orders arrive, routed round-robin
        for _ in range(PARENTS_PER_MIN):
            server = servers[order_id % len(servers)]
            state = server.handle_parent(order_id)
            order_id += 1
            if state == "FILLED":
                filled += 1
                children += CHILDS_PER_PARENT_OK
            elif state == "RUNAWAY":
                runaway_started_at.append(minute)
            elif state == "REJECTED":
                rejected += 1
        if loss_limit is not None and loss >= loss_limit:
            halted_at = minute       # automated kill switch trips
        if verbose_timeline and minute in (0, 5, 10, 15, 19, 20, 21, 25, 30, 40, 44):
            timeline.append((minute, len(runaway_started_at), children, loss))

    return dict(scenario=scenario, filled=filled, runaway=len(runaway_started_at),
                rejected=rejected, children=children, loss=loss, emails=emails,
                halted_at=halted_at, timeline=timeline, note=None)


def fmt_money(x):
    return f"${x:,.0f}"


def main():
    print("=== Knight Capital simulation: 45 min, 5 flagged parent orders/min, "
          "8 servers ===\n")

    scenarios = [
        ("full-deploy",         "correct deployment: new code on all 8 servers"),
        ("incident",            "actual bug: 1 of 8 servers still runs legacy code"),
        ("incident+rollback",   "+ minute 20: new code rolled back off the 7 good servers"),
        ("deploy-verification", "defense 1: post-deploy version check across servers"),
        ("dead-code-removed",   "defense 2: Power Peg deleted; unknown flag -> reject"),
        ("kill-switch",         "defense 3: automated $2M loss limit halts trading"),
    ]

    print(f"{'scenario':<20} {'filled':>7} {'runaway':>8} {'rejected':>9} "
          f"{'child orders':>13} {'loss':>15}  note")
    print("-" * 100)
    for name, desc in scenarios:
        r = run(name, verbose_timeline=(name == "incident+rollback"))
        note = r.get("note") or desc
        if r.get("halted_at") is not None:
            note += f" (halted at minute {r['halted_at']})"
        if r.get("emails"):
            note += f" [{r['emails']} pre-open warning e-mails ignored]"
        print(f"{name:<20} {r['filled']:>7} {r['runaway']:>8} {r['rejected']:>9} "
              f"{r['children']:>13,} {fmt_money(r['loss']):>15}  {note}")
        if name == "incident+rollback":
            rollback_run = r

    print("\n=== Timeline of 'incident+rollback' (the real 2012-08-01 shape) ===")
    print(f"{'minute':>6} {'runaway parents':>16} {'child orders':>13} {'cum. loss':>15}")
    for minute, n_run, children, loss in rollback_run["timeline"]:
        marker = "  <- rollback: ALL 8 servers now defective" if minute == 20 else ""
        print(f"{minute:>6} {n_run:>16} {children:>13,} {fmt_money(loss):>15}{marker}")

    print("""
Reading the results:
- full-deploy       : the NEW code was fine. 225 parents, 2,250 child orders, $0.
- incident          : identical code, identical orders — only the DEPLOYMENT
  differs. Every 8th parent hits the legacy server and turns into a runaway
  Power Peg loop (broken fill counter -> never terminates).
- incident+rollback : 'undo the release' redeployed the OLD flag semantics on
  all 8 servers — runaway creation rate x8. A rollback is a deployment; unverified,
  it carries the same risk as the original deploy.
- deploy-verification: the cheapest fix. The dangerous state was never 'the bug'
  alone but the MIXED-VERSION fleet; detecting version skew before open reduces
  the incident to a non-event.
- dead-code-removed : with Power Peg gone, the stale flag has no path to walk.
  Cost: some rejected orders + error logs — bounded, visible, recoverable.
- kill-switch       : does not prevent the fault, but converts an unbounded loss
  into a bounded one (this is what SEC Rule 15c3-5 required and Knight lacked).
""")


if __name__ == "__main__":
    main()
