import datetime
import logging
import os
from models import UserModel, BoardModel
from fastapi.testclient import TestClient
from src.main import app
from tests.conftest import clear_database, TEST_SQL_DATABASE_URL

client = TestClient(app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



def clearing_database(connect_to_database):
    # Очистка таблицы пользователей
    connect_to_database.query(UserModel).delete()
    connect_to_database.query(BoardModel).delete()
    connect_to_database.commit()
    logger.info("База данных очищена.")


def test_create_user(connect_to_database, test_client):

    logger.info("Запуск теста создания пользователя...")
    # Очистка БД перед тестом
    print("Используемая база данных:", TEST_SQL_DATABASE_URL)
    clear_database(connect_to_database)
    print("Используемая база данных:", TEST_SQL_DATABASE_URL)

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
    logging.basicConfig()
    logger.info(f"Test DB_______: {connect_to_database}")
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    print("Using DATABASE_URL:", os.getenv("TEST_SQL_DATABASE_URL"))


    # Создание тестового пользователя через API
    response = test_client.post("/api/user", json=test_user_data)

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
   
    logger.info(f'Найденный пользователь: {added_user}')


    
def test_search_users_list(connect_to_database, test_client):

    response = test_client.get("/api/user/list", params={"login": 'string'})
    resp_json = response.json()
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {resp_json}"
    assert response.status_code != 404, f"Expected 404, got {response.status_code}. Response: {resp_json}"    


def test_search_user_id(connect_to_database, test_client):
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
    response = test_client.get(f'/api/user/{1}')
    resp_json = response.json()
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {resp_json}"

    response_second = test_client.get(f'/api/user/{500}')
    resp_json_second = response_second.json()
    assert response_second.status_code == 400, f"Expected 400, got {response_second.status_code}. Response: {resp_json_second}"


def test_clear_database(connect_to_database):
    session = connect_to_database  # Получаем сессию для работы с базой данных

    # Создаем тестовые данные
    test_user = UserModel(
        login='test_user',
        password_hash='hashed_password',
        email='test@example.com',
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        is_admin=False
    )
    session.add(test_user)
    session.commit()

    # Проверяем, что данные добавлены
    results = session.query(UserModel).all()
    assert len(results) > 0, "Таблица не должна быть пустой"

    # Очищаем базу данных
    clear_database(session)

    session.invalidate()  # Сбрасываем кэш сессии после очистки

    # Проверяем, что данные удалены
    results = session.query(UserModel).all()
    assert len(results) == 0, "Таблица должна быть пустой после очистки"


def test_search_users_list_by_id(connect_to_database, test_client):
    
    # Ищем пользователя по ID
    response = test_client.get("/api/user/list", params={"id": 1})
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0  # Проверяем, что пользователи найдены



def test_search_users_list_by_email(connect_to_database, test_client):
    user_email = "test_@examples.com"  

    response = test_client.get("/api/user/list", params={"email": user_email})
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0 
    assert users[0]['email'] == user_email  


def test_search_user_by_delete(connect_to_database, test_client):
    test_user_login = f"test_user_{datetime.datetime.now().timestamp() - 1}"  # Пример логина для поиска
    added_user = connect_to_database.query(UserModel).filter(UserModel.login == test_user_login).first()
    
    if added_user is None:
        print("Не удалось найти пользователя в базе данных.")
        return
    
    user_id = added_user.id
    print(f"Используем ID найденного пользователя: {user_id}")

    # Удаляем пользователя
    response = test_client.delete(f'/api/user/{user_id}')
    assert response.status_code == 200, f"Ошибка при удалении пользователя: {response.json()}"
    
    # Проверка, что пользователь действительно удален
    deleted_user_response = test_client.get(f'/api/user/{user_id}')
    assert deleted_user_response.status_code == 404, "Пользователь все еще существует после удаления."

