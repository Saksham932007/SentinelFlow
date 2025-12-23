from __future__ import annotations
from typing import List, Tuple
import torch

class GNNDataset(torch.utils.data.Dataset):
    def __init__(self, edge_index: List[Tuple[int,int]], node_features: List[List[float]]):
        self.edge_index = edge_index
        self.node_features = torch.tensor(node_features, dtype=torch.float32)

    def __len__(self) -> int:
        return self.node_features.shape[0]

    def __getitem__(self, idx: int):
        return self.node_features[idx]
