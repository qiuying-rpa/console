"""

By Ziqiu Li
Created at 2023/3/24 9:26
"""
import base64

import jwt
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from typing import Union
from datetime import datetime, timedelta
from utils.common import get_conf


def gen_token(payload, expiry_seconds) -> str:
    jwt_secret = get_conf().get("auth").get("jwt_secret")
    expiry = (datetime.now() + timedelta(seconds=expiry_seconds)).timestamp()
    token = jwt.encode({**payload, "exp": expiry}, jwt_secret, algorithm="HS256")
    return token


def verify_token(token) -> tuple[int, Union[dict, str]]:
    jwt_secret = get_conf().get("auth").get("jwt_secret")
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return 0, payload
    except jwt.ExpiredSignatureError:
        return 1, "Out of date."
    except jwt.InvalidTokenError:
        return 2, "Invalid token."


def gen_rsa_keys():
    conf = get_conf("auth")
    rsa = RSA.generate(1024, Random.new().read)

    with open(conf.get("rsa_private_key_path"), "wb") as f:
        f.write(rsa.export_key())

    with open(conf.get("rsa_public_key_path"), "wb") as f:
        f.write(rsa.public_key().export_key())


def rsa_encrypt(message: str):
    conf = get_conf().get("auth")
    with open(conf.get("rsa_public_key_path"), "rb") as f:
        return base64.b64encode(
            PKCS1_v1_5.new(RSA.import_key(f.read())).encrypt(message.encode())
        )


def rsa_decrypt(crypto: str):
    conf = get_conf().get("auth")
    with open(conf.get("rsa_private_key_path"), "rb") as f:
        return (
            PKCS1_v1_5.new(RSA.import_key(f.read()))
            .decrypt(base64.b64decode(crypto), None)
            .decode()
        )
