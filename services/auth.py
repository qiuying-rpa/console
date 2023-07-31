"""

By Ziqiu Li
Created at 2023/3/24 11:00
"""
import hashlib
import random
from pathlib import Path

from flask import g
from functools import reduce
from models.user import User
from utils import repository
from utils.common import get_conf, update_conf
from utils.email import send_mail
from utils.encrypt import gen_token, verify_token, gen_rsa_keys, rsa_decrypt
from werkzeug.security import check_password_hash
from sqlalchemy import select


def login(username, password):
    user = repository.find(select(User).filter_by(email=username), first=True)
    if user:
        verify_result = check_password_hash(user.password, rsa_decrypt(password))
        if verify_result:
            return 0, gen_token_pair(user.id, username)
        else:
            return 1, "Wrong password"
    else:
        return 2, "User not exists"


def refresh(token):
    code, res = verify_token(token)
    if code == 0:
        user = repository.find_one(User, res["id"])
        if user:
            return 0, gen_token_pair(user.id, user.name)
        else:
            return 1, "User not exists"
    else:
        return 2, res


def gen_token_pair(user_id, username):
    app_conf = get_conf().get("auth")
    access_token = gen_token(
        {"id": user_id, "username": username}, app_conf.get("access_expire")
    )
    refresh_token = gen_token(
        {"id": user_id, "username": username}, app_conf.get("refresh_expire")
    )
    return access_token, refresh_token


def get_all_permissions():
    if g.get("current_user"):
        user = repository.find_one(User, g.current_user["id"])
        if user:
            if user.is_admin:
                return "*"
            else:
                return reduce(
                    lambda pre, curr: [*pre, *curr.permissions.get("actions", [])],
                    user.roles,
                    [],
                )
    return []


def send_verification_code(recipient: str):
    redis_conn = repository.use_redis()
    verification_code = random.randint(100000, 999999)
    mail_content = f"您好，您的验证码是：{verification_code}，请在5分钟内进行验证。若非本人操作，请无视。"
    redis_conn.set(name=recipient, value=verification_code, ex=300)
    return send_mail("秋英邮箱验证码: ", recipients=[recipient], content=mail_content)


def create_auth_keys():
    conf = get_conf()
    if conf:
        auth_conf = conf.get("auth")
        pub_key_path = Path(auth_conf.get("rsa_public_key_path"))
        pri_key_path = Path(auth_conf.get("rsa_private_key_path"))

        if not pub_key_path.exists() or not pri_key_path.exists():
            gen_rsa_keys()

        if not auth_conf.get("jwt_secret"):
            auth_conf["jwt_secret"] = hashlib.md5(
                str(random.random()).encode()
            ).hexdigest()
            update_conf(conf)
    else:
        raise RuntimeError("Failed to load configurations.")
