import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.routers import chat

# Load environment variables from .env file
load_dotenv()

# Test if the environment variable is correctly loaded
print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))


app = FastAPI()

origins = [
    "http://localhost:3000",  # Your React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)
Base.metadata.create_all(bind=engine)

app.include_router(chat.router, prefix="/api/v1")
