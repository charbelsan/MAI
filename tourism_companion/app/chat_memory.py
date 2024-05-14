from sqlalchemy.orm import Session
from langchain.chains.conversation.memory import ConversationBufferMemory
from app.models import Message

# Initialize a dictionary to store conversation memory for different sessions
conversation_memory_store = {}

def load_conversation_from_db(db: Session, session_id: int) -> ConversationBufferMemory:
    """
    Load conversation memory from the database based on the session ID.
    
    Args:
        db (Session): The database session.
        session_id (int): The session ID.
    
    Returns:
        ConversationBufferMemory: The conversation memory object for the given session.
    """
    memory = ConversationBufferMemory()
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.id).all()
    for message in messages:
        if message.sender == 'user':
            memory.add_user_input(message.content)
        elif message.sender == 'ai':
            memory.add_ai_response(message.content)
    return memory

def get_conversation_memory(db: Session, session_id: int) -> ConversationBufferMemory:
    """
    Retrieve the conversation memory for a given session. If it doesn't exist, create a new one.
    
    Args:
        db (Session): The database session.
        session_id (int): The ID of the session for which to retrieve or create the conversation memory.
    
    Returns:
        ConversationBufferMemory: The conversation memory object for the given session.
    """
    if session_id not in conversation_memory_store:
        conversation_memory_store[session_id] = load_conversation_from_db(db, session_id)
    return conversation_memory_store[session_id]
