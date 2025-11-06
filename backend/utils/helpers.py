"""
Utility helper functions
"""
from typing import Dict, List

def format_probability_distribution(probs: Dict[str, float], top_n: int = None) -> List[tuple]:
    """
    Format probability distribution as sorted list
    
    Args:
        probs: Dictionary of emotion probabilities
        top_n: Number of top results to return (None for all)
    
    Returns:
        List of (emotion, probability) tuples sorted by probability
    """
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    
    if top_n:
        return sorted_probs[:top_n]
    
    return sorted_probs

def print_emotion_distribution(probs: Dict[str, float], title: str = "Emotion Distribution"):
    """
    Pretty print emotion probability distribution
    
    Args:
        probs: Dictionary of emotion probabilities
        title: Title for the printout
    """
    print(f"\n{'='*50}")
    print(f"{title}")
    print('='*50)
    
    for emotion, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True):
        bar_length = int(prob * 40)  # Bar up to 40 chars
        bar = '█' * bar_length
        print(f"{emotion:12s}: {bar} {prob:.4f} ({prob*100:.2f}%)")
    
    print('='*50 + '\n')

def validate_audio_format(audio_bytes: bytes) -> str:
    """
    Detect audio format from magic bytes
    
    Args:
        audio_bytes: Raw audio file bytes
    
    Returns:
        Format string ('wav', 'webm', 'unknown')
    """
    if audio_bytes[:4] == b'\x1aE\xdf\xa3':
        return "webm"
    elif audio_bytes[:4] == b'RIFF':
        return "wav"
    elif audio_bytes[:3] == b'ID3' or audio_bytes[:2] == b'\xff\xfb':
        return "mp3"
    else:
        return "unknown"

def get_confidence_level(confidence: float) -> str:
    """
    Convert confidence score to human-readable level
    
    Args:
        confidence: Confidence score (0.0 to 1.0)
    
    Returns:
        Confidence level string
    """
    if confidence >= 0.8:
        return "Very High"
    elif confidence >= 0.6:
        return "High"
    elif confidence >= 0.4:
        return "Moderate"
    elif confidence >= 0.2:
        return "Low"
    else:
        return "Very Low"
