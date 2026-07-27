"""Lab 3 — gradient checkpointing: memory down, compute up, gradients identical.

A stack of n=8 transformer Blocks is run (a) normally and (b) with
torch.utils.checkpoint.checkpoint_sequential over k segments.  We measure:

  * saved-activation bytes that persist from forward into backward
    (pack-hook counter, dedup + params excluded, as in lab 2);
  * wall-clock time of one full fwd+bwd (mean over iters, after warm-up);
  * max |grad difference| vs the baseline — must be 0.0: recomputation
    replays the exact same kernels on the exact same inputs.

Notes on semantics: use_reentrant=True runs each checkpointed segment under
no_grad in forward, so nothing inside a segment is saved — only the segment
boundary inputs stashed by CheckpointFunction.save_for_backward (which our
pack hook still sees).  checkpoint_sequential does NOT checkpoint the last
segment, so its interior activations remain in the measurement.

Run:  python lab3_checkpointing.py
"""

import time

import torch
import torch.nn as nn
from torch.utils.checkpoint import checkpoint_sequential

from tinytransformer import Block

H, HEADS, N_BLOCKS, BATCH, SEQ = 256, 4, 8, 8, 64
ITERS, WARMUP = 10, 3


def make_model():
    torch.manual_seed(0)
    return nn.Sequential(*[Block(H, HEADS) for _ in range(N_BLOCKS)])


def make_input():
    g = torch.Generator().manual_seed(1)
    return torch.randn(BATCH, SEQ, H, generator=g, requires_grad=True)


def run(model, segments):
    def fwd(x):
        if segments == 0:
            return model(x)
        return checkpoint_sequential(model, segments, x, use_reentrant=True)

    # --- measurement 1: bytes saved for backward during forward ---
    seen, param_ptrs = {}, {p.data_ptr() for p in model.parameters()}

    def pack(t):
        if t.data_ptr() not in param_ptrs:
            seen[(t.data_ptr(), t.numel(), t.element_size())] = t.numel() * t.element_size()
        return t

    model.zero_grad(set_to_none=True)
    x = make_input()
    with torch.autograd.graph.saved_tensors_hooks(pack, lambda t: t):
        loss = fwd(x).square().mean()
    saved = sum(seen.values())
    loss.backward()
    grads = [p.grad.detach().clone() for p in model.parameters()]

    # --- measurement 2: wall time of fwd+bwd ---
    times = []
    for i in range(WARMUP + ITERS):
        model.zero_grad(set_to_none=True)
        xi = make_input()
        t0 = time.perf_counter()
        fwd(xi).square().mean().backward()
        if i >= WARMUP:
            times.append(time.perf_counter() - t0)
    return saved, sum(times) / len(times), grads


if __name__ == "__main__":
    torch.set_num_threads(1)
    model = make_model()

    base_saved, base_t, base_grads = run(model, segments=0)
    print(f"stack of {N_BLOCKS} Blocks (h={H}, b={BATCH}, s={SEQ}), fp32\n")
    print(f"{'variant':>22} | {'saved acts (MiB)':>16} | {'ratio':>6} | "
          f"{'fwd+bwd (ms)':>12} | {'slowdown':>8} | {'max|dgrad|':>10}")
    print("-" * 92)
    print(f"{'no checkpoint':>22} | {base_saved/2**20:>16.2f} | {'1.00':>6} | "
          f"{base_t*1e3:>12.1f} | {'1.00x':>8} | {'—':>10}")
    for k in (4, 2):
        saved, t, grads = run(model, segments=k)
        dmax = max((g1 - g2).abs().max().item() for g1, g2 in zip(base_grads, grads))
        print(f"{f'checkpoint k={k} segs':>22} | {saved/2**20:>16.2f} | "
              f"{saved/base_saved:>6.2f} | {t*1e3:>12.1f} | {t/base_t:>7.2f}x | {dmax:>10.1e}")

    print("\nreading: memory drops toward (boundaries + last segment), time rises by")
    print("roughly one extra forward; gradients are bit-identical (max|dgrad| = 0).")
