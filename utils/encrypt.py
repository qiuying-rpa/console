"""

By Ziqiu Li
Created at 2023/3/24 9:26
"""

import jwt
from typing import Union
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


jwt_secret = '23083B133BD91002551CBE0B80E08133'


def gen_token(payload=None, expiry=None) -> str:

    if payload is None:
        payload = {}
    if expiry is None:
        expiry = (datetime.now() + timedelta(hours=3)).timestamp()
    token = jwt.encode({**payload, 'exp': expiry}, jwt_secret)
    return token


def verify_token(token) -> Union[str, dict]:
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=['Hs256'])
        return payload
    except jwt.InvalidTokenError:
        return 'Invalid token.'
    except jwt.ExpiredSignatureError:
        return 'Out of date.'


def gen_password_hash(password: str) -> str:
    return generate_password_hash(password)


def verify_password_hash(pwd_hash: str, password: str) -> bool:
    return check_password_hash(pwd_hash, password)
