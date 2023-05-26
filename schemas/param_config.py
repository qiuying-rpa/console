"""

By Ziqiu Li
Created at 2023/5/25 14:19
"""

from apiflask import Schema
from apiflask.fields import String, UUID, List, Dict


class ParamConfigIn(Schema):
    name = String()
    params = List(Dict())
    desc = String()
    process_id = String()


class ParamConfigOut(Schema):
    id = UUID()
    name = String()
    params = String()
    desc = String()
