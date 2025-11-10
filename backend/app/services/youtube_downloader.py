import asyncio
from yt_dlp import YoutubeDL
import os
from typing import Literal, Optional
import tempfile
from app.config import settings
import logging

logger = logging.getLogger(__name__)

AllowedFormat = Literal["mp4", "mp3"]

# Directorio por defecto donde se guardarán los videos si no se especifica otro
DEFAULT_DOWNLOAD_DIR = settings.download_dir # <-- Usar variable de entorno
os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)

# Configuración anti-bot mejorada para evitar bloqueos de YouTube
def get_base_ydl_opts(target_dir: str) -> dict:
    """
    Configuración base optimizada para evitar detección de bots por YouTube.
    Esta configuración es crítica para descargas en producción.
    """
    opts = {
        'outtmpl': os.path.join(target_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'force_overwrites': True,
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': False,
        
        # === CONFIGURACIÓN ANTI-BOT CRÍTICA ===
        # User-Agent de navegador moderno para evitar detección
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        
        # Headers HTTP realistas
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Connection': 'keep-alive',
        },
        
        # Configuración de extractor para YouTube
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web', 'ios'],  # Usar múltiples clientes
                'player_skip': ['webpage'],  # Optimización
            }
        },
        
        # Evitar restricciones de edad
        'age_limit': None,
        
        # Reintentos en caso de error temporal
        'retries': 10,
        'fragment_retries': 10,
        
        # Delays para evitar rate limiting
        'sleep_interval': 1,
        'max_sleep_interval': 5,
        
        # Ignorar errores de geo-restricción cuando sea posible
        'geo_bypass': True,
        'geo_bypass_country': 'US',
    }
    
    # === CONFIGURACIÓN DE COOKIES (CRÍTICO PARA EVITAR BOT DETECTION) ===
    # Si se especifica un archivo de cookies, úsalo
    if settings.youtube_cookies_file and os.path.exists(settings.youtube_cookies_file):
        opts['cookiefile'] = settings.youtube_cookies_file
        logger.info(f"Usando archivo de cookies: {settings.youtube_cookies_file}")
    # Si se especifica un navegador, extrae cookies automáticamente
    elif settings.youtube_cookies_browser:
        opts['cookiesfrombrowser'] = (settings.youtube_cookies_browser,)
        logger.info(f"Extrayendo cookies del navegador: {settings.youtube_cookies_browser}")
    else:
        logger.info("Sin cookies configuradas - usando solo headers anti-bot")
        logger.warning("Para mejor funcionamiento en producción, configura YOUTUBE_COOKIES_FILE")
    
    return opts

async def download_media_content(url: str, output_format: AllowedFormat, output_dir: Optional[str] = None) -> dict:
    """
    Descarga contenido multimedia en el formato solicitado y retorna metadatos.
    
    Implementa estrategias anti-bot avanzadas para evitar bloqueos de YouTube:
    - User-agents realistas
    - Headers HTTP apropiados
    - Múltiples clientes de player
    - Sistema de reintentos robusto

    - Si se proporciona `output_dir`, los archivos se guardan allí (p. ej., directorios temporales por solicitud).
    - Si no se proporciona, se usa el directorio por defecto del servidor.
    """

    def blocking_download():
        target_dir = output_dir or DEFAULT_DOWNLOAD_DIR
        os.makedirs(target_dir, exist_ok=True)
        
        # Obtener configuración base anti-bot
        ydl_opts = get_base_ydl_opts(target_dir)
        
        # Configuración específica según el formato
        if output_format == "mp3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'writethumbnail': True,  # Indicar que se descargue la portada
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192', # Calidad de audio
                    },
                    {
                        'key': 'EmbedThumbnail', # Incrustar la portada en el archivo de audio
                    }
                ],
            })
            ext = 'mp3'
        else:
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            })
            ext = 'mp4'
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                # Extraer información primero
                logger.info(f"Extrayendo información de: {url}")
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'video_sin_titulo')
                
                # Sanitizar el título para que sea un nombre de archivo válido
                sanitized_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '.', '_')).rstrip()
                ydl_opts['outtmpl'] = os.path.join(target_dir, f'{sanitized_title}.%(ext)s')
                
                # Descargar con la configuración actualizada
                logger.info(f"Iniciando descarga de: {sanitized_title}")
                with YoutubeDL(ydl_opts) as ydl2:
                    ydl2.download([url])
                
                filepath = os.path.join(target_dir, f"{sanitized_title}.{ext}")
                logger.info(f"Descarga completada: {filepath}")
                
                return {"title": sanitized_title, "filepath": filepath}
                
        except Exception as e:
            logger.error(f"Error durante la descarga: {str(e)}")
            # Re-lanzar la excepción para que sea manejada por el endpoint
            raise

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_download)
    return result