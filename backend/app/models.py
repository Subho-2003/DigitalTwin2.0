"""
Database models for storing conversation memories and summaries
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    Stores user information.
    Simple user table for linking memories to users.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    memories = relationship("Memory", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Memory(Base):
    """
    Stores conversation memories with transcripts and AI-generated summaries.
    Links to users and assistants for organization.
    """
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    assistant_id = Column(String(100), nullable=False, index=True)  # Vapi assistant ID
    transcript = Column(Text, nullable=False)  # Full conversation transcript
    summary = Column(Text, nullable=False)  # AI-generated summary
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="memories")
    
    def __repr__(self):
        return f"<Memory(id={self.id}, user_id={self.user_id}, assistant_id={self.assistant_id})>"

