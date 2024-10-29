from typing import List
from fastapi import APIRouter
from src import core
from src.auth import auth_jwt
from src.schemas import (ColumnList, ColumnsModel, CreateColumn, PutColumn, SearchUsersList, Token, 
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

api_router_column = APIRouter(
    prefix="/api",
    tags=["api_column"]
)


@api_router_column.post('/board/board_id/column', response_model=ColumnsModel)
def create_column_model(data: CreateColumn, db: Session = Depends(get_db)):
    if core.if_column_exist(data, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error in data entry, such column already exists'
        )
    else:
        column = core.create_column(data, db)
        print(f"Created column: {column}")
        if column is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Failed to create column'
                )
        return column


@api_router_column.get('/board/board_id/column/list')
def show_column_list(id_board:int, title_column:str = None,  db: Session = Depends(get_db)):
    list_col = core.columns_list(PutColumn(id_board=id_board, title=title_column), db)
    if list_col:
        return list_col
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )

