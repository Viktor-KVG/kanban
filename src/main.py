from fastapi import FastAPI

from src.routers import general


app = FastAPI()
app.include_router(general.common_router)
app.include_router(general.api_router)
