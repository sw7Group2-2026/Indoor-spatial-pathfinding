import { useEffect, useState } from 'react'
import { getMaps, getRoute } from './api/maps'
import type { Shape } from './api/maps'
import LeafletMap from './components/LeafletMap'
import proj4 from 'proj4'
import QueryField from './components/QueryField'
import type { PointOnRoute } from '../types'

const floors = [2,1]


// This data below for points is simply for testing to have some base values
const startLocation: PointOnRoute = {
  floor: 1,
  point: [722900.12, 6172872.71],
}

export default function App() {
  // The first usestate is used to update which current floor is selected. Default value is 1 (floor 1)
  // Second is used to define the map shapes used for leaflet. This has type Shape array and is empty to start
  // Third usestate is used for storing errors from the map in case the data is all messed up
  const [selectedFloor, setSelectedFloor] = useState(1)
  const [shapes, setShapes] = useState<Shape[]>([])
  const [mapError, setMapError] = useState('')
  const [route, setRoute] = useState<PointOnRoute[]>([])

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

  async function onFindRoute(query: string, start: PointOnRoute) {
    try {
      const { route } = await getRoute(query, start)
      setRoute(route)
    } catch (error) {
      console.error('Could not load route', error)
    }
  }

  proj4.defs('EPSG25832', "+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs");



  return (
    <main className="mx-auto max-w-xl p-4">
      <div className="relative h-[80dvh] overflow-hidden rounded-xl bg-gray-200">
        <div className="relative z-0 h-full w-full">
          <LeafletMap
            shapes={shapes}
            selectedFloor={selectedFloor}
            route={route}
          />
        </div>

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
      <QueryField
        startLocation={startLocation}
        onFindRoute={onFindRoute}
      />
      <p>Route points loaded: {route.length}</p>
    </main>
  )
}