"""

By Ziqiu Li
Created at 2023/3/17 16:54
"""
from uuid import uuid4
from utils.repository import use_db

db = use_db()

user_role = db.Table(
    'user_role',
    db.Column('user_id', db.String(36), db.ForeignKey("user.id"), primary_key=True),
    db.Column('role_id', db.String(36), db.ForeignKey('role.id'), primary_key=True)
)