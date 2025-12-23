from __future__ import annotations
import json
from typing import Dict, Any
from confluent_kafka import Producer
from .producer import TransactionProducer
from config.settings import settings


class KafkaTransactionProducer(TransactionProducer):
    """Kafka implementation of TransactionProducer using confluent-kafka."""

    def __init__(self, bootstrap_servers: str | None = None) -> None:
        brokers = bootstrap_servers or settings.kafka_bootstrap
        self.producer = Producer({"bootstrap.servers": brokers})

    def send(self, topic: str, record: Dict[str, Any]) -> None:
        payload = json.dumps(record, default=str)

        def _delivery(err: Exception | None, msg) -> None:
            if err:
                # In production we'd have retries and logging
                print(f"Delivery failed: {err}")

        self.producer.produce(topic, payload.encode("utf-8"), callback=_delivery)
        self.producer.poll(0)

    def close(self) -> None:
        self.producer.flush()
