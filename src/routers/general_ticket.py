from typing import List
from fastapi import APIRouter
from src import core
from src.auth import auth_jwt
from src.schemas import (ColumnId, 
                         ColumnList, 
                         ColumnPut, 
                         ColumnsModel, 
                         CreateColumn, 
                         CreateTicket, PutTicket, 
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

api_router_ticket = APIRouter(
    prefix="/api",
    tags=["api_ticket"]
)

@api_router_ticket.post('/board/board_id/column/column_id/ticket', response_model=TicketsModel)
def creation_ticket(data: CreateTicket, db: Session = Depends(get_db)):
    if core.if_exist_ticket(data, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error in data entry, such ticket already exists'
        )
    else:
        creation = core.create_ticket(data, db)
        if creation is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Failed to create ticket'
                )
        return creation


@api_router_ticket.get('/board/{board_id}/column/{column_id}/ticket/list')
def show_tickets_list(board_id: int, column_id: int, title_ticket: str = None, db: Session = Depends(get_db)):
    search_ticket = core.tickets_list(TicketsList(id_board=board_id, id_column=column_id, title=title_ticket), db)
    if search_ticket:
        return search_ticket
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )
    

@api_router_ticket.get('/board/{board_id}/column/{column_id}/ticket/{ticket_id}', response_model=TicketsModel)
def show_tickets_by_id(board_id: int, column_id: int, ticket_id: int, db: Session = Depends(get_db)):
    ticket_by_id = core.search_ticket_by_id(TicketId(board_id=board_id,column_id=column_id, ticket_id=ticket_id),db)
    if ticket_by_id:
        return ticket_by_id
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )


@api_router_ticket.put('/board/{board_id}/column/{column_id}/ticket/{ticket_id}', response_model=TicketsModel)
def ticket_change(board_id: int, column_id: int, ticket_id: int, data: PutTicket, db: Session = Depends(get_db)):
    ticket_put = core.search_ticket_by_put(data, board_id, column_id, ticket_id, db)
    if ticket_put:
        return ticket_put
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )


@api_router_ticket.delete('/board/{board_id}/column/{column_id}/ticket/{ticket_id}')
def ticket_delete(board_id: int, column_id: int, ticket_id: int, db: Session = Depends(get_db)):
    ticket_del = core.search_ticket_by_del(TicketId(board_id=board_id, column_id=column_id, ticket_id=ticket_id), db)
    if ticket_del:
        return ticket_del
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )
