"""
Audio processing service - handles audio feature extraction
"""
import io
import numpy as np
import librosa
from pydub import AudioSegment
import logging

from config import SAMPLE_RATE, N_MFCC
from models.model_loader import get_feature_cols

logger = logging.getLogger(__name__)

def extract_handcrafted_features(y, sr, n_mfcc=N_MFCC):
    """
    Extract audio features from waveform
    
    Args:
        y: Audio waveform
        sr: Sample rate
        n_mfcc: Number of MFCC coefficients
    
    Returns:
        Dictionary of extracted features
        
    Raises:
        ValueError: If audio is empty or invalid
    """
    if y is None or len(y) == 0:
        raise ValueError("Audio waveform is empty")
    
    feats = {}
    
    try:
        # MFCC features (mean and std for each coefficient)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        for i in range(n_mfcc):
            feats[f"mfcc_mean_{i+1}"] = float(np.mean(mfcc[i]))
            feats[f"mfcc_std_{i+1}"] = float(np.std(mfcc[i]))
        
        # Zero Crossing Rate
        feats["zcr"] = float(np.mean(librosa.feature.zero_crossing_rate(y)))
        
        # Root Mean Square Energy
        feats["rmse"] = float(np.mean(librosa.feature.rms(y=y)))
        
        # Duration
        feats["duration"] = float(librosa.get_duration(y=y, sr=sr))
        
        logger.debug(f"Extracted {len(feats)} features from audio")
        return feats
    
    except Exception as e:
        logger.error(f"Feature extraction failed: {e}")
        raise ValueError(f"Could not extract audio features: {str(e)}")

def extract_features_from_audio_bytes(audio_bytes):
    """
    Extract features from audio file bytes (supports WAV and WebM)
    
    Args:
        audio_bytes: Raw audio file bytes
    
    Returns:
        NumPy array of features ready for model prediction
        
    Raises:
        ValueError: If audio format is unsupported or processing fails
    """
    if not audio_bytes or len(audio_bytes) == 0:
        raise ValueError("Audio bytes are empty")
    
    # Detect audio format by magic bytes
    if audio_bytes[:4] == b'\x1aE\xdf\xa3':  # WebM/Matroska signature
        format_type = "webm"
    elif audio_bytes[:4] == b'RIFF':
        format_type = "wav"
    else:
        logger.warning("Unknown audio format, defaulting to webm")
        format_type = "webm"  # default assumption

    try:
        # Load audio using pydub (handles multiple formats)
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format_type)
        
        if len(audio) == 0:
            raise ValueError("Audio file is empty or has zero duration")

        # Convert to mono and set sample rate
        audio = audio.set_channels(1).set_frame_rate(SAMPLE_RATE)

        # Export to WAV in memory
        wav_io = io.BytesIO()
        audio.export(wav_io, format='wav')
        wav_io.seek(0)

        # Load with librosa for feature extraction
        y, sr = librosa.load(wav_io, sr=SAMPLE_RATE, mono=True)
        
        if y is None or len(y) == 0:
            raise ValueError("Failed to load audio waveform")

    except Exception as e:
        logger.error(f"Audio processing error: {e}")
        raise ValueError(f"Could not process audio file: {str(e)}")

    # Extract features
    try:
        feats = extract_handcrafted_features(y, sr, N_MFCC)
    except Exception as e:
        logger.error(f"Feature extraction error: {e}")
        raise ValueError(f"Could not extract features: {str(e)}")
    
    # Convert to array in correct order
    try:
        feature_cols = get_feature_cols()
        if not feature_cols:
            raise ValueError("Feature columns not available")
        
        arr = np.array([feats.get(c, 0.0) for c in feature_cols]).reshape(1, -1)
        logger.info(f"Successfully extracted {arr.shape[1]} features")
        return arr
    
    except Exception as e:
        logger.error(f"Feature array conversion error: {e}")
        raise ValueError(f"Could not convert features to array: {str(e)}")

def get_audio_characteristics(features_dict):
    """
    Get human-readable audio characteristics
    
    Args:
        features_dict: Dictionary of extracted features
    
    Returns:
        Dictionary of audio characteristics
    """
    zcr = features_dict.get('zcr', 0.0)
    rmse = features_dict.get('rmse', 0.0)
    duration = features_dict.get('duration', 0.0)
    
    characteristics = {
        'energy_level': 'high' if rmse > 0.05 else 'low' if rmse < 0.03 else 'medium',
        'variability': 'high' if zcr > 0.06 else 'low' if zcr < 0.03 else 'medium',
        'duration_seconds': round(duration, 2),
        'duration_category': 'short' if duration < 2.0 else 'long' if duration > 5.0 else 'medium'
    }
    
    return characteristics
