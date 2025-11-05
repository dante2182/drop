import asyncio
from yt_dlp import YoutubeDL
import os
from typing import Literal, Optional
import tempfile

AllowedFormat = Literal["mp4", "mp3"]

# Directorio por defecto donde se guardarán los videos si no se especifica otro
DEFAULT_DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)

async def download_media_content(url: str, output_format: AllowedFormat, output_dir: Optional[str] = None) -> dict:
    """
    Descarga contenido multimedia en el formato solicitado y retorna metadatos.

    - Si se proporciona `output_dir`, los archivos se guardan allí (p. ej., directorios temporales por solicitud).
    - Si no se proporciona, se usa el directorio por defecto del servidor.
    """

    def blocking_download():
        target_dir = output_dir or DEFAULT_DOWNLOAD_DIR
        os.makedirs(target_dir, exist_ok=True)
        if output_format == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(target_dir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192', # Calidad de audio
                }],
                'force_overwrites': True,
            }
            ext = 'mp3'
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': os.path.join(target_dir, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'force_overwrites': True,
            }
            ext = 'mp4'
        with YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'video_sin_titulo')
            # Sanitizar el título para que sea un nombre de archivo válido
            sanitized_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '.', '_')).rstrip()
            ydl_opts['outtmpl'] = os.path.join(target_dir, f'{sanitized_title}.%(ext)s')
            
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            filepath = os.path.join(target_dir, f"{sanitized_title}.{ext}")
            
            return {"title": sanitized_title, "filepath": filepath}

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_download)
    return result