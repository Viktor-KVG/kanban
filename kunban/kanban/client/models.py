from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String, Boolean, ForeignKey, Float, \
    DateTime, func


metadata = MetaData()

engine = create_engine("postgresql+psycopg2://postgres:1234567890@localhost:5432/postgres", echo=True,)

user = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('login', String(length=60), nullable=False),
    Column('password_hash', String(length=60), nullable=False),
    Column('email', String(length=160), nullable=False),
    Column('created_at', DateTime(timezone=True), default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
    Column('is_admin', Boolean, default=False, nullable=False),
)


board = Table(
    'board',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(length=120)),
    Column('created_at', DateTime(timezone=True), default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
    Column('author_id', Integer, ForeignKey(user.c.id))
)


column = Table(
    'column',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(length=120)),
    Column('created_at', DateTime(timezone=True), default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
    Column('board_id', Integer, ForeignKey(board.c.id))
)


ticket = Table(
    'ticket',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(length=120)),
    Column('created_at', DateTime(timezone=True), default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
    Column('column_id', Integer, ForeignKey(column.c.id)),
    Column('description', String, nullable=False),
    Column('author_id', Integer, ForeignKey(user.c.id)),
    Column('deadline', String, nullable=True),
    Column('estimate', Float, nullable=True),
    Column('priority', String, nullable=True),
    Column('performer_id', Integer, ForeignKey(user.c.id))
)


others_users = Table(
    'others_users',
    metadata,
    Column('user_id', Integer, ForeignKey(user.c.id)),
    Column('board_id', Integer, ForeignKey(board.c.id)),
)


comment = Table(
    'comment',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('created_at', DateTime(timezone=True), default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
    Column('ticket_id', Integer, ForeignKey(ticket.c.id)),
    Column('author_id', Integer, ForeignKey(user.c.id)),
    Column('content', String, nullable=False)
)


metadata.create_all(engine)

print(engine)