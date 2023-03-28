"""

By Ziqiu Li
Created at 2023/3/24 10:48
"""

from functools import wraps
from flask import request, g
from services.auth import get_all_permission
from utils.encrypt import verify_token, gen_token
from datetime import datetime, timedelta


def bind_authentication_checker(app):
    """Bind authentication checker"""

    def is_white(path: str):
        white_list = ['/auth', '/static']
        for w in white_list:
            if path.startswith(w):
                return True
        return False

    def before_checker():
        app.logger.info('[E]..' + request.path)
        token = request.headers.get('x-access-token')
        if token:
            res = verify_token(token)
            if type(res) == str:
                app.logger.info('Invalid token' + res)
                return {'message': res}, 400
            else:
                app.logger.info('current_user:')
                app.logger.info(res)
                g.current_user = res
                return
        elif is_white(request.path):
            app.logger.info('This is a public route.')
            return
        else:
            app.logger.info('Unauthenticated')
            return {'message': 'Unauthenticated'}, 401

    def after_checker(response):
        """Token updating"""
        app.logger.info('[X]..' + request.path)
        if response.status == 200:
            payload = verify_token(request.headers.get('Authorization'))
            valid_delta = datetime.fromtimestamp(payload['exp']) - datetime.now()
            if valid_delta <= timedelta(minutes=5):
                del payload['exp']
                new_token = gen_token(payload)
                response.data['token'] = new_token
                return {'data': response.data}, 210
        return response

    app.before_request(before_checker)
    app.after_request(after_checker)


def require_permission(permission):
    if type(permission) in [str, list]:
        def permission_decorator(func):
            @wraps(func)
            def wrapped_function(*args, **kwargs):
                permissions = get_all_permission()
                if permissions == "*" or (permission in permissions if type(permission) == str else any(
                        map(lambda p: p in permissions, permission))):
                    return func(*args, **kwargs)
                else:
                    return {"message": 'Permission denied.', 'data': None}, 403
            return wrapped_function
        return permission_decorator
    else:
        raise RuntimeError('Invalid permission')
