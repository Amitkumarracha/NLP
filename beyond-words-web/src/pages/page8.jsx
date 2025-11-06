import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Page8() {
  const navigate = useNavigate();
  const [result, setResult] = useState(null);

  // Fetch result stored by Page6
  useEffect(() => {
    const stored = localStorage.getItem("emotionResult");
    if (stored) {
      setResult(JSON.parse(stored));
    }
  }, []);

  // Map emotions → wellbeing messages
  const messages = {
    angry: "It’s okay, I can understand! Take a deep breath — we can talk it out together.",
    sad: "I'm here for you. It’s okay to feel sad. Let’s focus on something comforting.",
    happy: "That’s awesome! Keep spreading the positivity around you!",
    calm: "Peaceful minds lead to peaceful days. Stay grounded 🌿",
    fearful: "Courage doesn’t mean no fear — it means moving forward despite it. You’re strong!",
    surprised: "Life is full of surprises! Let's see what this moment brings.",
    disgust: "That reaction makes sense — let’s unpack why you felt that way.",
    neutral: "A calm, steady state of mind — great place to reflect and grow.",
  };

  if (!result) {
    return (
      <div
        style={{
          minHeight: "100vh",
          width: "100%",
          backgroundColor: "#F7F4F2",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          color: "#4F3422",
          fontFamily: "Urbanist, sans-serif",
          fontSize: "clamp(1rem, 2vw, 1.25rem)",
          padding: "2rem",
          textAlign: "center",
        }}
      >
        No emotion data found. Please record your voice again.
      </div>
    );
  }

  const emotion = (
    result.final_emotion ||
    result.emotion_ensemble ||
    result.emotion_xgb ||
    result.emotion ||
    "neutral"
  ).toLowerCase();
  
  const confidence = (
    result.final_confidence ||
    result.confidence_ensemble ||
    result.confidence_xgb ||
    0
  );
  
  const transcription = result.transcription || "";
  const message = messages[emotion] || messages.neutral;

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        background: "#F7F4F2",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        boxSizing: "border-box",
        fontFamily: "Urbanist, sans-serif",
      }}
    >
      <div
        style={{
          maxWidth: "650px",
          width: "100%",
          background: "white",
          borderRadius: "24px",
          padding: "clamp(2rem, 5vw, 3.5rem)",
          boxShadow: "0 20px 60px rgba(79, 52, 34, 0.15)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          color: "#4F3422",
          gap: "clamp(1.5rem, 3vw, 2rem)",
        }}
      >
        {/* Transcription */}
        {transcription && (
          <div
            style={{
              width: "100%",
              padding: "clamp(1rem, 2vw, 1.5rem)",
              backgroundColor: "#F7F4F2",
              borderRadius: "16px",
              boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
            }}
          >
            <p
              style={{
                fontSize: "clamp(0.75rem, 1.5vw, 0.875rem)",
                fontWeight: 600,
                color: "#8B7355",
                marginBottom: "0.5rem",
                letterSpacing: "0.5px",
              }}
            >
              YOU SAID:
            </p>
            <p
              style={{
                fontSize: "clamp(0.875rem, 1.5vw, 1rem)",
                fontStyle: "italic",
                color: "#4F3422",
                lineHeight: 1.6,
              }}
            >
              "{transcription}"
            </p>
          </div>
        )}

        {/* Title */}
        <h2
          style={{
            fontSize: "clamp(1.25rem, 3vw, 1.75rem)",
            fontWeight: 600,
            marginBottom: 0,
          }}
        >
          Detected Emotion:
        </h2>

        {/* Emotion Display */}
        <h1
          style={{
            fontSize: "clamp(2rem, 5vw, 3rem)",
            fontWeight: 700,
            color: "#A63C24",
            marginBottom: 0,
            textTransform: "capitalize",
            lineHeight: "1.3",
          }}
        >
          You're feeling... <br /> {emotion}
        </h1>

        {/* Description */}
        <p
          style={{
            fontSize: "clamp(1rem, 2vw, 1.125rem)",
            lineHeight: "1.7",
            color: "#4F3422",
            maxWidth: "500px",
          }}
        >
          {message}
        </p>

        {/* Confidence Badge */}
        <div
          style={{
            padding: "clamp(0.5rem, 1vw, 0.75rem) clamp(1.25rem, 2vw, 1.75rem)",
            backgroundColor: confidence > 0.7 ? "#4F3422" : "#8B7355",
            color: "white",
            borderRadius: "1000px",
            fontSize: "clamp(0.875rem, 1.5vw, 1rem)",
            fontWeight: 600,
          }}
        >
          {(confidence * 100).toFixed(1)}% Confidence
        </div>

        {/* Buttons */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "clamp(0.75rem, 1.5vw, 1rem)",
            width: "100%",
            maxWidth: "400px",
          }}
        >
          <button
            onClick={() => navigate("/page7")}
            style={{
              backgroundColor: "#5F8C52",
              border: "none",
              color: "white",
              fontSize: "clamp(1rem, 2vw, 1.125rem)",
              padding: "clamp(0.875rem, 2vw, 1.125rem)",
              borderRadius: "1000px",
              fontWeight: 600,
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(95, 140, 82, 0.25)",
              transition: "all 0.3s ease",
              fontFamily: "Urbanist, sans-serif",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-2px)";
              e.currentTarget.style.boxShadow = "0 6px 20px rgba(95, 140, 82, 0.35)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0 4px 12px rgba(95, 140, 82, 0.25)";
            }}
          >
            Continue in Chat
          </button>

          <button
            onClick={() => navigate("/page9")}
            style={{
              backgroundColor: "#4F3422",
              border: "none",
              color: "white",
              fontSize: "clamp(1rem, 2vw, 1.125rem)",
              padding: "clamp(0.875rem, 2vw, 1.125rem)",
              borderRadius: "1000px",
              fontWeight: 600,
              cursor: "pointer",
              boxShadow: "0 4px 12px rgba(79, 52, 34, 0.25)",
              transition: "all 0.3s ease",
              fontFamily: "Urbanist, sans-serif",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-2px)";
              e.currentTarget.style.boxShadow = "0 6px 20px rgba(79, 52, 34, 0.35)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0 4px 12px rgba(79, 52, 34, 0.25)";
            }}
          >
            View Tips
          </button>

          <button
            onClick={() => navigate(-1)}
            style={{
              backgroundColor: "transparent",
              border: "2px solid #4F3422",
              color: "#4F3422",
              fontSize: "clamp(1rem, 2vw, 1.125rem)",
              padding: "clamp(0.875rem, 2vw, 1.125rem)",
              borderRadius: "1000px",
              fontWeight: 600,
              cursor: "pointer",
              transition: "all 0.3s ease",
              fontFamily: "Urbanist, sans-serif",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = "#4F3422";
              e.currentTarget.style.color = "white";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = "transparent";
              e.currentTarget.style.color = "#4F3422";
            }}
          >
            Go Back
          </button>
        </div>
      </div>
    </div>
  );
}
