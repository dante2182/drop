export default function CardFile() {
  const data = [
    {
      id: 1,
      name: 'Regalame Aunque Sea Una Noche',
      url: 'https://www.youtube.com/watch?v=pzODP90Ewf4&list=RDGMEM2VCIgaiSqOfVzBAjPJm-agVMpzODP90Ewf4&start_radio=1',
      format: 'mp4',
    },
  ]
  return (
    <div className="flex items-center gap-4 p-3 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
        <svg
          className="w-6 h-6 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">
          {data[0].name}
        </p>
      </div>
      <p className="text-xs text-gray-500 uppercase tracking-wide">
        {data[0].format}
      </p>
    </div>
  )
}
