"""
Machine Learning model loader and initializer
Loads XGBoost, text emotion classifier, Whisper, and conversational models
"""
import pickle
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

from config import (
    XGB_PATH, META_PATH, TEXT_EMOTION_MODEL, 
    CONVERSATIONAL_MODEL, WHISPER_MODEL_SIZE
)

# Global model instances
xgb_model = None
label_encoder = None
feature_cols = None
label_classes = None
best_weights = None

text_emotion_classifier = None
whisper_model = None
mental_health_model = None
mental_health_tokenizer = None

TRANSFORMER_AVAILABLE = False

def check_transformer_availability():
    """Check if transformers library is available"""
    global TRANSFORMER_AVAILABLE
    try:
        from transformers import pipeline as transformers_pipeline
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        TRANSFORMER_AVAILABLE = True
        print("✅ Transformers library loaded")
        return True
    except Exception as e:
        TRANSFORMER_AVAILABLE = False
        print(f"⚠️  Transformers not available: {e}")
        print("   Using audio-only emotion detection mode.")
        return False

def load_xgboost_model():
    """Load XGBoost emotion classification model and metadata"""
    global xgb_model, label_encoder, feature_cols, label_classes, best_weights
    
    print("🔄 Loading fine-tuned XGBoost model...")
    
    # Load metadata
    with open(META_PATH, "rb") as f:
        ensemble_meta = pickle.load(f)
    
    best_weights = ensemble_meta["weights"]
    feature_cols = ensemble_meta["feature_cols"]
    label_classes = ensemble_meta["label_encoder_classes"]
    
    # Initialize label encoder
    label_encoder = LabelEncoder()
    label_encoder.classes_ = np.array(label_classes)
    
    # Load XGBoost model
    xgb_model = xgb.XGBClassifier()
    xgb_model.load_model(XGB_PATH)
    
    print("✅ Fine-tuned XGBoost & metadata loaded successfully")
    return xgb_model, label_encoder, feature_cols, label_classes, best_weights

def load_text_emotion_model():
    """Load text-based emotion classification model"""
    global text_emotion_classifier
    
    if not TRANSFORMER_AVAILABLE:
        text_emotion_classifier = None
        return None
    
    try:
        from transformers import pipeline as transformers_pipeline
        
        print("🔄 Loading text-based emotion model...")
        text_emotion_classifier = transformers_pipeline(
            "text-classification",
            model=TEXT_EMOTION_MODEL,
            framework='pt',
            top_k=None
        )
        print("✅ Text-based emotion model loaded successfully")
        return text_emotion_classifier
    except Exception as e:
        print(f"⚠️  Could not load text model: {e}")
        text_emotion_classifier = None
        return None

def load_whisper_model():
    """Load Whisper speech-to-text model"""
    global whisper_model
    
    if not TRANSFORMER_AVAILABLE:
        whisper_model = None
        return None
    
    try:
        import whisper
        whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
        print(f"✅ Whisper speech-to-text loaded ({WHISPER_MODEL_SIZE} model)")
        return whisper_model
    except Exception as e:
        print(f"ℹ️  Whisper not available: {e}")
        whisper_model = None
        return None

def load_mental_health_model():
    """Load conversational model for mental health support"""
    global mental_health_model, mental_health_tokenizer
    
    if not TRANSFORMER_AVAILABLE:
        mental_health_model = None
        mental_health_tokenizer = None
        return None, None
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        print("🔄 Loading conversational model for empathetic responses...")
        mental_health_tokenizer = AutoTokenizer.from_pretrained(CONVERSATIONAL_MODEL)
        mental_health_model = AutoModelForCausalLM.from_pretrained(CONVERSATIONAL_MODEL)
        
        # Set padding token
        if mental_health_tokenizer.pad_token is None:
            mental_health_tokenizer.pad_token = mental_health_tokenizer.eos_token
        
        print("✅ Mental health conversational model loaded")
        return mental_health_model, mental_health_tokenizer
    except Exception as e:
        print(f"⚠️  Conversational model not available: {e}")
        print("   Using rule-based responses")
        mental_health_model = None
        mental_health_tokenizer = None
        return None, None

def initialize_all_models():
    """Initialize all models at startup"""
    check_transformer_availability()
    load_xgboost_model()
    load_text_emotion_model()
    load_whisper_model()
    load_mental_health_model()
    
    return {
        'xgb_model': xgb_model,
        'label_encoder': label_encoder,
        'feature_cols': feature_cols,
        'text_emotion_classifier': text_emotion_classifier,
        'whisper_model': whisper_model,
        'mental_health_model': mental_health_model,
        'mental_health_tokenizer': mental_health_tokenizer
    }

# Getter functions for models
def get_xgb_model():
    return xgb_model

def get_label_encoder():
    return label_encoder

def get_feature_cols():
    return feature_cols

def get_label_classes():
    return label_classes

def get_best_weights():
    return best_weights

def get_text_emotion_classifier():
    return text_emotion_classifier

def get_whisper_model():
    return whisper_model

def get_mental_health_model():
    return mental_health_model, mental_health_tokenizer
