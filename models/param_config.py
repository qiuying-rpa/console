"""

By Ziqiu Li
Created at 2023/2/15 13:55
"""
from uuid import uuid4
from utils.repository import use_db

db = use_db()


class ParamConfig(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), nullable=False)
    params = db.Column(db.Text)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"))
    process_id = db.Column(db.String(36), db.ForeignKey("process.id"))
