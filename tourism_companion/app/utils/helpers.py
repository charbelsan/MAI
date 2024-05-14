from sqlalchemy.orm import Session
from app.models import User, ConversationSession, Message

def start_or_get_session(db: Session, user_id: int) -> int:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    session = db.query(ConversationSession).filter(ConversationSession.user_id == user_id).first()
    if not session:
        session = ConversationSession(user_id=user_id)
        db.add(session)
        db.commit()
        db.refresh(session)

    return session.id

def store_message(db: Session, session_id: int, sender: str, content: str):
    message = Message(session_id=session_id, sender=sender, content=content)
    db.add(message)
    db.commit()
