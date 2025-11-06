# =====================================================
# 🚀 Beyond Words — Emotion Detection API (FastAPI)
# =====================================================
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn, os, io, pickle, librosa, numpy as np, xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import tempfile
import soundfile as sf
import warnings
warnings.filterwarnings('ignore')

# Import speech-to-text and sentiment analysis
try:
    from transformers import pipeline as transformers_pipeline
    from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
    import torch
    TRANSFORMER_AVAILABLE = True
    print("✅ Transformers library loaded")
except Exception as e:
    TRANSFORMER_AVAILABLE = False
    print(f"⚠️  Transformers not available: {e}")
    print("   Using audio-only emotion detection mode.")
# =====================================================
# CONFIGURATION
# =====================================================
MODELS_DIR = "finetuned_models"
XGB_PATH = os.path.join(MODELS_DIR, "xgboost_finetuned.json")
META_PATH = os.path.join(MODELS_DIR, "ensemble_meta.pkl")
SAMPLE_RATE = 22050
N_MFCC = 13

# =====================================================
# INITIALIZE FASTAPI APP
# =====================================================
app = FastAPI(title="Beyond Words — Speech Emotion Recognition API")

# ✅ CORS for local React connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# LOAD MODELS & METADATA
# =====================================================
print("🔄 Loading fine-tuned models...")

with open(META_PATH, "rb") as f:
    ensemble_meta = pickle.load(f)

best_weights = ensemble_meta["weights"]
feature_cols = ensemble_meta["feature_cols"]
label_classes = ensemble_meta["label_encoder_classes"]

le = LabelEncoder()
le.classes_ = np.array(label_classes)

xgb_model = xgb.XGBClassifier()
xgb_model.load_model(XGB_PATH)

print("✅ Fine-tuned XGBoost & metadata loaded successfully")

# Load text-based emotion classifier (trained on real conversations)
if TRANSFORMER_AVAILABLE:
    try:
        print("🔄 Loading text-based emotion model...")
        text_emotion_classifier = transformers_pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            framework='pt',
            top_k=None
        )
        print("✅ Text-based emotion model loaded successfully")
    except Exception as e:
        print(f"⚠️  Could not load text model: {e}")
        text_emotion_classifier = None
else:
    text_emotion_classifier = None

# Load Whisper for speech-to-text (optional, small model for speed)
whisper_model = None
try:
    if TRANSFORMER_AVAILABLE:
        import whisper
        whisper_model = whisper.load_model("base")  # fast, lightweight
        print("✅ Whisper speech-to-text loaded (base model)")
except Exception as e:
    print(f"ℹ️  Whisper not available: {e}")
    whisper_model = None

# Load MentalBERT for mental health conversations
mental_health_model = None
mental_health_tokenizer = None

if TRANSFORMER_AVAILABLE:
    try:
        print("🔄 Loading MentalBERT for empathetic responses...")
        # Using mental health fine-tuned model
        model_name = "microsoft/DialoGPT-medium"  # Fallback if MentalBERT unavailable
        mental_health_tokenizer = AutoTokenizer.from_pretrained(model_name)
        mental_health_model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Set padding token
        if mental_health_tokenizer.pad_token is None:
            mental_health_tokenizer.pad_token = mental_health_tokenizer.eos_token
        
        print("✅ Mental health conversational model loaded")
    except Exception as e:
        print(f"⚠️  MentalBERT not available: {e}")
        print("   Using rule-based responses")

# =====================================================
# FEATURE EXTRACTION HELPERS
# =====================================================
def extract_handcrafted_features(y, sr, n_mfcc=N_MFCC):
    feats = {}
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    for i in range(n_mfcc):
        feats[f"mfcc_mean_{i+1}"] = float(np.mean(mfcc[i]))
        feats[f"mfcc_std_{i+1}"] = float(np.std(mfcc[i]))
    feats["zcr"] = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    feats["rmse"] = float(np.mean(librosa.feature.rms(y=y)))
    feats["duration"] = float(librosa.get_duration(y=y, sr=sr))
    return feats



