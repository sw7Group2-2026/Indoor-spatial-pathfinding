from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
from database.supa_db_handler import SupaDatabaseHandler

app = FastAPI()


# This is basically like a typescript interface
# It is used for structuring data so we know what it should look like
# This shape is basically to enforce that each "Shape" has a floor number
# and a polygon that consists of 4 coordinates or "tuples" consisting of longitude lattitude
# We allow None value for the shape floor, since a transition area may not have a specific floor so for those unique cases we allow them to pass through for polygon creation
class Shape(BaseModel):
    floor: int | None
    kind: Literal["space", "transition"]
    polygon: list[tuple[float, float]]

# We expect to get a list of these shapes
class MapResponse(BaseModel):
    shapes: list[Shape]

class PointOnRoute(BaseModel):
    floor: int
    point: tuple[float, float]

class RouteResponse(BaseModel):
    route: list[PointOnRoute]

class RouteRequestBody(BaseModel):
    query: str
    startLocation: PointOnRoute



db = SupaDatabaseHandler()

@app.post("/api/route", response_model=RouteResponse)
def post_route(request: RouteRequest) -> RouteResponse:
    # BUILD THE ROUTE IN HERE SO HERE IS THE SQL FOR GETTING THE ROUTE
    # ALSO THE CODE FOR QUERYING LLM
    return RouteResponse(route=route)

@app.get("/api/maps", response_model=MapResponse)
def get_maps():

    # Query used to get data
    # Kind sets extra values on the object of the map response 
    rows = db.query("""
        SELECT
            floor_id AS floor,
            'space' AS kind,
            ST_AsGeoJSON(geom)::json AS geometry
        FROM indoor_space
        WHERE geom IS NOT NULL

        UNION ALL

        SELECT
            NULL AS floor,
            'transition' AS kind,
            ST_AsGeoJSON(geom)::json AS geometry
        FROM transition_area
        WHERE geom IS NOT NULL;
    """)

    shapes = []

    for row in rows:
        # Used for entering the nested coordinates inside the geometry object
        boundary = row["geometry"]["coordinates"][0][0]

        shapes.append({
            "floor": row["floor"],

            "kind": row["kind"],

            # This removes the 5th coordinate that closes polygons, since it isn't needed for map visual
            "polygon": boundary[:-1],
        })

    return {"shapes": shapes}