import React from "react";
import { useNavigate } from "react-router-dom";

export default function Page9() {
  const navigate = useNavigate();

  const tips = [
    {
      icon: "💧",
      title: "Drink Water",
      description: "Staying hydrated improves your mood and focus. Take a sip right now!",
    },
    {
      icon: "🌅",
      title: "Mindful Morning",
      description: "Start your day with deep breaths and gratitude. It sets a calm tone for the rest of the day.",
    },
    {
      icon: "💬",
      title: "Stay Connected",
      description: "Reach out to a friend or family member — small talks boost emotional balance.",
    },
  ];

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
        color: "#4F3422",
      }}
    >
      <div
        style={{
          maxWidth: "900px",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "clamp(2rem, 4vw, 3rem)",
        }}
      >
        {/* Header */}
        <div style={{ textAlign: "center" }}>
          <h2
            style={{
              fontSize: "clamp(2rem, 5vw, 3rem)",
              fontWeight: 700,
              color: "#642C2C",
              marginBottom: "0.75rem",
            }}
          >
            Daily Tips 🌸
          </h2>
          <p
            style={{
              fontSize: "clamp(1rem, 2vw, 1.25rem)",
              fontWeight: 500,
              color: "#4F3422",
              maxWidth: "600px",
              lineHeight: "1.6",
            }}
          >
            Here are some mindfulness and emotional wellness tips to brighten your day.
          </p>
        </div>

        {/* Tips Cards */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "clamp(1.5rem, 3vw, 2rem)",
            width: "100%",
          }}
        >
          {tips.map((tip, index) => (
            <div
              key={index}
              style={{
                background: "white",
                borderRadius: "20px",
                boxShadow: "0 10px 40px rgba(79, 52, 34, 0.12)",
                padding: "clamp(1.5rem, 3vw, 2rem)",
                transition: "all 0.3s ease",
                cursor: "default",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "translateY(-8px)";
                e.currentTarget.style.boxShadow = "0 15px 50px rgba(79, 52, 34, 0.18)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "translateY(0)";
                e.currentTarget.style.boxShadow = "0 10px 40px rgba(79, 52, 34, 0.12)";
              }}
            >
              <div
                style={{
                  fontSize: "clamp(2rem, 5vw, 3rem)",
                  marginBottom: "0.75rem",
                  textAlign: "center",
                }}
              >
                {tip.icon}
              </div>
              <div
                style={{
                  fontWeight: 700,
                  color: "#4F3422",
                  marginBottom: "0.5rem",
                  fontSize: "clamp(1.125rem, 2vw, 1.25rem)",
                  textAlign: "center",
                }}
              >
                {tip.title}
              </div>
              <div
                style={{
                  fontSize: "clamp(0.875rem, 1.5vw, 1rem)",
                  color: "#6E5844",
                  lineHeight: "1.6",
                  textAlign: "center",
                }}
              >
                {tip.description}
              </div>
            </div>
          ))}
        </div>

        {/* Back to Home Button */}
        <button
          onClick={() => navigate("/")}
          style={{
            padding: "clamp(1rem, 2vw, 1.25rem) clamp(2.5rem, 5vw, 4rem)",
            background: "#4F3422",
            border: "none",
            borderRadius: "1000px",
            color: "white",
            fontSize: "clamp(1.125rem, 2vw, 1.25rem)",
            fontWeight: 700,
            cursor: "pointer",
            boxShadow: "0 4px 20px rgba(79, 52, 34, 0.25)",
            fontFamily: "Urbanist, sans-serif",
            transition: "all 0.3s ease",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "translateY(-2px)";
            e.currentTarget.style.boxShadow = "0 6px 30px rgba(79, 52, 34, 0.35)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "0 4px 20px rgba(79, 52, 34, 0.25)";
          }}
        >
          Back to Home
        </button>
      </div>
    </div>
  );
}
