from __future__ import annotations
from typing import Optional
import torch
import torch.nn as nn

try:
    from torch_geometric.nn import SAGEConv
except Exception:
    SAGEConv = None


class GNNFraudDetector(nn.Module):
    """GraphSAGE-style GNN for transaction graph scoring.

    This is a lightweight implementation that will work if `torch_geometric` is installed.
    """

    def __init__(self, in_channels: int, hidden_channels: int = 64, out_channels: int = 1) -> None:
        super().__init__()
        if SAGEConv is None:
            raise RuntimeError("torch_geometric not available; install torch-geometric to use GNN component")
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, hidden_channels)
        self.fc = nn.Sequential(nn.Linear(hidden_channels, 32), nn.ReLU(), nn.Linear(32, out_channels), nn.Sigmoid())

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        x = torch.relu(x)
        # readout: assume node-level scoring
        return self.fc(x)
