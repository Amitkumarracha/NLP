"""
Pydantic models for API request/response schemas
"""
from pydantic import BaseModel
from typing import List

class EmotionResponse(BaseModel):
    """Response model for audio emotion prediction"""
    emotion_xgb: str
    confidence_xgb: float
    emotion_ensemble: str
    confidence_ensemble: float
    transcription: str = ""
    emotion_text: str = ""
    confidence_text: float = 0.0
    final_emotion: str = ""
    final_confidence: float = 0.0

class TextEmotionRequest(BaseModel):
    """Request model for text emotion analysis"""
    text: str

class TextEmotionResponse(BaseModel):
    """Response model for text emotion analysis"""
    text: str
    emotion: str
    confidence: float
    suggestions: List[str] = []

class ChatRequest(BaseModel):
    """Request model for chat conversation"""
    message: str
    emotion_context: str = "neutral"

class ChatResponse(BaseModel):
    """Response model for chat conversation"""
    response: str
    detected_emotion: str
    confidence: float
