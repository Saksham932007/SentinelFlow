# Ingestion

Run the synthetic transaction producer to publish events to Kafka.

Example:

```bash
python -m ingestion.main --rate 100 --topic raw-transactions
```
