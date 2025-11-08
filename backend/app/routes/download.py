from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from app.models.downloader import DownloadRequest, DownloadResponse
from app.services.youtube_downloader import download_media_content
import asyncio
import logging
import tempfile
import shutil
import os

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)

def download_task(url: str, output_format: str): # La función de fondo ahora acepta el formato
    try:
        # Pasa el formato a la función del servicio
        result = asyncio.run(download_media_content(url, output_format)) 
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


@router.post("/download/file")
async def download_file(request: DownloadRequest):
    """
    Descarga el contenido y lo devuelve como archivo adjunto en la respuesta HTTP
    para que el navegador del usuario lo guarde directamente en su dispositivo.
    No se persiste en el directorio de descargas del backend.
    """
    try:
        tmpdir = tempfile.mkdtemp()
        result = await download_media_content(request.url, request.output_format, output_dir=tmpdir)
        filepath = result["filepath"]
        filename = os.path.basename(filepath)

        media_type = "audio/mpeg" if request.output_format == "mp3" else "video/mp4"

        # Limpiar el directorio temporal una vez enviada la respuesta
        cleanup = BackgroundTask(shutil.rmtree, tmpdir, ignore_errors=True)

        # Exponer Content-Disposition para que el frontend pueda leer el nombre
        headers = {"Access-Control-Expose-Headers": "Content-Disposition"}

        return FileResponse(
            path=filepath,
            media_type=media_type,
            filename=filename,
            background=cleanup,
            headers=headers
        )
    except Exception as e:
        logging.exception("Error al realizar descarga directa")
        raise HTTPException(status_code=500, detail=f"Error al descargar el archivo: {str(e)}")