import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

interface SelectFormatProps {
  value: 'mp4' | 'mp3'
  onValueChange: (value: 'mp4' | 'mp3') => void
}

export default function SelectFormat({ value, onValueChange }: SelectFormatProps) {
  return (
    <Select value={value} onValueChange={onValueChange}>
      <SelectTrigger className="w-[100px]">
        <SelectValue placeholder="Format" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="mp4">MP4</SelectItem>
        <SelectItem value="mp3">MP3</SelectItem>
      </SelectContent>
    </Select>
  )
}
