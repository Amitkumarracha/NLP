"""
Beyond Words — Emotion Detection API (FastAPI)
Main application file with route definitions
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import configuration
from config import API_TITLE, API_HOST, API_PORT, CORS_ORIGINS

# Import models and schemas
from models.schemas import (
    EmotionResponse, TextEmotionRequest, TextEmotionResponse,
    ChatRequest, ChatResponse
)
from models.model_loader import initialize_all_models

# Import services
from services.audio_service import extract_features_from_audio_bytes
from services.text_service import transcribe_audio, analyze_text_emotion, get_emotion_suggestions
from services.emotion_service import predict_multimodal_emotion
from services.chat_service import generate_chat_response

# =====================================================
# INITIALIZE FASTAPI APP
# =====================================================
app = FastAPI(title=API_TITLE)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# STARTUP EVENT - LOAD ALL MODELS
# =====================================================
@app.on_event("startup")
async def startup_event():
    """Initialize all ML models on application startup"""
    logger.info("\n🚀 Starting Beyond Words API...")
    try:
        initialize_all_models()
        logger.info("✅ All models loaded successfully\n")
    except Exception as e:
        logger.error(f"❌ Failed to load models: {e}")
        raise

# =====================================================
# API ROUTES
# =====================================================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Beyond Words Emotion Detection API",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0"
    }

@app.post("/analyze_text", response_model=TextEmotionResponse)
async def analyze_text_endpoint(request: TextEmotionRequest):
    """
    Analyze emotion from text input
    
    Args:
        request: TextEmotionRequest containing text
    
    Returns:
        TextEmotionResponse with emotion, confidence, and suggestions
    """
    text = request.text
    
    try:
        # Detect emotion from text
        emotion, confidence = analyze_text_emotion(text)
        
        if not emotion:
            emotion = "neutral"
            confidence = 0.5
        
        # Get supportive suggestions
        suggestions = get_emotion_suggestions(emotion)
        
        logger.info(f"💬 Text Analysis: '{text[:50]}...'")
        logger.info(f"😊 Emotion: {emotion} (confidence: {confidence:.2f})")
    
        return {
            "text": text,
            "emotion": emotion,
            "confidence": confidence,
            "suggestions": suggestions,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Text analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Conversational chatbot with emotion awareness and empathetic responses
    
    Args:
        request: ChatRequest with user message and emotion context
    
    Returns:
        ChatResponse with bot response, detected emotion, and confidence
    """
    try:
        user_message = request.message
        emotion_context = request.emotion_context
        
        # Generate empathetic response
        response, detected_emotion, confidence = generate_chat_response(
            user_message, emotion_context
        )
        
        logger.info(f"💬 User: {user_message}")
        logger.info(f"😊 Detected: {detected_emotion} ({confidence:.2f})")
        logger.info(f"🤖 Bot: {response[:100]}...")
    
        return {
            "response": response,
            "detected_emotion": detected_emotion,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Chat generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Chat generation failed: {str(e)}")

@app.post("/predict", response_model=EmotionResponse)
async def predict_emotion_endpoint(file: UploadFile = File(...)):
    """
    Multi-modal emotion prediction from audio file
    Combines audio features, transcription, and text analysis
    
    Args:
        file: Uploaded audio file (WAV or WebM)
    
    Returns:
        EmotionResponse with all prediction results
    """
    try:
        audio_bytes = await file.read()
        
        logger.info(f"🎤 Processing audio file: {file.filename}")
        
        # Step 1: Transcribe audio to text
        transcription = transcribe_audio(audio_bytes)
        logger.info(f"📝 Transcription: '{transcription}'")
    
        # Step 2: Extract audio features
        audio_features = extract_features_from_audio_bytes(audio_bytes)
        logger.info(f"✅ Extracted {audio_features.shape[1]} audio features")
    
        # Step 3: Multi-modal prediction
        results = predict_multimodal_emotion(audio_features, transcription)
        
        # Log detailed results
        logger.info("\n" + "="*50)
        logger.info("🔍 PREDICTION DETAILS:")
        logger.info("="*50)
        logger.info(f"🎵 Audio (Rule-based): {results['emotion_xgb']} ({results['confidence_xgb']:.2f})")
        if results['emotion_text'] != "N/A":
            logger.info(f"📖 Text: {results['emotion_text']} ({results['confidence_text']:.2f})")
        logger.info(f"🎯 Final: {results['final_emotion']} ({results['final_confidence']:.2f})")
        logger.info("="*50)
        
        logger.info("\n📊 All Probabilities:")
        for emotion, prob in sorted(results['all_probabilities'].items(), 
                                    key=lambda x: x[1], reverse=True):
            logger.info(f"  {emotion:12s}: {prob:.4f} ({prob*100:.2f}%)")
    
        return {
            "emotion_xgb": results['emotion_xgb'],
            "confidence_xgb": results['confidence_xgb'],
            "emotion_ensemble": results['emotion_ensemble'],
            "confidence_ensemble": results['confidence_ensemble'],
            "transcription": transcription,
            "emotion_text": results['emotion_text'],
            "confidence_text": results['confidence_text'],
            "final_emotion": results['final_emotion'],
            "final_confidence": results['final_confidence'],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Emotion prediction failed: {str(e)}")

# =====================================================
# MAIN ENTRY POINT
# =====================================================
if __name__ == "__main__":
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)
