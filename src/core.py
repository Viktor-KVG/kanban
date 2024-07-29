# Сюда нужно поместить функции, реализующие бизнес-логику
# Например, процедура логина пользователя или его регистрация
# Эти функции из app.core импортируются в обработчики запросов (роуты) и вызываются

from hashlib import md5

from sqlalchemy import select

from src.models import UserModel
from src.schemas import UserCreate, UserLogin, UserCreateResponse, UserLoginForAdmin
from src.database import session_factory


def is_user_exist(data: UserCreate) -> bool:
    with session_factory() as session:
        same_user = session.query(UserModel).where(UserModel.login == data.login).first()
        if same_user:
            return True
        return False


def register_user(data: UserCreate) -> UserModel:
    with session_factory() as session:
        hashed_password = md5()
        hashed_password.update(data.password.encode('utf-8'))
        user = UserModel(
            password_hash=hashed_password.hexdigest(),
            **data.model_dump(exclude={"password"})
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    

def search_user_for_admin(data: UserLoginForAdmin):
    with session_factory() as session:
        search_login = session.query(UserModel).filter_by(login= data.login).first()
        if search_login:
            return search_login
        return False

        



        
 