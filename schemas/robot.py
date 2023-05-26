"""

By Ziqiu Li
Created at 2023/5/25 14:10
"""
from apiflask import Schema
from apiflask.fields import String, UUID, Nested


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
