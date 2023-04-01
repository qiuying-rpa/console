"""

By Allen Tao
Created at 2023/04/01 0:08
"""
from apiflask import Schema
from apiflask.fields import String


class TokenIn(Schema):
    mail = String(required=True)
    password = String(required=True)


class RefreshTokenIn(Schema):
    refresh_token = String(required=True)
    user_id = String(required=True)
