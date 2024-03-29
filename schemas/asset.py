"""

By Ziqiu Li
Created at 2023/5/25 11:28
"""

from apiflask.schemas import Schema
from apiflask.fields import String, UUID, Nested, Integer
from apiflask.validators import Range


class AssetIn(Schema):
    name = String()
    type = String()
    value = String()
    desc = String()


class AssetOut(Schema):
    id = UUID()
    name = String()
    type = String()
    value = String()
    desc = String()
    user = Nested("UserNameOut")


class AssetQuery(Schema):
    name = String()
    type = String()
    page = Integer(load_default=1)
    size = Integer(load_default=20, validate=Range(max=50))
