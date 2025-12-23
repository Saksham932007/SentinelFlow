from __future__ import annotations
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter('sentinelflow_requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('sentinelflow_request_latency_seconds', 'Request latency')

def start_metrics_server(port: int = 8003) -> None:
    start_http_server(port)
