"""

By Ziqiu Li
Created at 2023/3/24 10:48
"""

from models.user import User
from models.role import Role
from utils import repository
from utils.common import get_conf
from utils.repository import use_db
from utils.encrypt import gen_password_hash

db = use_db()
admin_password = get_conf().get('app').get('admin_password')


def create_one(mail: str, password: str, name: str = "", tel: str = "", is_admin: bool = False) -> tuple[int, str]:
    user = User.query.filter_by(mail=mail).first()
    if user:
        return 1, "Mail already exists."
    else:
        name = name if name else mail.split('@')[0]
        user = repository.create_one(User, mail=mail, password=gen_password_hash(password),
                                     name=name, tel=tel, is_admin=is_admin)
        return 0, user.id


def create_admin() -> tuple[int, str]:
    admin = User.query.filter(User.is_admin.is_(True)).first()
    if not admin:
        create_one("admin", admin_password, is_admin=True)
    else:
        return 0, admin.id


def delete_admin():
    admin = User.query.filter(User.is_admin.is_(True)).first()
    if admin:
        repository.delete_one(User, admin.id)


def find_user(user_id: str) -> User:
    user = repository.find_one(User, user_id)
    return user


def list_all() -> list:
    return list(filter(lambda x: not x.is_admin, repository.list_all(User)))


def update_one(user_id: str, props: dict) -> str:
    user = repository.find_one(User, user_id)
    direct_props = {**props}
    if 'roles' in direct_props:
        del direct_props['roles']
        roles = Role.query.filter(Role.id.in_(props['roles'])).all()
        user.roles = roles
        db.session.commit()
    result = repository.update_one(User, user_id, **direct_props)
    return '' if result else 'Fail to update.'


def delete_many(user_ids: list[str]) -> None:
    repository.delete_many(User, user_ids)



