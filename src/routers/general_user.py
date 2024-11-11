"""
Общий файл для всех роутеров. Если возникнет необходимость, то его можно поделить на отдельные файлы по сгруппированным endpoint'ам
Например: routers/user.py, routers/board.py и т.д.
"""

import hashlib
from typing import Any, List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import UJSONResponse
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query,  status, HTTPException

# from src.auth.auth_jwt import user_login
from src.database import session_factory, get_db
from src.models import UserModel
from src.schemas import (
    Token,
    UserId,
    UserLogin,
    UserCreate,
    UserCreateResponse,
    UserForAdmin,
    UserLoginForAdmin,
    SearchUsersList,
    UserList,
    UserUpdate
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
    if core.is_user_exist(data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error in data entry, such user already exists'
        )

    else:
        user = core.register_user(data)
        return user


@api_router.get("/user/list", response_model=List[UserList])
def search_users_list( user_id: int = None, user_login: str = None, user_email: str = None, db: Session = Depends(get_db)):  
    result_list = core.search_list_users(SearchUsersList(id=user_id, login=user_login, email=user_email), db)
    if result_list:
        return  result_list
    

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found'
    )


@api_router.get('/user/{user_id}')
def search_user_id( user_id: int ):
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail='User ID must not be zero'
        )    

    search_id = core.search_user_by_id(UserId(id=user_id))

    if search_id:
        return search_id
    
    if search_id == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user '
        )   


@api_router.put('/user/{user_id}', response_model=UserForAdmin)
def put_user_id(user_id: int, user_update: UserUpdate):
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail='User ID must not be zero'
        )    

    user_put = core.search_user_by_id_put(user_update, user_id)

    if user_put:
        return user_put
    
    if user_put == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user '
        )

@api_router.delete('/user/{user_id}')
def delete_user_id(user_id: int):
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail='User ID must not be zero'
        )    

    user_del = core.search_user_by_id_for_delete(UserId(id=user_id))

    if user_del:
        return user_del
    
    if user_del == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user '
        )     


@api_router.post("/user/login_jwt", response_model=Token)
def user_login_jwt(data: UserLogin):
    func = auth_jwt.user_login(data)

    if func:
        return {'token': func}
    
    elif func == False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal Server Error'
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Authentication error, incorrect credentials'
        )


@api_router.get('/user/login/{login}')
def user_login_for_admin(login:str):
    search_login = core.search_user_for_admin(UserLoginForAdmin(login=login))
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


@api_router.get('/logout')
def user_logout():
    return {"detail": "Successful logout"}

