import type { MapResponse, RouteResponse } from '../../types'


export async function getMaps(): Promise<MapResponse> {
  const response = await fetch('/api/maps')

  if (!response.ok) {
    throw new Error(`Could not load maps (${response.status})`)
  }

  const data: MapResponse = await response.json()
  // Uncomment to see the shapes when opening up the terminal in browser
  // console.log(JSON.stringify(data, null, 2))

  return data
}

export async function getRoute(): Promise<RouteResponse> {
  const response = await fetch('/api/maps')

  if (!response.ok) {
    throw new Error(`Could not load maps (${response.status})`)
  }

  const data: RouteResponse = await response.json()
  // Uncomment to see the shapes when opening up the terminal in browser
  // console.log(JSON.stringify(data, null, 2))

  return data
}