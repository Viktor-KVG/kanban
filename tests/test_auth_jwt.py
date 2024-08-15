# from src.auth import login_item, user_login
from conftest import client
from src.auth.auth_jwt import user_login
import json





def test_auth_jwt(user_jwt):
    fake_user = {
                "login": "strin",
                "password": "strin"
                }
    response = client.post("/user/login", data=json.dumps(fake_user))
    resp_json = response.json()

    assert user_jwt["login"] == fake_user['login']
    assert user_jwt["password"] == fake_user['password']
