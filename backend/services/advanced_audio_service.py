"""
Advanced Audio Feature Extraction Service
Comprehensive feature extraction including MFCC, Chroma, Spectral, and more
"""
import io
import numpy as np
import librosa
from pydub import AudioSegment
from typing import Dict, Tuple
import logging

from config import (
    SAMPLE_RATE, N_MFCC, N_MELS, N_FFT, HOP_LENGTH,
    MAX_AUDIO_LENGTH, FEATURE_CONFIG
)

logger = logging.getLogger(__name__)

# =====================================================
# COMPREHENSIVE FEATURE EXTRACTION
# =====================================================

def extract_comprehensive_features(y, sr=SAMPLE_RATE) -> Dict[str, np.ndarray]:
    """
    Extract comprehensive audio features for emotion recognition
    
    Features extracted:
    - MFCC (Mel-Frequency Cepstral Coefficients): 40 coefficients
    - Chroma (Pitch class profiles): 12 bins
    - Mel Spectrogram: 128 mel bands
    - Spectral Contrast: 7 bands
    - Tonnetz (Tonal centroid features): 6 features
    - Zero Crossing Rate
    - RMSE (Root Mean Square Energy)
    - Spectral Centroid
    - Spectral Rolloff
    - Spectral Bandwidth
    
    Args:
        y: Audio time series
        sr: Sample rate
    
    Returns:
        Dictionary of features with statistics (mean, std, max, min)
    """
    features = {}
    
    try:
        # 1. MFCC Features (captures spectral envelope)
        if FEATURE_CONFIG.get('mfcc', True):
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
            features['mfcc_mean'] = np.mean(mfcc, axis=1)
            features['mfcc_std'] = np.std(mfcc, axis=1)
            features['mfcc_max'] = np.max(mfcc, axis=1)
            features['mfcc_min'] = np.min(mfcc, axis=1)
            logger.debug(f"✓ MFCC: shape {mfcc.shape}")
        
        # 2. Chroma Features (pitch class profiles)
        if FEATURE_CONFIG.get('chroma', True):
            chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH)
            features['chroma_mean'] = np.mean(chroma, axis=1)
            features['chroma_std'] = np.std(chroma, axis=1)
            logger.debug(f"✓ Chroma: shape {chroma.shape}")
        
        # 3. Mel Spectrogram
        if FEATURE_CONFIG.get('mel_spectrogram', True):
            mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=N_MELS, n_fft=N_FFT, hop_length=HOP_LENGTH)
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
            features['mel_mean'] = np.mean(mel_spec_db, axis=1)
            features['mel_std'] = np.std(mel_spec_db, axis=1)
            logger.debug(f"✓ Mel Spectrogram: shape {mel_spec.shape}")
        
        # 4. Spectral Contrast (distinguishes peaks and valleys in spectrum)
        if FEATURE_CONFIG.get('spectral_contrast', True):
            contrast = librosa.feature.spectral_contrast(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH)
            features['contrast_mean'] = np.mean(contrast, axis=1)
            features['contrast_std'] = np.std(contrast, axis=1)
            logger.debug(f"✓ Spectral Contrast: shape {contrast.shape}")
        
        # 5. Tonnetz (Tonal Centroid Features)
        if FEATURE_CONFIG.get('tonnetz', True):
            tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
            features['tonnetz_mean'] = np.mean(tonnetz, axis=1)
            features['tonnetz_std'] = np.std(tonnetz, axis=1)
            logger.debug(f"✓ Tonnetz: shape {tonnetz.shape}")
        
        # 6. Zero Crossing Rate (voice/unvoiced)
        if FEATURE_CONFIG.get('zero_crossing_rate', True):
            zcr = librosa.feature.zero_crossing_rate(y)
            features['zcr_mean'] = np.mean(zcr)
            features['zcr_std'] = np.std(zcr)
            features['zcr_max'] = np.max(zcr)
            logger.debug(f"✓ ZCR: {features['zcr_mean']:.4f}")
        
        # 7. RMSE (Root Mean Square Energy - loudness)
        if FEATURE_CONFIG.get('rmse', True):
            rmse = librosa.feature.rms(y=y)
            features['rmse_mean'] = np.mean(rmse)
            features['rmse_std'] = np.std(rmse)
            features['rmse_max'] = np.max(rmse)
            logger.debug(f"✓ RMSE: {features['rmse_mean']:.4f}")
        
        # 8. Spectral Centroid (brightness of sound)
        if FEATURE_CONFIG.get('spectral_centroid', True):
            centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH)
            features['spectral_centroid_mean'] = np.mean(centroid)
            features['spectral_centroid_std'] = np.std(centroid)
            logger.debug(f"✓ Spectral Centroid: {features['spectral_centroid_mean']:.2f}")
        
        # 9. Spectral Rolloff (measure of shape of signal)
        if FEATURE_CONFIG.get('spectral_rolloff', True):
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH)
            features['spectral_rolloff_mean'] = np.mean(rolloff)
            features['spectral_rolloff_std'] = np.std(rolloff)
            logger.debug(f"✓ Spectral Rolloff: {features['spectral_rolloff_mean']:.2f}")
        
        # 10. Spectral Bandwidth
        bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH)
        features['spectral_bandwidth_mean'] = np.mean(bandwidth)
        features['spectral_bandwidth_std'] = np.std(bandwidth)
        
        # 11. Temporal Features
        features['duration'] = librosa.get_duration(y=y, sr=sr)
        features['tempo'] = librosa.beat.tempo(y=y, sr=sr)[0] if len(y) > sr else 0.0
        
        logger.info(f"✅ Extracted {sum(len(v) if isinstance(v, np.ndarray) else 1 for v in features.values())} features")
        
    except Exception as e:
        logger.error(f"❌ Feature extraction failed: {e}")
        raise
    
    return features

def flatten_features(features: Dict[str, np.ndarray]) -> np.ndarray:
    """
    Flatten feature dictionary into 1D array
    
    Args:
        features: Dictionary of feature arrays
    
    Returns:
        Flattened 1D numpy array
    """
    flat_features = []
    
    for key in sorted(features.keys()):
        value = features[key]
        if isinstance(value, np.ndarray):
            flat_features.extend(value.flatten())
        else:
            flat_features.append(float(value))
    
    return np.array(flat_features)

def generate_spectrogram(y, sr=SAMPLE_RATE, n_mels=N_MELS) -> np.ndarray:
    """
    Generate mel spectrogram for CNN/CRNN models
    
    Args:
        y: Audio time series
        sr: Sample rate
        n_mels: Number of mel bands
    
    Returns:
        Mel spectrogram as 2D array (n_mels x time_frames)
    """
    try:
        mel_spec = librosa.feature.melspectrogram(
            y=y, sr=sr, n_mels=n_mels, n_fft=N_FFT, hop_length=HOP_LENGTH
        )
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        logger.debug(f"✓ Spectrogram shape: {mel_spec_db.shape}")
        return mel_spec_db
    except Exception as e:
        logger.error(f"❌ Spectrogram generation failed: {e}")
        raise

def pad_or_trim_audio(y, sr=SAMPLE_RATE, max_length=MAX_AUDIO_LENGTH) -> np.ndarray:
    """
    Pad or trim audio to fixed length
    
    Args:
        y: Audio time series
        sr: Sample rate
        max_length: Maximum length in seconds
    
    Returns:
        Fixed-length audio array
    """
    target_length = int(max_length * sr)
    
    if len(y) < target_length:
        # Pad with zeros
        y_padded = np.pad(y, (0, target_length - len(y)), mode='constant')
    else:
        # Trim to target length
        y_padded = y[:target_length]
    
    return y_padded

def augment_audio(y, sr=SAMPLE_RATE, augmentation_type='all') -> np.ndarray:
    """
    Apply data augmentation to audio
    
    Args:
        y: Audio time series
        sr: Sample rate
        augmentation_type: Type of augmentation ('time_stretch', 'pitch_shift', 'noise', 'all')
    
    Returns:
        Augmented audio
    """
    augmented = y.copy()
    
    try:
        if augmentation_type in ['time_stretch', 'all']:
            # Time stretching (0.8x to 1.2x)
            rate = np.random.uniform(0.8, 1.2)
            augmented = librosa.effects.time_stretch(augmented, rate=rate)
        
        if augmentation_type in ['pitch_shift', 'all']:
            # Pitch shifting (-2 to +2 semitones)
            n_steps = np.random.randint(-2, 3)
            augmented = librosa.effects.pitch_shift(augmented, sr=sr, n_steps=n_steps)
        
        if augmentation_type in ['noise', 'all']:
            # Add random noise
            noise_factor = 0.005
            noise = np.random.randn(len(augmented))
            augmented = augmented + noise_factor * noise
        
        logger.debug(f"✓ Applied augmentation: {augmentation_type}")
    except Exception as e:
        logger.warning(f"⚠️  Augmentation failed: {e}")
        return y
    
    return augmented

def process_audio_for_models(audio_bytes) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Process audio for all model types
    
    Returns:
        Tuple of (feature_vector, spectrogram, raw_audio)
    """
    try:
        # Detect and convert format
        if audio_bytes[:4] == b'\x1aE\xdf\xa3':
            format_type = "webm"
        elif audio_bytes[:4] == b'RIFF':
            format_type = "wav"
        else:
            format_type = "webm"
        
        # Load audio
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format_type)
        audio = audio.set_channels(1).set_frame_rate(SAMPLE_RATE)
        
        # Export to WAV
        wav_io = io.BytesIO()
        audio.export(wav_io, format='wav')
        wav_io.seek(0)
        
        # Load with librosa
        y, sr = librosa.load(wav_io, sr=SAMPLE_RATE, mono=True)
        
        # 1. Extract comprehensive features for XGBoost
        features_dict = extract_comprehensive_features(y, sr)
        feature_vector = flatten_features(features_dict)
        
        # 2. Generate spectrogram for CNN/CRNN
        spectrogram = generate_spectrogram(y, sr)
        
        # 3. Pad/trim raw audio for Wav2Vec2/HuBERT
        raw_audio = pad_or_trim_audio(y, sr)
        
        logger.info(f"✅ Processed audio - Features: {len(feature_vector)}, Spec: {spectrogram.shape}, Audio: {len(raw_audio)}")
        
        return feature_vector, spectrogram, raw_audio
        
    except Exception as e:
        logger.error(f"❌ Audio processing failed: {e}")
        raise ValueError(f"Could not process audio file: {e}")
