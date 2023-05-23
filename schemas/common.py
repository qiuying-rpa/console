"""
Description

By Allen Tao
Created at 2023/4/10 17:02
"""
from apiflask import Schema
from apiflask.fields import String, List


class IdsIn(Schema):
    ids = List(String())
