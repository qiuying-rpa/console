"""

By Allen Tao
Created at 2023/02/10 18:03
"""
import datetime

from apiflask import Schema
from apiflask.fields import Field, String, DateTime


class BaseResponse(Schema):
    data = Field(dump_default=None)
    message = String(dump_default='Success')
    time = DateTime(dump_default=datetime.datetime.now)
