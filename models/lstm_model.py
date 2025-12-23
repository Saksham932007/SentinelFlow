from __future__ import annotations
from typing import Optional
import torch
import torch.nn as nn


class LSTMAnomalyDetector(nn.Module):
    """Simple LSTM-based sequence model for anomaly scoring."""

    def __init__(self, input_size: int, hidden_size: int = 64, num_layers: int = 2, dropout: float = 0.1) -> None:
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Sequential(nn.Linear(hidden_size, 32), nn.ReLU(), nn.Linear(32, 1), nn.Sigmoid())

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, features)
        out, _ = self.lstm(x)
        # take last time-step
        last = out[:, -1, :]
        return self.fc(last)
