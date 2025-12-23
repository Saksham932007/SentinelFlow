from __future__ import annotations
from typing import List
from pyspark.sql import SparkSession, DataFrame


def load_parquet_paths(paths: List[str], spark: SparkSession | None = None) -> DataFrame:
    """Load Parquet files from given s3a paths into a Spark DataFrame.

    Args:
        paths: List of s3a paths or local paths.
        spark: Optional SparkSession to use; will create one if not provided.
    """
    if spark is None:
        from processing.spark_utils import create_spark_session

        spark = create_spark_session()
    df = spark.read.parquet(*paths)
    return df
