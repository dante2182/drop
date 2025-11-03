from fastapi import FastAPI
from app.routes import download

# 1. Creación de la instancia de la aplicación
app = FastAPI(
    title="Universal Media Downloader API (Soporta YouTube, X, Instagram, etc.)",
    description="API usando FastAPI y yt-dlp para iniciar descargas de contenido multimedia de múltiples plataformas.",
    version="2025.2"
)

# 2. Inclusión de las rutas
app.include_router(download.router, tags=["Descarga de Video"])

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Visita /docs para ver la documentación de la API."}