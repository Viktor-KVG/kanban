from typing import List
from fastapi import APIRouter
from src import core
from src.auth import auth_jwt
from src.schemas import (SearchUsersList, Token, 
                         BoardsModel, 
                         CreateBoardModel,
                         BoardId, 
                         PutBoard, 
                         BoardListModel)
from fastapi import APIRouter, Depends, Query,  status, HTTPException
import logging

logger = logging.getLogger(__name__)

api_router_board = APIRouter(
    prefix="/api",
    tags=["api_board"]
)

@api_router_board.post("/board", response_model=BoardsModel) 
def create_board_model(data: CreateBoardModel):
    logger.info("Creating board with data: %s", data)
    if core.is_board_exist(data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error in data entry, such board already exists'
        )

    else:
        board = core.create_board(data)
        return board
    

@api_router_board.get('/board/list', response_model=List[BoardsModel])
def boards_list(board_title: str = None):
    boadrs = core.boards_list(BoardListModel(title=board_title))
    if boadrs:
        return boadrs
    
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Board not found'
            )


@api_router_board.get('/board/{board_id}')
def search_board_id(id_number: int):
    if id_number <= 0:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail='Board ID must not be zero'
        )
    
    id_board = core.board_id_number(BoardId(id=id_number))

    if id_board:
        return id_board
    
    if id_board == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid id number '
        )     
    

@api_router_board.put('/board/{board_id}', response_model=BoardsModel)
def put_board_id(board_id: int, board_update: PutBoard):
    if board_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail='Board ID must not be zero'
        )    

    board_put = core.serch_board_for_put(board_update, board_id)

    if board_put:
        return board_put
    
    if board_put == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid board '
        )
    

@api_router_board.delete('/board/{user_id}')
def delete_board_id(board_id: int):
    if board_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail='Board ID must not be zero'
        )    

    board_del = core.search_board_for_delete(BoardId(id=board_id))

    if board_del:
        return board_del
    
    if board_del == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid board '
        )   