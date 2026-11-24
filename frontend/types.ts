// Use type for unions, tuples, and aliases of existing types.
// Examples:
//   type Floor = 0 | 1 | 2
//   type Point = [number, number]
//   type ShapeId = string

// Use interface by default for object shapes, including React props
// and API response objects. Although if you are using an imported interface as a type, you usually use import type
// Also react props are usually bundled together with the component itself, so if something says "Props" it should usually 
// be in the same file as the component its provided for
// Example:
//   interface LeafletMapProps {
//     shapes: Shape[]
//     selectedFloor: number
//   }

export type Coordinate = [number, number]

export interface Shape {
    floor: number  
    kind: 'space' | 'transition'
    polygon: Coordinate[]
}

export interface MapResponse {
    shapes: Shape[]
}


export interface PointOnRoute {
    floor: number
    point: Coordinate
}

export interface RouteResponse {
    route: PointOnRoute[]
}