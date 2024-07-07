"""
Общий файл для всех роутеров. Если возникнет необходимость, то его можно поделить на отдельные файлы по сгруппированным endpoint'ам
Например: routers/user.py, routers/board.py и т.д.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

from src.database import session_factory, get_db
from src.models import UserModel
from src.schemas import (
    UserLogin,
    UserCreate,
    UserCreateResponse,
)
from src import core


common_router = APIRouter(
    tags=["common"]
)
api_router = APIRouter(
    prefix="/api",
    tags=["api"]
)


@common_router.get("/")
def index():
    return "health check"


@api_router.post("/user", response_model=UserCreateResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    # Вызов бизнес-логики по определению существования пользователя (функция is_user_exist)
    if core.is_user_exist(data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error in data entry, such user already exists'
        )
    # Вызов бизнес-логики по регистрации пользователя (функция register_user)
    user = core.register_user(data)
    return user


# @TODO переделать по аналогии с предыдущим EP
@api_router.post("/user/login")
def user_login(data: UserLogin):
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error in data entry, or user does not exist'
        )
    # elif data == data:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail='Error when entering data, such user already exists'
    #     )

    # >>> начало бизнес-логики
    with session_factory() as session:
        user = session.scalar(select(UserModel).where(UserModel.login == data.login))
        # @TODO проверить ещё и пароль
        session.query(user)
        session.commit()
    # @TODO сгенерировать jwt токен (PyJWT, секретный ключ придумать и положить в settings.py)
    # <<< конец бизнес-логики

        # @TODO вернуть jwt токен
        return {
            'login': user.login
        }
