"""Lab 2 — Manual gradient averaging vs DistributedDataParallel vs large-batch SGD.

Trains three copies of the same MLP from an identical initialization:
  ref    : single-process large-batch SGD on the full global batch (B = world * b),
           computed redundantly (and deterministically) on every rank
  manual : per-rank forward/backward on the local shard, then explicit
           all_reduce(grad) / world before the optimizer step
  ddp    : the same local-shard loop with the model wrapped in DDP

Claim under test (Section "synchronous data-parallel SGD" of the chapter):
all three follow the same parameter trajectory, up to floating-point
summation order. manual vs DDP should agree almost bitwise; both should agree
with the large-batch reference to fp32 rounding noise.

Run:  python lab2_ddp_equivalence.py [world_size]
"""

import copy
import sys

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parallel import DistributedDataParallel as DDP

from common import launch

B_GLOBAL = 64  # global batch size
STEPS = 30
LR = 0.1
MOMENTUM = 0.9


def make_model() -> nn.Module:
    torch.manual_seed(42)  # identical init on every rank / for every copy
    return nn.Sequential(
        nn.Linear(32, 64), nn.ReLU(),
        nn.Linear(64, 64), nn.ReLU(),
        nn.Linear(64, 10),
    )


def make_data() -> tuple[torch.Tensor, torch.Tensor]:
    g = torch.Generator().manual_seed(123)
    x = torch.randn(B_GLOBAL * STEPS, 32, generator=g)
    y = torch.randint(0, 10, (B_GLOBAL * STEPS,), generator=g)
    return x, y


def max_param_diff(m1: nn.Module, m2: nn.Module) -> float:
    return max(
        (p1 - p2).abs().max().item()
        for p1, p2 in zip(m1.parameters(), m2.parameters())
    )


def replicas_max_spread(model: nn.Module, world: int) -> float:
    """Max elementwise spread of `model`'s parameters across ranks (must be 0)."""
    flat = torch.cat([p.detach().reshape(-1) for p in model.parameters()])
    gathered = [torch.empty_like(flat) for _ in range(world)]
    dist.all_gather(gathered, flat)
    stacked = torch.stack(gathered)
    return (stacked.max(dim=0).values - stacked.min(dim=0).values).max().item()


def worker(rank: int, world: int) -> None:
    assert B_GLOBAL % world == 0
    b = B_GLOBAL // world
    x, y = make_data()  # deterministic: identical on every rank

    ref = make_model()
    manual = copy.deepcopy(ref)
    ddp = DDP(copy.deepcopy(ref))  # broadcasts rank 0's params at construction

    opts = {
        m: torch.optim.SGD(m.parameters(), lr=LR, momentum=MOMENTUM)
        for m in (ref, manual, ddp)
    }

    if rank == 0:
        print(f"world={world}  local batch b={b}  global batch B={B_GLOBAL}  "
              f"steps={STEPS}  SGD(lr={LR}, momentum={MOMENTUM})")
        print(f"\n{'step':>4} | {'loss(ref)':>9} | {'max|manual-ddp|':>15} | {'max|manual-ref|':>15}")
        print("-" * 55)

    for step in range(STEPS):
        xb = x[step * B_GLOBAL:(step + 1) * B_GLOBAL]
        yb = y[step * B_GLOBAL:(step + 1) * B_GLOBAL]
        xl, yl = xb[rank * b:(rank + 1) * b], yb[rank * b:(rank + 1) * b]  # local shard

        # (1) reference: full global batch, one process' worth of work, no comm
        opts[ref].zero_grad()
        loss_ref = F.cross_entropy(ref(xb), yb)  # mean over B
        loss_ref.backward()
        opts[ref].step()

        # (2) manual data parallelism: local mean loss, then average grads
        opts[manual].zero_grad()
        F.cross_entropy(manual(xl), yl).backward()  # mean over b
        for p in manual.parameters():
            dist.all_reduce(p.grad, op=dist.ReduceOp.SUM)
            p.grad /= world
        opts[manual].step()

        # (3) DDP: bucketing + overlapped allreduce happen inside backward()
        opts[ddp].zero_grad()
        F.cross_entropy(ddp(xl), yl).backward()
        opts[ddp].step()

        if rank == 0 and (step + 1) in (1, 5, 10, 20, 30):
            d_md = max_param_diff(manual, ddp.module)
            d_mr = max_param_diff(manual, ref)
            print(f"{step + 1:>4} | {loss_ref.item():>9.4f} | {d_md:>15.3e} | {d_mr:>15.3e}")

    # replicas must be perfectly in sync across ranks
    spread_manual = replicas_max_spread(manual, world)
    spread_ddp = replicas_max_spread(ddp.module, world)
    d_md = max_param_diff(manual, ddp.module)
    d_mr = max_param_diff(manual, ref)
    if rank == 0:
        print(f"\ncross-rank spread: manual={spread_manual:.3e}  ddp={spread_ddp:.3e}")
        print(f"final: max|manual-ddp|={d_md:.3e}  max|manual-ref|={d_mr:.3e}")
    assert spread_manual == 0.0 and spread_ddp == 0.0, "replicas diverged across ranks"
    assert d_md < 1e-6, f"manual DP and DDP trajectories diverged: {d_md}"
    assert d_mr < 1e-3, f"DP and large-batch trajectories diverged: {d_mr}"
    if rank == 0:
        print("OK: manual DP == DDP (~bitwise), both == large-batch SGD (fp noise)")


if __name__ == "__main__":
    world_size = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    launch(worker, world_size)
