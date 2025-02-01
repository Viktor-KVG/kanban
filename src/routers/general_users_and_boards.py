from typing import List
from fastapi import APIRouter
from src.models import OtherUsersModel
from src import core
from src.schemas import  ResponseUserBoards                       
from fastapi import APIRouter, Depends, Query,  status, HTTPException
import logging
from src.database import get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

api_router_users_and_boards = APIRouter(
    prefix="/api/users_and_boards",
    tags=["api_users_and_boards"]
)

@api_router_users_and_boards.get('/', response_model=List[ResponseUserBoards])
def insert_other_users(skip: int = Query(0, ge=0), limit: int = Query(100, gt=0), db: Session = Depends(get_db)):
    users = core.user_and_boards(skip, limit, db)
    if not users:
        print(bool(users))

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Error in data entry, such comment already exists'
                            )
    return users


@api_router_users_and_boards.delete('/delete')

def clear_other_users_model(db: Session = Depends(get_db)):
    try:
        db.query(OtherUsersModel).delete()
        db.commit()  
        return {"message": "Таблица OtherUsersModel успешно очищена."}
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=str(e))
