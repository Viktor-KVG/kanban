# Сюда нужно поместить функции, реализующие бизнес-логику
# Например, процедура логина пользователя или его регистрация
# Эти функции из app.core импортируются в обработчики запросов (роуты) и вызываются

from datetime import datetime
from hashlib import md5
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import select

from src.models import BoardModel, ColumnModel, UserModel
from src.schemas import (BoardListModel, ColumnsModel, CreateColumn, UserCreate, 
                        UserId, 
                        UserLogin, 
                        UserCreateResponse, 
                        UserLoginForAdmin, 
                        SearchUsersList, 
                        UserList, 
                        UserUpdate,
                        BoardsModel,
                        CreateBoardModel, 
                        PutBoard,
                        BoardId)
from src.database import session_factory
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


'''User'''

def is_user_exist(data: UserCreate) -> bool:
    with session_factory() as session:
        same_user = session.query(UserModel).where(UserModel.login == data.login).first() is not None
        if same_user:
            return True
        return False


def register_user(data: UserCreate) -> UserModel:

    with session_factory() as session:
        try:
            hashed_password = md5()
            hashed_password.update(data.password.encode('utf-8'))
            user = UserModel(
                password_hash=hashed_password.hexdigest(),
                **data.model_dump(exclude={"password"})
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    


def search_user_for_admin(data: UserLoginForAdmin):
    with session_factory() as session:
        search_login = session.query(UserModel).filter_by(login= data.login).first()
        if search_login:
            return search_login
        return False


def search_list_users(data1: SearchUsersList, db: Session):
    query = db.query(UserModel)

        # Добавим условия к запросу, если они указаны
    if data1.id is not None:
        query = query.filter(UserModel.id == data1.id)
    if data1.login:
        query = query.filter(UserModel.login == data1.login)
    if data1.email:
        query = query.filter(UserModel.email == data1.email)

    filtered_users = query.all()            
    result_list = []

    for user in filtered_users:
        # Получение всех досок, связанных с этим пользователем
        boards = db.query(BoardModel).filter(BoardModel.author_id == user.id).all()
        
        # Преобразование в список Pydantic моделей BoardsModel
        user_boards = [BoardsModel.from_orm(board) for board in boards]
        
        # Создаем объект Pydantic для пользователя и добавляем списки досок
        user_list_item = UserList.from_orm(user)
        user_list_item.boards = user_boards  # Присваиваем выделенные доски

        # Добавляем пользователя с его досками в результат
        result_list.append(user_list_item)

    return result_list # Возвращаем список пользователей (возможно, только один)
              
def search_user_by_id(data: UserId): 
    with session_factory() as session:
        query = session.query(UserModel)

        if data.id:
            query = query.filter(UserModel.id == data.id)

        result_id = query.first()
        logging.info(f"Retrieved user: {result_id}")

        if result_id:
            return UserList.from_orm(result_id)        
        return False

   
def search_user_by_id_put(data:UserUpdate, user_id:int):
    with session_factory() as session:
        query = session.query(UserModel).filter(UserModel.id == user_id).first()

        if query:
            query.login = data.login
            query.password = data.password
            query.email = data.email
            query.updated_at = datetime.now()
            session.commit()
            session.refresh(query)
            return query
        return False


def search_user_by_id_for_delete(data: UserId):
    with session_factory() as session:
        user_delete = session.query(UserModel).filter(UserModel.id == data.id).first()

        if user_delete:
            session.delete(user_delete)
            session.commit()
            return{'details': 'User deleted'}
        return False
        

'''Board'''

def is_board_exist(data: BoardsModel) -> bool:
    with session_factory() as session:
        same_boards = session.query(BoardModel).where(BoardModel.title == data.title).first() is not None
        if same_boards:
            return True
        return False


        
def create_board(data: CreateBoardModel):
    with session_factory() as session:
        board = BoardModel(title=data.title, author_id=data.author_id)

        if board:
            session.add(board)
            session.commit()
            session.refresh(board)
            return board

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)  

    return BoardsModel.from_orm(board)  # Используем Pydantic модель для возврата


def boards_list(data: BoardListModel):
    with session_factory() as session:
        query = session.query(BoardModel)
        if data.title:
            query = query.filter(BoardModel.title == data.title)

        list_boards = query.all()

        if list_boards:    
            return [BoardsModel.from_orm(board) for board in list_boards]
        return []


def board_id_number(data: BoardId):
    with session_factory() as session:
        board = session.query(BoardModel).where(BoardModel.id == data.id).first()
        if board:
            return board
        return False
    

def serch_board_for_put(data: PutBoard, board_id: int):
    with session_factory() as session:
        board = session.query(BoardModel).where(BoardModel.id == board_id).first()

        if board:
            board.title = data.title
            board.updated_at = datetime.now()
            session.commit()
            session.refresh(board)
            return board
        return False


def search_board_for_delete(data: BoardId):
    with session_factory() as session:
        board = session.query(BoardModel).where(BoardModel.id == data.id).first()

        if board:
            session.delete(board)
            session.commit()
            return{'details': 'Board deleted'}
        return False

'''Column'''

def if_column_exist(data: CreateColumn, db: Session):
    # Проверяем, существует ли доска с данным ID
    board = db.query(BoardModel).filter(BoardModel.id == data.boards).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Board not found'
        )

    # Проверяем, существует ли колонка с указанным заголовком в данной доске
    same_column = db.query(ColumnModel).filter(ColumnModel.title == data.title, ColumnModel.board_id == data.boards).first()  

    return same_column is not None


def create_column(data: CreateColumn, db: Session):
    if if_column_exist(data, db):
        return False  # Если колонка существует, вернуть None

    # Если колонка не существует, создаем новую
    new_column = ColumnModel(title=data.title, board_id=data.boards) # Указываем, к какой доске относится новая колонка
    db.add(new_column)
    db.commit()
    db.refresh(new_column)

    return ColumnsModel.from_orm(new_column)