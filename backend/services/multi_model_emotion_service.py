"""
Multi-Model Emotion Recognition Service
Integrates XGBoost, CNN/CRNN, Wav2Vec2, HuBERT, and Text-based models
Provides comprehensive emotion predictions with ensemble averaging
"""
import numpy as np
import time
import logging
from typing import Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

from config import ENSEMBLE_WEIGHTS, EMOTION_CLASSES, EMOTION_TO_IDX
from services.text_service import analyze_text_emotion
from services.emotion_service import rule_based_emotion_prediction

logger = logging.getLogger(__name__)

# =====================================================
# MODEL PREDICTION FUNCTIONS
# =====================================================

def predict_xgboost(feature_vector: np.ndarray) -> Tuple[str, float, Dict[str, float], float]:
    """
    Predict emotion using XGBoost on handcrafted features
    
    Args:
        feature_vector: Flattened feature array
    
    Returns:
        (emotion, confidence, probabilities, inference_time_ms)
    """
    start_time = time.time()
    
    try:
        from models.model_loader import get_xgb_model, get_label_encoder
        
        xgb_model = get_xgb_model()
        label_encoder = get_label_encoder()
        
        if xgb_model is None:
            logger.warning("⚠️  XGBoost model not loaded")
            return "neutral", 0.0, {}, 0.0
        
        # Reshape for prediction
        X = feature_vector.reshape(1, -1)
        
        # Get probabilities
        probs = xgb_model.predict_proba(X)[0]
        
        # Convert to dict
        prob_dict = {emotion: float(probs[i]) for i, emotion in enumerate(label_encoder.classes_)}
        
        # Get top prediction
        idx = int(np.argmax(probs))
        emotion = label_encoder.inverse_transform([idx])[0]
        confidence = float(probs[idx])
        
        inference_time = (time.time() - start_time) * 1000
        
        logger.debug(f"✓ XGBoost: {emotion} ({confidence:.3f}) [{inference_time:.1f}ms]")
        return emotion, confidence, prob_dict, inference_time
        
    except Exception as e:
        logger.error(f"❌ XGBoost prediction failed: {e}")
        return "neutral", 0.0, {}, 0.0

def predict_cnn(spectrogram: np.ndarray) -> Tuple[str, float, Dict[str, float], float]:
    """
    Predict emotion using CNN on mel spectrogram
    
    Args:
        spectrogram: Mel spectrogram (n_mels x time_frames)
    
    Returns:
        (emotion, confidence, probabilities, inference_time_ms)
    """
    start_time = time.time()
    
    try:
        from models.model_loader import get_cnn_model
        
        cnn_model = get_cnn_model()
        
        if cnn_model is None:
            logger.warning("⚠️  CNN model not loaded")
            return "neutral", 0.0, {}, 0.0
        
        # Prepare input (add batch and channel dimensions)
        # Expected shape: (batch, height, width, channels)
        spec_resized = np.expand_dims(spectrogram, axis=-1)  # Add channel
        spec_resized = np.expand_dims(spec_resized, axis=0)  # Add batch
        
        # Normalize
        spec_resized = (spec_resized - np.mean(spec_resized)) / (np.std(spec_resized) + 1e-8)
        
        # Predict
        probs = cnn_model.predict(spec_resized, verbose=0)[0]
        
        # Convert to dict
        prob_dict = {EMOTION_CLASSES[i]: float(probs[i]) for i in range(len(EMOTION_CLASSES))}
        
        # Get top prediction
        idx = int(np.argmax(probs))
        emotion = EMOTION_CLASSES[idx]
        confidence = float(probs[idx])
        
        inference_time = (time.time() - start_time) * 1000
        
        logger.debug(f"✓ CNN: {emotion} ({confidence:.3f}) [{inference_time:.1f}ms]")
        return emotion, confidence, prob_dict, inference_time
        
    except Exception as e:
        logger.error(f"❌ CNN prediction failed: {e}")
        return "neutral", 0.0, {}, 0.0

def predict_wav2vec2(raw_audio: np.ndarray) -> Tuple[str, float, Dict[str, float], float]:
    """
    Predict emotion using Wav2Vec2 transfer learning
    
    Args:
        raw_audio: Raw audio waveform
    
    Returns:
        (emotion, confidence, probabilities, inference_time_ms)
    """
    start_time = time.time()
    
    try:
        from models.model_loader import get_wav2vec2_model, get_wav2vec2_processor
        
        model = get_wav2vec2_model()
        processor = get_wav2vec2_processor()
        
        if model is None or processor is None:
            logger.warning("⚠️  Wav2Vec2 model not loaded")
            return "neutral", 0.0, {}, 0.0
        
        # Process audio
        inputs = processor(raw_audio, sampling_rate=16000, return_tensors="pt", padding=True)
        
        # Get predictions
        with torch.no_grad():
            logits = model(**inputs).logits
        
        # Convert to probabilities
        probs = torch.nn.functional.softmax(logits, dim=-1)[0].numpy()
        
        # Map to emotion classes
        prob_dict = {EMOTION_CLASSES[i]: float(probs[i]) for i in range(min(len(EMOTION_CLASSES), len(probs)))}
        
        # Get top prediction
        idx = int(np.argmax(probs))
        if idx < len(EMOTION_CLASSES):
            emotion = EMOTION_CLASSES[idx]
            confidence = float(probs[idx])
        else:
            emotion = "neutral"
            confidence = 0.5
        
        inference_time = (time.time() - start_time) * 1000
        
        logger.debug(f"✓ Wav2Vec2: {emotion} ({confidence:.3f}) [{inference_time:.1f}ms]")
        return emotion, confidence, prob_dict, inference_time
        
    except Exception as e:
        logger.error(f"❌ Wav2Vec2 prediction failed: {e}")
        return "neutral", 0.0, {}, 0.0

def predict_hubert(raw_audio: np.ndarray) -> Tuple[str, float, Dict[str, float], float]:
    """
    Predict emotion using HuBERT transfer learning
    
    Args:
        raw_audio: Raw audio waveform
    
    Returns:
        (emotion, confidence, probabilities, inference_time_ms)
    """
    start_time = time.time()
    
    try:
        from models.model_loader import get_hubert_model, get_hubert_processor
        
        model = get_hubert_model()
        processor = get_hubert_processor()
        
        if model is None or processor is None:
            logger.warning("⚠️  HuBERT model not loaded")
            return "neutral", 0.0, {}, 0.0
        
        # Process audio
        inputs = processor(raw_audio, sampling_rate=16000, return_tensors="pt", padding=True)
        
        # Get predictions
        with torch.no_grad():
            logits = model(**inputs).logits
        
        # Convert to probabilities
        probs = torch.nn.functional.softmax(logits, dim=-1)[0].numpy()
        
        # Map to emotion classes
        prob_dict = {EMOTION_CLASSES[i]: float(probs[i]) for i in range(min(len(EMOTION_CLASSES), len(probs)))}
        
        # Get top prediction
        idx = int(np.argmax(probs))
        if idx < len(EMOTION_CLASSES):
            emotion = EMOTION_CLASSES[idx]
            confidence = float(probs[idx])
        else:
            emotion = "neutral"
            confidence = 0.5
        
        inference_time = (time.time() - start_time) * 1000
        
        logger.debug(f"✓ HuBERT: {emotion} ({confidence:.3f}) [{inference_time:.1f}ms]")
        return emotion, confidence, prob_dict, inference_time
        
    except Exception as e:
        logger.error(f"❌ HuBERT prediction failed: {e}")
        return "neutral", 0.0, {}, 0.0

def predict_text_emotion(transcription: str) -> Tuple[str, float, Dict[str, float], float]:
    """
    Predict emotion from transcribed text
    
    Args:
        transcription: Transcribed text
    
    Returns:
        (emotion, confidence, probabilities, inference_time_ms)
    """
    start_time = time.time()
    
    if not transcription or len(transcription.strip()) == 0:
        return "neutral", 0.0, {}, 0.0
    
    try:
        emotion, confidence = analyze_text_emotion(transcription)
        
        if emotion is None:
            emotion = "neutral"
            confidence = 0.0
        
        # Create probability dict (simplified)
        prob_dict = {emotion: confidence}
        for e in EMOTION_CLASSES:
            if e not in prob_dict:
                prob_dict[e] = 0.0
        
        inference_time = (time.time() - start_time) * 1000
        
        logger.debug(f"✓ Text: {emotion} ({confidence:.3f}) [{inference_time:.1f}ms]")
        return emotion, confidence, prob_dict, inference_time
        
    except Exception as e:
        logger.error(f"❌ Text emotion prediction failed: {e}")
        return "neutral", 0.0, {}, 0.0

# =====================================================
# ENSEMBLE PREDICTION
# =====================================================

