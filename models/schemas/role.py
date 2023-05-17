"""
Role In/Out Schemas

By Allen Tao
Created at 2023/4/10 11:40
"""
from apiflask import Schema
from apiflask.fields import String, List, Nested, UUID


class Permissions(Schema):
    actions = List(String())
    menus = List(String())


class RoleOut(Schema):
    id = UUID()
    name = String()
    desc = String()


class RolePermissionsOut(Schema):
    permissions = Nested(Permissions)


class RoleIn(Schema):
    name = String()
    desc = String()
    permissions = Nested(Permissions)
