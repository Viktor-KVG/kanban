from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from src.settings import DB_SESSION_ECHO


# SQL_DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SQL_DATABASE_URL = 'postgresql+psycopg2://postgres:1234567890@172.28.0.1:9000/postgres'

engine = create_engine(SQL_DATABASE_URL, echo=DB_SESSION_ECHO)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
