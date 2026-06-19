"""Application configuration management using Pydantic Settings v2."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    db: DBSettings = Field(default_factory=DBSettings)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Factory function for loading settings."""

    return Settings()
