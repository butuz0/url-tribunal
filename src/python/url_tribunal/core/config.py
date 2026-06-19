"""Application configuration management using Pydantic Settings v2."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class FlaskSettings(BaseSettings):
    """Flask specific configuration."""

    model_config = SettingsConfigDict(env_prefix='FLASK_')

    debug: bool = False
    secret_key: str


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


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Factory function to safely load settings without import-time side effects."""

    return Settings()
