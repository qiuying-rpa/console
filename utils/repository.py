"""

By Allen Tao
Created at 2023/02/10 18:31
"""
from typing import Union

from flask_sqlalchemy import SQLAlchemy

_db: Union[SQLAlchemy, None] = None


def use_db(app=None):
    """Get the _db instance."""
    global _db
    if app is not None:
        _db = SQLAlchemy(app)
    return _db


def create_one(model, **props):
    """Create one"""
    one = model(**props)
    _db.session.add(one)
    _db.session.commit()
    return one


def update_one(model, one_id, **props):
    """Update one"""
    one = find_one(model, one_id)
    if one:
        for key, value in props.items():
            setattr(one, key, value)
        _db.session.commit()
        return True
    return False


def find_one(model, one_id):
    """Find one"""
    record = _db.session.execute(_db.select(model).filter_by(id=one_id)).first()
    return record[0] if record else None


def find_one_by(model, prop_name, prop_value):
    """Find one by a certain prop"""
    record = _db.session.execute(_db.select(model).filter_by(**{prop_name: prop_value})).first()
    return record[0] if record else None


def find_many(model, many_ids):
    """Find many"""
    return list(map(lambda x: x[0], _db.session.execute(_db.select(model).filter(model.id.in_(many_ids))).all()))


def find_many_by(model, prop_name, prop_value):
    """Find many by a certain prop"""
    return list(map(lambda x: x[0], _db.session.execute(_db.select(model).filter_by(**{prop_name: prop_value})).all()))


def find_other_with_same(model, the_id, prop_name, prop_value):
    """Find the other one with the same value of a certain prop"""
    record = _db.session.execute(_db.select(model).filter_by(
        **{prop_name: prop_value}).filter(model.id.isnot(the_id))).first()
    return record[0] if record else None


def list_all(model):
    """List all"""
    return list(map(lambda x: x[0], _db.session.execute(_db.select(model)).all()))


def delete_one(model, one_id):
    """Delete one"""
    _db.session.delete(find_one(model, one_id))
    _db.session.commit()


def delete_many(model, many_ids):
    """Delete many"""
    [_db.session.delete(one) for one in find_many(model, many_ids)]
    _db.session.commit()

