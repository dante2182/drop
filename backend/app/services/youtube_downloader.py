import asyncio
from yt_dlp import YoutubeDL
import os
from typing import Literal

AllowedFormat = Literal["mp4", "mp3"]

# Directorio donde se guardarán los videos
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def download_youtube_video(url: str, output_format: AllowedFormat) -> dict:

    def blocking_download():
        if output_format == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
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
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'force_overwrites': True,
            }
            ext = 'mp4'
        with YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'video_sin_titulo')
            
            ydl.download([url])
            
            filepath = os.path.join(DOWNLOAD_DIR, f"{video_title}.{ext}")
            
            return {"title": video_title, "filepath": filepath}

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_download)
    return result