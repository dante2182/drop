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

      // Agregar a la lista de descargas con el nombre final
      const newDownload = {
        id: Date.now(),
        name: filename,
        url: url,
        format: format,
        status: 'Descargado',
      }

      setDownloads((prev) => [newDownload, ...prev])
      setSuccess(`Descarga completada: ${filename}`)
      setUrl('') // Limpiar el input
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
    <div className="w-full max-w-3xl mx-auto p-8">
      <div className="flex flex-col gap-6">
        <div className="flex items-center gap-3">
          <Input
            placeholder="Pega tu enlace aquí (YouTube, Instagram, X, etc.)"
            className="flex-1 h-12 rounded-xl shadow-sm"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
          />
          <SelectFormat value={format} onValueChange={setFormat} />
        </div>

        <Button
          className="self-start px-6 py-3 rounded-lg shadow"
          onClick={handleDownload}
          disabled={loading || !url.trim()}
        >
          {loading ? 'Iniciando descarga...' : 'Descargar'}
        </Button>

        {error && (
          <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}

        {success && (
          <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
            <p className="text-sm text-green-600 dark:text-green-400">
              {success}
            </p>
          </div>
        )}

        {downloads.length > 0 && (
          <div className="flex flex-col gap-3">
            <h3 className="text-lg font-semibold">Descargas</h3>
            {downloads.map((download) => (
              <CardFile key={download.id} data={download} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
