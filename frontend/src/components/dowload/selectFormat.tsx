import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export default function SelectFormat() {
  return (
    <Select>
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
