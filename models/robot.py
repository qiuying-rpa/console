"""

By Ziqiu Li
Created at 2023/2/15 14:05
"""
from uuid import uuid4
from utils.repository import use_db

db = use_db()


class Robot(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), nullable=False)
    ip = db.Column(db.String(32))
    status = db.Column(db.String(32), nullable=False)
    desc = db.Column(db.Text)
    owner_id = db.Column(db.String(36), db.ForeignKey("user.id"))
    group_id = db.Column(db.String(36), db.ForeignKey("group.id"))
    jobs = db.relationship("Job", backref="robot")
