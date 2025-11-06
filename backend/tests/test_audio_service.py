"""
Unit tests for audio service
Tests audio feature extraction and processing
"""
import pytest
import numpy as np
import io
from services.audio_service import (
    extract_handcrafted_features,
    extract_features_from_audio_bytes,
    get_audio_characteristics
)

def test_extract_handcrafted_features():
    """Test basic feature extraction from waveform"""
    # Create a simple sine wave
    sr = 22050
    duration = 1.0
    frequency = 440  # A4 note
    t = np.linspace(0, duration, int(sr * duration))
    y = np.sin(2 * np.pi * frequency * t)
    
    features = extract_handcrafted_features(y, sr, n_mfcc=13)
    
    # Check all expected features are present
    assert 'zcr' in features
    assert 'rmse' in features
    assert 'duration' in features
    assert 'mfcc_mean_1' in features
    assert 'mfcc_std_1' in features
    
    # Check feature values are reasonable
    assert features['duration'] > 0
    assert features['rmse'] > 0
    assert 0 <= features['zcr'] <= 1

def test_extract_handcrafted_features_empty():
    """Test feature extraction with empty audio"""
    with pytest.raises(ValueError):
        extract_handcrafted_features(np.array([]), 22050)

def test_get_audio_characteristics():
    """Test audio characteristic categorization"""
    features = {
        'zcr': 0.05,
        'rmse': 0.06,
        'duration': 3.5
    }
    
    characteristics = get_audio_characteristics(features)
    
    assert 'energy_level' in characteristics
    assert 'variability' in characteristics
    assert 'duration_seconds' in characteristics
    assert 'duration_category' in characteristics
    
    # Check categorization logic
    assert characteristics['energy_level'] == 'high'  # rmse > 0.05
    assert characteristics['duration_category'] == 'medium'  # 2.0 < duration < 5.0

def test_audio_characteristics_low_energy():
    """Test low energy categorization"""
    features = {
        'zcr': 0.02,
        'rmse': 0.02,
        'duration': 1.5
    }
    
    characteristics = get_audio_characteristics(features)
    
    assert characteristics['energy_level'] == 'low'
    assert characteristics['duration_category'] == 'short'

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
