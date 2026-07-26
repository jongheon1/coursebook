#!/usr/bin/env python3
"""Lab 1 — Consistent hashing vs naive mod-N hashing.

Measures two things:
  1. Remap fraction: what fraction of keys change owner when a node is
     added to / removed from the cluster, under (a) mod-N hashing and
     (b) consistent hashing.
  2. Load uniformity: how evenly keys spread across nodes as a function
     of the number of virtual nodes (vnodes) per physical node.

Stdlib only. Run: python3 consistent_hashing.py
"""

import hashlib
import statistics
from bisect import bisect_right

NUM_KEYS = 100_000
BASE_NODES = [f"node-{i}" for i in range(10)]


def h64(s: str) -> int:
    """Stable 64-bit hash (truncated MD5).

    Python's built-in hash() is salted per process (PYTHONHASHSEED),
    so it cannot be used for a distributed hash ring.
    """
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")


class ModNTable:
    """Naive placement: owner = nodes[hash(key) mod N]."""

    def __init__(self, nodes):
        self.nodes = list(nodes)

    def lookup(self, key: str) -> str:
        return self.nodes[h64(key) % len(self.nodes)]


class ConsistentHashRing:
    """Classic hash ring (Karger et al. 1997) with virtual nodes.

    Each physical node is hashed at `vnodes` points on the ring.
    A key is owned by the first vnode point clockwise from hash(key).
    """

    def __init__(self, nodes, vnodes: int):
        self.vnodes = vnodes
        self._nodes = set(nodes)
        self._rebuild()

    def _rebuild(self):
        ring = []
        for n in self._nodes:
            for v in range(self.vnodes):
                ring.append((h64(f"{n}#vn{v}"), n))
        ring.sort()
        self.points = [p for p, _ in ring]
        self.owners = [o for _, o in ring]

    def add(self, node: str):
        self._nodes.add(node)
        self._rebuild()

    def remove(self, node: str):
        self._nodes.discard(node)
        self._rebuild()

    def lookup(self, key: str) -> str:
        i = bisect_right(self.points, h64(key))
        if i == len(self.points):
            i = 0  # wrap around
        return self.owners[i]


def remap_fraction(before: dict, after: dict) -> float:
    moved = sum(1 for k, owner in before.items() if after[k] != owner)
    return moved / len(before)


def experiment_remap():
    keys = [f"key-{i}" for i in range(NUM_KEYS)]

    print("=== Experiment 1: remap fraction on membership change ===")
    print(f"{NUM_KEYS:,} keys, 10 nodes -> add 1 node / remove 1 node\n")

    # --- mod-N ---
    m10 = ModNTable(BASE_NODES)
    before = {k: m10.lookup(k) for k in keys}

    m11 = ModNTable(BASE_NODES + ["node-10"])
    after_add = {k: m11.lookup(k) for k in keys}

    m9 = ModNTable([n for n in BASE_NODES if n != "node-3"])
    after_rm = {k: m9.lookup(k) for k in keys}

    print(f"mod-N        add node : {remap_fraction(before, after_add):6.1%} of keys remapped"
          f"   (theory ~ 1 - 1/11 = 90.9%)")
    print(f"mod-N        rm  node : {remap_fraction(before, after_rm):6.1%} of keys remapped")

    # --- consistent hashing ---
    ring = ConsistentHashRing(BASE_NODES, vnodes=100)
    before = {k: ring.lookup(k) for k in keys}

    ring.add("node-10")
    after_add = {k: ring.lookup(k) for k in keys}
    ring.remove("node-10")  # back to base

    ring.remove("node-3")
    after_rm = {k: ring.lookup(k) for k in keys}

    print(f"consistent   add node : {remap_fraction(before, after_add):6.1%} of keys remapped"
          f"   (theory ~ K/(N+1) = 1/11 = 9.1%)")
    print(f"consistent   rm  node : {remap_fraction(before, after_rm):6.1%} of keys remapped"
          f"   (theory ~ K/N = 1/10 = 10.0%)")


def experiment_vnodes():
    keys = [f"key-{i}" for i in range(NUM_KEYS)]

    print("\n=== Experiment 2: load uniformity vs vnode count (10 nodes) ===")
    print(f"{'vnodes':>7} | {'min/mean':>8} | {'max/mean':>8} | {'CV (std/mean)':>13}")
    print("-" * 48)
    for vnodes in (1, 10, 100, 1000):
        ring = ConsistentHashRing(BASE_NODES, vnodes=vnodes)
        counts = {n: 0 for n in BASE_NODES}
        for k in keys:
            counts[ring.lookup(k)] += 1
        loads = list(counts.values())
        mean = statistics.mean(loads)
        cv = statistics.pstdev(loads) / mean
        print(f"{vnodes:>7} | {min(loads) / mean:>8.2f} | {max(loads) / mean:>8.2f} | {cv:>13.3f}")
    print("\nExpected: imbalance shrinks roughly as 1/sqrt(vnodes).")


if __name__ == "__main__":
    experiment_remap()
    experiment_vnodes()
