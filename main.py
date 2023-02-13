import os

from apiflask import APIFlask
from models.schemas.response import BaseResponse
from utils.repository import use_db


def create_app():
    _app = APIFlask(__name__)

    _app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    _app.config["BASE_RESPONSE_SCHEMA"] = BaseResponse

    with _app.app_context():
        _db = use_db(_app)

        import views.pet
        import models.pet

        _db.create_all()
    return _app


app = create_app()
