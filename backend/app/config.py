from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    allowed_origins_list: str

    download_dir: str = "downloads"

    api_version: str = "2025.2"

settings = Settings()
