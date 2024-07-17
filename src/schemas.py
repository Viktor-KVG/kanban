from datetime import datetime

from pydantic import BaseModel


class UserLogin(BaseModel):
    login: str
    password: str




class UserCreate(BaseModel):
    login: str
    password: str
    email: str


class UserCreateResponse(BaseModel):
    id: int
    login: str
    email: str
    is_admin: bool

    class Config:
        orm_mode: True


class Token(BaseModel):
    token: str
