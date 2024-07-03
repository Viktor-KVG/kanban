from sqlalchemy import select
from app.models import UserModel
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from .core import session_factory, sessionmaker



app = FastAPI()

class UserLogin(BaseModel):
    login: str
    password_hash: str


class UserCreate(BaseModel):
    id: int
    login: str
    password_hash: str
    email: str
    created_at: str
    updated_at: str
    is_admin: bool    


@app.get("/user/login")
def user_login(data: UserLogin):
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error in data entry, or user does not exist'
        )
    
    elif data == data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error when entering data, such user already exists'
        )
   
    else:
        with session_factory() as session:
            user = session.scalar(select(UserModel).where(UserModel.login == data.login))
            session.query(user)
            session.commit()
    return {
        'login': user.login
    }   


@app.post("/user")
def create_user(data: UserCreate):
    same_user = (select(UserCreate).where(UserCreate.login == data.login))
    if data.login == same_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error in data entry, such user already exists'
        )
    
    else:
        with session_factory() as session:
            user = session.scalar(select(UserCreate))
            session.add(user)
            session.commit()
        return {
                "id": user.id,
                "login": user.login,
                "password_hash": user.password_hash,
                "email": user.email,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "is_admin": user.is_admin
        }   


