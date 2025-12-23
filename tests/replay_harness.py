"""Simple replay harness to read Parquet events and push them into Kafka for testing."""
from __future__ import annotations
from typing import List
import time
from ingestion.kafka_producer import KafkaTransactionProducer
from pyspark.sql import SparkSession

def replay(parquet_paths: List[str], topic: str = "raw-transactions", rate: float = 100.0) -> None:
    spark = SparkSession.builder.appName("replay_harness").getOrCreate()
    df = spark.read.parquet(*parquet_paths)
    producer = KafkaTransactionProducer()
    interval = 1.0 / rate
    for row in df.toLocalIterator():
        producer.send(topic, row.asDict())
        time.sleep(interval)
