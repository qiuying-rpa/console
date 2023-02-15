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
    account = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    tel = db.Column(db.String(11), unique=True)
    vouchers = db.relationship("Voucher", backref="user")
    param_configs = db.relationship("paramConfig", backref="user")
    assets = db.relationship("Asset", backref="user")

