"""Minimal decoder-only transformer for memory-accounting labs.

Deliberately hand-rolled (no nn.TransformerEncoder, no dropout, no bias)
so that every stored activation is visible in the code and the parameter
count matches 12*L*h^2 + 2*V*h + S*h (untied LM head) plus the LayerNorm
terms exactly -- see the assert below.
"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class CausalSelfAttention(nn.Module):
    def __init__(self, h: int, a: int):
        super().__init__()
        assert h % a == 0
        self.a, self.dh = a, h // a
        self.qkv = nn.Linear(h, 3 * h, bias=False)   # 3 h^2 params
        self.proj = nn.Linear(h, h, bias=False)      # 1 h^2 params

    def forward(self, x):
        B, S, H = x.shape
        q, k, v = self.qkv(x).split(H, dim=-1)
        # (B, S, H) -> (B, a, S, dh)
        q = q.view(B, S, self.a, self.dh).transpose(1, 2)
        k = k.view(B, S, self.a, self.dh).transpose(1, 2)
        v = v.view(B, S, self.a, self.dh).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.dh)   # (B, a, S, S)
        mask = torch.triu(torch.ones(S, S, dtype=torch.bool, device=x.device), 1)
        att = att.masked_fill(mask, float("-inf")).softmax(-1)  # saved for backward
        y = att @ v                                             # (B, a, S, dh)
        y = y.transpose(1, 2).reshape(B, S, H)
        return self.proj(y)


class Block(nn.Module):
    def __init__(self, h: int, a: int):
        super().__init__()
        self.ln1 = nn.LayerNorm(h)
        self.attn = CausalSelfAttention(h, a)
        self.ln2 = nn.LayerNorm(h)
        self.mlp = nn.Sequential(                    # 8 h^2 params
            nn.Linear(h, 4 * h, bias=False),
            nn.GELU(),
            nn.Linear(4 * h, h, bias=False),
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x


class TinyGPT(nn.Module):
    def __init__(self, vocab: int = 256, h: int = 128, layers: int = 4,
                 a: int = 4, max_seq: int = 128):
        super().__init__()
        self.tok = nn.Embedding(vocab, h)            # V h
        self.pos = nn.Embedding(max_seq, h)          # S h
        self.blocks = nn.ModuleList(Block(h, a) for _ in range(layers))
        self.ln_f = nn.LayerNorm(h)
        self.head = nn.Linear(h, vocab, bias=False)  # V h (untied)

    def forward(self, idx):
        B, S = idx.shape
        x = self.tok(idx) + self.pos(torch.arange(S, device=idx.device))
        for blk in self.blocks:
            x = blk(x)
        return self.head(self.ln_f(x))


def param_count(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())


if __name__ == "__main__":
    m = TinyGPT()
    n = param_count(m)
    # analytic: 12 L h^2 (attn 4h^2 + mlp 8h^2) + 2 V h + S h + LN terms
    h, L, V, S = 128, 4, 256, 128
    analytic = 12 * L * h * h + 2 * V * h + S * h + (2 * L + 1) * 2 * h
    print(f"params = {n:,} (analytic {analytic:,})")
    assert n == analytic
