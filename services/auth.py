"""

By Ziqiu Li
Created at 2023/3/24 11:00
"""
from flask import g
from functools import reduce
from models.user import User
from utils.encrypt import verify_password_hash, gen_token


def login(username, password):
    user = User.query.filter_by(mail=username).first()
    if user:
        verify_result = verify_password_hash(user.password, password)
        if verify_result:
            token = gen_token({"id": user.id, "username": username})
            return 0, token
        else:
            return 1, 'Wrong password'
    else:
        return 2, 'User not exists'


def get_all_permission():
    if g.get('current_user'):
        user = User.query.get(g.current_user['id'])
        if user:
            if user.is_admin:
                return "*"
            else:
                return reduce(lambda pre, curr: [*pre, *curr.permissions.split(',')], user.roles, [])
    return []

