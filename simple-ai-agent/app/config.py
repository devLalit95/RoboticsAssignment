"""Configuration module - Load and validate environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    gemini_api_key: str = Field(..., description="Gemini API key for LLM")
    gemini_model: str = Field(default="gemini-1.5-pro", description="Gemini model name")


settings = Settings()
