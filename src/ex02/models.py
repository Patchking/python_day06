import pydantic as py


class Officer(py.BaseModel):
    first_name: py.constr(min_length=1)
    last_name: py.constr(min_length=1)
    rank: py.constr(min_length=1)

class Spaceship(py.BaseModel):
    alignment: py.constr(min_length=1)
    name: py.constr(min_length=1)  # Assuming a maximum length for the name
    class_type: py.constr(min_length=1)
    length: py.PositiveFloat
    crew_size: py.PositiveInt
    armed: bool
    officers: list[Officer]

    def validate(obj):

        if obj.name == "Unknown" and obj.alignment == "Ally":
            raise ValueError("Name should be 'Unknown' for enemy ships only.")
        
        if obj.alignment not in ["Ally", "Enemy"]:
            raise ValueError(f"Invalid target status")

        class_constraints = {
            "Corvette": (80, 250, 4, 10, True, True),
            "Frigate": (300, 600, 10, 15, True, False),
            "Cruiser": (500, 1000, 15, 30, True, True),
            "Destroyer": (800, 2000, 50, 80, True, False),
            "Carrier": (1000, 4000, 120, 250, False, True),
            "Dreadnought": (5000, 20000, 300, 500, True, True),
        }

        if obj.class_type not in class_constraints:
            raise ValueError(f"{obj.class_type}: invalid class type '{obj.class_type}'")

        curclass = class_constraints[obj.class_type]

        if not (curclass[0] <= obj.length <= curclass[1]):
            raise ValueError(f"{obj.class_type}: invalid length '{obj.length}'")

        if not (curclass[2] <= obj.crew_size <= curclass[3]):
            raise ValueError(f"{obj.class_type}: invalid crew size '{obj.crew_size}'")

        if curclass[4] == False and obj.armed == True:
            raise ValueError(f"{obj.class_type}: invalid armed status. Can't be armed")

        if curclass[5] == False and obj.alignment == "Enemy":
            raise ValueError(f"{obj.class_type}: invalid hostility status. Can't be hostile")