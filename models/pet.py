"""

By Allen Tao
Created at 2023/02/10 16:38
"""
from uuid import uuid4

from utils.repository import use_db

db = use_db()


class Pet(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), unique=True, nullable=False)
    gender = db.Column(db.Integer)
