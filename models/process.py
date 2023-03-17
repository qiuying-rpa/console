"""

By Ziqiu Li
Created at 2023/2/15 14:23
"""
from uuid import uuid4
from utils.repository import use_db

db = use_db()


class Process(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), unique=True, nullable=False)
    start_params = db.Column(db.Text)
    nodes = db.Column(db.Text)
    desc = db.Column(db.Text)
    template = db.Column(db.String(256))
    developer_id = db.Column(db.String(36), db.ForeignKey("user.id"))
    demander_id = db.Column(db.String(36), db.ForeignKey("user.id"))
    group_id = db.Column(db.String(36), db.ForeignKey("group.id"))
    param_configs = db.relationship("paramConfig", backref="process")


