from fastapi import FastAPI

from .routers import (general_user, 
                     general_board, 
                     general_column)


app = FastAPI()
app.include_router(general_user.common_router)
app.include_router(general_user.api_router)
app.include_router(general_board.api_router_board)
app.include_router(general_column.api_router_column)