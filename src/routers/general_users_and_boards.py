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
                         PutBoard)
from fastapi import APIRouter, Depends, Query,  status, HTTPException
import logging
from src.database import session_factory, get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

api_router_comment = APIRouter(
    prefix="/api/board/{board_id}/column/{column_id}/ticket/{ticket_id}",
    tags=["api_comment"]
)