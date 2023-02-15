"""

By Ziqiu Li
Created at 2023/2/15 11:08
"""
from uuid import uuid4
from utils.repository import use_db

db = use_db()


class Voucher(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(128), nullable=False)
    account = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    # autherUserId  授权id怎么处理？
