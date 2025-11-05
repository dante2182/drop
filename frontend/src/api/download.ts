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
        error.response.data?.detail || error.response.data?.message || 'Error al iniciar la descarga'
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
