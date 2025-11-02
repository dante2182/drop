from pydantic import BaseModel, Field, conlist
from typing import Literal

AllowedFormat = Literal["mp4", "mp3"]

class DownloadRequest(BaseModel):
    url: str = Field(..., description="La URL completa del video de YouTube")
    output_format: AllowedFormat = Field(
        "mp4",
        description="Formato de salida deseado. 'mp4' (video) o 'mp3' (audio)."
    ) 

class DownloadResponse(BaseModel):
    message: str = Field(..., description= "Mensaje de estado de la operacón.")
    title: str = Field(..., description="Título del video descargado.") 
    filepath: str = Field(..., description="Ruta del archivo descargado.")