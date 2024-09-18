import hashlib
from models import UserModel
from src.auth.auth_jwt import user_login
import json
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)



def test_create_user(connect_to_database):
    fake_user = {
                "login": "string",
                "password": "string",
                "email": "string"
                }
    hashed_password = hashlib.md5(fake_user["password"].encode('utf-8')).hexdigest()
    user = UserModel(login=fake_user["login"], password_hash=hashed_password, email='string')
    connect_to_database.add(user)
    connect_to_database.commit()
    response = client.post("/api/user/login_jwt", json={'login': fake_user['login'], 'password': fake_user['password'], 'email': fake_user["email"]})
    resp_json = response.json()
    added_user = connect_to_database.query(UserModel).filter(UserModel.login == fake_user["login"]).first()
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {resp_json}"
    assert response.status_code != 400, f"Expected 200, got {response.status_code}. Response: {resp_json}"
    assert "token" in resp_json, "Expected key 'token' in the response."
    assert added_user is not None


def test_search_users_list(connect_to_database):

    response = client.get("/api/user/list", params={"login": 'string'})
    resp_json = response.json() 

    response_2 = client.get("/api/user/list", params={"email": "string"})
    resp_json_2 = response_2.json()

    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {resp_json}"
    assert response_2.status_code == 200, f"Expected 200, got {response_2.status_code}. Response: {resp_json_2}"
    assert resp_json[0]['id'] == 1
    assert resp_json[0]['login'] == 'string'
    assert resp_json[0]['email'] == 'string'


def test_earch_user_id(connect_to_database):
    response = client.get(f'/api/user/{1}')
    resp_json = response.json()
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {resp_json}"

    response_second = client.get(f'/api/user/{12}')
    resp_json_second = response_second.json()
    assert response_second.status_code == 400, f"Expected 400, got {response_second.status_code}. Response: {resp_json_second}"

