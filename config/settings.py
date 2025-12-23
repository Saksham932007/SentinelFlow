from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment or .env.

    Attributes:
        kafka_bootstrap: Kafka bootstrap servers.
        redis_url: Redis connection URL.
        minio_endpoint: MinIO endpoint.
    """

    kafka_bootstrap: str = Field("localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    minio_endpoint: str = Field("http://localhost:9000", env="MINIO_ENDPOINT")
    minio_access_key: str = Field("minioadmin", env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field("minioadmin", env="MINIO_SECRET_KEY")

    class Config:
        env_file = ".env"


settings = Settings()
