export default function Footer() {
  return (
    <footer className="fixed inset-x-0 bottom-0 backdrop-blur-sm bg-background/70">
      <div className="w-full mx-auto px-4 sm:px-6 lg:px-8">
        <div className="border-border border-t border-solid py-4 text-center">
          <p className="text-xs sm:text-sm text-muted-foreground">
            ⭐ Simple designs. Stunning results | Dante Rodríguez —{' '}
            {new Date().getFullYear()}
          </p>
        </div>
      </div>
    </footer>
  )
}