def ensemble_multimodal_predictions(
    predictions: Dict[str, Tuple[str, float, Dict[str, float], float]],
    transcription: Optional[str] = None
) -> Dict:
    """
    Combine predictions from multiple models using weighted ensemble
    
    Args:
        predictions: Dict of {model_name: (emotion, confidence, probs, time)}
        transcription: Optional transcription text
    
    Returns:
        Dict with final prediction and all model results
    """
    logger.info("\n" + "="*60)
    logger.info("🎯 ENSEMBLE PREDICTION")
    logger.info("="*60)
    
    # Initialize combined probabilities
    combined_probs = {emotion: 0.0 for emotion in EMOTION_CLASSES}
    total_weight = 0.0
    
    # Results storage
    all_model_results = {}
    
    # Combine predictions
    for model_name, (emotion, confidence, probs, inference_time) in predictions.items():
        weight = ENSEMBLE_WEIGHTS.get(model_name, 0.0)
        
        if weight > 0 and emotion != "neutral" or confidence > 0:
            # Add weighted probabilities
            for emo in EMOTION_CLASSES:
                if emo in probs:
                    combined_probs[emo] += weight * probs[emo]
            
            total_weight += weight
        
        # Store individual result
        all_model_results[model_name] = {
            "emotion": emotion,
            "confidence": round(confidence, 4),
            "inference_time_ms": round(inference_time, 2)
        }
        
        logger.info(f"  {model_name:15s}: {emotion:10s} ({confidence:.3f}) [{inference_time:.1f}ms] [weight: {weight}]")
    
    # Normalize probabilities
    if total_weight > 0:
        combined_probs = {k: v / total_weight for k, v in combined_probs.items()}
    else:
        # Fallback to equal distribution
        combined_probs = {k: 1.0 / len(EMOTION_CLASSES) for k in EMOTION_CLASSES}
    
    # Get final prediction
    final_emotion = max(combined_probs, key=combined_probs.get)  # type: ignore
    final_confidence = combined_probs[final_emotion]
    
    logger.info("="*60)
    logger.info(f"📊 Final Prediction: {final_emotion} ({final_confidence:.3f})")
    logger.info("="*60)
    
    # Top 3 emotions
    sorted_emotions = sorted(combined_probs.items(), key=lambda x: x[1], reverse=True)[:3]
    logger.info("\nTop 3 Emotions:")
    for emotion, prob in sorted_emotions:
        logger.info(f"  {emotion:10s}: {prob:.4f} ({prob*100:.2f}%)")
    
    return {
        "final_emotion": final_emotion,
        "final_confidence": round(final_confidence, 4),
        "all_probabilities": {k: round(v, 4) for k, v in combined_probs.items()},
        "model_predictions": all_model_results,
        "transcription": transcription or ""
    }

# =====================================================
# MAIN PREDICTION PIPELINE
# =====================================================

def predict_emotion_multimodal(
    feature_vector: np.ndarray,
    spectrogram: np.ndarray,
    raw_audio: np.ndarray,
    transcription: str = ""
) -> Dict:
    """
    Main prediction pipeline using all available models
    
    Args:
        feature_vector: Handcrafted features for XGBoost
        spectrogram: Mel spectrogram for CNN
        raw_audio: Raw waveform for Wav2Vec2/HuBERT
        transcription: Transcribed text
    
    Returns:
        Comprehensive prediction results
    """
    logger.info("\n🎤 Starting Multi-Model Emotion Prediction...")
    
    predictions = {}
    
    # 1. XGBoost (handcrafted features)
    try:
        predictions['xgboost'] = predict_xgboost(feature_vector)
    except Exception as e:
        logger.error(f"XGBoost failed: {e}")
    
    # 2. Rule-based (fallback)
    try:
        from models.model_loader import get_feature_cols
        feature_cols = get_feature_cols()
        if feature_cols:
            features_dict = {feature_cols[i]: feature_vector[i] for i in range(min(len(feature_cols), len(feature_vector)))}
            rule_probs = rule_based_emotion_prediction(features_dict)
            rule_emotion = max(rule_probs, key=rule_probs.get)  # type: ignore
            rule_conf = rule_probs[rule_emotion]
            predictions['rule_based'] = (rule_emotion, rule_conf, rule_probs, 0.0)
    except Exception as e:
        logger.error(f"Rule-based failed: {e}")
    
    # 3. CNN (spectrogram)
    try:
        predictions['cnn'] = predict_cnn(spectrogram)
    except Exception as e:
        logger.error(f"CNN failed: {e}")
    
    # 4. Wav2Vec2 (raw audio)
    try:
        predictions['wav2vec2'] = predict_wav2vec2(raw_audio)
    except Exception as e:
        logger.error(f"Wav2Vec2 failed: {e}")
    
    # 5. HuBERT (raw audio)
    try:
        predictions['hubert'] = predict_hubert(raw_audio)
    except Exception as e:
        logger.error(f"HuBERT failed: {e}")
    
    # 6. Text emotion (transcription)
    try:
        predictions['text'] = predict_text_emotion(transcription)
    except Exception as e:
        logger.error(f"Text emotion failed: {e}")
    
    # Ensemble all predictions
    result = ensemble_multimodal_predictions(predictions, transcription)
    
    logger.info(f"\n✅ Prediction complete: {result['final_emotion']} ({result['final_confidence']:.3f})\n")
    
    return result

# Import torch if available
try:
    import torch
except ImportError:
    logger.warning("⚠️  PyTorch not available - Wav2Vec2/HuBERT will not work")
    torch = None
