import hashlib
import os
import pytest
from sqlalchemy import create_engine, text
from src.main import app
from sqlalchemy.orm import sessionmaker, declarative_base
from src.database import get_db
from src.models import UserModel, BoardModel
import datetime

TEST_SQL_DATABASE_URL = 'postgresql+psycopg2://postgres:1234567890t@172.24.0.1:7000/postgres_test'

test_engine = create_engine(TEST_SQL_DATABASE_URL, echo=True)
test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
test_Base = declarative_base()

timestamp_value = datetime.datetime.now()



def create_test_user():

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
# def create_test_user():
#     with test_session_factory() as session:
#         new_user = UserModel(
#                login='string',
#                password_hash='string',
#                email='string',
#                created_at=timestamp_value,
#                updated_at=timestamp_value,
#                is_admin=False,
#                boards=[]
#            )
#         session.add(new_user)
#         session.commit()  # здесь получаем ID

#         print(f'Created user with ID: {new_user.id}')  # Логгирование ID пользователя

#         users_board = BoardModel(
#                title='First Board',
#                created_at=timestamp_value,
#                updated_at=timestamp_value,
#                author_id=new_user.id  # Теперь ID доступен
#            )
#         session.add(users_board)
#         session.commit()

# @pytest.fixture
# def test_user():

#     fake_user = {
#         "login": "test_user",
#         "password": "test_password",
#         "email": "test@example.com"
#     }
    
#     # Хеширование пароля
#     hashed_password = hashlib.md5(fake_user["password"].encode('utf-8')).hexdigest()
    
#     with test_session_factory() as session:
#         # Создание пользователя
#         new_user = UserModel(
#             login=fake_user["login"],
#             password_hash=hashed_password,
#             email=fake_user["email"],
#             created_at=timestamp_value,
#             updated_at=timestamp_value,
#             is_admin=False
#         )
#         session.add(new_user)
#         session.commit()

#         # Создание доски, связанной с пользователем
#         users_board = BoardModel(
#             title='First Board',
#             created_at=timestamp_value,
#             updated_at=timestamp_value,
#             author_id=new_user.id  # Используем ID нового пользователя
#         )
#         session.add(users_board)
#         session.commit()

#     return fake_user

def clear_database():
    # Получаем список таблиц
    '''
    - 'test_Base.metadata.sorted_tables':
    - 'metadata' — это объект SQLAlchemy, который содержит информацию о таблицах, связанных с базой данных.
    - 'sorted_tables' — это список всех таблиц, определенных в модели базы данных. 
       Он отсортирован в порядке, установленном в классах моделей.

    - Функция 'reversed()' возвращает итератор, который перебирает список в обратном порядке. 
      Это может быть полезно, если некоторые таблицы имеют зависимости (например, внешние ключи), и вы хотите удалять их в порядке, 
      противоположном тому, как они были добавлены, чтобы избежать ошибок ссылочной целостности.
    '''
    # print("Clearing the database...-----------")
    # tables = reversed(test_Base.metadata.sorted_tables)
    
    # for table in tables:
    #     with test_session_factory() as session:
    #         print(f"Deleting from table: {table.name}-----------------")
    #         session.execute(table.delete())
    #         session.commit()

    # print("Clearing the database...-----------")
    # tables = reversed(test_Base.metadata.sorted_tables)
       
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


    # print("Clearing the database...-----------")
    # tables = reversed(test_Base.metadata.sorted_tables)
       
    # for table in tables:
    #     with test_session_factory() as session:
    #         try:
    #             count_before = session.execute(text(f'SELECT COUNT(*) FROM "{table.name}"')).scalar()
    #             print(f"Clearing table {table.name} ------ Count before: {count_before}")
                
    #             session.execute(table.delete())
    #             session.commit()  # Убедитесь, что здесь вызывается commit
                
    #             count_after = session.execute(text(f'SELECT COUNT(*) FROM "{table.name}"')).scalar()
    #             print(f"Cleared table {table.name} ------ Count after: {count_after}")
    #         except Exception as e:
    #             print(f"Error clearing table {table.name}: {e}")
    #             session.rollback()  # Откатываем изменения при ошибке

@pytest.fixture(scope="function")
def connect_to_database():
    os.environ["TEST_SQL_DATABASE_URL"] = "postgresql+psycopg2://postgres:1234567890t@172.24.0.1:7000/postgres_test"
    test_Base.metadata.create_all(test_engine)

    session = test_session_factory()
    clear_database()
    create_test_user()

    yield session
    session.close()

    session.close()  # Сбрасываем сессию после завершения теста
    clear_database()  # Очищаем базу данных
    test_Base.metadata.drop_all(test_engine) 

@pytest.fixture()
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = test_session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# @pytest.fixture
# def test_user():

#     fake_user = {
#         "login": "test_user",
#         "password": "test_password",
#         "email": "test@example.com"
#     }
    
#     # Хеширование пароля
#     hashed_password = hashlib.md5(fake_user["password"].encode('utf-8')).hexdigest()
    
#     with test_session_factory() as session:
#         # Создание пользователя
#         new_user = UserModel(login=fake_user["login"], password_hash=hashed_password, email=fake_user["email"],created_at=timestamp_value,
#                              updated_at=timestamp_value,is_admin=False
#                             )
#         session.add(new_user)
#         session.commit()

#         # Создание доски, связанной с пользователем
#         users_board = BoardModel(title='First Board', created_at=timestamp_value, updated_at=timestamp_value, author_id=new_user.id  
#                                  # Используем ID нового пользователя
#         )
#         session.add(users_board)
#         session.commit()

    # return fake_user


  

