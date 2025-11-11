"""
Script auxiliar para exportar cookies desde tu navegador.
Esto es CRUCIAL para descargar contenido de sitios que requieren inicio de sesión
como Facebook, Instagram, X, TikTok, y para evitar la detección de bots en YouTube.

Uso:
    # Exportar cookies de todos los sitios (recomendado)
    python export_cookies.py [navegador] --all

    # Exportar solo cookies de YouTube (legado)
    python export_cookies.py [navegador]
El archivo de cookies se guardará en: youtube_cookies.txt
"""

import sys
import subprocess
import os

def export_cookies(browser='chrome', all_sites=False):
    """Exporta cookies usando yt-dlp"""
    output_file = 'youtube_cookies.txt'
    
    if all_sites:
        print(f"🍪 Exportando cookies de TODOS los sitios desde '{browser}'...")
        print("⚠️  Asegúrate de haber iniciado sesión en Facebook, Instagram, TikTok, etc. en tu navegador.")
        # No se necesita una URL de prueba cuando se usa --all-cookies
        target_url_arg = ['--all-cookies']
    else:
        print(f"🍪 Exportando cookies de YouTube desde '{browser}'...")
        print("⚠️  Asegúrate de haber iniciado sesión en YouTube en tu navegador.")
        # Video de prueba para forzar la extracción de cookies de YouTube
        target_url_arg = ['https://www.youtube.com/watch?v=jNQXAC9IVRw']

    print()
    
    try:
        # Comando para exportar cookies
        cmd = [
            'yt-dlp',
            '--cookies-from-browser', browser, 
            '--cookies', output_file,
            '--skip-download',
            '--no-warnings',
        ] + target_url_arg
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"✅ Cookies exportadas exitosamente a: {output_file}")
            print()
            print("📝 Próximos pasos:")
            print("1. Copia el archivo 'youtube_cookies.txt' a tu servidor de producción")
            print("2. Configura la variable de entorno:")
            print(f"   COOKIES_FILE=/ruta/a/youtube_cookies.txt")
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
    
    args = sys.argv[1:]
    browser = 'chrome' # Default
    all_sites = '--all' in args

    browser_args = [arg for arg in args if not arg.startswith('--')]
    if browser_args:
        browser = sys.argv[1].lower()
        if browser not in browsers:
            print(f"❌ Navegador no soportado: {browser}")
            print(f"✅ Navegadores soportados: {', '.join(browsers)}")
            sys.exit(1)
    
    print(f"ℹ️  Usando navegador: '{browser}'")
    print(f"   Para usar otro: python export_cookies.py [nombre_navegador]")
    print()
    
    success = export_cookies(browser, all_sites=all_sites)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
