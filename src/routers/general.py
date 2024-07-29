"""
Общий файл для всех роутеров. Если возникнет необходимость, то его можно поделить на отдельные файлы по сгруппированным endpoint'ам
Например: routers/user.py, routers/board.py и т.д.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

# from src.auth.auth_jwt import user_login
from src.database import session_factory, get_db
from src.models import UserModel
from src.schemas import (
    Token,
    UserLogin,
    UserCreate,
    UserCreateResponse,
    UserForAdmin,
    UserLoginForAdmin
)
from src import core
from src.auth import auth_jwt




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
    else:
        user = core.register_user(data)
        return user


# @TODO переделать по аналогии с предыдущим EP
@api_router.post("/user/login", response_model=Token)
def user_login_jwt(data: UserLogin):
    func: dict = auth_jwt.user_login(data)

    if func:
        return {'token': func}
    
    elif auth_jwt.user_login(data) is False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Authentication error, incorrect credentials'
        )


    # >>> начало бизнес-логики

        # @TODO проверить ещё и пароль

    # @TODO сгенерировать jwt токен (PyJWT, секретный ключ придумать и положить в settings.py)
    # <<< конец бизнес-логики

        # @TODO вернуть jwt токен

@api_router.post('/user/{login}', response_model=UserForAdmin)
def user_login_for_admin(data: UserLoginForAdmin):
    search_login = core.search_user_for_admin(data)
    if search_login:
        return search_login
    
    elif search_login == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid login supplied'
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_NOT_FOUND,
            detail='User not found'
        )




