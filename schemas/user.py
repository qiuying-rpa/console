"""

By Ziqiu Li
Created at 2023/3/24 14:18
"""
from apiflask import Schema
from apiflask.fields import String, List, Nested, UUID, Enum

from models.enums import ActionEnum


class UserOut(Schema):
    id = UUID()
    name = String()
    email = String()
    roles = Nested("RoleOut", many=True)


class UserNameOut(Schema):
    id = UUID()
    name = String()


class UserAdminIn(Schema):
    name = String(required=True)
    email = String(required=True)
    password = String()
    roles = List(String())


class UserSelfIn(Schema):
    name = String(required=True)
    email = String(required=True)
    password = String()
    verification_code = String(required=True)


class UserRolesIn(Schema):
    ids = List(String(), required=True)
    roles = List(String(), required=True)
    action = Enum(enum=ActionEnum, required=True)
