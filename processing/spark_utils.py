from typing import Any
from pyspark.sql import SparkSession


def create_spark_session(app_name: str = "sentinelflow-processing") -> SparkSession:
    """Create and return a SparkSession configured for Kafka integration.

    Args:
        app_name: Spark application name.
    """
    spark = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.driver.memory", "2g")
        .config("spark.executor.memory", "2g")
        .getOrCreate()
    )
    return spark
