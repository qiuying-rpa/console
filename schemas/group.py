"""

By Ziqiu Li
Created at 2023/5/25 13:53
"""
from apiflask import Schema
from apiflask.fields import String, UUID


class GroupIn(Schema):
    name = String()
    desc = String()


class GroupOut(Schema):
    id = UUID()
    name = String()
    desc = String()
