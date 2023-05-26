"""

By Ziqiu Li
Created at 2023/3/24 10:48
"""
from models.enums import ActionEnum
from models.user import User
from models.role import Role
from utils import repository
from utils.common import get_conf
from utils.repository import use_db
from werkzeug.security import generate_password_hash

db = use_db()


def create_user_by_self(
    email: str,
    password: str,
    name: str,
    verification_code: str,
) -> tuple[int, str]:
    user = repository.find_one_by(User, "email", email)
    if user:
        return 1, "Email already used."
    else:
        redis_conn = repository.use_redis()
        value = redis_conn.get(email)

        if verification_code != value:
            return 2, "Invalid verification code."
        else:
            redis_conn.delete(email)

        user = repository.create_one(
            User,
            email=email,
            password=generate_password_hash(password),
            name=name,
            is_admin=False,
        )

        # give default role
        default_role = repository.find_one_by(Role, "is_default", True)
        if default_role:
            user.roles.append(default_role)
            db.session.commit()
            return 0, user.id
        else:
            return 3, "No default role found."


def create_user_by_admin(email: str, password: str, name: str, roles=None):
    if roles is None:
        roles = []
    user_exists = repository.find_one_by(User, "email", email)
    if user_exists:
        return 1, "Email already used."
    else:
        user = repository.create_one(User, email=email, password=password, name=name)

        roles = repository.find_many(Role, roles)
        if len(roles) > 0:
            user.roles = roles
            db.session.commit()

        return 0, user.id


def create_admin() -> tuple[int, str]:
    admin = User.query.filter(User.is_admin.is_(True)).first()
    if not admin:
        conf = get_conf().get("auth")
        return 0, repository.create_one(
            User,
            email=conf.get("admin_email"),
            password=generate_password_hash(conf.get("admin_password")),
            name="admin",
            is_admin=True,
        )
    else:
        return 1, admin.id


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


def find_users_by(props: dict):
    return repository.find_many_by(User, **props)


def list_all() -> list:
    return repository.list_all(User, "is_admin", True)


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


def update_roles(user_ids: list[str], roles: list[str], action: ActionEnum):
    users = repository.find_many(User, user_ids)
    if action == ActionEnum.ADD:
        for user in users:
            roles_to_add = list(
                filter(lambda x: all(map(lambda _x: _x.id != x, user.roles)), roles)
            )
            print(roles_to_add)
            [user.roles.append(r) for r in repository.find_many(Role, roles_to_add)]
    else:
        for user in users:
            user.roles = list(
                filter(lambda x: all(map(lambda _x: _x != x.id, roles)), user.roles)
            )
    db.session.commit()
    return 0, ""
