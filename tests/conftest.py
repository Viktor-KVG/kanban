import pytest
from sqlalchemy import create_engine
from src.main import app
from sqlalchemy.orm import sessionmaker, declarative_base
from src.database import get_db
from src.models import UserModel, BoardModel
import datetime

TEST_SQL_DATABASE_URL = 'postgresql+psycopg2://postgres:1234567890t@172.24.0.1:7000/postgres'

test_engine = create_engine(TEST_SQL_DATABASE_URL, echo=True)
test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
test_Base = declarative_base()

timestamp_value = datetime.datetime.now()


def create_test_user():
    with test_session_factory() as session:
        new_user = UserModel(login='string', password_hash='string', email='string', created_at=timestamp_value, 
                             updated_at=timestamp_value,
                              is_admin=False, boards=[])
        session.add(new_user)
        session.commit()
        users_board = BoardModel(
              title='First Board', created_at=timestamp_value, updated_at=timestamp_value, author_id=new_user.id
         )        
        session.add(users_board)
        session.commit()


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
    tables = reversed(test_Base.metadata.sorted_tables)
    for table in tables:
        test_session_factory().execute(table.delete())
        test_session_factory().commit()


@pytest.fixture()
def connect_to_database():
    test_Base.metadata.create_all(test_engine)

    session = test_session_factory()
    clear_database()
    create_test_user()

    session.query(BoardModel).delete()
    session.query(UserModel).delete()
    session.commit()

    yield session
    session.close()

    test_Base.metadata.drop_all(test_engine) 





  

