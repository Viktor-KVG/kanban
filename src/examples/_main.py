from models import *
from kanban.app._draft import test_create_table
from sqlalchemy.orm import mapped_column



Base.metadata.create_all(engine)

test_create_table()

print(engine)