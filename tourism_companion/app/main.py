from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import chat, speech_to_text, text_to_speech

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Test if the environment variable is correctly loaded
print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))


app = FastAPI()
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(chat.router, prefix="/api/v1")
#app.include_router(circuit.router, prefix="/api/v1")
app.include_router(speech_to_text.router, prefix="/api/v1")
app.include_router(text_to_speech.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)