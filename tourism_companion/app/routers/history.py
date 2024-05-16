from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.schemas import ChatHistoryResponse, ChatMessage
from app.models import Message
from typing import List

router = APIRouter()

@router.get("/chat/history/{user_id}/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: int, session_id: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter_by(user_id=user_id, session_id=session_id).all()
    if not messages:
         return ChatHistoryResponse(messages=[])

    return ChatHistoryResponse(messages=[ChatMessage.from_orm(message) for message in messages])
