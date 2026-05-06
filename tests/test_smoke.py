"""Smoke test: package imports cleanly. If this fails, the env is wrong."""
from __future__ import annotations


def test_import_foo():
    import foo  # noqa: F401


def test_mlp_forward():
    import torch
    from foo.models import MLP

    model = MLP(in_dim=2, hidden_dims=[16, 16], out_dim=1)
    x = torch.randn(4, 2)
    y = model(x)
    assert y.shape == (4, 1)


def test_seed_is_deterministic():
    import torch
    from foo.utils import set_seed

    set_seed(0, deterministic=False)  # full-determ has perf hit; just check seeding
    a = torch.randn(3)
    set_seed(0, deterministic=False)
    b = torch.randn(3)
    assert torch.equal(a, b)
