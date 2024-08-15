import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from src.main import app
from sqlalchemy.orm import sessionmaker, declarative_base
from src.database import get_db
from src.models import UserModel


TEST_SQL_DATABASE_URL = 'postgresql+psycopg2://postgres:1234567890t@172.18.0.1:7000/postgres_test'

test_engine = create_engine(TEST_SQL_DATABASE_URL, echo=True)
test_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
test_Base = declarative_base()


client  = TestClient(app)

def test_get_db():
    db = test_session_factory()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = test_get_db


@pytest.fixture()
def user_jwt():
    test_Base.metadata.create_all(test_engine)
    from src.models import UserModel
    yield

    with test_Base() as session:
        session.commit()
    test_Base.metadata.drop_all(test_engine)    

        