export default function Footer() {
  return (
    <footer className="border-t mt-12 py-6">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-500">
        <p>
          ⭐ Simple designs. Stunning results | Dante Rodríguez -{' '}
          {new Date().getFullYear()}
        </p>
      </div>
    </footer>
  )
}
