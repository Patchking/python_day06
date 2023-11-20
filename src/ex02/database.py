# from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, insert, text
# import models
import database_models as dm

DATABASE_URI = "postgresql://patchking:debian@localhost:5432/patchking"


class Database():
    def initialize_database(self):
        engine = create_engine(DATABASE_URI)
        dm.metadata.drop_all(engine)
        dm.metadata.create_all(engine)

    def __init__(self):
        self.engine = create_engine(DATABASE_URI)

    def save_to_database(self, spaceship_to_add: dict):

        new_spaceship = spaceship_to_add.copy()
        del new_spaceship["officers"]

        with self.engine.connect() as conn:
            if spaceship_to_add["name"] != "Unknown":
                with conn.begin():
                    existing_spaceship = select(dm.spaceships_table).where(dm.spaceships_table.c.name == spaceship_to_add["name"])
                    ans = conn.execute(existing_spaceship).first()
            if spaceship_to_add["name"] == "Unknown" or not ans:
                with conn.begin():
                    prime_key = conn.execute(insert(dm.spaceships_table).values(**new_spaceship)).inserted_primary_key[0]
                with conn.begin():
                    for officer in spaceship_to_add["officers"]:
                        conn.execute(insert(dm.officers_table).values(**officer, spaceship_id=prime_key))

    def get_officers(self):
        ret = []
        with self.engine.connect() as conn:
            with conn.begin():
                req = select(dm.officers_table).join(dm.spaceships_table).where(dm.spaceships_table.c.alignment == "Enemy")
                ret = conn.execute(req).fetchall()
        return ret



if __name__ == "__main__":
    pass
    Database().initialize_database()