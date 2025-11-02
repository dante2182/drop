from pydantic import BaseModel, Field

class DownloadRequest(BaseModel):
    url: str = Field(..., description="La URL completa del video de YouTube")

class DownloadResponse(BaseModel):
    message: str = Field(..., description= "Mensaje de estado de la operacón.")
    title: str = Field(..., description="Título del video descargado.") 
    filepath: str = Field(..., description="Ruta del archivo descargado.")