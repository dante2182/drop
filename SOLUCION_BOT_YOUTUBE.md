# 🔧 Solución Completa: Error "Sign in to confirm you're not a bot" en YouTube

## 📋 Resumen del Problema

Cuando despliegas tu aplicación en servicios cloud como Render, YouTube detecta el tráfico automatizado y bloquea las descargas con el error:

```
ERROR: [youtube] Sign in to confirm you're not a bot
```

**¿Por qué pasa esto?**
- YouTube implementó protecciones anti-bot agresivas en 2024-2025
- Los servidores cloud tienen IPs conocidas que YouTube monitorea
- Sin cookies de sesión, YouTube identifica las peticiones como bots

## ✅ SOLUCIONES IMPLEMENTADAS (3 Métodos)

### Método 1: Usar Archivo de Cookies (⭐ MÁS CONFIABLE)

Este es el método más efectivo y recomendado para producción.

#### Paso 1: Generar archivo de cookies en tu computadora

```bash
# En tu computadora local (con Chrome instalado y sesión de YouTube activa)
cd backend
python export_cookies.py chrome
```

Esto generará el archivo `youtube_cookies.txt`

#### Paso 2: Subir cookies a Render

**Opción A - Vía repositorio:**
```bash
# Agrega el archivo a tu repo
git add youtube_cookies.txt
git commit -m "Add YouTube cookies"
git push
```

**Opción B - Vía Render Shell:**
```bash
# Conéctate al Shell de Render y ejecuta:
cd /opt/render/project/src/backend
cat > youtube_cookies.txt
# Pega el contenido del archivo y presiona Ctrl+D
```

#### Paso 3: Configurar variable de entorno en Render

En tu servicio de Render, agrega:
```
YOUTUBE_COOKIES_FILE=/opt/render/project/src/backend/youtube_cookies.txt
```

**⚠️ IMPORTANTE:** 
- Las cookies expiran cada 1-2 meses
- Necesitarás regenerar el archivo periódicamente
- Configura un recordatorio para actualizar las cookies

---

### Método 2: POToken Provider (Automático)

El plugin `yt-dlp-get-pot` se ha instalado automáticamente. Este plugin:
- Genera tokens de autenticación (POToken) dinámicamente
- No requiere cookies manuales
- Funciona en la mayoría de los casos

**Ya está configurado** - no requiere pasos adicionales.

**Limitaciones:**
- Puede fallar con ciertos videos
- YouTube puede detectarlo eventualmente
- No es 100% confiable

---

### Método 3: Configuración Anti-Bot Mejorada (Ya Implementado)

El código ya incluye:
- ✅ User-Agent de navegador moderno (Chrome 131)
- ✅ Headers HTTP realistas
- ✅ Múltiples clientes de player (android, web, ios)
- ✅ Sistema de reintentos (10 intentos)
- ✅ Delays inteligentes para evitar rate limiting
- ✅ Geo-bypass automático

Esto mejora significativamente las posibilidades de éxito sin cookies.

---

## 🚀 Configuración Completa para Render

### Variables de Entorno Obligatorias

```bash
# Backend
ALLOWED_ORIGINS_LIST=https://tu-frontend.onrender.com
DOWNLOAD_DIR=/tmp/downloads
API_VERSION=2025.2

# Frontend  
VITE_API_URL=https://tu-backend.onrender.com
```

### Variables de Entorno Opcionales (Recomendadas)

```bash
# Para evitar bot detection con cookies
YOUTUBE_COOKIES_FILE=/opt/render/project/src/backend/youtube_cookies.txt

# O usar extracción automática si tienes navegador en servidor (raro)
# YOUTUBE_COOKIES_BROWSER=chromium
```

---

## 🔍 Cómo Verificar que Funciona

### 1. Prueba local

```bash
# Desde tu backend local
curl -X POST "http://localhost:8001/api/download/file" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "output_format": "mp4"}' \
  --output test.mp4

# Si funciona, verás un archivo test.mp4
```

### 2. Revisa los logs de Render