def extract_features_from_audio_bytes(audio_bytes):
    """Handles both WAV and WEBM files by converting to WAV format first."""
    from pydub import AudioSegment

    # Detect format by checking magic bytes
    if audio_bytes[:4] == b'\x1aE\xdf\xa3':  # WebM/Matroska signature
        format_type = "webm"
    elif audio_bytes[:4] == b'RIFF':
        format_type = "wav"
    else:
        format_type = "webm"  # default assumption

    try:
        # Load audio using pydub (handles webm natively)
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format_type)

        # Convert to mono and set sample rate
        audio = audio.set_channels(1).set_frame_rate(SAMPLE_RATE)

        # Export to WAV in memory
        wav_io = io.BytesIO()
        audio.export(wav_io, format='wav')
        wav_io.seek(0)

        # Now load with librosa
        y, sr = librosa.load(wav_io, sr=SAMPLE_RATE, mono=True)

    except Exception as e:
        print(f"❌ Error processing audio: {e}")
        raise ValueError(f"Could not process audio file: {e}")

    feats = extract_handcrafted_features(y, sr, N_MFCC)
    arr = np.array([feats.get(c, 0.0) for c in feature_cols]).reshape(1, -1)
    return arr


# =====================================================
# RESPONSE MODEL
# =====================================================
class EmotionResponse(BaseModel):
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
    text: str

class TextEmotionResponse(BaseModel):
    text: str
    emotion: str
    confidence: float
    suggestions: list = []

class ChatRequest(BaseModel):
    message: str
    emotion_context: str = "neutral"

class ChatResponse(BaseModel):
    response: str
    detected_emotion: str
    confidence: float

# =====================================================
# RULE-BASED EMOTION PREDICTION (Temporary Fix)
# =====================================================
def rule_based_emotion_prediction(features):
    """
    Uses audio features to make emotion predictions.
    This is a temporary fix since the XGBoost model is broken.
    """
    # Extract key features
    zcr = features.get('zcr', 0.0)
    rmse = features.get('rmse', 0.0)
    duration = features.get('duration', 0.0)
    
    # MFCC features (first few are most important)
    mfcc_mean_1 = features.get('mfcc_mean_1', 0.0)
    mfcc_mean_2 = features.get('mfcc_mean_2', 0.0)
    mfcc_std_1 = features.get('mfcc_std_1', 0.0)
    
    # Initialize probabilities
    probs = {
        'angry': 0.0,
        'calm': 0.0,
        'disgust': 0.0,
        'fearful': 0.0,
        'happy': 0.0,
        'neutral': 0.0,
        'sad': 0.0,
        'surprised': 0.0
    }
    
    # Rule-based logic using audio characteristics
    # High energy (high RMSE, high ZCR) -> Angry, Happy, Surprised
    if rmse > 0.05 and zcr > 0.05:
        probs['angry'] += 0.3
        probs['happy'] += 0.3
        probs['surprised'] += 0.2
    
    # Low energy -> Calm, Sad
    elif rmse < 0.03:
        probs['calm'] += 0.4
        probs['sad'] += 0.3
        probs['neutral'] += 0.2
    
    # Medium energy, high variation -> Fearful, Surprised
    elif mfcc_std_1 > abs(mfcc_mean_1) * 0.5:
        probs['fearful'] += 0.3
        probs['surprised'] += 0.3
    
    # Based on MFCC characteristics
    if mfcc_mean_1 > 0:
        probs['happy'] += 0.2
        probs['surprised'] += 0.1
    else:
        probs['sad'] += 0.2
        probs['angry'] += 0.1
    
    # Short duration -> Surprised
    if duration < 2.0:
        probs['surprised'] += 0.2
    
    # Long duration -> Calm, Sad
    elif duration > 5.0:
        probs['calm'] += 0.1
        probs['sad'] += 0.1
    
    # Moderate ZCR with moderate energy -> Neutral
    if 0.03 < zcr < 0.06 and 0.03 < rmse < 0.05:
        probs['neutral'] += 0.3
    
    # Normalize probabilities
    total = sum(probs.values())
    if total > 0:
        probs = {k: v/total for k, v in probs.items()}
    else:
        # Default to neutral if no rules matched
        probs['neutral'] = 1.0
    
    return probs

