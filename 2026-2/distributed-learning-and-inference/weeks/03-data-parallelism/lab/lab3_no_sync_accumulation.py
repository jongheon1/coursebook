"""Lab 3 — Gradient accumulation and no_sync(): equivalence and communication cost.

Three DDP models from one initialization, each taking one optimizer step per
outer iteration over the same K * m samples per rank:

  big     : one forward/backward on the whole K*m local batch
  no_sync : K micro-batches; first K-1 backwards inside ddp.no_sync()
            (gradients accumulate locally, no communication), K-th backward
            outside the context triggers a single sync
  naive   : K micro-batches, no no_sync -> every backward all-reduces

Because allreduce is linear (avg of sums == sum of avgs), all three produce
the same parameter trajectory; they differ only in communication volume. A DDP
communication hook counts bucket-level allreduce calls to make that visible.

Run:  python lab3_no_sync_accumulation.py [world_size]
"""

import copy
import sys

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
from torch.distributed.algorithms.ddp_comm_hooks.default_hooks import allreduce_hook
from torch.nn.parallel import DistributedDataParallel as DDP

from common import launch

K = 4          # micro-batches per optimizer step
M = 8          # micro-batch size per rank
STEPS = 10
LR = 0.05
MOMENTUM = 0.9


def counting_hook(state: dict, bucket: dist.GradBucket):
    """Default allreduce hook + a call counter (one call per ready bucket)."""
    state["calls"] += 1
    return allreduce_hook(state["pg"], bucket)


def make_model() -> nn.Module:
    torch.manual_seed(7)
    return nn.Sequential(
        nn.Linear(32, 64), nn.ReLU(),
        nn.Linear(64, 64), nn.ReLU(),
        nn.Linear(64, 10),
    )


def max_param_diff(m1: nn.Module, m2: nn.Module) -> float:
    return max(
        (p1 - p2).abs().max().item()
        for p1, p2 in zip(m1.parameters(), m2.parameters())
    )


def worker(rank: int, world: int) -> None:
    g = torch.Generator().manual_seed(99)
    n_per_rank = K * M * STEPS
    x_all = torch.randn(world * n_per_rank, 32, generator=g)
    y_all = torch.randint(0, 10, (world * n_per_rank,), generator=g)
    # contiguous shard per rank
    x = x_all[rank * n_per_rank:(rank + 1) * n_per_rank]
    y = y_all[rank * n_per_rank:(rank + 1) * n_per_rank]

    base = make_model()
    models, counters = {}, {}
    for name in ("big", "no_sync", "naive"):
        m = DDP(copy.deepcopy(base))
        state = {"pg": None, "calls": 0}  # pg=None -> default WORLD group
        m.register_comm_hook(state, counting_hook)
        models[name], counters[name] = m, state
    opts = {
        name: torch.optim.SGD(m.parameters(), lr=LR, momentum=MOMENTUM)
        for name, m in models.items()
    }

    for step in range(STEPS):
        xs = x[step * K * M:(step + 1) * K * M]
        ys = y[step * K * M:(step + 1) * K * M]

        # (1) one big local batch of K*M samples
        opts["big"].zero_grad()
        F.cross_entropy(models["big"](xs), ys).backward()  # mean over K*M
        opts["big"].step()

        # (2) K micro-batches, sync only on the last one
        opts["no_sync"].zero_grad()
        for k in range(K):
            xm, ym = xs[k * M:(k + 1) * M], ys[k * M:(k + 1) * M]
            if k < K - 1:
                with models["no_sync"].no_sync():
                    (F.cross_entropy(models["no_sync"](xm), ym) / K).backward()
            else:  # forward AND backward outside no_sync -> triggers the sync
                (F.cross_entropy(models["no_sync"](xm), ym) / K).backward()
        opts["no_sync"].step()

        # (3) K micro-batches, naive: every backward communicates
        opts["naive"].zero_grad()
        for k in range(K):
            xm, ym = xs[k * M:(k + 1) * M], ys[k * M:(k + 1) * M]
            (F.cross_entropy(models["naive"](xm), ym) / K).backward()
        opts["naive"].step()

    d_ns_big = max_param_diff(models["no_sync"].module, models["big"].module)
    d_nv_big = max_param_diff(models["naive"].module, models["big"].module)
    d_ns_nv = max_param_diff(models["no_sync"].module, models["naive"].module)

    if rank == 0:
        print(f"world={world}  K={K} micro-batches x m={M} per rank, {STEPS} optimizer steps\n")
        print(f"{'variant':>8} | {'allreduce bucket calls':>22} | {'max|param - big|':>16}")
        print("-" * 55)
        for name, d in (("big", 0.0), ("no_sync", d_ns_big), ("naive", d_nv_big)):
            print(f"{name:>8} | {counters[name]['calls']:>22} | {d:>16.3e}")
        print(f"\nmax|no_sync - naive| = {d_ns_nv:.3e}")

    assert counters["no_sync"]["calls"] == counters["big"]["calls"], "no_sync must sync once per step"
    assert counters["naive"]["calls"] == K * counters["big"]["calls"], "naive must sync K times per step"
    assert d_ns_big < 1e-4 and d_nv_big < 1e-4 and d_ns_nv < 1e-4, "trajectories diverged"
    if rank == 0:
        print("OK: identical trajectories; no_sync cut communication by "
              f"{K}x (={counters['no_sync']['calls']} vs {counters['naive']['calls']} bucket allreduces)")


if __name__ == "__main__":
    world_size = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    launch(worker, world_size)
