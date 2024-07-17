import jwt
# from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from src.schemas import UserLogin
from src.models import UserModel
from src.database import session_factory



SECRET_KEY = "aa046a7bf9e7dac915c2e81cd826ea0ee73f62e953abcef2c5d495aaf6dc25c8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

false_test = {
  "login": "strin",
  "password": "strin"
}


def user_login(data: UserLogin):
    login_item = jsonable_encoder(data)
    with session_factory() as session:
        login_user_token = session.query(UserModel).where(UserModel.login == login_item['login'])
        password_user_token = session.query(UserModel).where(UserModel.password_hash == login_item['password'])
    if login_user_token == True and password_user_token == True:
    # if false_test["login"] == login_item['login'] and false_test["password"] == login_item['password']:
        encoded_jwt = jwt.encode(login_item, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    else:
        return False

