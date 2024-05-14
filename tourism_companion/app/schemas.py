from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class ChatRequest(BaseModel):
    text: Optional[str] = None
    file: Optional[UploadFile] = None
    image: Optional[UploadFile] = None
    user_id: int
    target_lang: str

class ChatResponse(BaseModel):
    response: str
    session_id: int
