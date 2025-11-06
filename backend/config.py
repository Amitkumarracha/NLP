"""
Configuration settings for Beyond Words API
Centralized configuration for models, database, and API settings
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "finetuned_models"
DATA_DIR = BASE_DIR / "data"
SPECTROGRAMS_DIR = DATA_DIR / "spectrograms"

# Create directories if they don't exist
MODELS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
SPECTROGRAMS_DIR.mkdir(exist_ok=True)

# =====================================================
# MODEL PATHS
# =====================================================
# Traditional ML models
XGB_PATH = MODELS_DIR / "xgboost_finetuned.json"
META_PATH = MODELS_DIR / "ensemble_meta.pkl"

# Deep Learning models
CNN_MODEL_PATH = MODELS_DIR / "cnn_emotion_model.h5"
CRNN_MODEL_PATH = MODELS_DIR / "crnn_emotion_model.h5"
WAV2VEC2_MODEL_PATH = MODELS_DIR / "wav2vec2_emotion"
HUBERT_MODEL_PATH = MODELS_DIR / "hubert_emotion"

# =====================================================
# AUDIO PROCESSING SETTINGS
# =====================================================
SAMPLE_RATE = 22050
N_MFCC = 40  # Increased for better feature representation
N_MELS = 128  # Mel spectrogram bins
N_FFT = 2048
HOP_LENGTH = 512
MAX_AUDIO_LENGTH = 5  # seconds

# Feature extraction configuration
FEATURE_CONFIG = {
    'mfcc': True,
    'chroma': True,
    'mel_spectrogram': True,
    'spectral_contrast': True,
    'zero_crossing_rate': True,
    'rmse': True,
    'spectral_centroid': True,
    'spectral_rolloff': True,
    'tonnetz': True
}

# =====================================================
# MODEL NAMES (Hugging Face)
# =====================================================
# Text emotion detection
TEXT_EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"

# Speech-to-text
WHISPER_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large

# Audio emotion models (transfer learning)
WAV2VEC2_BASE = "facebook/wav2vec2-base-960h"
WAV2VEC2_EMOTION = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
HUBERT_BASE = "facebook/hubert-base-ls960"
HUBERT_EMOTION = "superb/hubert-base-superb-er"

# Conversational models
CONVERSATIONAL_MODEL = "microsoft/DialoGPT-medium"
MENTAL_HEALTH_MODEL = "mental/mental-roberta-base"  # If available

# =====================================================
# ENSEMBLE WEIGHTS
# =====================================================
# Legacy weights for current implementation (3-model ensemble)
WEIGHT_TEXT = 0.5    # Text-based emotion model (most reliable)
WEIGHT_RULE = 0.35   # Rule-based audio features
WEIGHT_AUDIO = 0.15  # XGBoost audio model (least reliable)

# Future weights for full multi-model ensemble (6 models)
ENSEMBLE_WEIGHTS = {
    'text': 0.25,           # Text-based emotion model
    'wav2vec2': 0.25,       # Wav2Vec2 transfer learning
    'hubert': 0.20,         # HuBERT transfer learning
    'cnn': 0.15,            # CNN spectrogram model
    'xgboost': 0.10,        # XGBoost traditional features
    'rule_based': 0.05      # Rule-based heuristics
}

# =====================================================
# DATABASE CONFIGURATION
# =====================================================
# PostgreSQL / Supabase
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/beyond_words")

# MongoDB (alternative)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
MONGODB_DB_NAME = "beyond_words"

# Choose database type
DB_TYPE = os.getenv("DB_TYPE", "postgresql")  # Options: postgresql, mongodb

# =====================================================
# API SETTINGS
# =====================================================
API_TITLE = "Beyond Words — Multimodal Emotion-Aware Conversational Support System"
API_VERSION = "2.0.0"
API_DESCRIPTION = """
Advanced emotion recognition system using multiple models:
- Audio Mode: Wav2Vec2, HuBERT, CNN/CRNN, XGBoost
- Text Mode: DistilRoBERTa emotion classifier
- Multi-modal ensemble for robust predictions
"""
API_HOST = "0.0.0.0"
API_PORT = 8000

# CORS settings
CORS_ORIGINS = [
    "*",  # Allow all origins (can restrict to specific domains later)
    "https://*.vercel.app",  # Vercel deployments
    "http://localhost:3000",  # Local development
]

# =====================================================
# EMOTION CLASSES
# =====================================================
# Standard emotion classes (RAVDESS-based)
EMOTION_CLASSES = ['angry', 'calm', 'disgust', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

# Emotion to index mapping
EMOTION_TO_IDX = {emotion: idx for idx, emotion in enumerate(EMOTION_CLASSES)}
IDX_TO_EMOTION = {idx: emotion for idx, emotion in enumerate(EMOTION_CLASSES)}

# =====================================================
# MENTAL HEALTH SAFETY
# =====================================================
CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end it all', 'want to die',
    'hurt myself', 'self harm', 'no reason to live'
]

CRISIS_HOTLINES = {
    'US': '988 (Suicide & Crisis Lifeline)',
    'International': '741741 (Crisis Text Line - Text HOME)'
}

# =====================================================
# MODEL EVALUATION METRICS
# =====================================================
METRICS_TO_TRACK = [
    'accuracy',
    'precision',
    'recall',
    'f1_score',
    'confusion_matrix',
    'classification_report',
    'roc_auc'  # For binary/multi-class scenarios
]

# =====================================================
# TRAINING CONFIGURATION
# =====================================================
TRAIN_CONFIG = {
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.0001,
    'early_stopping_patience': 5,
    'validation_split': 0.2,
    'test_split': 0.1
}

# Data augmentation for audio
AUGMENTATION_CONFIG = {
    'time_stretch': True,
    'pitch_shift': True,
    'add_noise': True,
    'time_shift': True
}
