import { ModeToggle } from '../mode-toggle'

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/10 dark:bg-black/10 backdrop-blur-md border-b border-white/20 dark:border-black/20 shadow-sm">
      <div className="w-full max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="text-2xl font-bold tracking-tighter text-gray-900 dark:text-gray-100">
            Drop
          </div>
          <div className="flex items-center gap-6">
            <a
              href="/"
              className="text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Home
            </a>
            <a
              href="/features"
              className="text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Features
            </a>
            <ModeToggle />
          </div>
        </div>
      </div>
    </header>
  )
}
