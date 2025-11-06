#!/usr/bin/env python3
"""
Test the XGBoost model to check if it's predicting multiple emotions or stuck on one
"""
import pickle
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

# Load model and metadata
print("🔄 Loading model...")
with open("finetuned_models/ensemble_meta.pkl", "rb") as f:
    ensemble_meta = pickle.load(f)

feature_cols = ensemble_meta["feature_cols"]
label_classes = ensemble_meta["label_encoder_classes"]

le = LabelEncoder()
le.classes_ = np.array(label_classes)

xgb_model = xgb.XGBClassifier()
xgb_model.load_model("finetuned_models/xgboost_finetuned.json")

print("✅ Model loaded successfully")
print(f"📊 Number of features: {len(feature_cols)}")
print(f"🎭 Emotion classes: {label_classes}")
print()

# Test with random features to see if model can predict different emotions
print("=" * 60)
print("TESTING WITH RANDOM FEATURES")
print("=" * 60)

for test_num in range(5):
    print(f"\n--- Test {test_num + 1} ---")
    
    # Generate random features
    X_test = np.random.randn(1, len(feature_cols))
    
    # Get predictions
    probs = xgb_model.predict_proba(X_test)[0]
    
    # Show all probabilities
    for i, emotion in enumerate(label_classes):
        print(f"{emotion:12s}: {probs[i]:.4f} ({probs[i]*100:.2f}%)")
    
    # Show top prediction
    idx = np.argmax(probs)
    predicted_emotion = label_classes[idx]
    confidence = probs[idx]
    print(f"\n🎯 Predicted: {predicted_emotion} (confidence: {confidence:.4f})")

print("\n" + "=" * 60)
print("ANALYSIS")
print("=" * 60)

# Check if model is stuck on one class
predictions = []
for _ in range(100):
    X_test = np.random.randn(1, len(feature_cols))
    probs = xgb_model.predict_proba(X_test)[0]
    idx = np.argmax(probs)
    predictions.append(label_classes[idx])

from collections import Counter
prediction_counts = Counter(predictions)
print("\nPrediction distribution over 100 random samples:")
for emotion, count in prediction_counts.most_common():
    print(f"{emotion:12s}: {count}/100 ({count}%)")

if len(prediction_counts) == 1:
    print("\n⚠️  WARNING: Model is predicting only ONE emotion!")
    print("This indicates the model is not working correctly.")
elif len(prediction_counts) < 3:
    print("\n⚠️  WARNING: Model has very limited predictions!")
    print("This indicates potential model training issues.")
else:
    print("\n✅ Model appears to be working correctly.")
