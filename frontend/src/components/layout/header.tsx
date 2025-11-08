import { ModeToggle } from '../mode-toggle'

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-border bg-white/40 dark:bg-neutral-900/40 backdrop-blur-md shadow-sm">
      <div className="w-full max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-3">
          <a
            href="/"
            aria-label="Inicio"
            className="text-2xl font-bold tracking-tight text-foreground"
          >
            Drop
          </a>
          <nav
            aria-label="Principal"
            className="flex items-center gap-4 sm:gap-6"
          >
            <a
              href="/"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              aria-label="Ir a inicio"
            >
              Home
            </a>
            <a
              href="/features"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              aria-label="Ver características"
            >
              Features
            </a>
            <ModeToggle />
          </nav>
        </div>
      </div>
    </header>
  )
}
