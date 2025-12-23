from __future__ import annotations
import time
import numpy as np
from serving.triton_client import TritonClient

def bench(model_name: str = "lstm_fraud", iters: int = 100):
    client = TritonClient()
    inp = np.random.randn(1,10,8).astype(np.float32)
    t0 = time.time()
    for _ in range(iters):
        client.infer(model_name, [inp])
    dt = time.time() - t0
    print(f"{iters} inferences in {dt:.2f}s -> {iters/dt:.2f} qps")

if __name__ == "__main__":
    bench()
