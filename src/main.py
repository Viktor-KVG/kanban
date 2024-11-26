from fastapi import FastAPI

from .routers import (general_user, 
                     general_board, 
                     general_column,
                     general_ticket,
                     general_comment,
                     general_users_and_boards
                     )


app = FastAPI()
app.include_router(general_user.common_router)
app.include_router(general_user.api_router)
app.include_router(general_board.api_router_board)
app.include_router(general_column.api_router_column)
app.include_router(general_ticket.api_router_ticket)
app.include_router(general_comment.api_router_comment)
app.include_router(general_users_and_boards.api_router_users_and_boards)