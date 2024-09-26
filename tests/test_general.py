import datetime
import hashlib
import logging
import os
from models import UserModel, BoardModel
from src.auth.auth_jwt import user_login
import json
from fastapi.testclient import TestClient
from src.main import app
from tests import conftest
from tests.conftest import clear_database, connect_to_database

client = TestClient(app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clearing_database(connect_to_database):
    # Очистка таблицы пользователей
    connect_to_database.query(UserModel).delete()
    connect_to_database.query(BoardModel).delete()
    connect_to_database.commit()
    logger.info("База данных очищена.")

def test_create_user(connect_to_database):


    logger.info("Запуск теста создания пользователя...")
    # Очистка БД перед тестом
    clear_database()

    # Проверка количества пользователей до создания нового
    user_count_before = connect_to_database.query(UserModel).count()
    logger.info(f'Количество пользователей до теста: {user_count_before}')
   # Создание уникального тестового пользователя
    test_user_data = {
        "login": f"test_user_{datetime.datetime.now().timestamp()}",  # Используйте временную метку
        "password": "test_password",
        "email": f"test_{datetime.datetime.now().timestamp()}@example.com"  # Или те же временные значения
    }

    # Печать тестовой базы данных
    logger.info(f"Test DB_______: {connect_to_database}")
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    print("Using DATABASE_URL:", os.getenv("TEST_DATABASE_URL"))

    # Создание тестового пользователя через API
    response = client.post("/api/user", json=test_user_data)

    resp_json = response.json()
    if response.status_code != 200:
        logger.error(f"Ошибка при создании пользователя: {resp_json}")
    else:
        logger.info(f"Пользователь успешно создан: {resp_json}")
    connect_to_database.commit()

    
    logger.info(f"Статус ответа: {response.status_code}")
    logger.info(f"Ответ: {resp_json}")

    # Проверка наличия нового пользователя в базе данных
    added_user = connect_to_database.query(UserModel).filter(UserModel.login == test_user_data["login"]).first()
    

    # Логирование количества пользователей после создания
    user_count_after = connect_to_database.query(UserModel).count()
    logger.info(f'Количество пользователей после теста: {user_count_after}')
    

    # Проверка статуса ответа и наличия пользователя
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {resp_json}"
    # assert user_count_after == user_count_before + 1, "Количество пользователей не увеличилось."
    # assert added_user is not None, "Ожидался найденный пользователь."
    
    logger.info(f'Найденный пользователь: {added_user}')

def test_search_users_list(connect_to_database):

    response = client.get("/api/user/list", params={"login": 'string'})
    resp_json = response.json()
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {resp_json}"
    assert response.status_code != 404, f"Expected 404, got {response.status_code}. Response: {resp_json}"    


def test_search_user_id(connect_to_database):
    connect_to_database.query(BoardModel).delete()
    connect_to_database.query(UserModel).delete()
    
    connect_to_database.commit()
    logger.info("База данных очищена.")
    fake_user = {
                
                "login": "string",
                "email": "string"
                }
    

    user = UserModel( login=fake_user['login'], password_hash='', email=fake_user["email"])
    connect_to_database.add(user)
    connect_to_database.commit()
    response = client.get(f'/api/user/{1}')
    resp_json = response.json()
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {resp_json}"

    response_second = client.get(f'/api/user/{500}')
    resp_json_second = response_second.json()
    assert response_second.status_code == 400, f"Expected 400, got {response_second.status_code}. Response: {resp_json_second}"

from sqlalchemy import text

def test_clear_database(connect_to_database):
    session = connect_to_database  # Получаем сессию для работы с базой данных

    # Создаем тестовые данные
    session.execute(text("INSERT INTO \"user\" (login, password_hash, email, created_at, updated_at, is_admin) VALUES ('test_user', 'hashed_password', 'test@example.com', NOW(), NOW(), FALSE)"))
    session.commit()

    # Проверяем, что данные добавлены
    results = session.execute(text("SELECT * FROM \"user\"")).fetchall()
    assert len(results) > 0, "Таблица не должна быть пустой"

    # Очищаем базу данных
    clear_database()

    session.invalidate()  # Сбрасываем кэш сессии после очистки

    # Проверяем, что данные удалены
    results = session.execute(text("SELECT * FROM \"user\"")).fetchall()
    assert len(results) == 0, "Таблица должна быть пустой после очистки"



def test_search_users_list_by_id(connect_to_database):
    user_id = 38 

    response = client.get("/api/user/list", params={"id": user_id})
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0  # Проверяем, что пользователи найдены
    assert users[0]['id'] == user_id  # Проверяем, что ID совпадает


def test_search_users_list_by_email(connect_to_database):
    user_email = "test_1727370732.563326@example.com"  # Измените на email вашего тестового пользователя

    response = client.get("/api/user/list", params={"email": user_email})
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0  # Проверяем, что пользователи найдены
    assert users[0]['email'] == user_email  # Проверяем, что email совпадает    