"""Lab 2 — activation memory scales with batch size (and superlinearly with seq).

Two independent measurements of the forward pass of TinyGPT:

  1. torch.profiler(profile_memory=True, CPU): net bytes allocated during
     forward while the autograd graph is kept alive.  This includes saved
     activations + non-saved temporaries + the output logits.
  2. exact saved-activation bytes via torch.autograd.graph.saved_tensors_hooks:
     every tensor autograd stashes for backward, deduplicated by
     (data_ptr, numel, element_size), parameters excluded (they are saved
     too — matmul backward needs W — but cost no extra memory).

Expected: both columns grow ~linearly in batch size b at fixed seq s
(constant bytes/sample), and superlinearly in s at fixed b because the
attention matrices saved by softmax/matmul are (b, a, s, s).

Run:  python lab2_activation_scaling.py
"""

import torch
import torch.nn.functional as F
from torch.profiler import ProfilerActivity, profile

from tinytransformer import TinyGPT

VOCAB, H, LAYERS, HEADS = 256, 128, 4, 4


def saved_activation_bytes(model, x, y):
    seen, param_ptrs = {}, {p.data_ptr() for p in model.parameters()}

    def pack(t):
        key = (t.data_ptr(), t.numel(), t.element_size())
        if t.data_ptr() not in param_ptrs:
            seen[key] = t.numel() * t.element_size()
        return t

    with torch.autograd.graph.saved_tensors_hooks(pack, lambda t: t):
        logits = model(x)
        loss = F.cross_entropy(logits.view(-1, VOCAB), y.reshape(-1))
    return sum(seen.values()), loss


def profiler_forward_bytes(model, x, y):
    with profile(activities=[ProfilerActivity.CPU], profile_memory=True) as prof:
        logits = model(x)
        loss = F.cross_entropy(logits.view(-1, VOCAB), y.reshape(-1))
    net = sum(e.cpu_memory_usage for e in prof.events())
    return net, loss


def sweep(rows, title, unit_key):
    print(f"\n{title}")
    print(f"{'b':>4} {'s':>5} | {'profiler net (MiB)':>18} | {'saved acts (MiB)':>16} | "
          f"{'saved/' + unit_key + ' (KiB)':>18}")
    print("-" * 70)
    for b, s in rows:
        torch.manual_seed(0)
        model = TinyGPT(vocab=VOCAB, h=H, layers=LAYERS, a=HEADS, max_seq=512)
        g = torch.Generator().manual_seed(1)
        idx = torch.randint(0, VOCAB, (b, s + 1), generator=g)
        x, y = idx[:, :-1], idx[:, 1:]

        model(x)  # warm-up: one-time allocator effects out of the profiled region

        prof_bytes, loss1 = profiler_forward_bytes(model, x, y)
        saved_bytes, loss2 = saved_activation_bytes(model, x, y)
        assert torch.allclose(loss1, loss2)
        unit = b if unit_key == "sample" else b * s
        print(f"{b:>4} {s:>5} | {prof_bytes/2**20:>18.2f} | {saved_bytes/2**20:>16.2f} | "
              f"{saved_bytes/unit/2**10:>18.1f}")
        del loss1, loss2  # release graphs


if __name__ == "__main__":
    torch.set_num_threads(1)
    sweep([(b, 64) for b in (4, 8, 16, 32)],
          "sweep 1 — batch size b at fixed s=64 (expect: bytes/sample constant)",
          "sample")
    sweep([(8, s) for s in (32, 64, 128, 256)],
          "sweep 2 — seq length s at fixed b=8 (expect: bytes/token GROWS ~ s term)",
          "token")
    print("\nreading: per-sample cost is flat in sweep 1 (activations ~ b),"
          "\nper-token cost climbs in sweep 2 — the (b, a, s, s) attention matrices"
          "\nsaved by softmax and att@v add the 5·a·s/h-style quadratic term.")
