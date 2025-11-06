import React, { useState, useEffect } from "react";
import Beyound_words from "../assets/Beyond_words.png"; 

export default function Page1({ onSignIn }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isHovering, setIsHovering] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        background: "linear-gradient(135deg, #FAF8F6 0%, #F0ECE8 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "clamp(1.5rem, 3vw, 2.5rem) 2rem",
        boxSizing: "border-box",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Decorative Background Elements */}
      <div
        style={{
          position: "absolute",
          top: "-10%",
          right: "-5%",
          width: "clamp(300px, 40vw, 600px)",
          height: "clamp(300px, 40vw, 600px)",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(100, 44, 44, 0.03) 0%, transparent 70%)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "-10%",
          left: "-5%",
          width: "clamp(250px, 35vw, 500px)",
          height: "clamp(250px, 35vw, 500px)",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(79, 52, 34, 0.03) 0%, transparent 70%)",
          pointerEvents: "none",
        }}
      />

      {/* Main Content Container */}
      <div
        style={{
          maxWidth: "900px",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "clamp(1.5rem, 3vw, 2.25rem)",
          opacity: isLoaded ? 1 : 0,
          transform: isLoaded ? "translateY(0)" : "translateY(20px)",
          transition: "all 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
          position: "relative",
          zIndex: 1,
        }}
      >
        {/* Welcome Heading */}
        <h1
          style={{
            textAlign: "center",
            color: "#642C2C",
            fontSize: "clamp(2rem, 5vw, 3.5rem)",
            fontFamily: "Work Sans",
            fontWeight: "700",
            margin: 0,
            letterSpacing: "-0.03em",
            lineHeight: "1.1",
            textShadow: "0 2px 10px rgba(100, 44, 44, 0.1)",
            animation: isLoaded ? "fadeInDown 1s ease-out" : "none",
          }}
        >
          Welcome!
        </h1>

        {/* Logo Container with Ring Effect */}
        <div
          style={{
            position: "relative",
            animation: isLoaded ? "fadeInScale 1.2s ease-out 0.3s both" : "none",
          }}
        >
          {/* Animated Ring */}
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              width: "calc(100% + 40px)",
              height: "calc(100% + 40px)",
              borderRadius: "50%",
              border: "3px solid rgba(79, 52, 34, 0.15)",
              animation: isHovering ? "pulse 2s ease-in-out infinite" : "none",
              transition: "all 0.3s ease",
            }}
          />
          
          {/* Logo Image */}
          <img
            src={Beyound_words}
            alt="Beyond Words Logo - AI for Mental Wellness"
            onMouseEnter={() => setIsHovering(true)}
            onMouseLeave={() => setIsHovering(false)}
            style={{
              width: "clamp(180px, 22vw, 280px)",
              height: "clamp(180px, 22vw, 280px)",
              borderRadius: "50%",
              objectFit: "cover",
              boxShadow: isHovering
                ? "0 20px 60px rgba(79, 52, 34, 0.25), 0 0 0 8px rgba(79, 52, 34, 0.05)"
                : "0 15px 50px rgba(79, 52, 34, 0.2)",
              transform: isHovering ? "scale(1.03) rotate(2deg)" : "scale(1) rotate(0deg)",
              transition: "all 0.5s cubic-bezier(0.4, 0, 0.2, 1)",
              cursor: "pointer",
              border: "6px solid rgba(255, 255, 255, 0.8)",
            }}
          />
        </div>

        {/* Tagline Text */}
        <p
          style={{
            textAlign: "center",
            color: "#4F3422",
            fontSize: "clamp(1.125rem, 2.5vw, 1.75rem)",
            fontFamily: "Urbanist",
            fontWeight: "800",
            lineHeight: "1.5",
            maxWidth: "700px",
            margin: 0,
            padding: "0 1rem",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.5s both" : "none",
          }}
        >
          Ready for improving your{" "}
          <span
            style={{
              background: "linear-gradient(135deg, #642C2C 0%, #8B5A3C 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
            }}
          >
            Mental Health
          </span>
          {" "}with AI?
        </p>

        {/* Sign In Button */}
        <button
          onClick={() => onSignIn?.()}
          style={{
            padding: "clamp(0.875rem, 1.8vw, 1.125rem) clamp(2rem, 4vw, 2.75rem)",
            background: "linear-gradient(135deg, #4F3422 0%, #6E4C3A 100%)",
            borderRadius: "1000px",
            border: "none",
            cursor: "pointer",
            transition: "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
            boxShadow: "0 6px 25px rgba(79, 52, 34, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            position: "relative",
            overflow: "hidden",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.7s both" : "none",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "translateY(-3px) scale(1.02)";
            e.currentTarget.style.boxShadow = "0 10px 40px rgba(79, 52, 34, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "translateY(0) scale(1)";
            e.currentTarget.style.boxShadow = "0 6px 25px rgba(79, 52, 34, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)";
          }}
          onMouseDown={(e) => {
            e.currentTarget.style.transform = "translateY(-1px) scale(0.98)";
          }}
          onMouseUp={(e) => {
            e.currentTarget.style.transform = "translateY(-3px) scale(1.02)";
          }}
        >
          {/* Button Shimmer Effect */}
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
          
          <span
            style={{
              color: "white",
              fontSize: "clamp(1rem, 1.8vw, 1.25rem)",
              fontFamily: "Urbanist",
              fontWeight: "800",
              letterSpacing: "0.5px",
              textShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
              position: "relative",
              zIndex: 1,
            }}
          >
            Sign In
          </span>
        </button>

        {/* Subtle Feature Hint */}
        <p
          style={{
            fontSize: "clamp(0.875rem, 1.5vw, 1rem)",
            color: "#8B7355",
            fontFamily: "Urbanist",
            fontWeight: "500",
            margin: 0,
            opacity: 0.8,
            animation: isLoaded ? "fadeIn 1s ease-out 1s both" : "none",
          }}
        >
          Voice & Text Emotion Analysis • AI-Powered Support
        </p>
      </div>

      {/* Keyframe Animations */}
      <style>{`
        @keyframes fadeInDown {
          from {
            opacity: 0;
            transform: translateY(-30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeInScale {
          from {
            opacity: 0;
            transform: scale(0.8);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }

        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 0.8;
          }
        }

        @keyframes pulse {
          0%, 100% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.15;
          }
          50% {
            transform: translate(-50%, -50%) scale(1.05);
            opacity: 0.25;
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
