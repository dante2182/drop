from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.downloader import DownloadRequest, DownloadResponse
from app.services.youtube_downloader import download_youtube_video
import asyncio
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Función para ejecutar en segundo plano después de enviar la respuesta
def download_task(url: str):
    try:
        # Aquí ejecutamos la lógica de descarga real
        result = asyncio.run(download_youtube_video(url))
        logger.info(f"Descarga completada para '{result['title']}' en {result['filepath']}")
    except Exception as e:
        logger.error(f"Error durante la descarga de {url}: {e}")
        # En una API real, aquí notificarías al usuario o registrarías el error

@router.post("/download", response_model=DownloadResponse)
async def start_download(
    request: DownloadRequest, 
    background_tasks: BackgroundTasks
):
    """
    Inicia la descarga de un video de YouTube en segundo plano.
    La API responde inmediatamente.
    """
    # NOTA: La descarga de videos puede tomar mucho tiempo y es una tarea
    # de larga duración. Usar BackgroundTasks permite a la API responder 
    # inmediatamente al cliente (HTTP 200) mientras la tarea se ejecuta.

    # Agrega la tarea de descarga a las tareas de fondo de FastAPI
    background_tasks.add_task(download_task, request.url)
    
    return DownloadResponse(
        message=f"Descarga iniciada para la URL: {request.url}. El proceso se ejecutará en segundo plano.",
        title="N/A (La descarga se está procesando)",
        filepath="N/A (La descarga se está procesando)"
    )