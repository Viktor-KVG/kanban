import datetime
from sqlalchemy import text, insert, values, select
# from models import *
from .models import BoardModel, ColumnModel, CommentModel, OtherUsersModel, TicketModel, UserModel, engine

from sqlalchemy.orm import sessionmaker, mapped_column

timestamp_value = datetime.datetime.now()

session_factory = sessionmaker(autoflush=False, bind=engine)

def test_create_table():
    with session_factory() as session:
        stmt = UserModel(           
                id = 1, login = 'Ivan123', password_hash = '546389fjcn', email = 'IvanVanlov@mail.ru', created_at = timestamp_value, updated_at = datetime.datetime.now()                       
        )

        stmt_2 = UserModel(id = 2, login = 'Bart434', password_hash =  '4350sf099', email =  'BartSimpson@mail.ru', created_at = timestamp_value, updated_at = datetime.datetime.now()
        )
        session.add_all([stmt, stmt_2])
        session.commit()
        stmt_3 = BoardModel(
            id =  1, title = 'First Board', created_at = timestamp_value, updated_at =  datetime.datetime.now(), author_id = stmt_2.id
        )

        stmt_4 = ColumnModel(
            id = 1, title = 'First Column', created_at = timestamp_value, updated_at = datetime.datetime.now(), board_id = 1
        )

        stmt_5 = TicketModel(
            id = 1, title = 'First Task', created_at = timestamp_value, updated_at = datetime.datetime.now(), column_id = 1, description = 'perform testing of new tables',
             author_id = stmt_2.id, deadline = '02.06.2024', estimate = 3.5, priority = 'high', performer_id = stmt_2.id
        )

        stmt_6 = CommentModel(
            id = 1, created_at = timestamp_value, updated_at = datetime.datetime.now(), ticket_id = 1, author_id = stmt_2.id, content = 'content'
        )


        
        session.add_all([stmt_3, stmt_4, stmt_5, stmt_6])

        session.query(OtherUsersModel)
        session.query(BoardModel)
        session.query(UserModel.boards).all()
        session.commit()