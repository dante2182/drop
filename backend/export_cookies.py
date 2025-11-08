#!/usr/bin/env python3
"""
Script auxiliar para exportar cookies de YouTube desde tu navegador.
Esto resuelve el problema de bot detection en producción.

Uso:
    python export_cookies.py [chrome|firefox|edge|safari]

El archivo de cookies se guardará en: youtube_cookies.txt
"""

import sys
import subprocess
import os

def export_cookies(browser='chrome'):
    """Exporta cookies de YouTube usando yt-dlp"""
    output_file = 'youtube_cookies.txt'
    
    print(f"🍪 Exportando cookies de YouTube desde {browser}...")
    print("⚠️  Asegúrate de haber iniciado sesión en YouTube en tu navegador.")
    print()
    
    try:
        # Comando para exportar cookies
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', browser,
            '--cookies', output_file,
            '--skip-download',
            '--no-warnings',
            'https://www.youtube.com/watch?v=jNQXAC9IVRw'  # Video de prueba
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if os.path.exists(output_file):
            print(f"✅ Cookies exportadas exitosamente a: {output_file}")
            print()
            print("📝 Próximos pasos:")
            print("1. Copia el archivo 'youtube_cookies.txt' a tu servidor de producción")
            print("2. Configura la variable de entorno:")
            print(f"   YOUTUBE_COOKIES_FILE=/ruta/a/youtube_cookies.txt")
            print()
            print("⚠️  IMPORTANTE: Las cookies expiran. Regenera este archivo cada 1-2 meses.")
            return True
        else:
            print(f"❌ Error al exportar cookies")
            print(f"Salida: {result.stdout}")
            print(f"Error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Error: yt-dlp no está instalado")
        print("Instálalo con: pip install yt-dlp")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    browsers = ['chrome', 'firefox', 'edge', 'safari', 'brave', 'opera', 'chromium']
    
    if len(sys.argv) > 1:
        browser = sys.argv[1].lower()
        if browser not in browsers:
            print(f"❌ Navegador no soportado: {browser}")
            print(f"✅ Navegadores soportados: {', '.join(browsers)}")
            sys.exit(1)
    else:
        browser = 'chrome'  # Default
        print(f"ℹ️  Usando navegador por defecto: {browser}")
        print(f"   Para usar otro: python export_cookies.py [browser]")
        print()
    
    success = export_cookies(browser)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
