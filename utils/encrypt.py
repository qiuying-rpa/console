"""

By Ziqiu Li
Created at 2023/3/24 9:26
"""

import jwt
from typing import Union
from datetime import datetime, timedelta
from utils.common import get_conf


def gen_token(payload, expiry_seconds) -> str:
    jwt_secret = get_conf().get('app').get('jwt_secret')
    expiry = (datetime.now() + timedelta(seconds=expiry_seconds)).timestamp()
    token = jwt.encode({**payload, 'exp': expiry}, jwt_secret, algorithm='HS256')
    return token


def verify_token(token) -> tuple[int, Union[dict, str]]:
    jwt_secret = get_conf().get('app').get('jwt_secret')
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        return 0, payload
    except jwt.ExpiredSignatureError:
        return 1, 'Out of date.'
    except jwt.InvalidTokenError:
        return 2, 'Invalid token.'


