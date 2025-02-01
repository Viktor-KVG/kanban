
from fastapi import APIRouter
from src import core
from src.schemas import (ColumnId, 
                         ColumnList, 
                         ColumnPut, 
                         ColumnsModel, 
                         CreateColumn, 
)
from fastapi import APIRouter, Depends, Query,  status, HTTPException
import logging
from src.database import session_factory, get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

api_router_column = APIRouter(
    prefix="/api/board/{board_id}",
    tags=["api_column"]
)


@api_router_column.post('/column', response_model=ColumnsModel)
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


@api_router_column.get('/column/list')
def show_column_list(id_board: int, title_column: str = None,  db: Session = Depends(get_db)):
    list_col = core.columns_list(ColumnList(id_board=id_board, title=title_column), db)
    if list_col:
        return list_col
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )


@api_router_column.get('/column/{column_id}/', response_model= ColumnsModel)
def show_column_by_id(id_board: int, id_column: int, db: Session = Depends(get_db)):
    one_column = core.search_column_by_id(ColumnId(id_board=id_board, id_column=id_column), db)
    if one_column:
        return one_column
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )

    
@api_router_column.put('/column/{column_id}/', response_model= ColumnsModel)
def change_column(board_id:int, column_id: int, column: ColumnPut, db: Session = Depends(get_db)):
    print(f'Called change_column with board_id={board_id}, column_id={column_id}')
    column_update = core.search_column_for_put(column, board_id, column_id, db)

    if column_update:
        return column_update
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )


@api_router_column.delete('/column/{column_id}/')
def delete_column(board_id:int, column_id: int, db: Session = Depends(get_db)):
    column_delete = core.search_column_for_delete(board_id, column_id, db)
    if column_delete:
        return column_delete
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='The request failed'
                )
    


    