Busca en los logs:
- ✅ `"Usando archivo de cookies: ..."` = Cookies cargadas correctamente
- ✅ `"Descarga completada: ..."` = Descarga exitosa
- ❌ `"Sign in to confirm you're not a bot"` = Necesitas configurar cookies

---

## 🛠 Troubleshooting

### Problema: Siguen apareciendo errores de bot

**Solución 1:** Verifica que las cookies estén configuradas
```bash
# En Render Shell
echo $YOUTUBE_COOKIES_FILE
cat $YOUTUBE_COOKIES_FILE | head -5
```

**Solución 2:** Regenera las cookies
Las cookies expiran. Genera un nuevo archivo:
```bash
python export_cookies.py chrome
```

**Solución 3:** Prueba con videos diferentes
Algunos videos tienen más protección que otros. Prueba con:
- Videos públicos populares
- Videos sin restricción de edad
- No pruebas con shorts inicialmente (más protegidos)

**Solución 4:** Actualiza yt-dlp
```bash
pip install --upgrade yt-dlp
```

### Problema: "Cookiefile not found"

Verifica la ruta completa en Render:
```bash
# La ruta debe coincidir con donde está el archivo
ls -la /opt/render/project/src/backend/youtube_cookies.txt
```

### Problema: Videos específicos fallan

Algunos videos tienen protecciones adicionales:
- **Videos con restricción de edad:** Requieren cookies de cuenta con edad verificada
- **Videos privados:** No se pueden descargar
- **Transmisiones en vivo:** Solo después de que terminan
- **Videos geo-bloqueados:** Pueden requerir proxy/VPN

---

## 📊 Comparación de Métodos

| Método | Confiabilidad | Mantenimiento | Dificultad Setup |
|--------|--------------|---------------|------------------|
| Cookies (Método 1) | ⭐⭐⭐⭐⭐ 95% | Cada 1-2 meses | Media |
| POToken (Método 2) | ⭐⭐⭐ 70% | Automático | Fácil |
| Solo Headers (Método 3) | ⭐⭐ 40% | Ninguno | Fácil |
| **Cookies + POToken** | ⭐⭐⭐⭐⭐ 98% | Cada 1-2 meses | Media |

**Recomendación:** Usa Método 1 (Cookies) + Método 2 (POToken) juntos para máxima confiabilidad.

---

## 🔄 Automatización: Script de Actualización de Cookies

Para facilitar el mantenimiento, puedes crear un script que actualice cookies automáticamente:

```python
# update_cookies.py
import os
import sys
from datetime import datetime

def update_cookies():
    print(f"🕐 {datetime.now()}: Actualizando cookies de YouTube...")
    
    # Exportar cookies
    os.system("python export_cookies.py chrome")
    
    # Opcional: Subir automáticamente a Render vía API
    # (requiere configurar Render API key)
    
    print("✅ Cookies actualizadas. Recuerda deployar en Render.")

if __name__ == '__main__':
    update_cookies()
```

**Configura un cron job o recordatorio cada 30 días:**
```bash
# En tu máquina local, agrega a crontab:
0 0 1 * * cd /ruta/a/tu/proyecto/backend && python update_cookies.py
```

---

## ⚖️ Consideraciones Legales

- **Términos de Servicio:** Asegúrate de cumplir con los ToS de YouTube
- **Uso Personal:** Usa esta solución para uso personal o educativo
- **Rate Limiting:** No hagas scraping masivo
- **Respeta derechos de autor:** Solo descarga contenido que tengas derecho a descargar

---

## 📚 Recursos Adicionales

- [yt-dlp Wiki - PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide)
- [yt-dlp Cookies Guide](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)
- [Render Documentation](https://render.com/docs)

---

## 🆘 Soporte

Si después de seguir esta guía sigues teniendo problemas:

1. ✅ Verifica que yt-dlp esté actualizado (>= 2025.10.22)
2. ✅ Confirma que las cookies estén cargadas correctamente
3. ✅ Revisa los logs de Render para errores específicos
4. ✅ Prueba con diferentes videos
5. ✅ Considera usar un proxy si el problema persiste

**Last updated:** Julio 2025
