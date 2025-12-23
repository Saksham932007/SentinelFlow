from __future__ import annotations
from typing import Any
import numpy as np

def detect_drift(reference: np.ndarray, current: np.ndarray) -> dict:
    """Very small drift detector using mean/variance difference as placeholder."""
    ref_mean = reference.mean(axis=0)
    cur_mean = current.mean(axis=0)
    delta = np.abs(cur_mean - ref_mean)
    return {"mean_delta": delta.tolist(), "drift": bool((delta > 0.1).any())}
