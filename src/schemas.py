from datetime import datetime
from typing import Any, List, Optional, ClassVar, Union

from fastapi import Query
from pydantic import BaseModel, ConfigDict, conint

'''Boards'''
class BoardsModel(BaseModel):
    id: int
    title: str
    author_id: int
    class Config:

        from_attributes = True


class BoardListModel(BaseModel):
    title: Optional[str] = None

    class Config:
        from_attributes = True


class CreateBoardModel(BaseModel):
    title: str
    author_id: int


    class Config:
        from_attributes = True


class BoardId(BaseModel):
    id: int 

    class Config:
        from_attributes = True    


class PutBoard(BaseModel):
    title: str

    class Config:
        from_attributes = True
    

'''Column''' 
class ColumnsModel(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    board_id: int    #'BoardsModel.id'
    board: BoardsModel  # Загрузка родителя, если нужно
    tickets_list: List['TicketsModel'] = []  # Список тикетов, по умолчанию пустой
    class Config:
        from_attributes = True


class CreateColumn(BaseModel):
    title: str
    boards: int
    class Config:
        from_attributes = True


class ColumnId(BaseModel):
    id_board: int
    id_column: int 
    class Config:
        from_attributes = True


class ColumnList(BaseModel):
    id_board: int
    title: Optional[str] = None
    class Config:
        from_attributes = True


class ColumnPut(BaseModel):
    title: str
    class Config:
        from_attributes = True        


'''Ticket'''
class TicketsModel(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    column_id: int  #'ColumnModel.id'
    description: str
    author_id: int  #'UserId'
    deadline: str
    estimate: float
    priority: str
    performer_id: int  #'UserId'
    comments_list: List["CommentsModel"] = [] 
    class Config:
        from_attributes = True


class ListTickets(BaseModel):
    tickets_list: List[TicketsModel]
    class Config:
        from_attributes = True


class TicketsList(BaseModel):
    id_board: int
    id_column: int
    title: Optional[str] = None
    class Config:
        from_attributes = True        


class CreateTicket(BaseModel):
    title: str
    board_id: int 
    column_id: int    #'ColumnModel.id'
    description: str
    author_id: int   #'UserId'
    deadline: str
    estimate: float
    priority: str
    performer_id: int   #'UserId'
    class Config:
        from_attributes = True


class TicketId(BaseModel):
    board_id: int
    column_id: int
    ticket_id: int 
    class Config:
        from_attributes = True


class PutTicket(BaseModel):
    title: str
    description: str
    deadline: str
    estimate: float
    priority: str
    performer_id: int   #'UserId'    
    class Config:
        from_attributes = True


'''Comment'''
class CommentsModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    ticket_id: int   #'TicketModel.id'
    author_id: int   #"UserId"
    content: str
    class Config:
        from_attributes = True


class ListComment(BaseModel):
    comments_list: List[CommentsModel]
    class Config:
        from_attributes = True


class CommentsList(BaseModel):
    board_id: int
    column_id: int
    ticket_id: int 
    class Config:
        from_attributes = True    


class CreateComment(BaseModel):

    board_id: int
    column_id: int
    ticket_id: int   #'TicketModel.id'
    author_id: int
    content: str  
    class Config:
        from_attributes = True


class CommentId(BaseModel):
    id: int
    class Config:
        from_attributes = True


class PutComment(BaseModel):
    id: int
    content: str
    class Config:
        from_attributes = True
  

'''Users'''
class UserForAdmin(BaseModel):
    id: int
    login: str
    email: str
    created_at: datetime
    updated_at: datetime
    is_admin: bool
    boads: Union[list[BoardsModel], None] = Query(default=None)
    class Config:
        from_attributes = True 


class UserList(BaseModel):
    id: int
    login: str
    email: str
    created_at: datetime
    updated_at: datetime
    is_admin: bool
    boards: Optional[list[BoardsModel]] = None
    class Config:
        from_attributes = True   
 

class UserLoginForAdmin(BaseModel):
    login: str


class SearchUsersList(BaseModel):
    id: Optional[int] = None
    login: Optional[str] = None
    email: Optional[str] = None   
    class Config:
        from_attributes = True          



class UserLogin(BaseModel):
    login: str
    password: str
    class Config:
        from_attributes = True 


class UserCreate(BaseModel):
    login: str
    password: str
    email: str  
    class Config:
        from_attributes = True 


class UserCreateResponse(BaseModel):
    id: int
    login: str
    email: str
    is_admin: bool
    class Config:
        from_attributes = True 


class Token(BaseModel):
    token: str


class UserId(BaseModel):
    id: int 


class UserUpdate(BaseModel):
    login: str
    password: str
    email: str
    class Config:
        from_attributes = True 


class UsersAndBoards(BaseModel):
    user_id: int
    board_id: int
    class Config:
        from_attributes = True        


class ResponseUserBoards(BaseModel):
    user: int
    boards: List[BoardsModel] = []
    class Config:
        from_attributes = True 
