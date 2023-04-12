"""

By Ziqiu Li
Created at 2023/3/24 9:26
"""
import jwt
import rsa
from typing import Union
from datetime import datetime, timedelta
from utils.common import get_conf


def gen_token(payload, expiry_seconds) -> str:
    jwt_secret = get_conf().get('auth').get('jwt_secret')
    expiry = (datetime.now() + timedelta(seconds=expiry_seconds)).timestamp()
    token = jwt.encode({**payload, 'exp': expiry}, jwt_secret, algorithm='HS256')
    return token


def verify_token(token) -> tuple[int, Union[dict, str]]:
    jwt_secret = get_conf().get('auth').get('jwt_secret')
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        return 0, payload
    except jwt.ExpiredSignatureError:
        return 1, 'Out of date.'
    except jwt.InvalidTokenError:
        return 2, 'Invalid token.'


def gen_rsa_keys():
    public, private = rsa.newkeys(128)
    return public.save_pkcs1().decode(), private.save_pkcs1().decode()


def rsa_encrypt(content: str):
    conf = get_conf().get('auth')
    return rsa.encrypt(content.encode(), rsa.PublicKey.load_pkcs1(conf.get('rsa_public_key'))).decode()


def rsa_decrypt(crypto: str):
    conf = get_conf().get('auth')
    return rsa.decrypt(crypto.encode(), rsa.PrivateKey.load_pkcs1(conf.get('rsa_private_key'))).decode()
