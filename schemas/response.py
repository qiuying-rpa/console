"""

By Allen Tao
Created at 2023/02/10 18:03
"""
import datetime

from apiflask import Schema
from apiflask.fields import Field, String, DateTime, Integer


class BaseResponse(Schema):
    code = Integer()
    data = Field()
    message = String()
    time = String()
