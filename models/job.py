"""

By Ziqiu Li
Created at 2023/2/15 14:54
"""
from uuid import uuid4
from utils.repository import use_db
from datetime import datetime

db = use_db()


class Job(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    create_time = db.Column(db.DateTime, default=datetime.now)
    plan_run_time = db.Column(db.DateTime, default=datetime.now)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(32))
    result = db.Column(db.String(32))
    remark = db.Column(db.Text)
    creator_id = db.Column(db.String(36), db.ForeignKey("user.id"))
    process_id = db.Column(db.String(36), db.ForeignKey("process.id"))
    param_config_id = db.Column(db.String(36), db.ForeignKey("param_config.id"))
    robot_id = db.Column(db.String(36), db.ForeignKey("robot.id"))
