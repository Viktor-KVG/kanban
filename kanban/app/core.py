from sqlalchemy import text, insert, values, select
from models import *

timestamp_value = datetime.datetime.now()

def test_create_table():
    with engine.connect() as connect:
        stmt = insert(UserModel).values(
            [
                {'id': 1, 'login': 'Ivan123', 'password_hash': '546389fjcn', 'email': 'IvanVanlov@mail.ru', 'created_at': timestamp_value, 'updated_at': datetime.datetime.now()},
                {'id': 2, 'login': 'Bart434', 'password_hash': '4350sf099', 'email': 'BartSimpson@mail.ru', 'created_at': timestamp_value, 'updated_at': datetime.datetime.now()}

            ]
        )

        stmt_2 = insert(BoardModel).values(
            {'id': 1, 'title': 'First Board', 'created_at': timestamp_value, 'updated_at': datetime.datetime.now(), 'author_id': 1}
        )

        stmt_3 = insert(ColumnModel).values(
            {'id': 1, 'title': 'First Column', 'created_at': timestamp_value, 'updated_at': datetime.datetime.now(), 'board_id': 1}
        )

        stmt_4 = insert(TicketModel).values(
            {'id': 1, 'title': 'First Task', 'created_at': timestamp_value, 'updated_at': datetime.datetime.now(), 'column_id': 1, 'description': 'perform testing of new tables',
             'author_id': 1, 'deadline': '02.06.2024', 'estimate': 3.5, 'priority': 'high', 'performer_id': 2}
        )

        stmt_5 = insert(CommentModel).values(
            {'id': 1, 'created_at': timestamp_value, 'updated_at': datetime.datetime.now(), 'ticket_id': 1, 'author_id': 2, 'content': 'content'}
        )

        query = select(OtherUsersModel)
        query_2 = select(BoardModel)
        query_3 = select(UserModel.boards)


        connect.execute(stmt)
        connect.execute(stmt_2)
        connect.execute(stmt_3)
        connect.execute(stmt_4)
        connect.execute(stmt_5)
        connect.execute(query)
        connect.execute(query_2)
        connect.execute(query_3)
        connect.commit()