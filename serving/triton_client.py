from __future__ import annotations
from typing import Any, List
import numpy as np
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput
from config.settings import settings


class TritonClient:
    def __init__(self, url: str = "localhost:8001") -> None:
        self.client = InferenceServerClient(url=url)

    def infer(self, model_name: str, inputs: List[np.ndarray]) -> List[np.ndarray]:
        infer_inputs = []
        for i, arr in enumerate(inputs):
            inp = InferInput(f"input", arr.shape, "FP32")
            inp.set_data_from_numpy(arr.astype(np.float32))
            infer_inputs.append(inp)

        outputs = [InferRequestedOutput("score")]
        result = self.client.infer(model_name, infer_inputs, outputs=outputs)
        out = result.as_numpy("score")
        return out
