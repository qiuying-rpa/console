"""

By Ziqiu Li
Created at 2023/5/25 14:10
"""
from apiflask import Schema
from apiflask.fields import String, UUID, Nested, Integer
from apiflask.validators import Range


class RobotIn(Schema):
    name = String()
    ip = String()
    desc = String()
    owner_id = String()
    group_id = String()


class RobotOut(Schema):
    id = UUID()
    name = String()
    ip = String()
    desc = String()
    owner = Nested("UserOut")
    group = Nested("GroupOut")


class RobotQuery(Schema):
    name = String()
    group_name = String()
    page = Integer(load_default=1)
    size = Integer(load_default=20, validate=Range(max=50))
