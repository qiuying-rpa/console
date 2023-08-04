"""

By Ziqiu Li
Created at 2023/5/16 21:08
"""
from datetime import datetime


def make_resp(code=0, res=None, msg="", pagination=None):
    """
    Build a generic response structure.

    :param code: Business status code, and default is 0.
    :param res: To success response, this param represents data, otherwise it represents failure message.
    :param msg: Message. Only works if res is falsy when failing.
    :param pagination: Pagination. Sqlalchemy paginate object.
    :return: A generic response structure.
    """
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resp = {"code": code, "data": res, "message": msg or "Success.", "time": time}
    if code:
        resp.update({"data": None, "message": res or msg or "Fail."})
        return resp
    if pagination:
        resp.update({"data": pagination.items, "total": pagination.total})
    return resp

    # return (
    #     {"code": code, "data": res, "message": msg or "Success", "time": time}
    #     if code == 0
    #     else {"code": code, "data": None, "message": res or msg or "Fail", "time": time}
    # )
