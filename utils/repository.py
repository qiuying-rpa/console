"""

By Allen Tao
Created at 2023/02/10 18:31
"""
from typing import Union
from redis import Redis, ConnectionPool
from flask_sqlalchemy import SQLAlchemy

from utils.common import get_conf

__db: Union[SQLAlchemy, None] = None
__redis_conn_pool: Union[ConnectionPool, None] = None


def use_db(app=None):
    """Get the __db instance."""
    global __db
    if app:
        __db = SQLAlchemy(app)
    return __db


def create_one(model, **props):
    """Create one"""
    one = model(**props)
    __db.session.add(one)
    __db.session.commit()
    return one


def update_one(model, one_id, **props):
    """Update one"""
    one = find_one(model, one_id)
    if one:
        for key, value in props.items():
            setattr(one, key, value)
        __db.session.commit()
        return 0, ""
    return 1, "Target not exists."


def find_one(model, one_id):
    """Find one"""
    record = __db.session.execute(__db.select(model).filter_by(id=one_id)).first()
    return record[0] if record else None


def find_one_by(model, prop_name, prop_value):
    """Find one by a certain prop"""
    record = __db.session.execute(
        __db.select(model).filter_by(**{prop_name: prop_value})
    ).first()
    return record[0] if record else None


def find_many(model, many_ids):
    """Find many"""
    return list(
        map(
            lambda x: x[0],
            __db.session.execute(
                __db.select(model).filter(model.id.in_(many_ids))
            ).all(),
        )
    )


def find_many_by(model, prop_name, prop_value):
    """Find many by a certain prop"""
    return list(
        map(
            lambda x: x[0],
            __db.session.execute(
                __db.select(model).filter_by(**{prop_name: prop_value})
            ).all(),
        )
    )


def find_other_with_same(model, the_id, prop_name, prop_value):
    """Find the other one with the same value of a certain prop"""
    record = __db.session.execute(
        __db.select(model)
        .filter_by(**{prop_name: prop_value})
        .filter(model.id.isnot(the_id))
    ).first()
    return record[0] if record else None


def list_all(model):
    """List all"""
    return list(map(lambda x: x[0], __db.session.execute(__db.select(model)).all()))


def delete_one(model, one_id):
    """Delete one"""
    __db.session.delete(find_one(model, one_id))
    __db.session.commit()


def delete_many(model, many_ids):
    """Delete many"""
    [__db.session.delete(one) for one in find_many(model, many_ids)]
    __db.session.commit()


def init_redis_conn_pool():
    """Init redis connection pool"""
    global __redis_conn_pool
    __redis_conn_pool = ConnectionPool.from_url(
        url=get_conf("db.redis_url"), decode_responses=True
    )


def use_redis() -> Redis:
    """Get redis connection instance"""
    redis_conn = Redis(connection_pool=__redis_conn_pool)
    return redis_conn
