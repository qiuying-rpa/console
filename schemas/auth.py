"""

By Allen Tao
Created at 2023/04/01 0:08
"""
from apiflask import Schema
from apiflask.fields import String, Enum, Field
from marshmallow import ValidationError


class TokenIn(Schema):
    email = String(required=True)
    password = String(required=True)


class TokenOut(Schema):
    access_token = String()
    refresh_token = String()


class RefreshTokenIn(Schema):
    refresh_token = String(required=True)


class PermissionValueField(Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or (
            isinstance(value, list) and all(map(lambda x: isinstance(x, str), value))
        ):
            return value
        else:
            raise ValidationError("Field should be str or list[str]")


class PermissionsOut(Schema):
    menus = PermissionValueField()
    actions = PermissionValueField()
