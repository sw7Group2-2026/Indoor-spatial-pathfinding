import { useEffect, useState } from 'react'
import { getMaps } from './api/maps'
import type { Shape } from './api/maps'
import LeafletMap from './components/LeafletMap'

const floors = [1, 2]

export default function App() {
  // The first usestate is used to update which current floor is selected. Default value is 1 (floor 1)
  // Second is used to define the map shapes used for leaflet. This has type Shape array and is empty to start
  // Third usestate is used for storing errors from the map in case the data is all messed up
  const [selectedFloor, setSelectedFloor] = useState(1)
  const [shapes, setShapes] = useState<Shape[]>([])
  const [mapError, setMapError] = useState('')

  // Use effects run after the component (in this case app) first appear
  // I.E this is when they people enter the website. 
  // So immediatly on entry of website we attempt to query map data, we get it all once
  // Since we'll need to switch anyways between floors. The empty brackets at the end of this
  // Use effect means it won't trigger again (unless the page is reloaded)
  useEffect(() => {
    async function loadMapData(){
      try {
        // Simple asynch for getting mapdata from server
        const mapData = await getMaps()
        setShapes(mapData.shapes)
      } catch (error){
        setMapError(
          // If it's an existing error type load the message along with it, otherwise
          // just load a regular couldnt load maps message
          error instanceof Error ? error.message : 'Could not load maps'
        )
      }
    }
    loadMapData()
  }, []);


  return (
    <main className="mx-auto max-w-xl p-4">
      <div className="relative aspect-[4/3] overflow-hidden rounded-xl bg-gray-200">
        <LeafletMap
          shapes={shapes}
          selectedFloor={selectedFloor}
        />

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
      
      {/* Temp loading of mapdata untill we get it in properly */}
      <p>{mapError || `Loaded ${shapes.length} shapes`}</p>

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