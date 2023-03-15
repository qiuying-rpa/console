"""

By Ziqiu Li
Created at 2023/2/15 14:18
"""
from uuid import uuid4
from utils.repository import use_db

db = use_db()


class Group(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), unique=True, nullable=False)
    desc = db.Column(db.Text)
    robots = db.relationship("Robot", backref="group")
    processes = db.relationship("Process", backref="group")
