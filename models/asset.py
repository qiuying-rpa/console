"""

By Ziqiu Li
Created at 2023/2/15 16:22
"""
from uuid import uuid4
from utils.repository import use_db

db = use_db()


class Asset(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(64), unique=True, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(128))
    value = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"))
