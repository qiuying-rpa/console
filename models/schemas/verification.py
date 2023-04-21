"""

By Ziqiu Li
Created at 2023/3/30 10:44
"""
from apiflask import Schema
from apiflask.fields import String


class VerificationIn(Schema):
    email = String()
