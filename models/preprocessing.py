from __future__ import annotations
from typing import Tuple, List
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def build_preprocessing_pipeline(numeric_features: List[str], categorical_features: List[str]) -> Pipeline:
    """Return a scikit-learn Pipeline to preprocess features.

    Args:
        numeric_features: list of numeric column names.
        categorical_features: list of categorical column names.
    """
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )
    pipeline = Pipeline(steps=[("preprocessor", preprocessor)])
    return pipeline
