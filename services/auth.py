"""

By Ziqiu Li
Created at 2023/3/24 11:00
"""
import random
from flask import g
from functools import reduce
from models.user import User
from utils import repository
from utils.common import get_conf
from utils.email import send_mail
from utils.encrypt import gen_token, verify_token
from werkzeug.security import check_password_hash


def login(username, password):
    user = User.query.filter_by(mail=username).first()
    if user:
        verify_result = check_password_hash(user.password, password)
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
                return reduce(lambda pre, curr: [*pre, *curr.permissions.get('actions', [])], user.roles, [])
    return []


def send_verification_code(recipient: str):
    redis_conn = repository.use_redis()
    verification_code = random.randint(100000, 999999)
    mail_content = f'您好，您的验证码是：{verification_code}，请在5分钟内进行验证。若非本人操作，请无视。'
    redis_conn.set(name=recipient, value=verification_code, ex=300)
    return send_mail('秋英邮箱验证码: ', recipients=[recipient], content=mail_content)
