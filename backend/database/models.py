"""
Database models for PostgreSQL
Defines User, Conversation, and EmotionLog tables
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base

# =====================================================
# USER MODEL
# =====================================================
class User(Base):
    """User profile table"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

# =====================================================
# CONVERSATION MODEL
# =====================================================
class Conversation(Base):
    """Conversation history table"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Input data
    mode = Column(String(20), nullable=False)  # 'audio' or 'text'
    user_input = Column(Text, nullable=False)  # Text or transcription
    audio_path = Column(String(500), nullable=True)  # Path to audio file if audio mode
    
    # Emotion detection results
    detected_emotion = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    model_used = Column(String(100), nullable=False)
    all_predictions = Column(JSON, nullable=True)  # Store all model predictions
    
    # Response
    bot_response = Column(Text, nullable=False)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    session_id = Column(String(100), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    emotion_logs = relationship("EmotionLog", back_populates="conversation")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, emotion={self.detected_emotion})>"

# =====================================================
# EMOTION LOG MODEL
# =====================================================
class EmotionLog(Base):
    """Detailed emotion prediction log from all models"""
    __tablename__ = "emotion_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    
    # Model-specific predictions
    model_name = Column(String(100), nullable=False)  # e.g., 'wav2vec2', 'xgboost', 'text'
    predicted_emotion = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    probabilities = Column(JSON, nullable=True)  # All class probabilities
    
    # Performance metrics
    inference_time_ms = Column(Float, nullable=True)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="emotion_logs")
    
    def __repr__(self):
        return f"<EmotionLog(model={self.model_name}, emotion={self.predicted_emotion}, conf={self.confidence})>"

# =====================================================
# MONGODB SCHEMA (Document structure reference)
# =====================================================
"""
MongoDB Collections:

1. users
{
    "_id": ObjectId,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": ISODate,
    "last_active": ISODate
}

2. conversations
{
    "_id": ObjectId,
    "user_id": "user_object_id",
    "mode": "audio" | "text",
    "user_input": "transcription or text",
    "audio_path": "path/to/audio.wav",
    "detected_emotion": "happy",
    "confidence": 0.89,
    "model_used": "wav2vec2",
    "all_predictions": {
        "wav2vec2": {"emotion": "happy", "confidence": 0.89},
        "hubert": {"emotion": "happy", "confidence": 0.85},
        "xgboost": {"emotion": "neutral", "confidence": 0.65}
    },
    "bot_response": "I'm glad to hear that!",
    "timestamp": ISODate,
    "session_id": "session_xyz"
}

3. emotions
{
    "_id": ObjectId,
    "conversation_id": "conversation_object_id",
    "model_name": "wav2vec2",
    "predicted_emotion": "happy",
    "confidence": 0.89,
    "probabilities": {
        "angry": 0.02,
        "happy": 0.89,
        "sad": 0.05,
        ...
    },
    "inference_time_ms": 125.5,
    "timestamp": ISODate
}
"""
