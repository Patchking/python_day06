import grpc
import generated_pb2 as pb2
import generated_pb2_grpc as pb2_grpc
import sys
import json

def run_client(coordinates):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.ReportingServerStub(channel)
        response = stub.GetSpaceships(pb2.Coordinates(coordinates=coordinates))
        for spaceship in response:
            print(json.dumps([str(spaceship)]))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: reporting_client.py <coordinates>")
        sys.exit(1)

    coordinates = sys.argv[1]
    run_client(coordinates)
