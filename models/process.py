"""

By Ziqiu Li
Created at 2023/2/15 14:23
"""
from uuid import uuid4
from utils.repository import use_db
from datetime import datetime

db = use_db()


class Process(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), unique=True, nullable=False)
    start_params = db.Column(db.Text)
    nodes = db.Column(db.Text)
    desc = db.Column(db.Text)
    template = db.Column(db.String(256))
    updater_id = db.Column(db.String(36), db.ForeginKey("user.id"))
    updater = db.relationship("User", foregin_keys=[updater_id])
    update_time = db.Column(db.DateTime, default=lambda: datetime.now())
    developer_id = db.Column(db.String(36), db.ForeignKey("user.id"))
    developer = db.relationship("User", foregin_keys=[developer_id])
    demander_id = db.Column(db.String(36), db.ForeignKey("user.id"))
    demander = db.relationship("User", foregin_keys=[demander_id])
    group_id = db.Column(db.String(36), db.ForeignKey("group.id"))
    param_configs = db.relationship("ParamConfig", backref="process")
    jobs = db.relationship("Job", backref="process")
