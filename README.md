# SentinelFlow

Distributed real-time fraud detection reference implementation.

## Architecture

Mermaid diagram (high level):

```mermaid
flowchart LR
	Producer[Producer\n(ingestion)] -->|raw-transactions| Kafka((Kafka))
	Kafka --> Spark[Processing\n(Spark Structured Streaming)]
	Spark --> MinIO[MinIO Data Lake]
	Spark --> Redis[Redis Feature Store]
	Models[Models\n(LSTM + GNN)] -->|ONNX| Triton[Triton Server]
	FastAPI --> Triton
	FastAPI --> Redis
	Prometheus --> Triton
	Grafana --> Prometheus
```

## Tech Stack

- Kafka (Confluent images)
- Spark Structured Streaming (PySpark)
- Redis (feature store)
- MinIO (data lake)
- PyTorch (LSTM) + PyG (GNN)
- ONNX + Triton Inference Server
- FastAPI for serving
- Prometheus + Grafana for observability

## Getting Started (local)

1. Start services:

```bash
cd deploy
docker-compose up -d
```

2. Produce synthetic transactions:

```bash
python -m ingestion.main --rate 100 --topic raw-transactions
```

3. Run Spark processing (ensure `pyspark` configured with s3a if using MinIO):

```bash
python -m processing.main
```

4. Train models (toy example):

```bash
python -m models.train --out models/artifacts
python -m models.export_onnx
```

5. Start API server:

```bash
uvicorn serving.app:app --host 0.0.0.0 --port 8080
```

6. Query prediction:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"nameOrig": "C000001"}' http://localhost:8080/predict
```

## Notes

- Some components (PyG, Triton GPU image) may require additional setup or GPU-enabled hosts.
- The repository focuses on architecture and integration patterns; adapt resource configs for production.
