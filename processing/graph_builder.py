from __future__ import annotations
from typing import List, Tuple
from pyspark.sql import DataFrame

def build_transaction_graph(df: DataFrame) -> Tuple[List, List]:
    """Build edge list and node features from transactions DataFrame.

    Returns (edge_index, node_features) placeholders for GNN training.
    """
    # Example: collect a small sample and build simple mappings
    rows = df.limit(1000).collect()
    nodes = {}
    edges = []
    feats = []
    for r in rows:
        src = r['nameOrig']
        dst = r['nameDest']
        if src not in nodes:
            nodes[src] = len(nodes)
            feats.append([0.0])
        if dst not in nodes:
            nodes[dst] = len(nodes)
            feats.append([0.0])
        edges.append((nodes[src], nodes[dst]))
    return edges, feats
