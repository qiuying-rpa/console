import importlib
from functools import reduce
from pathlib import Path
from apiflask import APIFlask
from models.schemas.response import BaseResponse
from utils.repository import use_db, init_redis_conn_pool
from utils.common import get_conf
from dotenv import load_dotenv

load_dotenv(verbose=True)


app = APIFlask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_conf().get('db').get('db_url')
app.config["BASE_RESPONSE_SCHEMA"] = BaseResponse

redis_url = get_conf().get('db').get('redis_url')
init_redis_conn_pool(redis_url)

with app.app_context():
    db = use_db(app)

    # register views & models
    vms = reduce(lambda pre, curr: not pre.extend(curr) and pre, [
        [f'{pkg}.{p.stem}' for p in Path(pkg).glob('[!_]*.py')] for pkg in ['models', 'views']], [])
    for vm in vms:
        importlib.import_module(vm)

    db.create_all()

    from utils.permissions import bind_auth_checker
    bind_auth_checker(app)


if __name__ == '__main':
    from services.user import create_admin
    from services.role import create_default
    
    create_admin()
    create_default()
