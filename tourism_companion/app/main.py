# from fastapi import FastAPI
# from app.database import engine
# from app.models import Base
# from app.routers import chat, speech_to_text, text_to_speech, history, tourist_circuit
# from app.services.utils import setup_logging

# from dotenv import load_dotenv
# import os
# import warnings
# warnings.filterwarnings("ignore")

# # Set up logging
# logger = setup_logging('logs/main.log')

# # Load environment variables from .env file
# load_dotenv()

# # Test if the environment variable is correctly loaded
# print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))

# logger.info(f"Load APP on MAIN")
# logger.info(f"Loaded API Key:, {os.getenv('OPENAI_API_KEY')}")

# app = FastAPI()
# Base.metadata.create_all(bind=engine)

# # Include routers
# app.include_router(chat.router, prefix="/api/v1")
# app.include_router(tourist_circuit.router, prefix="/api/v1")
# app.include_router(speech_to_text.router, prefix="/api/v1")
# app.include_router(text_to_speech.router, prefix="/api/v1")
# app.include_router(history.router, prefix="/api/v1")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5000)




from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import chat, speech_to_text, text_to_speech, history, tourist_circuit
from app.services.utils import setup_logging
 
from dotenv import load_dotenv
import os
import warnings
from fastapi.middleware.cors import CORSMiddleware
warnings.filterwarnings("ignore")
 
# Set up logging
logger = setup_logging('logs/main.log')
 
# Load environment variables from .env file
load_dotenv()
 
# Test if the environment variable is correctly loaded
print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))
 
logger.info(f"Load APP on MAIN")
logger.info(f"Loaded API Key:, {os.getenv('OPENAI_API_KEY')}")
 
app = FastAPI()
origins = [
    "http://localhost:8000",
    "https://front-hackaton.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)
Base.metadata.create_all(bind=engine)
 
# Include routers
app.include_router(chat.router, prefix="/api/v1")
app.include_router(tourist_circuit.router, prefix="/api/v1")
app.include_router(speech_to_text.router, prefix="/api/v1")
app.include_router(text_to_speech.router, prefix="/api/v1")
app.include_router(history.router, prefix="/api/v1")
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)