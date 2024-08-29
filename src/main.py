from fastapi import FastAPI

from .routers import general_user


app = FastAPI()
app.include_router(general_user.common_router)
app.include_router(general_user.api_router)