"""
Text-based emotion analysis and speech-to-text transcription service
"""
import tempfile
import os

from models.model_loader import get_text_emotion_classifier, get_whisper_model

# Emotion mapping to standardize labels
EMOTION_MAP = {
    'neutral': 'neutral',
    'calm': 'calm',
    'joy': 'happy',
    'happy': 'happy',
    'sadness': 'sad',
    'sad': 'sad',
    'anger': 'angry',
    'angry': 'angry',
    'fear': 'fearful',
    'fearful': 'fearful',
    'disgust': 'disgust',
    'surprise': 'surprised',
    'surprised': 'surprised'
}

def analyze_text_emotion(text: str):
    """
    Analyze emotion from text using transformer model
    
    Args:
        text: Input text to analyze
    
    Returns:
        Tuple of (emotion_label, confidence_score)
    """
    text_emotion_classifier = get_text_emotion_classifier()
    
    if not text_emotion_classifier or not text.strip():
        return None, 0.0
    
    try:
        # Run text classification (limit to 512 tokens)
        emotions = text_emotion_classifier(text[:512])
        
        if emotions and len(emotions[0]) > 0:
            # Get top emotion
            top_emotion = max(emotions[0], key=lambda x: x['score'])
            
            # Map to standardized emotion labels
            emotion_label = EMOTION_MAP.get(top_emotion['label'].lower(), 'neutral')
            confidence = float(top_emotion['score'])
            
            return emotion_label, confidence
    except Exception as e:
        print(f"⚠️  Text emotion analysis failed: {e}")
    
    return None, 0.0

def transcribe_audio(audio_bytes):
    """
    Transcribe audio to text using Whisper
    
    Args:
        audio_bytes: Raw audio file bytes
    
    Returns:
        Transcribed text string
    """
    whisper_model = get_whisper_model()
    
    if not whisper_model:
        return ""
    
    try:
        # Save audio to temporary file for Whisper
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        
        # Transcribe audio
        result = whisper_model.transcribe(tmp_path, language="en", fp16=False)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return result.get("text", "").strip()
    except Exception as e:
        print(f"⚠️  Transcription failed: {e}")
        return ""

def get_emotion_suggestions(emotion: str):
    """
    Get supportive suggestions based on detected emotion
    
    Args:
        emotion: Detected emotion label
    
    Returns:
        List of suggestion strings
    """
    suggestions_map = {
        'angry': [
            "Take a few deep breaths",
            "Try counting to 10",
            "Consider what triggered this feeling"
        ],
        'sad': [
            "It's okay to feel sad sometimes",
            "Reach out to someone you trust",
            "Practice self-compassion"
        ],
        'fearful': [
            "You're safe right now",
            "Ground yourself with 5-4-3-2-1 technique",
            "Focus on what you can control"
        ],
        'happy': [
            "Cherish this moment",
            "Share your joy with others",
            "Practice gratitude"
        ],
        'neutral': [
            "Take a moment to check in with yourself",
            "Notice your surroundings",
            "How can I support you?"
        ],
        'calm': [
            "Enjoy this peaceful moment",
            "Notice how relaxation feels",
            "Carry this calm with you"
        ],
        'surprised': [
            "Take a moment to process",
            "It's okay to feel caught off guard",
            "How does this surprise make you feel?"
        ],
        'disgust': [
            "Honor your boundaries",
            "It's valid to feel uncomfortable",
            "What can you do to feel more comfortable?"
        ]
    }
    
    return suggestions_map.get(emotion, suggestions_map['neutral'])
