"""
Database repository layer
Handles all CRUD operations for both PostgreSQL and MongoDB
"""
from datetime import datetime
from typing import Dict, List, Optional
import logging

from config import DB_TYPE

logger = logging.getLogger(__name__)

# =====================================================
# POSTGRESQL REPOSITORY
# =====================================================
if DB_TYPE == "postgresql":
    from database.connection import SessionLocal
    from database.models import User, Conversation, EmotionLog
    
    class PostgresRepository:
        """PostgreSQL database operations"""
        
        @staticmethod
        def create_user(username: str, email: Optional[str] = None) -> int:
            """Create new user"""
            db = SessionLocal()
            try:
                # Check if user exists
                existing = db.query(User).filter(User.username == username).first()
                if existing:
                    return existing.id
                
                user = User(username=username, email=email)
                db.add(user)
                db.commit()
                db.refresh(user)
                return user.id
            except Exception as e:
                db.rollback()
                logger.error(f"Failed to create user: {e}")
                raise
            finally:
                db.close()
        
        @staticmethod
        def store_conversation(
            user_id: int,
            mode: str,
            user_input: str,
            detected_emotion: str,
            confidence: float,
            model_used: str,
            bot_response: str,
            audio_path: Optional[str] = None,
            all_predictions: Optional[Dict] = None,
            session_id: Optional[str] = None
        ) -> int:
            """Store conversation in database"""
            db = SessionLocal()
            try:
                conversation = Conversation(
                    user_id=user_id,
                    mode=mode,
                    user_input=user_input,
                    audio_path=audio_path,
                    detected_emotion=detected_emotion,
                    confidence=confidence,
                    model_used=model_used,
                    all_predictions=all_predictions,
                    bot_response=bot_response,
                    session_id=session_id
                )
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
                return conversation.id
            except Exception as e:
                db.rollback()
                logger.error(f"Failed to store conversation: {e}")
                raise
            finally:
                db.close()
        
        @staticmethod
        def store_emotion_log(
            conversation_id: int,
            model_name: str,
            predicted_emotion: str,
            confidence: float,
            probabilities: Optional[Dict] = None,
            inference_time_ms: Optional[float] = None
        ) -> int:
            """Store detailed emotion prediction log"""
            db = SessionLocal()
            try:
                emotion_log = EmotionLog(
                    conversation_id=conversation_id,
                    model_name=model_name,
                    predicted_emotion=predicted_emotion,
                    confidence=confidence,
                    probabilities=probabilities,
                    inference_time_ms=inference_time_ms
                )
                db.add(emotion_log)
                db.commit()
                db.refresh(emotion_log)
                return emotion_log.id
            except Exception as e:
                db.rollback()
                logger.error(f"Failed to store emotion log: {e}")
                raise
            finally:
                db.close()
        
        @staticmethod
        def get_conversation_history(user_id: int, limit: int = 50) -> List[Dict]:
            """Retrieve conversation history for a user"""
            db = SessionLocal()
            try:
                conversations = db.query(Conversation).filter(
                    Conversation.user_id == user_id
                ).order_by(Conversation.timestamp.desc()).limit(limit).all()
                
                return [{
                    'id': conv.id,
                    'mode': conv.mode,
                    'user_input': conv.user_input,
                    'detected_emotion': conv.detected_emotion,
                    'confidence': conv.confidence,
                    'model_used': conv.model_used,
                    'bot_response': conv.bot_response,
                    'timestamp': conv.timestamp.isoformat()
                } for conv in conversations]
            except Exception as e:
                logger.error(f"Failed to retrieve conversation history: {e}")
                return []
            finally:
                db.close()
        
        @staticmethod
        def get_emotion_analytics(user_id: int) -> Dict:
            """Get emotion analytics for a user"""
            db = SessionLocal()
            try:
                conversations = db.query(Conversation).filter(
                    Conversation.user_id == user_id
                ).all()
                
                if not conversations:
                    return {}
                
                # Count emotions
                emotion_counts = {}
                for conv in conversations:
                    emotion = conv.detected_emotion
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                
                total = len(conversations)
                emotion_percentages = {
                    emotion: (count / total) * 100 
                    for emotion, count in emotion_counts.items()
                }
                
                return {
                    'total_conversations': total,
                    'emotion_distribution': emotion_counts,
                    'emotion_percentages': emotion_percentages,
                    'most_common_emotion': max(emotion_counts, key=emotion_counts.get),
                    'average_confidence': sum(c.confidence for c in conversations) / total
                }
            except Exception as e:
                logger.error(f"Failed to get emotion analytics: {e}")
                return {}
            finally:
                db.close()
    
    Repository = PostgresRepository

