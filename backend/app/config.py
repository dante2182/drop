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
    
    # Opcional: Ruta a un archivo de cookies para evitar bloqueos de sitios
    # como YouTube, Facebook, Instagram, etc.
    # Genera este archivo con: python export_cookies.py --all
    cookies_file: Optional[str] = None
    
    # Opcional: browser para extraer cookies automáticamente
    # Opciones: 'chrome', 'firefox', 'edge', 'safari', 'chromium', 'brave', 'opera'
    
settings = Settings()
