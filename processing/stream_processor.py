from __future__ import annotations
from typing import Optional
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType


TRANSACTION_SCHEMA = StructType(
    [
        StructField("step", IntegerType()),
        StructField("type", StringType()),
        StructField("amount", DoubleType()),
        StructField("nameOrig", StringType()),
        StructField("nameDest", StringType()),
        StructField("isFraud", IntegerType()),
    ]
)


def read_kafka_stream(spark: SparkSession, bootstrap_servers: str, topic: str) -> DataFrame:
    """Read a Kafka topic as a DataFrame of parsed transactions."""
    df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", topic)
        .option("startingOffsets", "earliest")
        .load()
    )
    json_df = df.select(from_json(col("value").cast("string"), TRANSACTION_SCHEMA).alias("data"))
    parsed = json_df.select("data.*")
    return parsed
