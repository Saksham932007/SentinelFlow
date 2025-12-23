from __future__ import annotations
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from typing import Dict, Any
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent / "schemas" / "transaction.avsc"


class AvroTransactionProducer:
    """Lightweight Avro producer that registers/uses schema in Schema Registry.

    Note: Requires `schema.registry.url` in config.
    """

    def __init__(self, config: Dict[str, Any]):
        with open(SCHEMA_PATH, "r") as f:
            schema_str = f.read()
        self.value_schema = avro.loads(schema_str)
        self.producer = AvroProducer(config, default_value_schema=self.value_schema)

    def send(self, topic: str, record: Dict[str, Any]) -> None:
        self.producer.produce(topic=topic, value=record)
        self.producer.flush()
