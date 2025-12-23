from __future__ import annotations
from processing.spark_utils import create_spark_session
from processing.stream_processor import read_kafka_stream
from processing.feature_engineering import velocity_aggregation
from processing.redis_sink import write_to_redis
from processing.minio_sink import write_raw_to_minio
from config.settings import settings


def main() -> None:
    spark = create_spark_session()
    df = read_kafka_stream(spark, settings.kafka_bootstrap, "raw-transactions")

    # Write raw events to MinIO
    raw_query = (
        df.writeStream
        .foreachBatch(write_raw_to_minio)
        .outputMode("append")
        .start()
    )

    # Compute velocity aggregates and write to Redis
    agg = velocity_aggregation(df)
    agg_query = (
        agg.writeStream
        .foreachBatch(write_to_redis)
        .outputMode("update")
        .start()
    )

    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()
