import jwt
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from src.schemas import UserLogin
from src.models import UserModel
from src.database import session_factory



SECRET_KEY = "aa046a7bf9e7dac915c2e81cd826ea0ee73f62e953abcef2c5d495aaf6dc25c8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def user_login(data: UserLogin) -> UserModel:
    login_item = jsonable_encoder(data)
    with session_factory() as session:
        login = session.query(UserModel).where(UserModel.login == login_item.login)
        password = session.query(UserModel).where(UserModel.password_hash == login_item.password)
    if login and password:
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    else:
        return False

