"""

By Ziqiu Li
Created at 2023/5/16 21:08
"""
from datetime import datetime


def make_resp(code=0, data=None, message=""):
    return {"code": code, "data": data, "message": message, "time": datetime.now()}


def make_resp_concise(code=0, res=None, message=""):
    """

    :param code:
    :param res:
    :param message:
    :return:
    """
    return (
        make_resp(code=code, data=res, message=message or "Success.")
        if code == 0
        else make_resp(code=code, message=res or message or "Fail.")
    )
