from sqlalchemy import create_engine, Column, Table, Integer, String, Boolean, ForeignKey, Float, \
    DateTime, func
from sqlalchemy.orm import Session, declarative_base, mapped_column, Mapped, relationship
from typing import List


engine = create_engine("postgresql+psycopg2://postgres:1234567890@localhost:5432/postgres", echo=True,)
Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(60), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    boards: Mapped[List["BoardModel"]] = relationship(back_populates="user", uselist=True, secondary='others_users')


class BoardModel(Base):
    __tablename__ = 'board'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))   
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["UserModel"] = relationship(back_populates="boards", uselist=False)
    board_column: Mapped[List["ColumnModel"]] = relationship(back_populates="board", uselist=True, secondary='others_users')


class ColumnModel(Base):
    __tablename__ = 'column'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    board_id: Mapped[int] = mapped_column(ForeignKey('board.id'))
    board: Mapped["BoardModel"] = relationship(back_populates="board_column", uselist=False)
    tickets_list: Mapped[List["TicketModel"]] = relationship(back_populates="column", uselist=True)    


class TicketModel(Base):
    __tablename__ = 'ticket'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    column_id: Mapped[int] = mapped_column(ForeignKey('column.id'))
    description: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    deadline: Mapped[str] = mapped_column(nullable=True)
    estimate: Mapped[float] = mapped_column(nullable=True)
    priority: Mapped[str] = mapped_column(nullable=True)
    performer_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    column: Mapped["ColumnModel"] = relationship(back_populates="tickets_list", uselist=False)
    comments_list: Mapped[List["CommentModel"]] = relationship(back_populates="tickets", uselist=True)


class OtherUsersModel(Base):
    __tablename__ = 'others_users'
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey('board.id'), primary_key=True)


class CommentModel(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    ticket_id: Mapped[int] = mapped_column(ForeignKey('ticket.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    content: Mapped[str] = mapped_column(nullable=True)
    tikets: Mapped['TicketModel'] = relationship(back_populates='comments_list', uselist=False)




Base.metadata.create_all(engine)

print(engine)

