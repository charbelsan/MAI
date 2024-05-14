from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import chat
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test if the environment variable is correctly loaded
print("key",os.getenv('OPENAI_API_KEY'))


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(chat.router, prefix="/api/v1")
