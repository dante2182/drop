from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import download

# 1. Creación de la instancia de la aplicación
app = FastAPI(
    title="Universal Media Downloader API (Soporta YouTube, X, Instagram, etc.)",
    description="API usando FastAPI y yt-dlp para iniciar descargas de contenido multimedia de múltiples plataformas.",
    version="2025.2"
)

# Allow client side to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Inclusión de las rutas
app.include_router(download.router, tags=["Descarga de Video"])

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Visita /docs para ver la documentación de la API."}