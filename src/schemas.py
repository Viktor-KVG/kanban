from datetime import datetime
from typing import Any, List, Optional, ClassVar, Union

from fastapi import Query
from pydantic import BaseModel, ConfigDict, conint

'''Boards'''
class BoardsModel(BaseModel):
    title: str
    created_at: datetime
    updated_at: datetime
    author_id: 'UserId'
    board_column: Union[List['ColumnModel'], None] = None
    class Config:

        from_attributes = True


class CreateBoardModel(BaseModel):
    title: str
    author_id: 'UserId'
    board_column: Union[List['ColumnModel'], None] = None


class BoardId(BaseModel):
    id: int 


class PutBoard(BaseModel):
    title: str

    


'''Column''' 
class ColumnModel(BaseModel):
    title: str
    created_at: datetime
    updated_at: datetime
    board_id: 'BoardsModel.id'
    board: 'BoardsModel'
    tickets_list: List['TicketModel']


class ColumnList(BaseModel):
    board_column: List['ColumnModel']


class CreateColumn(BaseModel):
    title: str
    created_at: datetime
    updated_at: datetime


class ColumnId(BaseModel):
    id: int 


class PutColumn(BaseModel):
    title: str



'''Ticket'''
class TicketModel(BaseModel):
    title: str
    created_at: datetime
    updated_at: datetime
    column_id: ColumnModel.id
    description: str
    author_id: 'UserId'
    deadline: str
    estimate: float
    priority: str
    performer_id: 'UserId'
    comments_list: List["CommentModel"] 


class ListTickets(BaseModel):
    tickets_list: List[TicketModel]


class CreateTicket(BaseModel):
    title: str
    created_at: datetime
    updated_at: datetime
    column_id: ColumnModel.id
    description: str
    author_id: 'UserId'
    deadline: str
    estimate: float
    priority: str
    performer_id: 'UserId'


class TicketId(BaseModel):
    id: int 


class PutTicket(BaseModel):
    title: str
    column_id: ColumnModel.id
    description: str
    author_id: 'UserId'
    deadline: str
    estimate: float
    priority: str
    performer_id: 'UserId'    


'''Comment'''
class CommentModel(BaseModel):
    created_at: datetime
    updated_at: datetime
    ticket_id: 'TicketModel.id'
    author_id: "UserId"
    content: str

class ListComment(BaseModel):
    comments_list: List[CommentModel]


class CreateComment(BaseModel):

    ticket_id: 'TicketModel.id'
    content: str  


class CommentId(BaseModel):
    id: int



class PutComment(BaseModel):
    id: int
    content: str

  

'''Users'''
class UserForAdmin(BaseModel):
    # model_config = ConfigDict(ignored_types=(IgnoredType,))
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
    # model_config = ConfigDict(ignored_types=(IgnoredType,))
    id: int
    login: str
    email: str
    created_at: datetime
    updated_at: datetime
    is_admin: bool
    boads: Union[list[BoardsModel], None] = None

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


