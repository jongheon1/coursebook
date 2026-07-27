"""Lab 1 — count the actual bytes behind the "16 bytes per parameter" rule.

For each training configuration we materialize params / grads / optimizer
states by running one real train step, then measure every tensor with
numel() * element_size().  Expected bytes/param:

  fp32 + SGD                     4 + 4 + 0            =  8
  fp32 + SGD(momentum)           4 + 4 + 4            = 12
  fp32 + Adam                    4 + 4 + (4+4)        = 16
  fp16 + fp32-master Adam        2 + 2 + (4+4+4)      = 16   (ZeRO K=12 layout)
  pure bf16 + Adam (no master)   2 + 2 + (2+2)        =  8   (cheap but unsafe)

Run:  python lab1_memory_accounting.py
"""

import torch
import torch.nn.functional as F

from tinytransformer import TinyGPT, param_count

VOCAB, SEQ, BATCH = 256, 64, 8


def data(seed=0):
    g = torch.Generator().manual_seed(seed)
    idx = torch.randint(0, VOCAB, (BATCH, SEQ + 1), generator=g)
    return idx[:, :-1], idx[:, 1:]


def tensor_bytes(tensors):
    return sum(t.numel() * t.element_size() for t in tensors if torch.is_tensor(t))


def opt_state_bytes(opt):
    total = 0
    for state in opt.state.values():          # per-param dict: exp_avg, exp_avg_sq, step, ...
        total += tensor_bytes(state.values())
    return total


def one_step(model, opt):
    x, y = data()
    logits = model(x)
    loss = F.cross_entropy(logits.float().view(-1, VOCAB), y.reshape(-1))
    loss.backward()
    opt.step()


def account(name, model, opt, extra_master=None):
    psi = param_count(model)
    p_bytes = tensor_bytes(model.parameters())
    g_bytes = tensor_bytes(p.grad for p in model.parameters() if p.grad is not None)
    s_bytes = opt_state_bytes(opt) + (tensor_bytes(extra_master) if extra_master else 0)
    total = p_bytes + g_bytes + s_bytes
    print(f"{name:>28} | {p_bytes/psi:6.2f} | {g_bytes/psi:6.2f} | {s_bytes/psi:6.2f} | "
          f"{total/psi:6.2f} | {total/2**20:8.2f} MiB")
    return total / psi


def run_fp32(opt_ctor, name):
    torch.manual_seed(0)
    model = TinyGPT(vocab=VOCAB, max_seq=SEQ)
    opt = opt_ctor(model.parameters())
    one_step(model, opt)
    account(name, model, opt)


def run_low_precision_pure(dtype, name):
    torch.manual_seed(0)
    model = TinyGPT(vocab=VOCAB, max_seq=SEQ).to(dtype)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3, eps=1e-4)
    one_step(model, opt)                       # states are created in the params' dtype
    account(name, model, opt)


def run_fp16_master_adam():
    """Megatron/ZeRO-style layout: fp16 model+grads, fp32 master weights inside
    the optimizer, static loss scaling."""
    torch.manual_seed(0)
    model = TinyGPT(vocab=VOCAB, max_seq=SEQ).half()
    master = [p.detach().clone().float() for p in model.parameters()]
    opt = torch.optim.Adam(master, lr=1e-3)
    SCALE = 1024.0

    x, y = data()
    logits = model(x)
    loss = F.cross_entropy(logits.float().view(-1, VOCAB), y.reshape(-1))
    (loss * SCALE).backward()                  # scaled fp16 grads
    for m, p in zip(master, model.parameters()):
        m.grad = p.grad.float() / SCALE        # unscale into fp32
    opt.step()
    for m, p in zip(master, model.parameters()):
        p.data.copy_(m)                        # fp32 master -> fp16 model
    account("fp16 + fp32-master Adam", model, opt, extra_master=master)


if __name__ == "__main__":
    psi = param_count(TinyGPT(vocab=VOCAB, max_seq=SEQ))
    print(f"model: TinyGPT  psi = {psi:,} params\n")
    print(f"{'configuration':>28} | params | grads  | states | B/param | total")
    print("-" * 84)
    run_fp32(lambda p: torch.optim.SGD(p, lr=0.1), "fp32 + SGD")
    run_fp32(lambda p: torch.optim.SGD(p, lr=0.1, momentum=0.9), "fp32 + SGD(momentum=0.9)")
    run_fp32(lambda p: torch.optim.Adam(p, lr=1e-3), "fp32 + Adam")
    run_fp16_master_adam()
    run_low_precision_pure(torch.bfloat16, "pure bf16 + Adam (unsafe)")
    print("\nnote: Adam's per-tensor 'step' scalars add ~0.00 B/param; "
          "everything else matches the closed-form accounting.")
