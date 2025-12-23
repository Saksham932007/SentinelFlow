"""Entrypoint to run the transaction generator and publish to Kafka."""
from __future__ import annotations
import argparse
from ingestion.data_generator import TransactionGenerator, to_json
from ingestion.kafka_producer import KafkaTransactionProducer


def run(rate: int, topic: str, brokers: str | None = None) -> None:
    gen = TransactionGenerator()
    producer = KafkaTransactionProducer(bootstrap_servers=brokers)
    try:
        for record in gen.stream(rate_per_sec=rate):
            producer.send(topic, record)
    except KeyboardInterrupt:
        print("Shutting down producer")
    finally:
        producer.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rate", type=int, default=100)
    parser.add_argument("--topic", type=str, default="raw-transactions")
    parser.add_argument("--brokers", type=str, default=None)
    args = parser.parse_args()
    run(args.rate, args.topic, args.brokers)


if __name__ == "__main__":
    main()
