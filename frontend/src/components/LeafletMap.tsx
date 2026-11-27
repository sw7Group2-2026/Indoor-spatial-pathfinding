
import { MapContainer, TileLayer, Polygon, Polyline } from 'react-leaflet'
import type { LatLngExpression } from 'leaflet'
import L from 'leaflet'
import type { Shape, Coordinate, RouteSegment } from '../../types'
import { useEffect } from 'react'
import proj4 from 'proj4'

type LeafletMapProps = {
  shapes: Shape[]
  selectedFloor: number
  route: RouteSegment[]
}

export default function LeafletMap({
  shapes,
  selectedFloor,
  route,
}: LeafletMapProps) {


  proj4.defs(
    'EPSG:25832',
    '+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs +type=crs'
  )

  const transformedShapes = shapes
    .filter((shape) => shape.kind === 'transition' || shape.floor === selectedFloor)
    .filter((shape) => Array.isArray(shape.polygon))
    .map((shape) => ({
      ...shape,
      polygon: shape.polygon.map(([x, y]): Coordinate => {
        const [lng, lat] = proj4('EPSG:25832', 'WGS84', [x, y])
        return [lat, lng]
      }),
    }))
    .filter((shape) => shape.polygon.length >= 3)

  const points: LatLngExpression[][] = route
    .filter((segment) => segment.floor === selectedFloor)
    .map((segment) =>
      segment.points.map(([x, y]): Coordinate => {
        const [lng, lat] = proj4('EPSG:25832', 'WGS84', [x, y])
        return [lat, lng]
      })
    )

  L.Map.include({
    latLngToLayerPoint(latlng: LatLngExpression) {
      return this.project(L.latLng(latlng))
        .subtract(this.getPixelOrigin())
    },
  })

  // Leaflet but for react
  return (
    <MapContainer
      center={[55.650666, 12.541614]}
      zoom={19}
      minZoom={5}
      maxZoom={22}
      preferCanvas={true}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxNativeZoom={19}
         maxZoom={22}
      />
        {transformedShapes.map((shape, index) => (
          <Polygon
            key={index}
            positions={shape.polygon}
            smoothFactor={0}
            noClip={true}
            pathOptions={{
              color: 'blue',
              weight: 0.5,
            }}
          />
        ))}
      <Polyline
        positions={points}
        pathOptions={{
          color: 'red',
          weight: 1,
          opacity: 0.8,
        }}
      />
    </MapContainer>
  )
}
