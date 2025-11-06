"""
Emotion prediction service - handles multi-modal emotion detection
Combines audio features, text analysis, and rule-based predictions
"""
import numpy as np

from config import WEIGHT_TEXT, WEIGHT_RULE, WEIGHT_AUDIO, EMOTION_CLASSES
from models.model_loader import get_xgb_model, get_label_encoder, get_best_weights

def rule_based_emotion_prediction(features):
    """
    Rule-based emotion prediction using audio features
    (Temporary fix for unreliable XGBoost model)
    
    Args:
        features: Dictionary of audio features
    
    Returns:
        Dictionary of emotion probabilities
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
    probs = {emotion: 0.0 for emotion in EMOTION_CLASSES}
    
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

def predict_audio_emotion(audio_features):
    """
    Predict emotion from audio features using XGBoost model
    
    Args:
        audio_features: NumPy array of audio features
    
    Returns:
        Tuple of (emotion_label, confidence, probabilities_array)
    """
    xgb_model = get_xgb_model()
    label_encoder = get_label_encoder()
    
    # Get predictions from XGBoost
    xgb_probs = xgb_model.predict_proba(audio_features)[0]
    
    # Get top prediction
    idx = int(np.argmax(xgb_probs))
    emotion = label_encoder.inverse_transform([idx])[0]
    confidence = float(xgb_probs[idx])
    
    return emotion, confidence, xgb_probs

def ensemble_predictions(audio_prob, text_emotion, text_conf, rule_prob):
    """
    Combine audio-based, text-based, and rule-based predictions
    
    Args:
        audio_prob: Probability array from XGBoost model
        text_emotion: Emotion detected from text
        text_conf: Confidence of text emotion
        rule_prob: Probability dictionary from rule-based system
    
    Returns:
        Tuple of (final_emotion, final_confidence, all_probabilities)
    """
    label_encoder = get_label_encoder()
    
    # Build combined probability distribution
    combined_probs = {}
    
    for emotion in EMOTION_CLASSES:
        prob = 0.0
        
        # Add rule-based probability
        prob += WEIGHT_RULE * rule_prob.get(emotion, 0.0)
        
        # Add audio model probability (if available)
        if emotion in label_encoder.classes_:
            idx = list(label_encoder.classes_).index(emotion)
            prob += WEIGHT_AUDIO * audio_prob[idx]
        
        combined_probs[emotion] = prob
    
    # Add text-based prediction (boost the detected emotion)
    if text_emotion and text_emotion in EMOTION_CLASSES:
        combined_probs[text_emotion] += WEIGHT_TEXT * text_conf
    
    # Normalize probabilities
    total = sum(combined_probs.values())
    if total > 0:
        combined_probs = {k: v/total for k, v in combined_probs.items()}
    
    # Get top prediction
    top_emotion = max(combined_probs, key=combined_probs.get)
    confidence = combined_probs[top_emotion]
    
    return top_emotion, confidence, combined_probs

def predict_multimodal_emotion(audio_features, transcription):
    """
    Main function to predict emotion using all available modalities
    
    Args:
        audio_features: NumPy array of audio features
        transcription: Transcribed text from audio
    
    Returns:
        Dictionary containing all prediction results
    """
    from services.text_service import analyze_text_emotion
    from models.model_loader import get_feature_cols
    
    # Step 1: XGBoost audio prediction
    emotion_xgb, conf_xgb, xgb_probs = predict_audio_emotion(audio_features)
    
    # Step 2: Rule-based audio prediction
    feature_cols = get_feature_cols()
    features_dict = {}
    for i, col in enumerate(feature_cols):
        features_dict[col] = audio_features[0, i]
    
    rule_probs = rule_based_emotion_prediction(features_dict)
    rule_probs_array = np.array([rule_probs.get(e, 0.0) for e in get_label_encoder().classes_])
    
    # Use rule-based instead of broken XGBoost for individual predictions
    idx_rule = int(np.argmax(rule_probs_array))
    emotion_rule = get_label_encoder().inverse_transform([idx_rule])[0]
    conf_rule = float(rule_probs_array[idx_rule])
    
    # Step 3: Text-based emotion analysis
    text_emotion, text_conf = analyze_text_emotion(transcription)
    
    # Step 4: Ensemble prediction
    final_emotion, final_conf, all_probs = ensemble_predictions(
        xgb_probs, text_emotion, text_conf, rule_probs
    )
    
    return {
        'emotion_xgb': emotion_rule,  # Using rule-based instead
        'confidence_xgb': conf_rule,
        'emotion_ensemble': emotion_rule,
        'confidence_ensemble': conf_rule,
        'emotion_text': text_emotion or "N/A",
        'confidence_text': text_conf,
        'final_emotion': final_emotion,
        'final_confidence': final_conf,
        'all_probabilities': all_probs,
        'xgb_probs': xgb_probs,
        'rule_probs': rule_probs
    }
