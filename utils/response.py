"""

By Ziqiu Li
Created at 2023/5/16 21:08
"""
from datetime import datetime


def make_resp(code=0, res=None, msg=""):
    """
    Build a generic response structure.

    :param code: Business status code, and default is 0.
    :param res: To success response, this param represents data, otherwise it represents failure message.
    :param msg: Message. Only works if res is falsy when failing.
    :return: A generic response structure.
    """
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        {"code": code, "data": res, "message": msg or "Success", "time": time}
        if code == 0
        else {"code": code, "data": None, "message": res or msg or "Fail", "time": time}
    )
