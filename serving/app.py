from __future__ import annotations
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from typing import Dict

from serving.feature_store import FeatureStore
from serving.triton_client import TritonClient
import numpy as np

app = FastAPI(title="SentinelFlow Serving")


class LatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        resp = await call_next(request)
        duration = (time.time() - start) * 1000
        # In production we'd use structured logging
        print(f"{request.method} {request.url.path} took {duration:.2f}ms")
        return resp


app.add_middleware(LatencyMiddleware)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/predict")
async def predict(payload: Dict) -> Dict:
    """Predict whether to BLOCK or ALLOW a transaction.

    Expects payload to contain `nameOrig`, and optionally features.
    """
    user = payload.get("nameOrig")
    fs = FeatureStore()
    velocity = fs.get_velocity(user)

    # Prepare inputs for Triton (dummy shaping)
    triton = TritonClient()
    lstm_in = np.random.randn(1, 10, 8).astype(np.float32)
    gnn_in = np.random.randn(1, 16).astype(np.float32)

    try:
        lstm_score = float(triton.infer("lstm_fraud", [lstm_in])[0][0])
    except Exception:
        lstm_score = 0.0
    try:
        gnn_score = float(triton.infer("gnn_fraud", [gnn_in])[0][0])
    except Exception:
        gnn_score = 0.0

    # Ensemble: weighted by 0.6 LSTM, 0.4 GNN, and adjust slightly by velocity
    score = 0.6 * lstm_score + 0.4 * gnn_score + min(1.0, velocity / 100.0) * 0.1
    action = "BLOCK" if score > 0.5 else "ALLOW"
    return {"score": score, "action": action, "velocity": velocity}
