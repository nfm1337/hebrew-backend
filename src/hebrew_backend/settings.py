from typing import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    database_url: str = ""

    anthropic_api_key: str = ""
    google_api_key: str = ""
    openai_api_key: str = ""

    debug: bool = False
    port: int = 8000

    @model_validator(mode="after")
    def validate_at_least_one_llm_key(self) -> Self:
        if not any([self.anthropic_api_key, self.google_api_key, self.openai_api_key]):
            raise ValueError(
                "At least one LLM API must be set: "
                "ANTHROPIC_API_KEY, GOOGLE_API_KEY or OPENAI_API_KEY"
            )
        return self

    @model_validator(mode="after")
    def compose_database_url(self) -> Self:
        if not self.database_url:
            url = URL.create(
                drivername="postgresql+asyncpg",
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                database=self.postgres_db,
            )
            self.database_url = url.render_as_string(hide_password=False)
        return self


settings = Settings()  # pyright: ignore[reportCallIssue]
