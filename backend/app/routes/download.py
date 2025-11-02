from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.downloader import DownloadRequest, DownloadResponse
from app.services.youtube_downloader import download_youtube_video
import asyncio
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def download_task(url: str, output_format: str): # La función de fondo ahora acepta el formato
    try:
        # Pasa el formato a la función del servicio
        result = asyncio.run(download_youtube_video(url, output_format)) 
        logger.info(f"Descarga completada para '{result['title']}' en {result['filepath']}")
    except Exception as e:
        logger.error(f"Error durante la descarga de {url} en formato {output_format}: {e}")
        # Manejo de errores

@router.post("/download", response_model=DownloadResponse)
async def start_download(
    request: DownloadRequest, 
    background_tasks: BackgroundTasks
):
    """
    Inicia la descarga de un video de YouTube en el formato especificado en segundo plano.
    """
    # Se extraen los dos campos de la solicitud
    url = request.url
    output_format = request.output_format 

    # Se agregan los dos parámetros a la tarea de fondo
    background_tasks.add_task(download_task, url, output_format)
    
    return DownloadResponse(
        message=f"Descarga en formato '{output_format}' iniciada para la URL: {url}. El proceso se ejecutará en segundo plano.",
        title="N/A (La descarga se está procesando)",
        filepath="N/A (La descarga se está procesando)"
    )