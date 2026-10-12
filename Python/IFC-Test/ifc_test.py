import ifcopenshell
from pathlib import Path

ifc_path = Path(__file__).parent / "name of ifc file.ifc"
model = ifcopenshell.open(str(ifc_path))


print("IFC Schema:", model.schema)

# getting different building elements
print("Walls:", len(model.by_type("IfcWall")))
print("Doors:", len(model.by_type("IfcDoor")))
print("Rooms:", len(model.by_type("IfcSpace")))
print("Floors:", len(model.by_type("IfcBuildingStorey")))
print("Windows:", len(model.by_type("IfcWindow")))

# Printing floors or levels or stories or whatever we call em
print("\n--- Floors ---")
for floor in model.by_type("IfcBuildingStorey"):
    print("Name:", floor.Name, "| Elevation:", floor.Elevation)

# Print rooms (spoilers there is only 1 which i don't understand)
print("\n--- Rooms ---")
for room in model.by_type("IfcSpace"):
    print("Name:", room.Name, "| ID:", room.GlobalId)