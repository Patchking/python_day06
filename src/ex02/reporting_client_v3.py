import grpc
import generated_pb2 as pb2
import generated_pb2_grpc as pb2_grpc
import json
from pydantic import ValidationError
import models as pydantic_models
import argparse
import database

def spaceship_to_dict(spaceship):
    # Convert Pydantic model to a dictionary
    return {
        "alignment": spaceship.alignment,
        "name": spaceship.name,
        "class_type": spaceship.class_type,
        "length": spaceship.length,
        "crew_size": spaceship.crew_size,
        "armed": spaceship.armed,
        "officers": [
            {
                "first_name": officer.first_name,
                "last_name": officer.last_name,
                "rank": officer.rank,
            }
            for officer in spaceship.officers
        ],
    }

def run_client(coordinates, pretty, do_filter):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.ReportingServerStub(channel)
        response = stub.GetSpaceships(pb2.Coordinates(coordinates=coordinates))
        database_obj = database.Database()
        for spaceship in response:
            try:

                spaceship_json = spaceship_to_dict(spaceship)
                if do_filter:
                    pydantic_models.Spaceship.model_validate(spaceship_json).validate()
                if pretty:
                    print(json.dumps(spaceship_json, indent=4))
                else:
                    print(json.dumps(spaceship_json))
                database_obj.save_to_database(spaceship_json)
            except ValueError as e:
                print(f"Invalid spaceship received: {str(e)}")
                pass
            except ValidationError as e:
                # print(f"ship not valid")
                pass

def list_traitors():
    database_obj = database.Database()
    lst = database_obj.get_officers()
    new_set = set()
    for off in lst:
        new_set.add(f"{{'first_name': '{off[1]}', 'last_name': \
'{off[2]}', 'rank': '{off[3]}'}}")
    print(*new_set, sep="\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser_command = parser.add_subparsers(dest="command", required=True)
    parser.add_argument("-p", "--pretty", action="store_true")

    scan_parser = parser_command.add_parser("scan")
    scan_parser.add_argument("astronomical_coordinate")
    scan_parser.add_argument("--filter", action="store_true")
    parser_command.add_parser("list_traitors")
    args = parser.parse_args()

    print_pretty = args.pretty
    if args.command == "scan":
        coordinates = args.astronomical_coordinate
        do_filter = args.filter
        run_client(coordinates, print_pretty, do_filter)
    else:
        list_traitors()
