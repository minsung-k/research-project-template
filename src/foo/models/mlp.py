"""Placeholder MLP. Replace with real models as the project grows."""
from __future__ import annotations

import torch
import torch.nn as nn


class MLP(nn.Module):
    """Simple feed-forward network. Variable names match the math:
        x \\in R^{B x in_dim}     ->  y \\in R^{B x out_dim}
    """

    def __init__(
        self,
        in_dim: int,
        hidden_dims: list[int],
        out_dim: int,
        activation: str = "gelu",
    ) -> None:
        super().__init__()
        act_cls = {"relu": nn.ReLU, "gelu": nn.GELU, "tanh": nn.Tanh}[activation]
        dims = [in_dim, *hidden_dims, out_dim]
        layers: list[nn.Module] = []
        for i in range(len(dims) - 1):
            layers.append(nn.Linear(dims[i], dims[i + 1]))
            if i < len(dims) - 2:
                layers.append(act_cls())
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
