"""

By Ziqiu Li
Created at 2023/3/17 16:51
"""
from uuid import uuid4
from utils.repository import use_db

db = use_db()


class Role(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(128))
    is_default = db.Column(db.Boolean)
    # be like, {'actions': ['user:create', 'user:update'], 'menus': ['/system/users', '/processes/:id']}
    permissions = db.Column(db.PickleType)
