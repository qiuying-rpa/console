"""
Role In/Out Schemas

By Allen Tao
Created at 2023/4/10 11:40
"""
from apiflask import Schema
from apiflask.fields import String, List, Nested, UUID


class Permission(Schema):
    actions = List(String())
    menus = List(String())


class RoleOut(Schema):
    id = UUID()
    name = String()
    desc = String()


class RoleWithPermissionsOut(Schema):
    id = UUID()
    name = String()
    desc = String()
    permissions = Nested(Permission())


class RoleIn(Schema):
    name = String()
    desc = String()
    permissions = Nested(Permission())
