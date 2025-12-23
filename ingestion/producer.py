from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any


class TransactionProducer(ABC):
    """Abstract interface for transaction producers.

    Implementations should provide `send` and `close` methods.
    """

    @abstractmethod
    def send(self, topic: str, record: Dict[str, Any]) -> None:
        """Send a single transaction record to `topic`.

        Args:
            topic: Kafka topic or equivalent sink name.
            record: Serialized transaction dictionary.
        """

    @abstractmethod
    def close(self) -> None:
        """Close any underlying connections/resources."""
