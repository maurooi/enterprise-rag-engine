from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    app_name: str
    app_env: Literal["development", "staging", "production"]
    openai_api_key: SecretStr
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: SecretStr
    postgres_db: str
    version: str

    @property
    def async_database_url(self) -> str:
        """Assembles and returns the database URL"""
        url = (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password.get_secret_value()}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

        return url


@lru_cache
def get_settings() -> Settings:
    """Loads and returns settings as a Settings object"""
    return Settings()
