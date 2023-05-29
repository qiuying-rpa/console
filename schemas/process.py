"""

By Ziqiu Li
Created at 2023/5/25 14:52
"""
from apiflask import Schema
from apiflask.fields import String, UUID, Nested, DateTime


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


class ProcessJobOut(Schema):
    id = UUID()
    name = String()
    start_params = String()
    desc = String()
    template = String()
    group = Nested("GroupOut")
