from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str = Field(default=...)
    page_urls_path: str = Field(default=...)
    domains_path: str = Field(default=...)
    skipped_urls_path: str = Field(default=...)
    users: list = Field(default=...)
    target_chat_id: str = Field(default=...)
    default_hashtag: str = Field(default=...)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
