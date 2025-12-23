from __future__ import annotations
import json
from typing import Any, Optional
import redis
from config.settings import settings


class FeatureStore:
    """Simple FeatureStore client to read velocity counts from Redis."""

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None) -> None:
        self._r = redis.Redis(host=host or settings.redis_host, port=port or settings.redis_port)

    def get_velocity(self, user_id: str) -> int:
        key = f"velocity:{user_id}"
        raw = self._r.get(key)
        if not raw:
            return 0
        payload = json.loads(raw)
        return int(payload.get("velocity_count", 0))
