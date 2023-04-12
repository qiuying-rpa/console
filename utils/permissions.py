"""

By Ziqiu Li
Created at 2023/3/24 10:48
"""
import re
from functools import wraps
from flask import request, g
from services.auth import get_all_permission
from utils.common import get_conf
from utils.encrypt import verify_token


def bind_auth_checker(app):
    """Bind authentication checker"""

    def is_public(path: str):
        """A path is like '/user/<id>/vouchers'"""
        public_routes = get_conf().get('app').get('public_routes')
        path_parts = path.split('/')
        return any(map(
            lambda x: x == path or all(map(
                lambda y: re.match('<.*?>', y[1]) or (len(path_parts) > y[0] and path_parts[y[0]] == y[1]),
                enumerate(x.split('/')))), public_routes))

    def before_checker():
        app.logger.info('[E]..' + request.path)
        token = request.headers.get(get_conf().get('auth').get('access_token_key'))
        if token:
            code, res = verify_token(token)
            if code == 0:
                app.logger.info('current_user:')
                app.logger.info(res)
                g.current_user = res
            else:
                app.logger.info('Invalid token: ' + res)
                if code == 1:
                    return {'message': res}, 426
                else:
                    return {'message': res}, 400
        elif is_public(request.path):
            app.logger.info(f'Public route {request.path} requested.')
        else:
            app.logger.info('Unauthenticated')
            return {'message': 'Unauthenticated'}, 401

    def after_checker(response):
        app.logger.info('[X]..' + request.path)
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