# =====================================================
# MONGODB REPOSITORY
# =====================================================
elif DB_TYPE == "mongodb":
    from database.connection import get_mongo_db
    from bson import ObjectId
    
    class MongoRepository:
        """MongoDB database operations"""
        
        @staticmethod
        def create_user(username: str, email: Optional[str] = None) -> str:
            """Create new user"""
            try:
                db = get_mongo_db()
                users = db["users"]
                
                # Check if user exists
                existing = users.find_one({"username": username})
                if existing:
                    return str(existing["_id"])
                
                user_doc = {
                    "username": username,
                    "email": email,
                    "created_at": datetime.utcnow(),
                    "last_active": datetime.utcnow()
                }
                result = users.insert_one(user_doc)
                return str(result.inserted_id)
            except Exception as e:
                logger.error(f"Failed to create user: {e}")
                raise
        
        @staticmethod
        def store_conversation(
            user_id: str,
            mode: str,
            user_input: str,
            detected_emotion: str,
            confidence: float,
            model_used: str,
            bot_response: str,
            audio_path: Optional[str] = None,
            all_predictions: Optional[Dict] = None,
            session_id: Optional[str] = None
        ) -> str:
            """Store conversation in MongoDB"""
            try:
                db = get_mongo_db()
                conversations = db["conversations"]
                
                conv_doc = {
                    "user_id": user_id,
                    "mode": mode,
                    "user_input": user_input,
                    "audio_path": audio_path,
                    "detected_emotion": detected_emotion,
                    "confidence": confidence,
                    "model_used": model_used,
                    "all_predictions": all_predictions,
                    "bot_response": bot_response,
                    "session_id": session_id,
                    "timestamp": datetime.utcnow()
                }
                result = conversations.insert_one(conv_doc)
                return str(result.inserted_id)
            except Exception as e:
                logger.error(f"Failed to store conversation: {e}")
                raise
        
        @staticmethod
        def store_emotion_log(
            conversation_id: str,
            model_name: str,
            predicted_emotion: str,
            confidence: float,
            probabilities: Optional[Dict] = None,
            inference_time_ms: Optional[float] = None
        ) -> str:
            """Store emotion prediction log"""
            try:
                db = get_mongo_db()
                emotions = db["emotions"]
                
                emotion_doc = {
                    "conversation_id": conversation_id,
                    "model_name": model_name,
                    "predicted_emotion": predicted_emotion,
                    "confidence": confidence,
                    "probabilities": probabilities,
                    "inference_time_ms": inference_time_ms,
                    "timestamp": datetime.utcnow()
                }
                result = emotions.insert_one(emotion_doc)
                return str(result.inserted_id)
            except Exception as e:
                logger.error(f"Failed to store emotion log: {e}")
                raise
        
        @staticmethod
        def get_conversation_history(user_id: str, limit: int = 50) -> List[Dict]:
            """Retrieve conversation history"""
            try:
                db = get_mongo_db()
                conversations = db["conversations"]
                
                cursor = conversations.find(
                    {"user_id": user_id}
                ).sort("timestamp", -1).limit(limit)
                
                return [{
                    'id': str(doc['_id']),
                    'mode': doc['mode'],
                    'user_input': doc['user_input'],
                    'detected_emotion': doc['detected_emotion'],
                    'confidence': doc['confidence'],
                    'model_used': doc['model_used'],
                    'bot_response': doc['bot_response'],
                    'timestamp': doc['timestamp'].isoformat()
                } for doc in cursor]
            except Exception as e:
                logger.error(f"Failed to retrieve conversation history: {e}")
                return []
        
        @staticmethod
        def get_emotion_analytics(user_id: str) -> Dict:
            """Get emotion analytics for a user"""
            try:
                db = get_mongo_db()
                conversations = db["conversations"]
                
                cursor = conversations.find({"user_id": user_id})
                convs = list(cursor)
                
                if not convs:
                    return {}
                
                # Count emotions
                emotion_counts = {}
                for conv in convs:
                    emotion = conv['detected_emotion']
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                
                total = len(convs)
                emotion_percentages = {
                    emotion: (count / total) * 100 
                    for emotion, count in emotion_counts.items()
                }
                
                return {
                    'total_conversations': total,
                    'emotion_distribution': emotion_counts,
                    'emotion_percentages': emotion_percentages,
                    'most_common_emotion': max(emotion_counts, key=emotion_counts.get),
                    'average_confidence': sum(c['confidence'] for c in convs) / total
                }
            except Exception as e:
                logger.error(f"Failed to get emotion analytics: {e}")
                return {}
    
    Repository = MongoRepository

else:
    # No database configured
    class DummyRepository:
        """Dummy repository when no database is configured"""
        @staticmethod
        def create_user(*args, **kwargs):
            return "dummy_user_id"
        
        @staticmethod
        def store_conversation(*args, **kwargs):
            return "dummy_conversation_id"
        
        @staticmethod
        def store_emotion_log(*args, **kwargs):
            return "dummy_log_id"
        
        @staticmethod
        def get_conversation_history(*args, **kwargs):
            return []
        
        @staticmethod
        def get_emotion_analytics(*args, **kwargs):
            return {}
    
    Repository = DummyRepository
