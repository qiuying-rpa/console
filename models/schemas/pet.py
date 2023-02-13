"""

By Allen Tao
Created at 2023/02/10 17:19
"""
from apiflask import Schema
from apiflask.fields import String, Integer, List, Nested, UUID


class PetOut(Schema):
    id = UUID()
    name = String()


class PetsOut(Schema):
    pets = List(Nested(PetOut))


class PetIn(Schema):
    name = String(required=True)
    gender = Integer()


class PetsIn(Schema):
    ids = List(String())
