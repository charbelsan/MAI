import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
 
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
 
@app.get("/api/v1/chat/history/1/1")
async def process_audio():
    print("yes")
    return {"text": "hello"}
 
 
 
# Run the application with: uvicorn main:app --reload