from __future__ import annotations
from pyspark.sql import DataFrame
from pyspark.sql.functions import window, col, count


def velocity_aggregation(df: DataFrame, time_col: str = "step", window_minutes: int = 10) -> DataFrame:
    """Compute rolling count of transactions per `nameOrig` over a sliding window.

    Note: Assumes `step` is a monotonically increasing integer representing time buckets.
    In a production system you'd convert to timestamp; here we provide a generic example.
    """
    # In practice, transform 'step' to timestamp. For demo, use processing-time window.
    agg = (
        df.withColumn("ts", col("step").cast("long"))
        .groupBy(window(col("ts").cast("timestamp"), f"{window_minutes} minutes"), col("nameOrig"))
        .agg(count("*").alias("velocity_count"))
    )
    return agg
