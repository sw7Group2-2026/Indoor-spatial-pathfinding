import { useState } from 'react'

const floors = [0, 1, 2]

export default function App() {
  const [selectedFloor, setSelectedFloor] = useState(0)

  return (
    <main className="mx-auto max-w-xl p-4">
      <div className="relative aspect-[4/3] rounded-xl bg-gray-200">
        {/* Add the Leaflet map here. */}
        <div className="absolute bottom-3 right-3 grid gap-2">
          {floors.map((floor) => (
            <button
              key={floor}
              type="button"
              aria-pressed={selectedFloor === floor}
              onClick={() => setSelectedFloor(floor)}
              className="size-11 rounded-full bg-white aria-pressed:bg-gray-900 aria-pressed:text-white"
            >
              {floor}
            </button>
          ))}
        </div>
      </div>

      <form className="mt-4" onSubmit={(event) => event.preventDefault()}>
        <label htmlFor="query" className="mb-2 block">
          Where do you want to go?
        </label>

        <div className="flex gap-2">
          <input
            id="query"
            name="query"
            placeholder="Where’s the nearest toilet?"
            className="min-w-0 flex-1 rounded-lg border border-gray-300 px-3"
          />
          <button type="submit" className="min-h-11 rounded-lg bg-gray-900 px-3 text-white">
            Find route
          </button>
        </div>
      </form>
    </main>
  )
}