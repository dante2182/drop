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
    
    # Opcional: ruta a archivo de cookies para evitar bot detection de YouTube
    # Genera cookies desde tu navegador usando: 
    # chrome -> yt-dlp --cookies-from-browser chrome
    # firefox -> yt-dlp --cookies-from-browser firefox  
    youtube_cookies_file: Optional[str] = None
    
    # Opcional: browser para extraer cookies automáticamente
    # Opciones: 'chrome', 'firefox', 'edge', 'safari', 'chromium', 'brave', 'opera'
    youtube_cookies_browser: Optional[str] = None

settings = Settings()
