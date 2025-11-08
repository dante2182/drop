# Guía de Despliegue en Render - Solución Problema YouTube

## 🎯 Problema Solucionado

YouTube estaba bloqueando las descargas en producción con el error:
```
ERROR: Sign in to confirm you're not a bot
```

## ✅ Soluciones Implementadas

### 1. **Actualización de yt-dlp a última versión**
- Versión actualizada: `2025.10.22`
- YouTube actualiza constantemente sus protecciones anti-bot
- Las versiones antiguas son bloqueadas rápidamente

### 2. **Configuración Anti-Bot Avanzada**

Se han implementado las siguientes técnicas en `youtube_downloader.py`:

- ✅ **User-Agent realista**: Chrome 131 moderno
- ✅ **Headers HTTP apropiados**: Simulan un navegador real
- ✅ **Múltiples clientes de player**: `['android', 'web']`
- ✅ **Sistema de reintentos**: 10 intentos con delays inteligentes
- ✅ **Geo-bypass**: Evita restricciones geográficas
- ✅ **Sleep intervals**: Previene rate limiting

### 3. **Mejoras en Manejo de Errores**
- Mensajes de error más específicos y útiles
- Limpieza adecuada de archivos temporales
- Logging detallado para debugging

## 🚀 Configuración para Render

### Variables de Entorno Requeridas

En tu servicio de Render, configura estas variables de entorno:

```bash
# Backend
ALLOWED_ORIGINS_LIST=https://tu-frontend.onrender.com
DOWNLOAD_DIR=/tmp/downloads
API_VERSION=2025.2

# Frontend
VITE_API_URL=https://tu-backend.onrender.com
```

### Archivos Críticos para Render

#### `render.yaml` (en la raíz del proyecto)
```yaml
services:
  # Backend Service
  - type: web
    name: youtube-downloader-api
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: ALLOWED_ORIGINS_LIST
        sync: false
      - key: DOWNLOAD_DIR
        value: /tmp/downloads
      - key: API_VERSION
        value: 2025.2
    
  # Frontend Service
  - type: web
    name: youtube-downloader-frontend
    env: node
    buildCommand: cd frontend && yarn install && yarn build
    startCommand: cd frontend && yarn preview --host 0.0.0.0 --port $PORT
    envVars:
      - key: VITE_API_URL
        sync: false
```

### Instalación de FFmpeg en Render

Render puede requerir ffmpeg para conversiones de audio/video. Crea un archivo `render-build.sh`:

```bash
#!/bin/bash
# Instalar dependencias del sistema
apt-get update
apt-get install -y ffmpeg

# Instalar dependencias de Python
pip install -r requirements.txt
```

Luego en el `render.yaml`, usa:
```yaml
buildCommand: ./render-build.sh
```

## 🔧 Troubleshooting

### Si sigues teniendo problemas de bot detection:

1. **Actualiza yt-dlp regularmente** en Render:
   ```bash
   pip install --upgrade yt-dlp
   ```

2. **Prueba con diferentes videos**: Algunos videos tienen más protección que otros

3. **Considera implementar cookies** (opcional avanzado):
   - Exporta cookies de tu navegador usando extensión
   - Pasa las cookies a yt-dlp usando la opción `cookiefile`
   - Requiere actualizar el código para aceptar cookies del usuario

4. **Usa proxies** (opcional):
   - Configura proxies rotativos si el tráfico es alto
   - Agrega `proxy` en las opciones de yt-dlp

### Limitar Rate

Si experimentas bloqueos frecuentes, considera:

```python
# En youtube_downloader.py, aumentar los delays:
'sleep_interval': 3,
'max_sleep_interval': 10,
```

## 📊 Monitoreo

Para monitorear el estado de las descargas en producción:

1. Revisa los logs de Render regularmente
2. Implementa alertas para errores 500
3. Considera agregar rate limiting en el backend

## 🔄 Actualizaciones Futuras

YouTube cambia sus protecciones constantemente. Para mantener el servicio funcionando:

1. **Actualiza yt-dlp cada 2-4 semanas**:
   ```bash
   pip install --upgrade yt-dlp
   ```

2. **Monitorea el repositorio oficial**: https://github.com/yt-dlp/yt-dlp

3. **Lee los changelogs**: Busca "YouTube" en las notas de versión

## ⚠️ Notas Importantes

- **Uso Legal**: Asegúrate de cumplir con los Términos de Servicio de YouTube
- **Rate Limiting**: No hagas demasiadas peticiones simultáneas
- **Videos Privados**: No pueden descargarse por limitaciones de la API
- **Transmisiones en Vivo**: Solo funcionan una vez que terminan

## 📝 Checklist de Deployment

- [ ] Variables de entorno configuradas en Render
- [ ] FFmpeg instalado (para conversiones de audio)
- [ ] yt-dlp actualizado a última versión
- [ ] Archivos .env NO comprometidos en git (.gitignore configurado)
- [ ] Logs habilitados para debugging
- [ ] CORS configurado con el dominio de frontend correcto
- [ ] Directorio `/tmp/downloads` con permisos adecuados

## 🆘 Soporte

Si después de implementar estas soluciones sigues teniendo problemas:

1. Verifica que la versión de yt-dlp sea la más reciente
2. Revisa los logs completos del error
3. Prueba el mismo video en local vs producción
4. Considera implementar un sistema de cookies de usuario
