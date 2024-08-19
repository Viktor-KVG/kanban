# Сюда нужно поместить функции, реализующие бизнес-логику
# Например, процедура логина пользователя или его регистрация
# Эти функции из app.core импортируются в обработчики запросов (роуты) и вызываются

from hashlib import md5

from sqlalchemy import select

from src.models import UserModel
from src.schemas import UserCreate, UserLogin, UserCreateResponse, UserLoginForAdmin, SearchUsersList, UserList
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


def search_list_users(data1: SearchUsersList):
    with session_factory() as session:
        query = session.query(UserModel)

        # Добавим условия к запросу, если они указаны
        if data1.id:
            query = query.filter(UserModel.id == data1.id)
        if data1.login:
            query = query.filter(UserModel.login == data1.login)
        if data1.email:
            query = query.filter(UserModel.email == data1.email)

        # Получаем отфильтрованные результаты
        filtered_users = query.all()  # Теперь это будет только те пользователи, которые соответствуют условиям

        if filtered_users:
            return [UserList.from_orm(user) for user in filtered_users]  # Возвращает только соответствующих пользователей

        return False                   



   

        



        
 