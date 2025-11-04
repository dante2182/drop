export default function footer() {
  return (
    <div className="container max-w-4xl flex-1 flex flex-col items-center mx-auto my-10">
      <div className="flex justify-between w-full">
        <p>⭐ Simple designs. Stunning results</p>
        <div className="flex gap-2 items-center">
          <h2>Dante Rodríguez</h2>
          <span>-</span>
          <p>{new Date().getFullYear()}</p>
        </div>
      </div>
    </div>
  )
}
