import grpc
import generated_pb2 as pb2
import generated_pb2_grpc as pb2_grpc
import sys
import json
from pydantic import BaseModel, ValidationError
import pydantic as py
import argparse


class Officer(BaseModel):
    first_name: py.constr(min_length=1)
    last_name: py.constr(min_length=1)
    rank: py.constr(min_length=1)

class Spaceship(BaseModel):
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
            raise ValueError(f"Invalid class type")

        curclass = class_constraints[obj.class_type]

        if not (curclass[0] <= obj.length <= curclass[1]):
            raise ValueError(f"Invalid length")

        if not (curclass[2] <= obj.crew_size <= curclass[3]):
            raise ValueError(f"Invalid crew size")

        if curclass[4] == False and obj.armed == True:
            raise ValueError(f"Invalid armed status. Can't be armed")

        if curclass[5] == False and obj.alignment == "Enemy":
            raise ValueError(f"Invalid hostility status. Can't be hostile")


def pd2_to_json(spaceship):
    def get_officer(officer):
        return {
            "first_name": officer.first_name,
            "last_name": officer.last_name,
            "rank": officer.rank
        }

    out = dict()
    out["alignment"] = spaceship.alignment
    out["name"] = spaceship.name
    out["class_type"] = spaceship.class_type
    out["length"] = spaceship.length
    out["crew_size"] = spaceship.crew_size
    out["armed"] = spaceship.armed
    out["officers"] = [get_officer(officer) for officer in spaceship.officers]
    return out

def run_client(coordinates, pretty):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.ReportingServerStub(channel)
        response = stub.GetSpaceships(pb2.Coordinates(coordinates=coordinates))
        for spaceship in response:
            try:

                spaceship_json = pd2_to_json(spaceship)
                Spaceship.model_validate(spaceship_json).validate()
                if pretty:
                    print(json.dumps(spaceship_json, indent=4))
                else:
                    print(json.dumps(spaceship_json))
            except ValueError as e:
                # print(f"Invalid spaceship received: {str(e)}")
                pass
            except ValidationError as e:
                # print(f"ship not valid")
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="astronomical_coordinate")
    parser.add_argument("-p", "--pretty", action="store_true")
    args = parser.parse_args()

    print_pretty = args.pretty
    coordinates = args.astronomical_coordinate

    run_client(coordinates, print_pretty)
