from __future__ import annotations
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI(title="SentinelFlow Serving")


class LatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        resp = await call_next(request)
        duration = (time.time() - start) * 1000
        # In production we'd use structured logging
        print(f"{request.method} {request.url.path} took {duration:.2f}ms")
        return resp


app.add_middleware(LatencyMiddleware)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
