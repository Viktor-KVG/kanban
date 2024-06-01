from models import *
from core import test_create_table
from sqlalchemy.orm import Session, declarative_base


Base.metadata.create_all(engine)
test_create_table()

print(engine)