"""

By Ziqiu Li
Created at 2023/3/24 10:48
"""
from models.user import User
from models.role import Role
from utils import repository
from utils.common import get_conf
from utils.repository import use_db
from werkzeug.security import generate_password_hash

db = use_db()


def create_one(
    email: str,
    password: str,
    name: str = "",
    is_admin: bool = False,
    verification_code: str = "",
) -> tuple[int, str]:
    user = User.query.filter_by(email=email).first()
    if user:
        return 1, "Email already used."
    else:
        if not is_admin:
            redis_conn = repository.use_redis()
            value = redis_conn.get(email)
            redis_conn.delete(email)
            if verification_code != value:
                return 2, "Invalid verification code."
        name = name if name else email.split("@")[0]
        user = repository.create_one(
            User,
            email=email,
            password=generate_password_hash(password),
            name=name,
            is_admin=is_admin,
        )
        # give default role
        default_role = repository.find_one_by(Role, "is_default", True)
        if default_role:
            user.roles.append(default_role)
            db.session.commit()
            return 0, user.id
        else:
            return 3, "No default role found."


def create_admin() -> tuple[int, str]:
    admin = User.query.filter(User.is_admin.is_(True)).first()
    if not admin:
        conf = get_conf().get("auth")
        create_one(conf.get("admin_email"), conf.get("admin_password"), is_admin=True)
    else:
        return 0, admin.id


def delete_admin():
    admin = User.query.filter(User.is_admin.is_(True)).first()
    if admin:
        repository.delete_one(User, admin.id)


def find_user(user_id: str):
    user = repository.find_one(User, user_id)
    if user:
        return 0, user
    else:
        return 1, f"User {user_id} not found."


def find_admin() -> User:
    admin = repository.find_one_by(User, "is_admin", True)
    return admin


def list_all() -> list:
    return list(filter(lambda x: not x.is_admin, repository.list_all(User)))


def update_one(user_id: str, props: dict):
    user = repository.find_one(User, user_id)
    direct_props = {**props}
    if "roles" in direct_props:
        del direct_props["roles"]
        roles = repository.find_many(Role, props["roles"])
        user.roles = roles
        db.session.commit()
    if "password" in direct_props:
        redis_conn = repository.use_redis()
        value = redis_conn.get(user.email)
        redis_conn.delete(user.email)
        if direct_props["verification_code"] != value:
            return 2, "Invalid verification code."
        direct_props["password"] = generate_password_hash(direct_props["password"])
    ret = repository.update_one(User, user_id, **direct_props)
    return ret


def delete_many(user_ids: list[str]) -> None:
    repository.delete_many(User, user_ids)
