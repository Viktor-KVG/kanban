# Сюда нужно поместить функции, реализующие бизнес-логику
# Например, процедура логина пользователя или его регистрация
# Эти функции из app.core импортируются в обработчики запросов (роуты) и вызываются

from datetime import datetime
from hashlib import md5
import logging

from fastapi import HTTPException, status
from sqlalchemy import select

from src.models import UserModel
from src.schemas import UserCreate, UserId, UserLogin, UserCreateResponse, UserLoginForAdmin, SearchUsersList, UserList, UserUpdate
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
        if data1.id is not None:
            query = query.filter(UserModel.id == data1.id)
        if data1.login:
            query = query.filter(UserModel.login == data1.login)
        if data1.email:
            query = query.filter(UserModel.email == data1.email)
            
        # Получаем отфильтрованные результаты
        filtered_users = query.all()  # Теперь это будет только те пользователи, которые соответствуют условиям

        if filtered_users:

            return [UserList.from_orm(user) for user in filtered_users] 
        return False  

              
def search_user_by_id(data: UserId): 
    with session_factory() as session:
        query = session.query(UserModel)

        if data.id:
            query = query.filter(UserModel.id == data.id)

        result_id = query.first()
        logging.info(f"Retrieved user: {result_id}")

        if result_id:
            return UserList.from_orm(result_id)        
        return False

   
def search_user_by_id_put(data:UserUpdate, user_id:int):
    with session_factory() as session:
        query = session.query(UserModel).filter(UserModel.id == user_id).first()

        if query:
            query.login = data.login
            query.password = data.password
            query.email = data.email
            query.updated_at = datetime.now()
            session.commit()
            session.refresh(query)
            return query
        return False


        



        
 