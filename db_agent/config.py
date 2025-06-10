import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LLM_MODEL: str
    LLM_API_KEY: str
    LLM_API_BASE: str

    MCP_SERVER_URL: str = "http://localhost:8001/mcp"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
