"""Shared building blocks for the course labs.

Later weeks reuse these as the single-device baseline: `build_model` for a
small MLP/CNN, `synthetic_batches` for input data with zero I/O overhead,
`count_params` for the parameter census. Keep this file dependency-free
beyond torch so any week's lab can import it.
"""

import torch
import torch.nn as nn

NUM_CLASSES = 10


class MLP(nn.Module):
    """784 -> 1024 -> 1024 -> 10 (bias included). ~1.86M params."""

    def __init__(self, in_dim: int = 784, hidden: int = 1024):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, NUM_CLASSES),
        )

    def forward(self, x):
        return self.net(x)


class SmallCNN(nn.Module):
    """1x28x28 -> conv32 -> conv64 -> maxpool -> fc128 -> 10. ~1.63M params."""

    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1), nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 14 * 14, 128), nn.ReLU(),
            nn.Linear(128, NUM_CLASSES),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


def build_model(name: str) -> nn.Module:
    if name == "mlp":
        return MLP()
    if name == "cnn":
        return SmallCNN()
    raise ValueError(f"unknown model: {name}")


def input_shape(name: str) -> tuple:
    return (784,) if name == "mlp" else (1, 28, 28)


def synthetic_batches(name: str, num_batches: int, batch_size: int, seed: int = 0):
    """Pre-generated random (x, y) batches -> data loading cost is ~zero,
    so measured step time isolates compute (fwd/bwd/opt)."""
    g = torch.Generator().manual_seed(seed)
    shape = input_shape(name)
    return [
        (
            torch.randn(batch_size, *shape, generator=g),
            torch.randint(0, NUM_CLASSES, (batch_size,), generator=g),
        )
        for _ in range(num_batches)
    ]


def count_params(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())
