"""

By Ziqiu Li
Created at 2023/5/26 14:31
"""

from apiflask import Schema
from apiflask.fields import String, UUID, DateTime, List, Nested


class JobIn(Schema):
    process_id = String()
    param_config_id = String()
    remark = String()
    status = String()
    plan_run_time = DateTime()


class JobOut(Schema):
    id = UUID()
    create_time = DateTime()
    plan_run_time = DateTime()
    start_time = DateTime()
    end_time = DateTime()
    status = String()
    result = String()
    remark = String()
    creator = Nested("UserNameOut")
    process = Nested("ProcessJobOut")
    robot = Nested("RobotOut")
    param_config = Nested("ParamConfigOut")
