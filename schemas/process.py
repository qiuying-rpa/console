"""

By Ziqiu Li
Created at 2023/5/25 14:52
"""
from apiflask import Schema
from apiflask.fields import String, UUID, Nested, DateTime, Integer
from apiflask.validators import Range


class ProcessIn(Schema):
    name = String()
    start_params = String()
    nodes = String()
    desc = String()
    template = String()
    developer_id = String()
    demander_id = String()
    group_id = String()


class ProcessOut(Schema):
    id = UUID()
    name = String()
    start_params = String()
    nodes = String()
    desc = String()
    template = String()
    updater = Nested("UserNameOut")
    update_time = DateTime()
    developer = Nested("UserNameOut")
    demander = Nested("UserNameOut")
    group = Nested("GroupOut")


class ProcessQuery(Schema):
    name = String()
    developer_name = String()
    group_name = String()
    page = Integer(load_default=1)
    size = Integer(load_default=20, validate=Range(max=50))


class ProcessJobOut(Schema):
    id = UUID()
    name = String()
    start_params = String()
    desc = String()
    template = String()
    group = Nested("GroupOut")
