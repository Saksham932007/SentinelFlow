from __future__ import annotations
import os
import torch
from models.lstm_model import LSTMAnomalyDetector


def export_lstm_to_onnx(pt_path: str, onnx_path: str) -> None:
    model = LSTMAnomalyDetector(input_size=8)
    model.load_state_dict(torch.load(pt_path))
    model.eval()
    dummy = torch.randn(1, 10, 8)
    os.makedirs(os.path.dirname(onnx_path), exist_ok=True)
    torch.onnx.export(model, dummy, onnx_path, opset_version=13, input_names=["input"], output_names=["score"])


def export_gnn_to_onnx(pt_path: str, onnx_path: str) -> None:
    # Placeholder: GNN export requires graph inputs; implement when training available.
    open(onnx_path, "wb").close()


if __name__ == "__main__":
    export_lstm_to_onnx("models/artifacts/lstm.pt", "deploy/model_repository/lstm_fraud/1/model.onnx")
