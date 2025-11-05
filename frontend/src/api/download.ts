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
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        error.response?.data?.detail || 'Error al iniciar la descarga'
      )
    }
    throw error
  }
}
