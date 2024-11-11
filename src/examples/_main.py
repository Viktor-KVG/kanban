from models import *
# from kanban.app. draft import test_create_table
from sqlalchemy.orm import mapped_column
from src.database import engine



Base.metadata.create_all(engine)

# test_create_table()

print(engine)