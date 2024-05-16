import uuid
from sqlalchemy.orm import Session
from app.models import User, Conversation, Message, TouristCircuit as TouristCircuitModel, TouristPoint as TouristPointModel
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_or_get_session(db: Session, user_id: int) -> str:
    """
    Start a new session or get the existing session ID for the user.
    """
    logger.info(f"Checking existence of user with ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.info(f"User with ID {user_id} not found, creating new user.")
        new_user = User(id=user_id, username=f"user_{user_id}", email=f"user_{user_id}@example.com", hashed_password="password")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user

    # Check for an existing session
    conversation = db.query(Conversation).filter(Conversation.user_id == user_id).first()
    if conversation:
        logger.info(f"Existing session found for user ID {user_id}: {conversation.session_id}")
        return conversation.session_id

    # Create a new session if none exists
    new_session = Conversation(user_id=user_id, session_id=str(uuid.uuid4()))
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    logger.info(f"New session created for user ID {user_id}: {new_session.session_id}")
    return new_session.session_id

def store_message(db: Session, session_id: str, sender: str, message: str):
    """
    Store a message in the database.
    """
    new_message = Message(
        session_id=session_id,
        user_id=db.query(Conversation).filter(Conversation.session_id == session_id).first().user_id,
        sender=sender,
        message=message,
        timestamp=datetime.utcnow()
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

def save_tourist_circuit(db: Session, user_id: int, session_id: str, circuit_data: dict):
    """
    Save the validated tourist circuit to the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.
        session_id (str): The session ID.
        circuit_data (dict): The data of the circuit including GPS coordinates.

    Returns:
        None
    """
    # Create the tourist circuit entry
    circuit = TouristCircuitModel(user_id=user_id, session_id=session_id, validated=True)
    db.add(circuit)
    db.commit()
    db.refresh(circuit)

    # Create tourist points entries
    for point in circuit_data.get("points", []):
        tourist_point = TouristPointModel(
            circuit_id=circuit.id,
            name=point.get("name"),
            description=point.get("description"),
            visited=False
        )
        db.add(tourist_point)
    
    db.commit()
