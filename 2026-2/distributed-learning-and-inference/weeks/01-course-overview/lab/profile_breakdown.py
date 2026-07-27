"""Lab 2 — decompose a training step with torch.profiler.

Answers two questions from the chapter with measurements:
  1. How does step time split into forward / backward / optimizer?
     (chapter section 1.2 predicts backward ~= 2x forward for dense layers)
  2. How many FLOPs does a step actually execute vs the 6*N*B estimate?
     (for the CNN, weight sharing makes 6*N*B a large underestimate)

Usage:
  python profile_breakdown.py --model mlp --batch-size 256
  python profile_breakdown.py --model cnn --batch-size 256
"""

import argparse

import torch
import torch.nn as nn
from torch.profiler import ProfilerActivity, profile, record_function

from common import build_model, count_params, synthetic_batches

PHASES = ("forward", "backward", "optimizer_step")


def train_step(model, batch, optimizer, loss_fn):
    x, y = batch
    optimizer.zero_grad(set_to_none=True)
    with record_function("forward"):
        loss = loss_fn(model(x), y)
    with record_function("backward"):
        loss.backward()
    with record_function("optimizer_step"):
        optimizer.step()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=["mlp", "cnn"], default="mlp")
    ap.add_argument("--batch-size", type=int, default=256)
    ap.add_argument("--steps", type=int, default=10, help="profiled steps")
    ap.add_argument("--warmup", type=int, default=5)
    args = ap.parse_args()

    torch.manual_seed(0)
    model = build_model(args.model)
    n_params = count_params(model)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    loss_fn = nn.CrossEntropyLoss()
    batches = synthetic_batches(args.model, num_batches=8, batch_size=args.batch_size)

    for step in range(args.warmup):
        train_step(model, batches[step % len(batches)], optimizer, loss_fn)

    with profile(activities=[ProfilerActivity.CPU], with_flops=True) as prof:
        for step in range(args.steps):
            train_step(model, batches[step % len(batches)], optimizer, loss_fn)

    averages = prof.key_averages()

    # Phase split from the record_function scopes (cpu_time_total includes children).
    phase_us = {evt.key: evt.cpu_time_total for evt in averages if evt.key in PHASES}
    total_us = sum(phase_us.values())
    print(f"model={args.model}  batch={args.batch_size}  params={n_params:,}  "
          f"profiled steps={args.steps}")
    print(f"\nphase split (avg per step, {args.steps} steps):")
    for phase in PHASES:
        us = phase_us.get(phase, 0) / args.steps
        print(f"  {phase:<15} {us / 1e3:8.2f} ms  ({100 * phase_us.get(phase, 0) / total_us:5.1f}%)")
    fwd, bwd = phase_us.get("forward", 1), phase_us.get("backward", 0)
    print(f"  backward/forward ratio: {bwd / fwd:.2f}x  (chapter prediction for dense layers: ~2x)")

    # Measured FLOPs (profiler counts matmul/conv ops, fwd+bwd) vs the 6*N*B estimate.
    measured = sum(evt.flops for evt in averages if evt.flops) / args.steps
    estimate = 6 * n_params * args.batch_size
    print(f"\nFLOPs per step:   measured {measured / 1e9:6.2f} GFLOPs  |  "
          f"6*N*B estimate {estimate / 1e9:6.2f} GFLOPs  |  ratio {measured / estimate:.2f}x")

    print("\ntop ops by self CPU time:")
    print(averages.table(sort_by="self_cpu_time_total", row_limit=8))


if __name__ == "__main__":
    main()
