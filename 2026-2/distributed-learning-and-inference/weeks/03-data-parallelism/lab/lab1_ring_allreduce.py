"""Lab 1 — Ring-allreduce from point-to-point send/recv vs dist.all_reduce.

Implements the two-phase ring algorithm (reduce-scatter + all-gather) using
only isend/recv, verifies it against the built-in collective, and benchmarks
both across tensor sizes.

Run:  python lab1_ring_allreduce.py [world_size]
"""

import sys
import time

import torch
import torch.distributed as dist

from common import launch


def ring_allreduce(x: torch.Tensor) -> torch.Tensor:
    """Sum-allreduce of `x` across all ranks via a logical ring.

    Phase 1 (reduce-scatter): p-1 steps. At step t, rank r sends chunk
    (r - t) mod p to its right neighbor and adds the incoming chunk
    (r - t - 1) mod p from its left neighbor. After p-1 steps, rank r owns
    the fully reduced chunk (r + 1) mod p.

    Phase 2 (all-gather): p-1 steps. At step t, rank r sends chunk
    (r + 1 - t) mod p and overwrites chunk (r - t) mod p with the incoming
    fully reduced chunk.

    Per phase each rank sends (p-1) * N/p elements -> total 2 (p-1)/p * N.
    Returns a new tensor; `x` is left unmodified.
    """
    rank, p = dist.get_rank(), dist.get_world_size()
    n = x.numel()
    pad = (-n) % p  # chunks must be equal-sized; pad with zeros
    flat = torch.cat([x.reshape(-1), x.new_zeros(pad)]) if pad else x.reshape(-1).clone()
    chunks = list(flat.chunk(p))  # views into `flat`
    right, left = (rank + 1) % p, (rank - 1) % p

    # Phase 1: reduce-scatter
    for t in range(p - 1):
        send_idx = (rank - t) % p
        recv_idx = (rank - t - 1) % p
        recv_buf = torch.empty_like(chunks[recv_idx])
        send_req = dist.isend(chunks[send_idx], dst=right)  # non-blocking: avoids ring deadlock
        dist.recv(recv_buf, src=left)
        send_req.wait()
        chunks[recv_idx] += recv_buf

    # Phase 2: all-gather
    for t in range(p - 1):
        send_idx = (rank + 1 - t) % p
        recv_idx = (rank - t) % p
        recv_buf = torch.empty_like(chunks[recv_idx])
        send_req = dist.isend(chunks[send_idx], dst=right)
        dist.recv(recv_buf, src=left)
        send_req.wait()
        chunks[recv_idx].copy_(recv_buf)

    return flat[:n].reshape(x.shape)


def bench(fn, x: torch.Tensor, iters: int, warmup: int = 2) -> float:
    for _ in range(warmup):
        fn(x)
    dist.barrier()
    t0 = time.perf_counter()
    for _ in range(iters):
        fn(x)
    dist.barrier()
    return (time.perf_counter() - t0) / iters


def worker(rank: int, world: int) -> None:
    torch.manual_seed(1234)  # same base tensor everywhere, then shift per rank

    # --- correctness ---------------------------------------------------
    x = torch.randn(1_000_003) + rank  # deliberately not divisible by p
    ours = ring_allreduce(x)
    ref = x.clone()
    dist.all_reduce(ref, op=dist.ReduceOp.SUM)
    err = (ours - ref).abs().max().item()
    if rank == 0:
        print(f"[correctness] world={world}  N=1,000,003  max|ring - all_reduce| = {err:.3e}")
    assert err < 1e-4, f"ring_allreduce mismatch: {err}"

    # --- benchmark -----------------------------------------------------
    def native(t: torch.Tensor) -> None:
        buf = t.clone()
        dist.all_reduce(buf, op=dist.ReduceOp.SUM)

    if rank == 0:
        print(f"\n{'N (floats)':>12} | {'ring (ms)':>10} | {'dist.all_reduce (ms)':>20} | {'ratio':>6}")
        print("-" * 60)
    for size in (4_096, 65_536, 1_048_576, 4_194_304):
        t = torch.randn(size)
        iters = 20 if size <= 1_048_576 else 10
        t_ring = bench(ring_allreduce, t, iters)
        t_nat = bench(native, t, iters)
        if rank == 0:
            print(f"{size:>12,} | {t_ring * 1e3:>10.3f} | {t_nat * 1e3:>20.3f} | {t_ring / t_nat:>5.1f}x")


if __name__ == "__main__":
    world_size = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    launch(worker, world_size)