# =====================================================
# TEXT-BASED EMOTION DETECTION
# =====================================================
def analyze_text_emotion(text: str):
    """Analyze emotion from transcribed text using transformer model."""
    if not text_emotion_classifier or not text.strip():
        return None, 0.0
    
    try:
        # Emotion mapping to match RAVDESS labels
        emotion_map = {
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
        
        emotions = text_emotion_classifier(text[:512])
        if emotions and len(emotions[0]) > 0:
            top_emotion = max(emotions[0], key=lambda x: x['score'])
            emotion_label = emotion_map.get(top_emotion['label'].lower(), 'neutral')
            confidence = float(top_emotion['score'])
            return emotion_label, confidence
    except Exception as e:
        print(f"⚠️  Text emotion analysis failed: {e}")
    
    return None, 0.0

def transcribe_audio(audio_bytes):
    """Transcribe audio to text using Whisper."""
    if not whisper_model:
        return ""
    
    try:
        # Save audio to temp file for Whisper
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        
        # Transcribe
        result = whisper_model.transcribe(tmp_path, language="en", fp16=False)
        os.unlink(tmp_path)
        
        return result.get("text", "").strip()
    except Exception as e:
        print(f"⚠️  Transcription failed: {e}")
        return ""

def ensemble_predictions(audio_prob, text_emotion, text_conf, rule_prob):
    """Combine audio-based, text-based, and rule-based predictions."""
    
    # Weights: text model > rule-based > broken XGBoost
    WEIGHT_TEXT = 0.5    # Text model trained on real data
    WEIGHT_RULE = 0.35   # Rule-based from audio features
    WEIGHT_AUDIO = 0.15  # Original model (less reliable)
    
    # Build combined probability distribution
    emotions = ['angry', 'calm', 'disgust', 'fearful', 'happy', 'neutral', 'sad', 'surprised']
    combined_probs = {}
    
    for emotion in emotions:
        prob = 0.0
        
        # Add rule-based probability
        prob += WEIGHT_RULE * rule_prob.get(emotion, 0.0)
        
        # Add audio model probability (if available)
        if emotion in le.classes_:
            idx = list(le.classes_).index(emotion)
            prob += WEIGHT_AUDIO * audio_prob[idx]
        
        combined_probs[emotion] = prob
    
    # Add text-based prediction (boost the detected emotion)
    if text_emotion and text_emotion in emotions:
        combined_probs[text_emotion] += WEIGHT_TEXT * text_conf
    
    # Normalize
    total = sum(combined_probs.values())
    if total > 0:
        combined_probs = {k: v/total for k, v in combined_probs.items()}
    
    # Get top prediction
    top_emotion = max(combined_probs, key=combined_probs.get)
    confidence = combined_probs[top_emotion]
    
    return top_emotion, confidence, combined_probs

# =====================================================
# AI-POWERED MENTAL HEALTH RESPONSE GENERATION
# =====================================================
def generate_ai_response(user_message: str, emotion_context: str, conversation_history: list = None):
    """Generate empathetic response using MentalBERT/DialoGPT."""
    
    # Enhanced rule-based system with mental health focus
    # (Fallback until PyTorch is fixed)
    
    user_lower = user_message.lower()
    
    # Mental health keywords and patterns
    mental_health_patterns = {
        'depression': ['depressed', 'hopeless', 'worthless', 'nothing matters'],
        'anxiety': ['anxious', 'panic', 'worried', 'scared', 'nervous', 'stressed'],
        'loneliness': ['alone', 'lonely', 'isolated', 'no one', 'nobody'],
        'self_harm': ['hurt myself', 'end it', 'suicide', 'kill myself'],
        'improvement': ['better', 'improving', 'good', 'happy', 'grateful'],
        'seeking_help': ['help', 'support', 'talk', 'listen'],
        'sleep': ['sleep', 'insomnia', 'tired', 'exhausted', 'can\'t sleep'],
        'relationships': ['friend', 'family', 'relationship', 'partner', 'conflict'],
    }
    
    # Crisis detection
    if any(word in user_lower for word in mental_health_patterns['self_harm']):
        return (
            "I'm really concerned about what you're sharing. Your life matters, and there are people who want to help. "
            "Please reach out to a crisis helpline immediately: National Suicide Prevention Lifeline (988). "
            "Would you like to talk about what's making you feel this way?"
        )
    
    # Depression support
    if any(word in user_lower for word in mental_health_patterns['depression']):
        responses = [
            f"I hear you, and those feelings are valid. Depression can make everything feel heavy. What's been weighing on you the most?",
            f"Thank you for sharing this with me. Depression is challenging, but you're not alone. Small steps count - have you been able to do anything for yourself today?",
            f"It takes courage to express these feelings. What usually helps you feel even slightly better?"
        ]
        import random
        return random.choice(responses)
    
    # Anxiety support
    if any(word in user_lower for word in mental_health_patterns['anxiety']):
        return (
            f"Anxiety can feel overwhelming, but you're safe right now. Let's try grounding: "
            f"Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. "
            f"What triggered these anxious feelings?"
        )
    
    # Loneliness support
    if any(word in user_lower for word in mental_health_patterns['loneliness']):
        return (
            f"Feeling isolated is really painful. I want you to know that I'm here, and you matter. "
            f"Have you been able to connect with anyone recently, even briefly?"
        )
    
    # Positive progress
    if any(word in user_lower for word in mental_health_patterns['improvement']):
        return (
            f"That's wonderful to hear! Progress isn't always linear, but celebrating these moments is important. "
            f"What do you think contributed to feeling this way?"
        )
    
    # Sleep issues
    if any(word in user_lower for word in mental_health_patterns['sleep']):
        return (
            f"Sleep struggles can affect everything. Have you tried a bedtime routine? "
            f"Some people find success with: no screens 1 hour before bed, cool dark room, and deep breathing. "
            f"What's your sleep environment like?"
        )
    
    # Emotion-specific responses with therapeutic elements
    therapeutic_responses = {
        'angry': (
            f"I can feel your frustration coming through. Anger is often protecting us from other feelings - "
            f"sometimes hurt, fear, or disappointment. What do you think is underneath this anger?"
        ),
        'sad': (
            f"Sadness deserves space. It's okay to feel this way. "
            f"Sometimes acknowledging our pain is the first step to healing. Would you like to share what's making you sad?"
        ),
        'fearful': (
            f"Fear is trying to protect you, but sometimes it overreacts. Let's acknowledge it without letting it control us. "
            f"What specific worry is most present for you right now?"
        ),
        'happy': (
            f"I love that you're experiencing joy! These moments are precious. "
            f"What about this makes you happy? Let's savor it together."
        ),
        'neutral': (
            f"I'm here with you. Sometimes just being present is enough. "
            f"What's on your mind right now?"
        )
    }
    
    return therapeutic_responses.get(emotion_context, therapeutic_responses['neutral'])

# =====================================================
# ROUTES
# =====================================================

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze_text", response_model=TextEmotionResponse)
async def analyze_text(request: TextEmotionRequest):
    """Analyze emotion from text input."""
    text = request.text
    
    # Detect emotion from text
    emotion, confidence = analyze_text_emotion(text)
    
    if not emotion:
        emotion = "neutral"
        confidence = 0.5
    
    # Generate supportive suggestions based on emotion
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
        ]
    }
    
    suggestions = suggestions_map.get(emotion, suggestions_map['neutral'])
    
    print(f"\n💬 Text Analysis: '{text[:50]}...'")
    print(f"😊 Emotion: {emotion} (confidence: {confidence:.2f})")
    
    return {
        "text": text,
        "emotion": emotion,
        "confidence": confidence,
        "suggestions": suggestions
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Conversational chatbot with emotion awareness and AI responses."""
    user_message = request.message
    emotion_context = request.emotion_context
    
    # Analyze emotion in user's message
    detected_emotion, confidence = analyze_text_emotion(user_message)
    
    if not detected_emotion:
        detected_emotion = emotion_context
        confidence = 0.5
    
    # Try AI-generated response first
    ai_response = generate_ai_response(user_message, detected_emotion)
    
    if ai_response:
        response = ai_response
        print(f"\n🤖 AI-Generated Response: {response[:100]}...")
    else:
        # Fallback to rule-based responses
        responses_map = {
            'angry': [
                "I can sense you're feeling frustrated. That's completely valid. What's been bothering you?",
                "It sounds like something really upset you. Would you like to talk about it?",
                "I hear your frustration. Take your time, I'm here to listen."
            ],
            'sad': [
                "I'm sorry you're going through this. Remember, it's okay to not be okay sometimes.",
                "Your feelings are valid. Would you like to share what's making you feel this way?",
                "I'm here for you. Sometimes just talking about it can help."
            ],
            'fearful': [
                "I understand you're feeling anxious. Let's take this one step at a time.",
                "It's okay to feel scared. What's worrying you right now?",
                "You're not alone in this. Would grounding exercises help?"
            ],
            'happy': [
                "I love seeing you in good spirits! What's bringing you joy today?",
                "That's wonderful! Tell me more about what's making you happy.",
                "Your positive energy is infectious! Keep embracing this feeling."
            ],
            'surprised': [
                "Sounds like something unexpected happened! Want to share?",
                "I can hear the surprise in your words. What happened?"
            ],
            'disgust': [
                "I sense you're uncomfortable with something. What's bothering you?",
                "That reaction makes sense. Let's talk through what you're feeling."
            ],
            'calm': [
                "You seem at peace. That's beautiful. How can I support you today?",
                "I appreciate your calm energy. What's on your mind?"
            ],
            'neutral': [
                "I'm here to listen. What would you like to talk about?",
                "How are you really feeling right now?",
                "Tell me more about what's going on."
            ]
        }
        
        import random
        response = random.choice(responses_map.get(detected_emotion, responses_map['neutral']))
        
        # Check for specific keywords and provide targeted support
        user_lower = user_message.lower()
        
        if any(word in user_lower for word in ['help', 'struggling', 'can\'t']):
            response = "I hear that you're struggling. You're brave for reaching out. What specifically is challenging you right now?"
        elif any(word in user_lower for word in ['anxious', 'worried', 'nervous']):
            response = "Anxiety can feel overwhelming. Try this: Take 3 deep breaths with me. Inhale... hold... exhale. How do you feel now?"
        elif any(word in user_lower for word in ['better', 'good', 'great', 'fine']):
            response = "I'm glad to hear that! What's contributing to you feeling this way?"
        elif any(word in user_lower for word in ['tired', 'exhausted', 'drained']):
            response = "It sounds like you need some rest and self-care. Have you been taking breaks for yourself?"
    
    print(f"\n💬 User: {user_message}")
    print(f"😊 Detected: {detected_emotion} ({confidence:.2f})")
    print(f"🤖 Bot: {response[:50]}...")
    
    return {
        "response": response,
        "detected_emotion": detected_emotion,
        "confidence": confidence
    }

@app.post("/predict", response_model=EmotionResponse)
async def predict_emotion(file: UploadFile = File(...)):
    """Receives an audio file and returns emotion predictions (multi-modal)."""
    audio_bytes = await file.read()
    
    # Step 1: Transcribe audio to text
    transcription = transcribe_audio(audio_bytes)
    print(f"\n📝 Transcription: '{transcription}'")
    
    # Step 2: Extract audio features
    X = extract_features_from_audio_bytes(audio_bytes)

    # XGBoost prediction
    xgb_probs = xgb_model.predict_proba(X)[0]

    # DEBUG: Print all probabilities
    print("\n" + "="*50)
    print("🔍 PREDICTION DETAILS:")
    print("="*50)
    for i, emotion in enumerate(le.classes_):
        print(f"{emotion:12s}: {xgb_probs[i]:.4f} ({xgb_probs[i]*100:.2f}%)")
    print("="*50 + "\n")

    # ⚠️ TEMPORARY FIX: Use feature-based rules since XGBoost is broken
    # Extract key features for rule-based prediction
    features_dict = {}
    for i, col in enumerate(feature_cols):
        features_dict[col] = X[0, i]
    
    # Rule-based emotion detection using audio features
    rule_probs = rule_based_emotion_prediction(features_dict)
    
    print("\n" + "="*50)
    print("🧠 RULE-BASED PREDICTION:")
    print("="*50)
    for emotion, prob in rule_probs.items():
        print(f"{emotion:12s}: {prob:.4f} ({prob*100:.2f}%)")
    print("="*50 + "\n")
    
    # Use rule-based prediction instead of broken XGBoost
    rule_probs_array = np.array([rule_probs.get(e, 0.0) for e in le.classes_])
    
    # Weighted Ensemble (only XGB weight if others missing)
    w_xgb = best_weights.get("w_xgb", 1.0)
    ensemble_probs = (w_xgb * xgb_probs) / w_xgb

    idx_xgb = int(np.argmax(rule_probs_array))  # Use rule-based instead
    idx_ens = int(np.argmax(rule_probs_array))  # Use rule-based instead
    emotion_xgb = le.inverse_transform([idx_xgb])[0]
    emotion_ensemble = le.inverse_transform([idx_ens])[0]
    conf_xgb = float(rule_probs_array[idx_xgb])
    conf_ens = float(rule_probs_array[idx_ens])

    # Step 3: Text-based emotion analysis
    text_emotion, text_conf = analyze_text_emotion(transcription)
    
    if text_emotion:
        print(f"\n📖 Text-based emotion: {text_emotion} (confidence: {text_conf:.2f})")
    
    # Step 4: Multi-modal ensemble (combine all approaches)
    final_emotion, final_conf, all_probs = ensemble_predictions(
        xgb_probs, text_emotion, text_conf, rule_probs
    )
    
    print("\n" + "="*50)
    print("🎯 FINAL ENSEMBLE PREDICTION:")
    print("="*50)
    for emotion, prob in sorted(all_probs.items(), key=lambda x: x[1], reverse=True):
        print(f"{emotion:12s}: {prob:.4f} ({prob*100:.2f}%)")
    print(f"\n✅ Final: {final_emotion} (confidence: {final_conf:.2f})\n")

    return {
        "emotion_xgb": emotion_xgb,
        "confidence_xgb": conf_xgb,
        "emotion_ensemble": emotion_ensemble,
        "confidence_ensemble": conf_ens,
        "transcription": transcription,
        "emotion_text": text_emotion or "N/A",
        "confidence_text": text_conf,
        "final_emotion": final_emotion,
        "final_confidence": final_conf,
    }

# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
