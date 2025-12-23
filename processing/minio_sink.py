from __future__ import annotations
from typing import Any
from pyspark.sql import DataFrame
from config.settings import settings


def write_raw_to_minio(batch_df: DataFrame, batch_id: int) -> None:
    """Write incoming raw events as Parquet to MinIO via s3a path.

    Requires Spark to be configured with MinIO credentials and s3a support.
    """
    # Example s3a path; bucket should exist beforehand
    path = f"s3a://sentinelflow/raw_events/partition={batch_id}"
    batch_df.write.mode("append").parquet(path)
