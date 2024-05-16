from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user")
    messages = relationship("Message", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, created_at={self.created_at})>"

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_id = Column(String, index=True, nullable=False, unique=True)
    started_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, session_id={self.session_id}, started_at={self.started_at})>"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey('conversations.session_id'), index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sender = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, session_id={self.session_id}, user_id={self.user_id}, sender={self.sender}, message={self.message}, timestamp={self.timestamp})>"

class TouristCircuit(Base):
    __tablename__ = "tourist_circuits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_id = Column(String, index=True)
    validated = Column(Boolean, default=False)
    points = relationship("TouristPoint", back_populates="circuit")

class TouristPoint(Base):
    __tablename__ = "tourist_points"

    id = Column(Integer, primary_key=True, index=True)
    circuit_id = Column(Integer, ForeignKey('tourist_circuits.id'), nullable=False)
    name = Column(String)
    description = Column(String)
    visited = Column(Boolean, default=False)
    circuit = relationship("TouristCircuit", back_populates="points")
