import jwt
# from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from src.schemas import UserLogin
from src.models import UserModel
from src.database import session_factory
import json
import hashlib



SECRET_KEY = "aa046a7bf9e7dac915c2e81cd826ea0ee73f62e953abcef2c5d495aaf6dc25c8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




def user_login(data: UserLogin):

    with session_factory() as session:

        login_item = jsonable_encoder(data)
        login_item_login = login_item['login']
        login_item_password = login_item['password']
        hashed_password = hashlib.md5(login_item_password.encode('utf-8')).hexdigest()
        login_user_token = session.query(UserModel.login).filter_by(login=login_item_login).first()     
        password_user_token = session.query(UserModel.password_hash).filter_by(password_hash=hashed_password).first()

        # print(hashed_password)       
        # print(login_item_login)
        # print(login_item_password)
        # print(login_user_token)
        # print(password_user_token)

    try:

        if login_item_login == login_user_token[0] and hashed_password == password_user_token[0]:

            encoded_jwt = jwt.encode(login_item, SECRET_KEY, algorithm=ALGORITHM)
            session.commit()
     
            return encoded_jwt
    
    except TypeError:

        return False        



