from sqlalchemy.orm import Session
from app.models import Message
from langchain.memory import ConversationBufferMemory

conversation_memory_store = {}

def load_conversation_from_db(db: Session, session_id: str) -> ConversationBufferMemory:
    """
    Load the conversation history from the database and populate the ConversationBufferMemory.

    Args:
        db (Session): The database session.
        session_id (str): The session ID.

    Returns:
        ConversationBufferMemory: The populated conversation memory.
    """
    messages = db.query(Message).filter_by(session_id=session_id).order_by(Message.timestamp).all()
    memory = ConversationBufferMemory()
    for message in messages:
        if message.sender == "user":
            memory.save_context({"input": message.message}, {})
        elif message.sender == "ai":
            memory.save_context({}, {"output": message.message})
    return memory

def get_conversation_memory(db: Session, session_id: str) -> ConversationBufferMemory:
    """
    Get the conversation memory for a session. If it does not exist, load it from the database.

    Args:
        db (Session): The database session.
        session_id (str): The session ID.

    Returns:
        ConversationBufferMemory: The conversation memory.
    """
    if session_id not in conversation_memory_store:
        conversation_memory_store[session_id] = load_conversation_from_db(db, session_id)
    return conversation_memory_store[session_id]
