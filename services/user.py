"""

By Ziqiu Li
Created at 2023/3/24 10:48
"""
import random

from models.user import User
from models.role import Role
from utils import repository
from utils.email import send_mail
from utils.common import get_conf
from utils.repository import use_db
from werkzeug.security import generate_password_hash

db = use_db()
admin_password = get_conf().get('app').get('admin_password')


def create_one(mail: str, password: str, name: str = '', tel: str = '',
               is_admin: bool = False, verification_code: str = '') -> tuple[int, str]:
    user = User.query.filter_by(mail=mail).first()
    if user:
        return 1, "Mail already exists."
    else:
        if not is_admin:
            redis_conn = repository.use_redis()
            value = redis_conn.get(mail)
            redis_conn.delete(mail)
            if verification_code != value:
                return 2, 'Invalid verification code.'
        name = name if name else mail.split('@')[0]
        user = repository.create_one(User, mail=mail, password=generate_password_hash(password),
                                     name=name, tel=tel, is_admin=is_admin)
        return 0, user.id


def create_admin() -> tuple[int, str]:
    admin = User.query.filter(User.is_admin.is_(True)).first()
    if not admin:
        create_one("admin@qiuying.com", admin_password, is_admin=True)
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
    if 'password' in direct_props:
        redis_conn = repository.use_redis()
        value = redis_conn.get(user.mail)
        redis_conn.delete(user.mail)
        if direct_props['verification_code'] != value:
            return 'Invalid verification code.'
        direct_props['password'] = generate_password_hash(direct_props['password'])
    result = repository.update_one(User, user_id, **direct_props)
    return '' if result else 'Fail to update.'


def delete_many(user_ids: list[str]) -> None:
    repository.delete_many(User, user_ids)


def send_verification_code(recipient: str):
    redis_conn = repository.use_redis()
    verification_code = random.randint(100000, 999999)
    mail_content = f'您好，您的验证码是：{verification_code}，请在5分钟内进行验证。若非本人操作，请无视。'
    redis_conn.set(name=recipient, value=verification_code, ex=300)
    return send_mail('秋英邮箱验证码: ', recipients=[recipient], content=mail_content)

