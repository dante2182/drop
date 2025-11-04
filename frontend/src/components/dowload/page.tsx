import { Button } from '../ui/button'
import { Input } from '../ui/input'
import SelectFormat from './selectFormat'
import CardFile from './cardFile'

export default function DownloadPage() {
  return (
    <div className="w-full max-w-3xl mx-auto p-8">
      <div className="flex flex-col gap-6">
        <div className="flex items-center gap-3">
          <Input
            placeholder="Pega tu enlace aquí"
            className="flex-1 h-12 rounded-xl shadow-sm"
          />
          <SelectFormat />
        </div>
        <Button className="self-start px-6 py-3 rounded-lg shadow">
          Descargar
        </Button>
        <CardFile />
      </div>
    </div>
  )
}
