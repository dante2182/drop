import asyncio
from yt_dlp import YoutubeDL
import os

# Directorio donde se guardarán los videos
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")

# Asegura que el directorio exista
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def download_youtube_video(url: str) -> dict:
    """
    Descarga un video de YouTube usando yt-dlp en un thread separado.
    Retorna el título y la ruta del archivo.
    """
    # Función de I/O bloqueante que ejecutaremos en un thread
    def blocking_download():
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4', # Forzar la conversión a mp4
            'noplaylist': True,
            'force_overwrites': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            # Extraer la información primero para obtener el título
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'video_sin_titulo')
            
            # Ejecutar la descarga real
            ydl.download([url])
            
            # Construir la ruta final esperada
            filepath = os.path.join(DOWNLOAD_DIR, f"{video_title}.mp4")
            
            return {"title": video_title, "filepath": filepath}

    # Ejecuta la función de descarga en un thread pool, 
    # liberando el event loop de FastAPI (async/await)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_download)
    return result