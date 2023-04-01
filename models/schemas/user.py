"""

By Ziqiu Li
Created at 2023/3/24 14:18
"""
from apiflask import Schema
from apiflask.fields import String, List, Nested, UUID, Boolean


class UserOut(Schema):
    id = UUID()
    name = String()
    mail = String()
    tel = String()
    is_admin = Boolean()
    roles = List(String())


class UsersOut(Schema):
    users = List(Nested(UserOut))


class UserIn(Schema):
    name = String()
    mail = String()
    password = String()
    tel = String()
    is_admin = Boolean()
    verification_code = String()


class UsersIn(Schema):
    ids = List(String())
