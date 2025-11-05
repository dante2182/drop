import { Button } from '../ui/button'
import { Input } from '../ui/input'
import SelectFormat from './selectFormat'
import CardFile from './cardFile'
import { useState } from 'react'
import { downloadMediaFile } from '@/api/download'

export default function DownloadPage() {
  const [url, setUrl] = useState('')
  const [format, setFormat] = useState<'mp4' | 'mp3'>('mp4')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [downloads, setDownloads] = useState<
    Array<{
      id: number
      name: string
      url: string
      format: string
      status: string
    }>
  >([])
  const [success, setSuccess] = useState<string | null>(null)

  const handleDownload = async () => {
    if (!url.trim()) {
      setError('Por favor ingresa una URL válida')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const { filename } = await downloadMediaFile(url, format)

      const newDownload = {
        id: Date.now(),
        name: filename,
        url: url,
        format: format,
        status: 'Descargado',
      }

      setDownloads((prev) => [newDownload, ...prev])
      setSuccess(`Descarga completada: ${filename}`)
      setUrl('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al descargar')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !loading) {
      handleDownload()
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl">
          Descarga Fácil de Medios
        </h1>
        <p className="mt-3 max-w-2xl mx-auto text-lg text-gray-500 sm:mt-4">
          Pega un enlace de YouTube, Instagram, X u otra plataforma para
          descargar videos o música de forma rápida y sencilla.
        </p>
      </div>

      <div className="max-w-2xl mx-auto">
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-3">
            <Input
              placeholder="Pega tu enlace aquí..."
              className="flex-1 h-14 rounded-xl shadow-sm text-lg"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
            />
            <SelectFormat value={format} onValueChange={setFormat} />
          </div>

          <Button
            className="w-full h-12 rounded-xl shadow-lg text-lg font-semibold"
            onClick={handleDownload}
            disabled={loading || !url.trim()}
          >
            {loading ? 'Iniciando descarga...' : 'Descargar'}
          </Button>

          {error && (
            <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl">
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </div>
          )}

          {success && (
            <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-xl">
              <p className="text-sm text-green-600 dark:text-green-400">
                {success}
              </p>
            </div>
          )}

          {downloads.length > 0 && (
            <div className="flex flex-col gap-4 mt-8">
              <h3 className="text-2xl font-bold tracking-tighter">
                Descargas Recientes
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">
                {downloads.map((download) => (
                  <CardFile key={download.id} data={download} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
