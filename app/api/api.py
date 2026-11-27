from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
from database.supa_db_handler import SupaDatabaseHandler
from database.routing_algorithm import get_parameterised_routing_sql
from interpreter.input_interpreter import InputInterpreter

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
    start_location: PointOnRoute



db = SupaDatabaseHandler()
queryHandler = InputInterpreter(debug = True)

@app.post("/api/route", response_model=RouteResponse)
def post_route(request: RouteRequestBody) -> RouteResponse:
    # BUILD THE ROUTE IN HERE SO HERE IS THE SQL FOR GETTING THE ROUTE
    # ALSO THE CODE FOR QUERYING LLM
    # STRUCTURE FOR THE WHOLE ENTIRE PROCESS
    # First save query and startlocation in variables
    # Pass query to the LLM sandwich and get a structured output object
    # Pass the sandwich output into the filtration algorithm for Start location and Targets (destinations)
    # Save those start location and targets in variables
    # Pass the start location and target SQL variable queries into the routing query
    # Return the route from the routing query to be displayed in the frontend
    
    print(request.query)

    query_string = request.query
    start_location = request.start_location

    print("Query:", query_string)
    print("Start location POINT:", start_location.point)
    print("Start location FLOOR:", start_location.floor)
    queryResult = queryHandler.query(query_string)
    print("QUERY RESULT OBJECT: ", queryResult)
    route_sql, params_list = get_parameterised_routing_sql(start_location,queryResult)
    route_data = db.web_query(route_sql, params_list)
    route_formatted = []

    for row in route_data:
        geometry = row["st_asgeojson"]
        floor = row["floor_id"]

        if geometry["type"] != "LineString":
            continue

        coordinates = geometry["coordinates"]

        for point in coordinates:
            route_formatted.append({
                "floor": floor,
                "point": point
            })

    print("Route floors:", set(p["floor"] for p in route_formatted))

    for point in route_formatted:
        print(point)

    return RouteResponse(route=route_formatted)

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