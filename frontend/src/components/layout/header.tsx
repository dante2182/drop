import { ModeToggle } from '../mode-toggle'

export default function header() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 flex justify-between items-center px-6 py-3 bg-white/10 dark:bg-black/10 backdrop-blur-md border-b border-white/20 dark:border-black/20 shadow-sm">
      <div className="text-xl font-light tracking-wider text-gray-900 dark:text-gray-100">
        drop
      </div>
      <div className="flex items-center gap-6">
        <a
          href="/"
          className="text-sm text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
        >
          Home
        </a>
        <a
          href="/features"
          className="text-sm text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
        >
          Features
        </a>
        <ModeToggle />
      </div>
    </nav>
  )
}
