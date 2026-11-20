
import { MapContainer, TileLayer, Polygon, Polyline } from 'react-leaflet'
import type { LatLngExpression } from 'leaflet'
import type { Shape } from './api/maps'
import { useEffect } from 'react'

type LeafletMapProps = {
  shapes: Shape[]
  selectedFloor: number
}

export default function LeafletMap({
  shapes,
  selectedFloor,
}: LeafletMapProps) {

  // Only show shapes on the selected floor (isn't used rn untill we actually get the real cords)
  const visibleShapes = shapes.filter(
    (shape) => shape.floor === selectedFloor
  )

  // Example coords from earlier thingy
  // Leaflet had specific lat lng apparently i shoulda known mb
  const boundsMultiple: LatLngExpression[][] = [
    [
      [55.6506, 12.5416],
      [55.6506, 12.5417],
      [55.6507, 12.5417],
      [55.6507, 12.5416],
    ],
    [
      [55.6508, 12.5418],
      [55.6508, 12.5419],
      [55.6509, 12.5419],
      [55.6509, 12.5418],
    ],
  ]

  const points: LatLngExpression[] = [
    [55.6509, 12.5415],
    [55.6509, 12.5416],
    [55.6510, 12.5416],
    [55.6511, 12.5417],
  ]


  // Leaflet but for react
  return (
    <MapContainer
      center={[55.650666, 12.541614]}
      zoom={19}
      minZoom={5}
      maxZoom={22}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxNativeZoom={19}
         maxZoom={22}
      />
      {boundsMultiple.map((coordinates, index) => (
        <Polygon
          key={index}
          positions={coordinates}
          pathOptions={{ color: 'blue' }}
        />
      ))}
      <Polyline
        positions={points}
        pathOptions={{
          color: 'red',
          weight: 3,
          opacity: 0.8,
          dashArray: '3, 7',
        }}
      />
    </MapContainer>
  )
}
