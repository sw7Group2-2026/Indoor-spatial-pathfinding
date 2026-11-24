import type { MapResponse, PointOnRoute, RouteResponse } from '../../types'


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

export async function getRoute(
  query: string,
  startLocation: PointOnRoute,
): Promise<RouteResponse> {
  const response = await fetch('/api/route', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      start_location: startLocation,
    }),
  })

  if (!response.ok) {
    throw new Error(`Route request failed (${response.status})`)
  }

  return response.json()
}