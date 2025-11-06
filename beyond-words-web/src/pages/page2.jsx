import React, { useState, useEffect } from "react";
import { FaGoogle, FaApple, FaFacebookF } from "react-icons/fa";

export default function Page2({ onNext }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [emailFocused, setEmailFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);

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
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        boxSizing: "border-box",
        fontFamily: "Urbanist, sans-serif",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Decorative Background Elements */}
      <div
        style={{
          position: "absolute",
          top: "-5%",
          right: "-3%",
          width: "clamp(250px, 30vw, 400px)",
          height: "clamp(250px, 30vw, 400px)",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(100, 44, 44, 0.04) 0%, transparent 70%)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "-5%",
          left: "-3%",
          width: "clamp(200px, 25vw, 350px)",
          height: "clamp(200px, 25vw, 350px)",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(79, 52, 34, 0.04) 0%, transparent 70%)",
          pointerEvents: "none",
        }}
      />

      <div
        style={{
          maxWidth: "480px",
          width: "100%",
          background: "white",
          borderRadius: "24px",
          padding: "clamp(2rem, 4vw, 2.5rem) clamp(1.75rem, 4vw, 2.25rem)",
          boxShadow: "0 20px 60px rgba(79, 52, 34, 0.12)",
          opacity: isLoaded ? 1 : 0,
          transform: isLoaded ? "translateY(0) scale(1)" : "translateY(30px) scale(0.95)",
          transition: "all 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
          position: "relative",
          zIndex: 1,
        }}
      >
        {/* Heading */}
        <h1
          style={{
            textAlign: "center",
            fontSize: "clamp(1.75rem, 3.5vw, 2.25rem)",
            fontWeight: "800",
            color: "#4F3422",
            marginBottom: "0.5rem",
            animation: isLoaded ? "fadeInDown 1s ease-out 0.2s both" : "none",
          }}
        >
          Sign In
        </h1>
        <p
          style={{
            textAlign: "center",
            fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
            color: "#6E5844",
            marginBottom: "clamp(1.75rem, 3vw, 2.25rem)",
            animation: isLoaded ? "fadeInDown 1s ease-out 0.3s both" : "none",
          }}
        >
          Please enter your details to continue
        </p>

        {/* Input fields */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "clamp(0.875rem, 1.8vw, 1.125rem)",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.4s both" : "none",
          }}
        >
          <input
            type="email"
            placeholder="Email address"
            onFocus={() => setEmailFocused(true)}
            onBlur={() => setEmailFocused(false)}
            style={{
              width: "100%",
              padding: "clamp(0.875rem, 1.8vw, 1rem) clamp(1rem, 2vw, 1.25rem)",
              borderRadius: "12px",
              border: emailFocused ? "2px solid #4F3422" : "2px solid #E6D8CF",
              fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
              outline: "none",
              backgroundColor: emailFocused ? "white" : "#FAFAFA",
              color: "#4F3422",
              transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
              boxSizing: "border-box",
              boxShadow: emailFocused ? "0 4px 12px rgba(79, 52, 34, 0.08)" : "none",
            }}
          />
          <input
            type="password"
            placeholder="Password"
            onFocus={() => setPasswordFocused(true)}
            onBlur={() => setPasswordFocused(false)}
            style={{
              width: "100%",
              padding: "clamp(0.875rem, 1.8vw, 1rem) clamp(1rem, 2vw, 1.25rem)",
              borderRadius: "12px",
              border: passwordFocused ? "2px solid #4F3422" : "2px solid #E6D8CF",
              fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
              outline: "none",
              backgroundColor: passwordFocused ? "white" : "#FAFAFA",
              color: "#4F3422",
              transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
              boxSizing: "border-box",
              boxShadow: passwordFocused ? "0 4px 12px rgba(79, 52, 34, 0.08)" : "none",
            }}
          />
        </div>

        {/* Sign In button */}
        <button
          onClick={onNext}
          style={{
            width: "100%",
            marginTop: "clamp(1.5rem, 2.5vw, 1.875rem)",
            background: "linear-gradient(135deg, #4F3422 0%, #6E4C3A 100%)",
            color: "white",
            fontSize: "clamp(1rem, 1.8vw, 1.125rem)",
            fontWeight: 700,
            border: "none",
            borderRadius: "1000px",
            padding: "clamp(0.875rem, 1.8vw, 1rem) 0",
            cursor: "pointer",
            boxShadow: "0px 6px 20px rgba(79, 52, 34, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            transition: "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.5s both" : "none",
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
          onMouseDown={(e) => {
            e.currentTarget.style.transform = "translateY(0) scale(0.98)";
          }}
          onMouseUp={(e) => {
            e.currentTarget.style.transform = "translateY(-2px) scale(1)";
          }}
        >
          {/* Button Shimmer */}
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
          <span style={{ position: "relative", zIndex: 1 }}>Sign In</span>
        </button>

        {/* OR separator */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            margin: "clamp(1.75rem, 2.5vw, 2rem) 0 clamp(1.25rem, 2vw, 1.5rem)",
            color: "#8B7C6F",
            fontSize: "clamp(0.8rem, 1.5vw, 0.875rem)",
            animation: isLoaded ? "fadeIn 1s ease-out 0.6s both" : "none",
          }}
        >
          <div style={{ flex: 1, height: 1, background: "#D6CCC6" }}></div>
          <span style={{ margin: "0 1rem", fontWeight: 600 }}>OR</span>
          <div style={{ flex: 1, height: 1, background: "#D6CCC6" }}></div>
        </div>

        {/* Social login buttons */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "clamp(1rem, 2.5vw, 1.5rem)",
            marginBottom: "clamp(1.5rem, 2.5vw, 1.875rem)",
            animation: isLoaded ? "fadeInScale 1s ease-out 0.7s both" : "none",
          }}
        >
          {[
            { Icon: FaGoogle, color: "#DB4437", size: 22 },
            { Icon: FaApple, color: "#000000", size: 24 },
            { Icon: FaFacebookF, color: "#4267B2", size: 22 },
          ].map(({ Icon, color, size }, index) => (
            <div
              key={index}
              style={{
                width: "clamp(2.75rem, 7vw, 3.25rem)",
                height: "clamp(2.75rem, 7vw, 3.25rem)",
                borderRadius: "50%",
                background: "#FFFFFF",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
                cursor: "pointer",
                transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                border: "2px solid #F7F4F2",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "translateY(-4px) scale(1.05)";
                e.currentTarget.style.boxShadow = "0 8px 20px rgba(0,0,0,0.12)";
                e.currentTarget.style.borderColor = color;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "translateY(0) scale(1)";
                e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.08)";
                e.currentTarget.style.borderColor = "#F7F4F2";
              }}
            >
              <Icon color={color} size={size} />
            </div>
          ))}
        </div>

        {/* Forgot password text */}
        <p
          style={{
            textAlign: "center",
            color: "#4F3422",
            fontSize: "clamp(0.8rem, 1.5vw, 0.875rem)",
            fontWeight: 600,
            cursor: "pointer",
            textDecoration: "underline",
            transition: "color 0.3s ease",
            margin: 0,
            animation: isLoaded ? "fadeIn 1s ease-out 0.8s both" : "none",
          }}
          onMouseEnter={(e) => (e.target.style.color = "#642C2C")}
          onMouseLeave={(e) => (e.target.style.color = "#4F3422")}
        >
          Forgot your password?
        </p>
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

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
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
