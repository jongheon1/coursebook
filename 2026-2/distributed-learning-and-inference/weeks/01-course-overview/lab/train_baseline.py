"""Lab 1 — baseline training loop with instrumentation.

Trains a small MLP or CNN on synthetic data (CPU) and measures what every
later week's experiments are compared against:

  - parameter count
  - per-step wall time (mean / p50 / p90 after warmup)
  - throughput (samples/s)
  - a 6*N*B FLOPs-per-step estimate and the implied achieved FLOP/s

Usage:
  python train_baseline.py --model mlp --batch-size 256 --steps 50
  python train_baseline.py --model cnn --batch-size 256 --steps 50
"""

import argparse
import statistics
import time

import torch
import torch.nn as nn

from common import build_model, count_params, synthetic_batches


def run(model, batches, steps, warmup, optimizer, loss_fn):
    """Run warmup+timed steps; return per-step wall times (s) and final loss."""
    times, loss = [], None
    for step in range(warmup + steps):
        x, y = batches[step % len(batches)]
        t0 = time.perf_counter()
        optimizer.zero_grad(set_to_none=True)
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()
        t1 = time.perf_counter()
        if step >= warmup:
            times.append(t1 - t0)
    return times, loss.item()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=["mlp", "cnn"], default="mlp")
    ap.add_argument("--batch-size", type=int, default=256)
    ap.add_argument("--steps", type=int, default=50, help="timed steps")
    ap.add_argument("--warmup", type=int, default=10, help="untimed warmup steps")
    ap.add_argument("--optimizer", choices=["sgd", "adam"], default="sgd")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    model = build_model(args.model)
    n_params = count_params(model)
    optimizer = (
        torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
        if args.optimizer == "sgd"
        else torch.optim.Adam(model.parameters(), lr=1e-3)
    )
    batches = synthetic_batches(args.model, num_batches=8, batch_size=args.batch_size, seed=args.seed)

    times, final_loss = run(model, batches, args.steps, args.warmup, optimizer, nn.CrossEntropyLoss())

    mean = statistics.fmean(times)
    p50 = statistics.median(times)
    p90 = sorted(times)[int(0.9 * len(times)) - 1]
    throughput = args.batch_size / mean
    flops_est = 6 * n_params * args.batch_size  # C ~= 6*N*B (dense-layer approx, fwd+bwd)

    print(f"model={args.model}  optimizer={args.optimizer}  batch={args.batch_size}  "
          f"steps={args.steps} (+{args.warmup} warmup)  threads={torch.get_num_threads()}  "
          f"torch={torch.__version__}")
    print(f"parameters:       {n_params:,}")
    print(f"step time:        mean {mean * 1e3:8.2f} ms | p50 {p50 * 1e3:8.2f} ms | p90 {p90 * 1e3:8.2f} ms")
    print(f"throughput:       {throughput:,.0f} samples/s")
    print(f"6*N*B estimate:   {flops_est / 1e9:.2f} GFLOPs/step "
          f"-> achieved ~{flops_est / mean / 1e9:.1f} GFLOP/s"
          + ("" if args.model == "mlp" else "  (UNDERestimate for CNN: weight sharing)"))
    print(f"final loss:       {final_loss:.4f}")


if __name__ == "__main__":
    main()
