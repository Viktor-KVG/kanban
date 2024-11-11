from typing import List

from sqlalchemy import (
    func,
    Float,
    Table,
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
    declarative_base,
)


Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(60), nullable=False )
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False) 
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    boards: Mapped[List["BoardModel"]] = relationship(back_populates="user", secondary='others_users', uselist=True)

    # users_many: Mapped[List["UserModel"]] = relationship('UserModel', back_populates="board.boards_many", uselist=True, secondary='others_users',
    #                                                   primaryjoin=id == "others_users.board_id",
    #                                                   secondaryjoin=id == "others_users.user_id")


class BoardModel(Base):
    __tablename__ = 'board'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))   
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["UserModel"] = relationship(back_populates="boards", uselist=False, secondary='others_users')
    board_column: Mapped[List["ColumnModel"]] = relationship(back_populates="board", uselist=True)
    # boards_many: Mapped[List["BoardModel"]] = relationship('BoardModel', back_populates="user.users_many", uselist=True,
    #                                                        secondary='others_users',
    #                                                        primaryjoin=id == "others_users.c.user_id",
    #                                                        secondaryjoin=id == "others_users.c.board_id")


class ColumnModel(Base):
    __tablename__ = 'column_board'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    board_id: Mapped[int] = mapped_column(ForeignKey('board.id'))
    board: Mapped["BoardModel"] = relationship(back_populates="board_column", uselist=False)
    tickets_list: Mapped[List["TicketModel"]] = relationship(back_populates="column", uselist=True)    


class TicketModel(Base):
    __tablename__ = 'ticket'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    column_id: Mapped[int] = mapped_column(ForeignKey('column_board.id'))
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
    __table_args__ = (
        UniqueConstraint('user_id', 'board_id', name='others_u'),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey('board.id'), primary_key=True)


class CommentModel(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    ticket_id: Mapped[int] = mapped_column(ForeignKey('ticket.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    content: Mapped[str] = mapped_column(nullable=True)
    tickets: Mapped['TicketModel'] = relationship(back_populates='comments_list', uselist=False)
