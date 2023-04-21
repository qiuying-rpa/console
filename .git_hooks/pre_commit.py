"""
Remove auth keys before committing

By Allen Tao
Created at 2023/4/21 10:54
"""
import sys

sys.path.append(".")

from utils.common import set_conf

conf = set_conf("auth.jwt_secret", "")
set_conf("email.sender_password", "", conf, True)
