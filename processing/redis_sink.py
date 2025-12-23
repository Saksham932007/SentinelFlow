from __future__ import annotations
import json
from typing import Any
import redis
from pyspark.sql import DataFrame
from config.settings import settings


def write_to_redis(batch_df: DataFrame, batch_id: int) -> None:
    """Write aggregated velocity counts to Redis within foreachBatch.

    Keys: velocity:{nameOrig}
    Value: JSON payload with latest window and count.
    """
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port)
    rows = batch_df.collect()
    pipe = r.pipeline()
    for row in rows:
        name = row['nameOrig']
        count = int(row['velocity_count'])
        payload = json.dumps({"velocity_count": count})
        pipe.set(f"velocity:{name}", payload)
    pipe.execute()
