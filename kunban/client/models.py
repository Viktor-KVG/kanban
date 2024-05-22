from sqlalchemy import create_engine, Column, Table, Integer, String, Boolean, ForeignKey, Float, \
    DateTime, func
from sqlalchemy.orm import Session, declarative_base


engine = create_engine("postgresql+psycopg2://postgres:1234567890@localhost:5432/postgres", echo=True,)
Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String(length=60), nullable=False)
    password_hash = Column(String(length=60), nullable=False) 
    email = Column( String(length=160), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_admin = Column(Boolean, default=False, nullable=False)


class BoardModel(Base):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    title = Column(String(length=120))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(ForeignKey('user.c.id'))


class ColumnModel(Base):
    __tablename__ = 'column'
    id = Column(Integer, primary_key=True)
    title = Column(String(length=120))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    board_id = Column(ForeignKey('board.c.id'))    


class TicketModel(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True)
    title = Column(String(length=120))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    column_id = Column(ForeignKey('column.c.id'))
    description = Column(String, nullable=False)
    author_id = Column(ForeignKey('user.c.id'))
    deadline = Column(String, nullable=True)
    estimate = Column(Float, nullable=True)
    priority = Column(String, nullable=True)
    performer_id = Column(ForeignKey('user.c.id'))


class OtherUsersModel(Base):
    __tablename__ = 'others_users'
    user_id = Column(ForeignKey('user.c.id'))
    board_id = Column(ForeignKey('board.c.id'))


class CommentModel(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    ticket_id = Column(ForeignKey('ticket.c.id'))
    author_id = Column(ForeignKey('user.c.id'))
    content = Column(String, nullable=False)

# with Session(engine) as session:
#     with session.begin():
#         UserModel.metadata.create_all(engine)
#         user = UserModel(user_id=1, name='Jack', fullname='Jack Cow')
#         session.add(user)


#Base.create_all(engine)

print(engine)
