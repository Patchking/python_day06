from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, Table, MetaData
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()

officers_table = Table(
    'officers', metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('rank', String, nullable=False),
    Column('spaceship_id', Integer, ForeignKey('spaceships.id'))
)

spaceships_table = Table(
    'spaceships', metadata,
    Column('id', Integer, primary_key=True),
    Column('alignment', String, nullable=False),
    Column('name', String, nullable=False),
    Column('class_type', String, nullable=False),
    Column('length', Float, nullable=False),
    Column('crew_size', Integer, nullable=False),
    Column('armed', Boolean, nullable=False),
)
