from datetime import datetime
from typing import Any, Optional, ClassVar, Union

from fastapi import Query
from pydantic import BaseModel, ConfigDict

class BoardsModel(BaseModel):
    pass


class UserForAdmin(BaseModel):
    # model_config = ConfigDict(ignored_types=(IgnoredType,))
    id: int
    login: str
    email: str
    created_at: datetime
    created_up: Union[datetime, None] = Query(default=None)
    is_admin: bool
    boads: Union[list[BoardsModel], None] = Query(default=None)

    class Config:
        from_attributes = True 

class UserList(BaseModel):
    # model_config = ConfigDict(ignored_types=(IgnoredType,))
    id: int
    login: str
    email: str
    created_at: datetime
    created_up: Union[datetime, None] = None
    is_admin: bool
    boads: Union[list[BoardsModel], None] = None

    class Config:

        from_attributes = True      

class UserLoginForAdmin(BaseModel):
    login: str


class SearchUsersList(BaseModel):
    id: int
    login: str
    email: str 
    
    class Config:
        from_attributes = True          



class UserLogin(BaseModel):
    login: str
    password: str

    class Config:
        from_attributes = True 



class UserCreate(BaseModel):
    login: str
    password: str
    email: str

   
    class Config:
        from_attributes = True 



class UserCreateResponse(BaseModel):
    id: int
    login: str
    email: str
    is_admin: bool


    class Config:
        from_attributes = True 


class Token(BaseModel):
    token: str

class UserId(BaseModel):
    id: int
