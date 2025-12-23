from __future__ import annotations
import argparse
import os
import torch
from torch.utils.data import DataLoader, TensorDataset
from models.lstm_model import LSTMAnomalyDetector
from models.gnn_model import GNNFraudDetector
import numpy as np


def train_lstm(save_path: str, epochs: int = 2) -> None:
    # Toy data: random sequences
    X = np.random.randn(100, 10, 8).astype(np.float32)
    y = np.random.randint(0, 2, size=(100, 1)).astype(np.float32)
    ds = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    dl = DataLoader(ds, batch_size=16, shuffle=True)
    model = LSTMAnomalyDetector(input_size=8)
    optim = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.BCELoss()
    model.train()
    for _ in range(epochs):
        for xb, yb in dl:
            pred = model(xb).squeeze(1)
            loss = loss_fn(pred, yb.squeeze(1))
            optim.zero_grad()
            loss.backward()
            optim.step()
    os.makedirs(save_path, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(save_path, "lstm.pt"))


def train_gnn(save_path: str) -> None:
    # Placeholder: create minimal torch_geometric-like tensors if available
    try:
        import torch_geometric
    except Exception:
        # Skip real training if torch_geometric not installed
        open(os.path.join(save_path, "gnn.pt"), "wb").close()
        return


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="models/artifacts")
    args = parser.parse_args()
    train_lstm(args.out)
    train_gnn(args.out)


if __name__ == "__main__":
    main()
