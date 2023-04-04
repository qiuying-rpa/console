"""

By Ziqiu Li
Created at 2023/3/24 11:00
"""
from datetime import datetime, timedelta

from flask import g
from functools import reduce
from models.user import User
from utils import repository
from utils.common import get_conf
from utils.encrypt import verify_password_hash, gen_token, verify_token


def login(username, password):
    user = User.query.filter_by(mail=username).first()
    if user:
        verify_result = verify_password_hash(user.password, password)
        if verify_result:
            return 0, gen_token_pair(user.id, username)
        else:
            return 1, 'Wrong password'
    else:
        return 2, 'User not exists'


def refresh(user_id, token):
    code, res = verify_token(token)
    if code == 0:
        user = repository.find_one(User, user_id)
        if user:
            return 0, gen_token_pair(user.id, user.name)
        else:
            return 1, 'User not exists'
    else:
        return 2, res


def gen_token_pair(user_id, username):
    app_conf = get_conf().get('app')
    access_token = gen_token({"id": user_id, "username": username}, app_conf.get('access_expire'))
    refresh_token = gen_token({"id": user_id, "username": username},  app_conf.get('refresh_expire'))
    return access_token, refresh_token


def get_all_permission():
    if g.get('current_user'):
        user = repository.find_one(User, g.current_user['id'])
        if user:
            if user.is_admin:
                return "*"
            else:
                return reduce(lambda pre, curr: [*pre, *curr.permissions.split(',')], user.roles, [])
    return []

