"""Shared helpers for single-machine multi-process labs (CPU + gloo).

Every lab spawns `world_size` processes with torch.multiprocessing, forms a
process group over loopback TCP, runs a worker function, and tears down.
"""

import os
import socket
import sys

import torch
import torch.distributed as dist
import torch.multiprocessing as mp


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def init_worker(rank: int, world_size: int, port: int) -> None:
    """Called at the top of every spawned worker process."""
    if sys.platform == "darwin":
        # gloo needs an explicit interface on macOS in some setups; loopback is lo0.
        os.environ.setdefault("GLOO_SOCKET_IFNAME", "lo0")
    torch.set_num_threads(1)  # fair timing: 1 compute thread per process
    dist.init_process_group(
        backend="gloo",
        init_method=f"tcp://127.0.0.1:{port}",
        rank=rank,
        world_size=world_size,
    )


def _entry(rank: int, fn, world_size: int, port: int, args: tuple) -> None:
    init_worker(rank, world_size, port)
    try:
        fn(rank, world_size, *args)
    finally:
        dist.barrier()
        dist.destroy_process_group()


def launch(fn, world_size: int, *args) -> None:
    """Spawn `world_size` processes running fn(rank, world_size, *args)."""
    port = _free_port()
    mp.spawn(_entry, args=(fn, world_size, port, args), nprocs=world_size, join=True)
