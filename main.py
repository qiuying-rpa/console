import importlib
import os
from functools import reduce
from pathlib import Path

from apiflask import APIFlask
from models.schemas.response import BaseResponse
from utils.repository import use_db, init_redis_conn_pool
from utils.mail import use_mail
from utils.common import get_conf
from dotenv import load_dotenv

load_dotenv(verbose=True)


def create_app():
    _app = APIFlask(__name__)
    _app.config['SQLALCHEMY_DATABASE_URI'] = get_conf().get('db').get('sqlite_url')
    _app.config["BASE_RESPONSE_SCHEMA"] = BaseResponse
    _app.config['MAIL_SERVER'] = get_conf().get('mail').get('server')
    _app.config['MAIL_PORT'] = get_conf().get('mail').get('port')
    _app.config['MAIL_USERNAME'] = get_conf().get('mail').get('username')
    _app.config['MAIL_PASSWORD'] = get_conf().get('mail').get('password')
    _app.config['MAIL_DEFAULT_SENDER'] = f"Qiuying <{get_conf().get('mail').get('username')}>"
    _app.config['MAIL_USE_TLS'] = False
    _app.config['MAIL_USE_SSL'] = True

    redis_url = get_conf().get('db').get('redis_url')
    init_redis_conn_pool(redis_url)

    with _app.app_context():
        _db = use_db(_app)
        _mail = use_mail(_app)

        # register views & models
        vms = reduce(lambda pre, curr: not pre.extend(curr) and pre, [
            [f'{pkg}.{p.stem}' for p in Path(pkg).glob('[!_]*.py')] for pkg in ['models', 'views']], [])

        for vm in vms:
            importlib.import_module(vm)

        _db.create_all()
    return _app


app = create_app()
