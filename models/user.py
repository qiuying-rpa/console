"""

By Ziqiu Li
Created at 2023/2/15 10:59
"""
from uuid import uuid4

from models.user_role import user_role
from utils.repository import use_db

db = use_db()


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    param_configs = db.relationship("ParamConfig", backref="user")
    assets = db.relationship("Asset", backref="user")
    roles = db.relationship("Role", backref="users", secondary=user_role)
    jobs = db.relationship("Job", backref="user")
