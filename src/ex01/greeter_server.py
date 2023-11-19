import grpc
from concurrent import futures
import time
import random
import generated_pb2 as pb2
import generated_pb2_grpc as pb2_grpc

class ReportingServer(pb2_grpc.ReportingServerServicer):
    def GetSpaceships(self, request, context):
        # Generate a random number of spaceships (1-10)
        random.seed(request.coordinates)

        num_spaceships = random.randint(1, 10)
        for _ in range(num_spaceships):
            yield self.generate_random_spaceship()

    def generate_random_spaceship(self):
        # Generate a random spaceship using predefined values
        alignment = random.choice(["Ally", "Enemy"])
        name = "Spaceship" + str(random.randint(1, 1000))
        if alignment == "Enemy":
            name = random.choice([name, "Unknown"])
        spaceship_class = random.choice(["Corvette", "Frigate", "Cruiser", "Destroyer", "Carrier", "Dreadnought"])
        length = round(random.uniform(100.0, 20000.0), 2)
        crew_size = random.randint(1, 500)
        armed = random.choice([True, False])
        officers = self.generate_random_officers()

        # Create a protobuf Spaceship message
        spaceship = pb2.Spaceship(
            alignment=alignment,
            name=name,
            class_type=spaceship_class,
            length=length,
            crew_size=crew_size,
            armed=armed,
            officers=officers,
        )

        return spaceship

    def generate_random_officers(self):
        # Generate a random number of officers (0-10)
        num_officers = random.randint(0, 10)
        officers = []

        for _ in range(num_officers):
            first_name = "First" + str(random.randint(1, 100))
            last_name = "Last" + str(random.randint(1, 100))
            rank = random.choice(["Commander", "Lieutenant", "Ensign"])

            # Create a protobuf Officer message
            officer = pb2.Officer(
                first_name=first_name, last_name=last_name, rank=rank
            )
            officers.append(officer)

        return officers

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ReportingServerServicer_to_server(ReportingServer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
