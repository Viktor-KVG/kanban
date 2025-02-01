import hashlib
import os
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from src.main import app
from sqlalchemy.orm import sessionmaker, declarative_base
from src.database import get_db
from src.models import UserModel, BoardModel
import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TEST_SQL_DATABASE_URL = 'postgresql+psycopg2://postgres:1234567890t@172.24.0.1:7000/postgres_test'

test_engine = create_engine(TEST_SQL_DATABASE_URL, echo=True)
test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
test_Base = declarative_base()

timestamp_value = datetime.datetime.now()


def override_get_db():
    print("Using test database!++++++++++++++++++++++++")
    logger.info(f"Используемая база данных: {TEST_SQL_DATABASE_URL}")

    db = test_session_factory()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db       


def create_test_user(session):

    fake_user = {
        "login": "test_user",
        "password": "test_password",
        "email": "test_@examples.com"
    }
    
    # Хеширование пароля
    hashed_password = hashlib.md5(fake_user["password"].encode('utf-8')).hexdigest()

    with test_session_factory() as session:
        new_user = UserModel(login=fake_user["login"], password_hash=hashed_password, email=fake_user["email"],created_at=timestamp_value,
                             updated_at=timestamp_value, is_admin=False)
        session.add(new_user)
        session.commit()
        print(f"Created user ID: {new_user.id}")
        users_board = BoardModel(
              title='First Board', created_at=timestamp_value, updated_at=timestamp_value, author_id=new_user.id
         )        
        session.add(users_board)
        session.commit()
    return fake_user    


def clear_database(session):      
    print("Clearing the database...-----------")
    # Сначала удаляем из дочерних таблиц
    with test_session_factory() as session:
        print("Before Clearing: ", session.query(UserModel).count(), " users found initial.")
        # Удаляем все записи из BoardModel
        print("Deleting from BoardModel-----------------")
        session.execute(BoardModel.__table__.delete())
        session.commit()

    # Теперь очищаем из UserModel
    with test_session_factory() as session:
        print("Deleting from UserModel-----------------")
        session.execute(UserModel.__table__.delete())
        session.commit()
    print("After Clearing: ", session.query(UserModel).count(), " users found ending.")    



@pytest.fixture(scope="function")
def connect_to_database():
    # Установите тестовую базу данных
    os.environ["TEST_SQL_DATABASE_URL"] = TEST_SQL_DATABASE_URL
    test_Base.metadata.create_all(test_engine)

    session = test_session_factory()
    clear_database(session)  # Очистите базу данных перед тестом
    create_test_user(session)  # Создайте тестовые данные

    yield session

    session.close()  # Закройте сессию после теста
    clear_database(session)  # Очистите базу данных после теста
    test_Base.metadata.drop_all(test_engine)  # Удалите все таблицы


@pytest.fixture()
def test_client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides[get_db] = lambda: None 




  

