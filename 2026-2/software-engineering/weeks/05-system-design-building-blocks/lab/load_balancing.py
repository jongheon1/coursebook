#!/usr/bin/env python3
"""Lab 3 — Load balancing policies under heavy-tailed service times.

Discrete-event simulation of 10 single-worker FIFO servers behind a
dispatcher. The same arrival process and per-request service times are
replayed against three dispatch policies (paired comparison):

  round-robin (RR) / uniform random / least-connections

Service times ~ Pareto(alpha=2.5) (heavy-tailed); an exponential
baseline with the same mean shows the gap narrowing on light tails.

Stdlib only. Run: python3 load_balancing.py
"""

import random
from collections import deque

N_SERVERS = 10
N_REQUESTS = 200_000
MEAN_SERVICE = 0.05          # 50 ms mean service time -> 200 req/s capacity
UTILIZATION = 0.8            # offered load / capacity
LAMBDA = UTILIZATION * N_SERVERS / MEAN_SERVICE   # 160 req/s
PARETO_ALPHA = 2.5
PARETO_XM = MEAN_SERVICE * (PARETO_ALPHA - 1) / PARETO_ALPHA
SEED = 7


def gen_workload(dist: str, seed: int):
    """Pre-generate (arrival_time, service_time) so all policies see the
    exact same workload."""
    rng = random.Random(seed)
    t = 0.0
    workload = []
    for _ in range(N_REQUESTS):
        t += rng.expovariate(LAMBDA)  # Poisson arrivals
        if dist == "pareto":
            s = PARETO_XM / (rng.random() ** (1.0 / PARETO_ALPHA))
        else:  # exponential
            s = rng.expovariate(1.0 / MEAN_SERVICE)
        workload.append((t, s))
    return workload


def simulate(policy: str, workload, seed: int):
    """Each server = single-worker FIFO queue. Dispatch happens at arrival
    time (no central queue). Returns list of waiting times."""
    rng = random.Random(seed)
    free_at = [0.0] * N_SERVERS            # when server finishes its backlog
    in_flight = [deque() for _ in range(N_SERVERS)]  # departure times
    waits = []

    for i, (arrival, service) in enumerate(workload):
        if policy == "rr":
            s = i % N_SERVERS
        elif policy == "random":
            s = rng.randrange(N_SERVERS)
        elif policy == "least-conn":
            # active connections = requests assigned but not yet departed
            best, best_conn = 0, None
            for j in range(N_SERVERS):
                q = in_flight[j]
                while q and q[0] <= arrival:
                    q.popleft()
                if best_conn is None or len(q) < best_conn:
                    best, best_conn = j, len(q)
            s = best
        else:
            raise ValueError(policy)

        start = max(arrival, free_at[s])
        waits.append(start - arrival)
        free_at[s] = start + service
        in_flight[s].append(free_at[s])

    return waits


def pct(sorted_xs, p: float) -> float:
    """Nearest-rank percentile on a pre-sorted list."""
    idx = min(len(sorted_xs) - 1, max(0, int(p / 100.0 * len(sorted_xs)) - 1))
    return sorted_xs[idx]


def report(dist_label: str, workload):
    print(f"--- service time: {dist_label}, {N_SERVERS} servers, "
          f"rho = {UTILIZATION}, {N_REQUESTS:,} requests ---")
    print(f"{'policy':>11} | {'mean':>8} | {'p50':>8} | {'p95':>8} | {'p99':>8} | {'max':>8}")
    print("-" * 66)
    for policy in ("random", "rr", "least-conn"):
        waits = sorted(simulate(policy, workload, seed=SEED + 100))
        mean = sum(waits) / len(waits)
        row = [mean, pct(waits, 50), pct(waits, 95), pct(waits, 99), waits[-1]]
        cells = " | ".join(f"{1000 * v:>6.1f}ms" for v in row)
        print(f"{policy:>11} | {cells}")
    print()


if __name__ == "__main__":
    print("=== Waiting time by dispatch policy (paired workloads) ===\n")
    report(f"Pareto(alpha={PARETO_ALPHA}) — heavy tail", gen_workload("pareto", SEED))
    report("Exponential — light tail (baseline)", gen_workload("exp", SEED + 1))
    print("Expected: least-conn crushes the p99 under heavy tails, because it")
    print("routes around servers stuck behind one elephant request; RR/random")
    print("keep feeding blocked servers. The gap narrows on light tails.")
