from sqlalchemy.orm import Session
from app.models import User, Conversation

def start_or_get_session(db: Session, user_id: int) -> str:
    """
    Start a new session or get the existing session ID for the user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    # Check for an existing session
    conversation = db.query(Conversation).filter(Conversation.user_id == user_id).first()
    if conversation:
        return conversation.session_id

    # Create a new session if none exists
    new_session = Conversation(user_id=user_id, session_id=str(uuid.uuid4()))
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session.session_id


def store_message(db: Session, session_id: int, sender: str, content: str):
    message = Message(session_id=session_id, sender=sender, content=content)
    db.add(message)
    db.commit()


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