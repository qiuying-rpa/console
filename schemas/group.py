"""

By Ziqiu Li
Created at 2023/5/25 13:53
"""
from apiflask import Schema
from apiflask.fields import String, UUID, Integer
from apiflask.validators import Range


class GroupIn(Schema):
    name = String()
    desc = String()


class GroupOut(Schema):
    id = UUID()
    name = String()
    desc = String()


class GroupQuery(Schema):
    name = String()
    page = Integer(load_default=1)
    size = Integer(load_default=20, validate=Range(max=50))
