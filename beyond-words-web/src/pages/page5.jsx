import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";

export default function Page5() {
  const navigate = useNavigate();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const goNext = () => navigate("/page6");
  const goBack = () => navigate(-1);

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        background: "linear-gradient(135deg, #FAF8F6 0%, #F0ECE8 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        boxSizing: "border-box",
        fontFamily: "Urbanist, sans-serif",
        color: "#4F3422",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          maxWidth: "750px",
          width: "100%",
          background: "white",
          borderRadius: "24px",
          padding: "clamp(2rem, 4vw, 3rem)",
          boxShadow: "0 20px 60px rgba(79, 52, 34, 0.12)",
          position: "relative",
          opacity: isLoaded ? 1 : 0,
          transform: isLoaded ? "translateY(0) scale(1)" : "translateY(30px) scale(0.95)",
          transition: "all 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
        }}
      >
        {/* Back Button */}
        <button
          onClick={goBack}
          style={{
            position: "absolute",
            top: "clamp(1.5rem, 3vw, 2rem)",
            left: "clamp(1.5rem, 3vw, 2rem)",
            border: "none",
            background: "#F7F4F2",
            color: "#4F3422",
            width: "clamp(2.5rem, 6vw, 3rem)",
            height: "clamp(2.5rem, 6vw, 3rem)",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            transition: "all 0.3s ease",
            fontSize: "clamp(1rem, 2vw, 1.25rem)",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "#4F3422";
            e.currentTarget.style.color = "white";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "#F7F4F2";
            e.currentTarget.style.color = "#4F3422";
          }}
        >
          <FaArrowLeft />
        </button>

        {/* Title */}
        <h1
          style={{
            fontSize: "clamp(1.75rem, 4vw, 2.5rem)",
            fontWeight: "800",
            marginBottom: "clamp(1rem, 2vw, 1.5rem)",
            textAlign: "center",
            color: "#642C2C",
            animation: isLoaded ? "fadeInDown 1s ease-out 0.2s both" : "none",
          }}
        >
          About Beyond Words
        </h1>

        {/* Main Content */}
        <div
          style={{
            fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
            color: "#6E5844",
            lineHeight: "1.8",
            marginBottom: "clamp(2rem, 3vw, 2.5rem)",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.4s both" : "none",
          }}
        >
          <p style={{ marginBottom: "1.5rem", textAlign: "justify" }}>
            Our app uses AI-powered analysis to detect emotions from your voice
            and text. Speak into your device or type a message, and the app
            identifies emotions such as happiness, sadness, anger, surprise, or
            neutrality. It provides instant feedback, helping you understand
            emotional cues in yourself and others.
          </p>

          <h3
            style={{
              fontSize: "clamp(1.125rem, 2.5vw, 1.5rem)",
              fontWeight: "700",
              marginBottom: "1rem",
              marginTop: "2rem",
              color: "#4F3422",
            }}
          >
            Uses of This App
          </h3>

          <ul
            style={{
              listStyle: "none",
              padding: 0,
              margin: 0,
            }}
          >
            {[
              {
                title: "Self-Awareness",
                desc: "Recognize your own emotions through voice and text.",
              },
              {
                title: "Mental Health Support",
                desc: "Track emotional trends to improve well-being.",
              },
              {
                title: "Communication Improvement",
                desc: "Understand others' emotions more accurately.",
              },
              {
                title: "Fun & Interactive",
                desc: "Explore emotional patterns in conversations or share with friends.",
              },
            ].map((item, index) => (
              <li
                key={index}
                style={{
                  marginBottom: "1rem",
                  padding: "1rem",
                  background: "#F7F4F2",
                  borderRadius: "12px",
                  borderLeft: "4px solid #4F3422",
                }}
              >
                <strong style={{ color: "#4F3422" }}>• {item.title}:</strong>{" "}
                {item.desc}
              </li>
            ))}
          </ul>
        </div>

        {/* Action Buttons */}
        <div
          style={{
            display: "flex",
            gap: "clamp(1rem, 2vw, 1.5rem)",
            flexWrap: "wrap",
            justifyContent: "center",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.6s both" : "none",
          }}
        >
          <button
            onClick={goNext}
            style={{
              flex: "1 1 200px",
              padding: "clamp(0.875rem, 1.8vw, 1.125rem) clamp(2rem, 3.5vw, 2.5rem)",
              borderRadius: "1000px",
              border: "none",
              background: "linear-gradient(135deg, #4F3422 0%, #6E4C3A 100%)",
              color: "white",
              fontSize: "clamp(1rem, 1.8vw, 1.125rem)",
              fontWeight: 700,
              cursor: "pointer",
              boxShadow: "0px 6px 20px rgba(79, 52, 34, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
              transition: "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
              position: "relative",
              overflow: "hidden",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-2px)";
              e.currentTarget.style.boxShadow = "0px 8px 30px rgba(79, 52, 34, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.15)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0px 6px 20px rgba(79, 52, 34, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1)";
            }}
          >
            <span
              style={{
                position: "absolute",
                top: 0,
                left: "-100%",
                width: "100%",
                height: "100%",
                background: "linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent)",
                animation: "shimmer 3s infinite",
              }}
            />
            <span style={{ position: "relative", zIndex: 1 }}>Continue</span>
          </button>
        </div>
      </div>

      {/* Keyframe Animations */}
      <style>{`
        @keyframes fadeInDown {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes shimmer {
          0% {
            left: -100%;
          }
          100% {
            left: 100%;
          }
        }
      `}</style>
    </div>
  );
}
