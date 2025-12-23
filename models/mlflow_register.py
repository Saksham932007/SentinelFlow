from __future__ import annotations
import mlflow
import os

def register_model(artifact_path: str, model_name: str = "sentinelflow_lstm") -> None:
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.register_model(artifact_path, model_name)


if __name__ == "__main__":
    register_model("models/artifacts/lstm.pt", "sentinelflow_lstm")
