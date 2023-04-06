import importlib
from functools import reduce
from pathlib import Path

from apiflask import APIFlask

from models.schemas.response import BaseResponse
from utils.repository import use_db, init_redis_conn_pool
from utils.common import get_conf
from dotenv import load_dotenv

load_dotenv(verbose=True)


def create_app():
    _app = APIFlask(__name__)
    _app.config['SQLALCHEMY_DATABASE_URI'] = get_conf().get('db').get('db_url')
    _app.config["BASE_RESPONSE_SCHEMA"] = BaseResponse

    redis_url = get_conf().get('db').get('redis_url')
    init_redis_conn_pool(redis_url)

    with _app.app_context():
        _db = use_db(_app)

        # register views & models
        vms = reduce(lambda pre, curr: not pre.extend(curr) and pre, [
            [f'{pkg}.{p.stem}' for p in Path(pkg).glob('[!_]*.py')] for pkg in ['models', 'views']], [])
        for vm in vms:
            importlib.import_module(vm)

        _db.create_all()

        from utils.permissions import bind_authentication_checker
        bind_authentication_checker(_app)

    return _app


app = create_app()

if __name__ == '__main':
    from services.user import create_admin
    create_admin()
