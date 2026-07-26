#!/usr/bin/env python3
"""Lab 2 — Cache eviction policies (FIFO / LRU / LFU) under a Zipf workload.

Experiment 1: hit rate vs cache size on a stationary Zipf(s=1.0) workload.
Experiment 2: popularity shift halfway through the trace — shows LFU's
              aging problem (stale frequency counts) vs LRU's fast adaptation.

Stdlib only. Run: python3 cache_eviction.py
"""

import heapq
import itertools
import random
from collections import OrderedDict

N_ITEMS = 10_000
N_REQUESTS = 200_000
ZIPF_S = 1.0
SEED = 42


class FIFOCache:
    """Evicts in insertion order; a hit does NOT refresh position."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.od = OrderedDict()

    def access(self, key) -> bool:
        if key in self.od:
            return True
        if len(self.od) >= self.capacity:
            self.od.popitem(last=False)
        self.od[key] = True
        return False


class LRUCache:
    """Evicts the least recently used entry; a hit refreshes recency."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.od = OrderedDict()

    def access(self, key) -> bool:
        if key in self.od:
            self.od.move_to_end(key)
            return True
        if len(self.od) >= self.capacity:
            self.od.popitem(last=False)
        self.od[key] = True
        return False


class LFUCache:
    """Evicts the least frequently used entry (ties -> oldest heap entry).

    Frequency is tracked only while the item is cached (classic in-cache
    LFU): evicting an item discards its count, re-admission starts at 1.
    Implemented with a lazy-deletion heap: each frequency bump pushes a
    fresh (freq, seq, key) entry; stale entries are skipped at evict time.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.freq = {}
        self.heap = []
        self.seq = itertools.count()

    def access(self, key) -> bool:
        if key in self.freq:
            self.freq[key] += 1
            heapq.heappush(self.heap, (self.freq[key], next(self.seq), key))
            return True
        if len(self.freq) >= self.capacity:
            while True:
                f, _, victim = heapq.heappop(self.heap)
                if victim in self.freq and self.freq[victim] == f:
                    del self.freq[victim]
                    break
        self.freq[key] = 1
        heapq.heappush(self.heap, (1, next(self.seq), key))
        return False


def zipf_trace(n_items: int, s: float, n_requests: int, rng: random.Random):
    """Sample item ids 0..n_items-1 with P(rank r) ∝ 1/r^s (rank = id + 1)."""
    weights = [1.0 / (rank ** s) for rank in range(1, n_items + 1)]
    cum = list(itertools.accumulate(weights))
    return rng.choices(range(n_items), cum_weights=cum, k=n_requests)


def run(policy_cls, capacity: int, trace) -> float:
    cache = policy_cls(capacity)
    hits = sum(cache.access(k) for k in trace)
    return hits / len(trace)


def static_optimal(capacity: int) -> float:
    """Hit rate of an omniscient static cache pinning the top-C items."""
    weights = [1.0 / (rank ** ZIPF_S) for rank in range(1, N_ITEMS + 1)]
    return sum(weights[:capacity]) / sum(weights)


def experiment_stationary():
    rng = random.Random(SEED)
    trace = zipf_trace(N_ITEMS, ZIPF_S, N_REQUESTS, rng)

    print("=== Experiment 1: hit rate on stationary Zipf(s=1.0) workload ===")
    print(f"{N_ITEMS:,} items, {N_REQUESTS:,} requests\n")
    print(f"{'capacity':>8} | {'FIFO':>7} | {'LRU':>7} | {'LFU':>7} | {'static-opt':>10}")
    print("-" * 52)
    for cap in (100, 500, 1000):
        fifo = run(FIFOCache, cap, trace)
        lru = run(LRUCache, cap, trace)
        lfu = run(LFUCache, cap, trace)
        print(f"{cap:>8} | {fifo:>7.1%} | {lru:>7.1%} | {lfu:>7.1%} | {static_optimal(cap):>10.1%}")
    print("\nExpected ordering: LFU > LRU > FIFO (skewed, stationary popularity).")


def experiment_shift():
    rng = random.Random(SEED + 1)
    half = N_REQUESTS // 2
    phase1 = zipf_trace(N_ITEMS, ZIPF_S, half, rng)
    # Phase 2: same Zipf shape, but popularity ranks are rotated by N/2 —
    # yesterday's hot items become cold and vice versa.
    phase2 = [(k + N_ITEMS // 2) % N_ITEMS for k in zipf_trace(N_ITEMS, ZIPF_S, half, rng)]

    print("\n=== Experiment 2: popularity shift at t = 50% (capacity 500) ===")
    print(f"{'policy':>7} | {'phase-1 hit':>11} | {'phase-2 first 20k':>17} | {'phase-2 all':>11}")
    print("-" * 58)
    for name, cls in (("FIFO", FIFOCache), ("LRU", LRUCache), ("LFU", LFUCache)):
        cache = cls(500)
        h1 = sum(cache.access(k) for k in phase1) / half
        adapt_window = phase2[:20_000]
        ha = sum(cache.access(k) for k in adapt_window) / len(adapt_window)
        h2_rest = sum(cache.access(k) for k in phase2[20_000:])
        h2 = (ha * len(adapt_window) + h2_rest) / half
        print(f"{name:>7} | {h1:>11.1%} | {ha:>17.1%} | {h2:>11.1%}")
    print("\nExpected: LFU adapts slowest after the shift (stale frequency counts")
    print("keep old-hot items pinned) — the aging problem TinyLFU fixes.")


if __name__ == "__main__":
    experiment_stationary()
    experiment_shift()
