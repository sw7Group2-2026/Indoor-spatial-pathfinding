from fastapi import FastAPI
from pydantic import BaseModel
from database.supa_db_handler import SupaDatabaseHandler

app = FastAPI()


# This is basically like a typescript interface
# It is used for structuring data so we know what it should look like
# This shape is basically to enforce that each "Shape" has a floor number
# and a polygon that consists of 4 coordinates or "tuples" consisting of longitude lattitude
class Shape(BaseModel):
    floor: int
    polygon: list[tuple[float, float]]

# We expect to get a list of these shapes
class MapResponse(BaseModel):
    shapes: list[Shape]

db = SupaDatabaseHandler()


@app.get("/api/maps", response_model=MapResponse)
def get_maps():

    # THIS QUERY HAS TEMPORARILY BEEN OMITTED UNTILL FURTHER DISCUSSION WITH GROUP
    rows = db.query()

    shapes = []

    for row in rows:
        # Used for entering the nested coordinates inside the geometry object
        boundary = row["geometry"]["coordinates"][0][0]

        shapes.append({
            "floor": row["floor"],

            # This removes the 5th coordinate that closes polygons, since it isn't needed for map visual
            "polygon": boundary[:-1],
        })

    return {"shapes": shapes}