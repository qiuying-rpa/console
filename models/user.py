"""

By Ziqiu Li
Created at 2023/2/15 10:59
"""
from uuid import uuid4
from utils.repository import use_db

db = use_db()


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), nullable=False)
    mail = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    tel = db.Column(db.String(32), unique=True)
    is_admin = db.Column(db.Boolean)
    vouchers = db.relationship("Voucher", backref="user")
    param_configs = db.relationship("paramConfig", backref="user")
    assets = db.relationship("Asset", backref="user")

