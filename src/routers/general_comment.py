from typing import List
from fastapi import APIRouter
from src import core
from src.auth import auth_jwt
from src.schemas import (ColumnId, 
                         ColumnList, 
                         ColumnPut, 
                         ColumnsModel, CommentId, CommentsList, CommentsModel, 
                         CreateColumn, CreateComment, 
                         CreateTicket, PutComment, PutTicket, 
                         SearchUsersList, TicketId, TicketsList, 
                         TicketsModel, 
                         Token, 
                         BoardsModel, 
                         CreateBoardModel,
                         BoardId, 
                         PutBoard, 
                         BoardListModel)
from fastapi import APIRouter, Depends, Query,  status, HTTPException
import logging
from src.database import session_factory, get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

api_router_comment = APIRouter(
    prefix="/api/board/{board_id}/column/{column_id}/ticket/{ticket_id}",
    tags=["api_comment"]
)


@api_router_comment.post('/comment', response_model=CommentsModel)
def creation_comment(data: CreateComment, db: Session = Depends(get_db)):
    if core.if_exist_comment(data, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error in data entry, such comment already exists'
        )
    else:
        creation = core.create_comment(data, db)
        if creation is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Failed to create comment'
                )
        return creation
    

@api_router_comment.get('/comment/list')
def show_comments_list(board_id: int, column_id: int, ticket_id: int , db: Session = Depends(get_db)):
    search_comment = core.comments_list(CommentsList(board_id=board_id, column_id=column_id, ticket_id=ticket_id), db)
    if search_comment:
        return search_comment
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )    


@api_router_comment.get('/comment/{comment_id}', response_model=CommentsModel)
def show_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment_by_id = core.search_comment_by_id(CommentId(id=comment_id),db)
    if comment_by_id:
        return comment_by_id
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )


@api_router_comment.put('/comment/{comment_id}', response_model=CommentsModel)
def comment_change(data: PutComment, db: Session = Depends(get_db)):
    comment_put = core.show_comment_by_put(data, db)
    if comment_put:
        return comment_put
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )


@api_router_comment.delete('/comment/{comment_id}')
def comment_delete(data: CommentId, db: Session = Depends(get_db)):
    comment_del = core.search_comment_by_del(data, db)
    if comment_del:
        return comment_del
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )