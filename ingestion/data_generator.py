import json
import random
import time
from dataclasses import dataclass, asdict
from typing import Iterator, Dict, Any


@dataclass
class Transaction:
    step: int
    type: str
    amount: float
    nameOrig: str
    nameDest: str
    isFraud: int


class TransactionGenerator:
    """Synthetic transaction generator inspired by PaySim.

    Yields Transaction objects.
    """

    TYPES = ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"]

    def __init__(self, seed: int = 42) -> None:
        random.seed(seed)
        self._step = 0

    def _sample_customer(self) -> str:
        return f"C{random.randint(1,10000):06d}"

    def next(self) -> Transaction:
        self._step += 1
        ttype = random.choices(self.TYPES, weights=[60,10,10,10,10])[0]
        amt = round(max(0.01, random.expovariate(1/50)), 2)
        orig = self._sample_customer()
        dest = self._sample_customer()
        is_fraud = 1 if (ttype == "TRANSFER" and amt > 2000 and random.random() < 0.05) else 0
        return Transaction(step=self._step, type=ttype, amount=amt, nameOrig=orig, nameDest=dest, isFraud=is_fraud)

    def stream(self, rate_per_sec: int = 100) -> Iterator[Dict[str, Any]]:
        """Yield dicts at approximately rate_per_sec events.

        Args:
            rate_per_sec: events to emit per second.
        """
        interval = 1.0 / max(1, rate_per_sec)
        while True:
            txn = self.next()
            yield asdict(txn)
            time.sleep(interval)


def to_json(record: Dict[str, Any]) -> str:
    return json.dumps(record, default=str)
