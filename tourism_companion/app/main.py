from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import chat

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(chat.router, prefix="/api/v1")
