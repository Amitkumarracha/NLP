"""
Database connection and initialization
Supports both PostgreSQL and MongoDB based on configuration
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import logging

from config import DATABASE_URL, MONGODB_URL, MONGODB_DB_NAME, DB_TYPE

logger = logging.getLogger(__name__)

# =====================================================
# POSTGRESQL / SUPABASE CONNECTION
# =====================================================
if DB_TYPE == "postgresql":
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        
        def get_db():
            """Get database session"""
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
        
        logger.info("✅ PostgreSQL database configured")
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection failed: {e}")
        engine = None
        SessionLocal = None
        Base = None

# =====================================================
# MONGODB CONNECTION
# =====================================================
elif DB_TYPE == "mongodb":
    try:
        mongo_client = MongoClient(MONGODB_URL)
        mongo_db = mongo_client[MONGODB_DB_NAME]
        
        # Collections
        users_collection = mongo_db["users"]
        conversations_collection = mongo_db["conversations"]
        emotions_collection = mongo_db["emotions"]
        
        def get_mongo_db():
            """Get MongoDB database"""
            return mongo_db
        
        logger.info("✅ MongoDB database configured")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        mongo_client = None
        mongo_db = None

else:
    logger.warning("⚠️  No database configured")
    engine = None
    SessionLocal = None
    Base = None
    mongo_client = None
    mongo_db = None

# =====================================================
# HELPER FUNCTIONS
# =====================================================
def init_db():
    """Initialize database tables/collections"""
    if DB_TYPE == "postgresql" and Base is not None:
        try:
            from database.models import User, Conversation, EmotionLog
            Base.metadata.create_all(bind=engine)
            logger.info("✅ PostgreSQL tables created")
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
    
    elif DB_TYPE == "mongodb" and mongo_db is not None:
        try:
            # Create indexes for better performance
            conversations_collection.create_index("user_id")
            conversations_collection.create_index("timestamp")
            emotions_collection.create_index("conversation_id")
            logger.info("✅ MongoDB indexes created")
        except Exception as e:
            logger.error(f"❌ Failed to create indexes: {e}")

def test_connection():
    """Test database connection"""
    try:
        if DB_TYPE == "postgresql" and engine is not None:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        elif DB_TYPE == "mongodb" and mongo_client is not None:
            mongo_client.server_info()
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {e}")
        return False
