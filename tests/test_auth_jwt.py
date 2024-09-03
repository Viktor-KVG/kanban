
import hashlib
from models import UserModel
from src.auth.auth_jwt import user_login
import json
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)



def test_auth_jwt(connect_to_database):
    fake_user = {
                "login": "string",
                "password": "string"
                }
    hashed_password = hashlib.md5(fake_user["password"].encode('utf-8')).hexdigest()
    user = UserModel(login=fake_user["login"], password_hash=hashed_password, email='string')
    connect_to_database.add(user)
    connect_to_database.commit()

    response = client.post("/api/user/login_jwt", json={'login': fake_user['login'], 'password': fake_user['password']})
    resp_json = response.json()

    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {resp_json}"
    assert 'token' in resp_json, f"Token not found in response: {resp_json}"



    