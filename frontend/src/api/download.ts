import axios from './axios'

export interface DownloadRequest {
  url: string
  output_format: 'mp4' | 'mp3'
}

export interface DownloadResponse {
  message: string
  title: string
  filepath: string
}

/**
 * Inicia la descarga de un video en el formato especificado
 * @param url - URL del video a descargar
 * @param format - Formato de salida (mp4 o mp3)
 * @returns Promise con la respuesta del servidor
 */
export const downloadMedia = async (
  url: string,
  format: 'mp4' | 'mp3'
): Promise<DownloadResponse> => {
  try {
    const response = await axios.post<DownloadResponse>('/download', {
      url,
      output_format: format,
    })
    return response.data
  } catch (error: any) {
    if (error.response) {
      // Error de respuesta del servidor
      throw new Error(
        error.response.data?.detail ||
          error.response.data?.message ||
          'Error al iniciar la descarga'
      )
    } else if (error.request) {
      // Error de red
      throw new Error('No se pudo conectar con el servidor')
    } else {
      // Otro tipo de error
      throw new Error(error.message || 'Error al iniciar la descarga')
    }
  }
}

/**
 * Descarga el archivo directamente y fuerza la descarga en el dispositivo del usuario.
 * Devuelve el nombre de archivo utilizado para la descarga.
 */
export const downloadMediaFile = async (
  url: string,
  format: 'mp4' | 'mp3'
): Promise<{ filename: string }> => {
  try {
    const response = await axios.post(
      '/download/file',
      { url, output_format: format },
      {
        responseType: 'blob',
      }
    )

    const disposition: string | undefined =
      response.headers['content-disposition']
    let filename = `download.${format}`
    if (disposition) {
      // RFC 5987 support: filename*=UTF-8''<urlencoded>
      const extMatch = /filename\*=([^']+)''([^;]+)/i.exec(disposition)
      if (extMatch && extMatch[2]) {
        try {
          filename = decodeURIComponent(extMatch[2])
        } catch {
          filename = extMatch[2]
        }
      } else {
        const match = /filename="?([^";]+)"?/i.exec(disposition)
        if (match && match[1]) {
          filename = match[1]
        }
      }
    }

    const blobUrl = window.URL.createObjectURL(response.data)
    const a = document.createElement('a')
    a.href = blobUrl
    a.download = filename
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(blobUrl)

    return { filename }
  } catch (error: any) {
    if (error.response) {
      throw new Error(
        error.response.data?.detail ||
          error.response.data?.message ||
          'Error al descargar el archivo'
      )
    } else if (error.request) {
      throw new Error('No se pudo conectar con el servidor')
    } else {
      throw new Error(error.message || 'Error al descargar el archivo')
    }
  }
}
