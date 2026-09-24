from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(
        default="Business Research AI",
        validation_alias="APP_NAME",
    )

    app_env: str = Field(
        default="development",
        validation_alias="APP_ENV",
    )

    debug: bool = Field(
        default=True,
        validation_alias="DEBUG",
    )

    openai_api_key: str = Field(
        validation_alias="OPENAI_API_KEY",
    )

    llm_model: str = Field(
        default="gpt-5.6-luna",
        validation_alias="LLM_MODEL",
    )

    llm_timeout: int = Field(
        default=60,
        validation_alias="LLM_TIMEOUT",
    )

    llm_max_retries: int = Field(
        default=2,
        validation_alias="LLM_MAX_RETRIES",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()