"""Application configuration settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class FlaskSettings(BaseSettings):
    """Flask specific configuration."""

    model_config = SettingsConfigDict(env_prefix='FLASK_')

    debug: bool = False
    secret_key: str


class ProvidersSettings(BaseSettings):
    """Security scan providers configuration."""

    virustotal_api_key: str
    urlscan_api_key: str


class CelerySettings(BaseSettings):
    """Celery configuration."""

    model_config = SettingsConfigDict(env_prefix='CELERY_')

    broker_url: str
    result_backend: str
    task_serializer: str = 'json'
    result_serializer: str = 'json'
    accept_content: list[str] = ['json']
    worker_max_tasks_per_child: int = 1000
    result_chord_join_timeout: float = 600.0


class DBSettings(BaseSettings):
    """Database connection settings."""

    model_config = SettingsConfigDict(env_prefix='DB_')

    host: str
    port: int = Field(3306, ge=1, le=65535)
    name: str
    user: str
    password: str
    statement_timeout_ms: int = 5000


class Settings(BaseSettings):
    """Root settings aggregator."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    flask: FlaskSettings = Field(default_factory=FlaskSettings)
    db: DBSettings = Field(default_factory=DBSettings)
    celery: CelerySettings = Field(default_factory=CelerySettings)
    providers: ProvidersSettings = Field(default_factory=ProvidersSettings)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Factory function for settings loading."""

    return Settings()
