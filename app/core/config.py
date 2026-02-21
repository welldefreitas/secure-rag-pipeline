from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized environment configuration.

    Keep it small and explicit. Anything security-relevant must be validated here.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = Field(default="dev", alias="APP_ENV")
    app_name: str = Field(default="secure-rag-pipeline", alias="APP_NAME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # Auth
    jwt_secret: str = Field(default="change-me", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")

    # RAG
    vector_backend: str = Field(default="inmemory", alias="VECTOR_BACKEND")
    allowlist_sources: str = Field(default="", alias="ALLOWLIST_SOURCES")
    max_prompt_chars: int = Field(default=8000, alias="MAX_PROMPT_CHARS")
    top_k: int = Field(default=5, alias="TOP_K")

    # Optional vector db config
    qdrant_url: str = Field(default="http://qdrant:6333", alias="QDRANT_URL")

    @property
    def allowlist_sources_list(self) -> list[str]:
        if not self.allowlist_sources.strip():
            return []
        return [s.strip() for s in self.allowlist_sources.split(",") if s.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
