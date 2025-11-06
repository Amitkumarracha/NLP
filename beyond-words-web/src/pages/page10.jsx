import React from "react";
import { useNavigate } from "react-router-dom";

export default function Page10() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        background: "linear-gradient(180deg, #F7F4F2 0%, #E8DFD6 100%)",
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
          maxWidth: "700px",
          width: "100%",
          background: "white",
          borderRadius: "24px",
          padding: "clamp(2.5rem, 5vw, 4rem) clamp(2rem, 4vw, 3rem)",
          boxShadow: "0 20px 60px rgba(79, 52, 34, 0.15)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          gap: "clamp(1.5rem, 3vw, 2.5rem)",
        }}
      >
        {/* Success Icon */}
        <div
          style={{
            width: "clamp(100px, 20vw, 150px)",
            height: "clamp(100px, 20vw, 150px)",
            borderRadius: "50%",
            background: "linear-gradient(135deg, #5F8C52 0%, #76A66A 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "clamp(3rem, 10vw, 5rem)",
            color: "white",
            boxShadow: "0 10px 40px rgba(95, 140, 82, 0.3)",
          }}
        >
          ✓
        </div>

        {/* Thank You Message */}
        <h1
          style={{
            fontSize: "clamp(2rem, 5vw, 3rem)",
            fontWeight: 800,
            color: "#642C2C",
            marginBottom: 0,
          }}
        >
          Thank You!
        </h1>

        <p
          style={{
            fontSize: "clamp(1rem, 2vw, 1.25rem)",
            lineHeight: "1.7",
            color: "#4F3422",
            maxWidth: "500px",
          }}
        >
          Your emotional wellness journey matters. Keep taking care of yourself, one step at a time.
        </p>

        {/* Stats/Summary */}
        <div
          style={{
            background: "#F7F4F2",
            borderRadius: "20px",
            padding: "clamp(1.5rem, 3vw, 2rem)",
            width: "100%",
            boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
            borderLeft: "6px solid #4F3422",
          }}
        >
          <h3
            style={{
              fontSize: "clamp(1.125rem, 2vw, 1.375rem)",
              fontWeight: 700,
              marginBottom: "1rem",
              color: "#4F3422",
            }}
          >
            Remember:
          </h3>
          <ul
            style={{
              textAlign: "left",
              fontSize: "clamp(0.875rem, 1.5vw, 1rem)",
              lineHeight: "2",
              color: "#6E5844",
              paddingLeft: "clamp(1.25rem, 3vw, 1.75rem)",
              margin: 0,
            }}
          >
            <li>Your emotions are valid</li>
            <li>Practice self-compassion daily</li>
            <li>Reach out when you need support</li>
            <li>Small steps lead to big changes</li>
          </ul>
        </div>

        {/* Action Buttons */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "clamp(0.75rem, 1.5vw, 1rem)",
            width: "100%",
            maxWidth: "450px",
          }}
        >
          <button
            onClick={() => navigate("/page4")}
            style={{
              width: "100%",
              padding: "clamp(1rem, 2vw, 1.25rem)",
              borderRadius: "1000px",
              border: "none",
              background: "#4F3422",
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
            Start New Session
          </button>

          <button
            onClick={() => navigate("/")}
            style={{
              width: "100%",
              padding: "clamp(1rem, 2vw, 1.25rem)",
              borderRadius: "1000px",
              border: "2px solid #4F3422",
              background: "transparent",
              color: "#4F3422",
              fontSize: "clamp(1.125rem, 2vw, 1.25rem)",
              fontWeight: 700,
              cursor: "pointer",
              fontFamily: "Urbanist, sans-serif",
              transition: "all 0.3s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "#4F3422";
              e.currentTarget.style.color = "white";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "transparent";
              e.currentTarget.style.color = "#4F3422";
            }}
          >
            Back to Home
          </button>
        </div>
      </div>
    </div>
  );
}
