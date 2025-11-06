import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaMicrophone, FaKeyboard, FaInfoCircle } from "react-icons/fa";

export default function Page4() {
  const navigate = useNavigate();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  // Navigation handlers
  const goToChat = () => navigate("/page7");   // 📝 text chat page
  const goToRecord = () => navigate("/page6"); // 🎙 voice recording page
  const goToAbout = () => navigate("/page5");

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
      {/* Decorative Background */}
      <div
        style={{
          position: "absolute",
          bottom: "-8%",
          left: "-5%",
          width: "clamp(280px, 32vw, 450px)",
          height: "clamp(280px, 32vw, 450px)",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(79, 52, 34, 0.04) 0%, transparent 70%)",
          pointerEvents: "none",
        }}
      />

      <div
        style={{
          maxWidth: "750px",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "clamp(1.75rem, 3vw, 2.5rem)",
          opacity: isLoaded ? 1 : 0,
          transform: isLoaded ? "translateY(0)" : "translateY(30px)",
          transition: "all 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
          position: "relative",
          zIndex: 1,
        }}
      >
        {/* Title */}
        <div
          style={{
            textAlign: "center",
            maxWidth: "600px",
            animation: isLoaded ? "fadeInDown 1s ease-out 0.2s both" : "none",
          }}
        >
          <h2
            style={{
              fontSize: "clamp(1.5rem, 3.5vw, 2rem)",
              fontWeight: "800",
              marginBottom: "1rem",
              lineHeight: "1.3",
            }}
          >
            How would you like to share your thoughts with me?
          </h2>

          <p
            style={{
              fontSize: "clamp(0.9rem, 1.8vw, 1.125rem)",
              color: "#6E5844",
              lineHeight: "1.6",
            }}
          >
            You can either type or speak freely to express how you feel.
          </p>
        </div>

        {/* Option Cards */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
            gap: "clamp(1.25rem, 2.5vw, 1.75rem)",
            width: "100%",
            animation: isLoaded ? "fadeInScale 1s ease-out 0.4s both" : "none",
          }}
        >
          {/* Type Text Card */}
          <div
            onClick={goToChat}
            style={{
              background: "white",
              borderRadius: "20px",
              padding: "clamp(1.75rem, 3.5vw, 2.25rem)",
              boxShadow: "0 10px 40px rgba(79, 52, 34, 0.1)",
              cursor: "pointer",
              transition: "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              textAlign: "center",
              gap: "1.5rem",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-6px)";
              e.currentTarget.style.boxShadow = "0 15px 50px rgba(79, 52, 34, 0.15)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0 10px 40px rgba(79, 52, 34, 0.1)";
            }}
          >
            <div
              style={{
                width: "clamp(3.5rem, 9vw, 4.5rem)",
                height: "clamp(3.5rem, 9vw, 4.5rem)",
                borderRadius: "50%",
                background: "linear-gradient(135deg, #4F3422 0%, #6E4C3A 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 6px 20px rgba(79, 52, 34, 0.25)",
              }}
            >
              <FaKeyboard size={window.innerWidth < 768 ? 24 : 28} color="white" />
            </div>
            <div>
              <h3
                style={{
                  fontSize: "clamp(1.125rem, 2.5vw, 1.375rem)",
                  fontWeight: "700",
                  marginBottom: "0.5rem",
                  color: "#4F3422",
                }}
              >
                Type Text
              </h3>
              <p
                style={{
                  fontSize: "clamp(0.875rem, 1.5vw, 0.9375rem)",
                  color: "#6E5844",
                  lineHeight: "1.5",
                }}
              >
                Express yourself through writing in our AI-powered chat
              </p>
            </div>
          </div>

          {/* Speak/Record Card */}
          <div
            onClick={goToRecord}
            style={{
              background: "white",
              borderRadius: "20px",
              padding: "clamp(1.75rem, 3.5vw, 2.25rem)",
              boxShadow: "0 10px 40px rgba(159, 130, 91, 0.1)",
              cursor: "pointer",
              transition: "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              textAlign: "center",
              gap: "1.5rem",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-6px)";
              e.currentTarget.style.boxShadow = "0 15px 50px rgba(159, 130, 91, 0.15)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0 10px 40px rgba(159, 130, 91, 0.1)";
            }}
          >
            <div
              style={{
                width: "clamp(3.5rem, 9vw, 4.5rem)",
                height: "clamp(3.5rem, 9vw, 4.5rem)",
                borderRadius: "50%",
                background: "linear-gradient(135deg, #9F825B 0%, #B89872 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 6px 20px rgba(159, 130, 91, 0.25)",
              }}
            >
              <FaMicrophone size={window.innerWidth < 768 ? 24 : 28} color="white" />
            </div>
            <div>
              <h3
                style={{
                  fontSize: "clamp(1.125rem, 2.5vw, 1.375rem)",
                  fontWeight: "700",
                  marginBottom: "0.5rem",
                  color: "#4F3422",
                }}
              >
                Speak / Record Audio
              </h3>
              <p
                style={{
                  fontSize: "clamp(0.875rem, 1.5vw, 0.9375rem)",
                  color: "#6E5844",
                  lineHeight: "1.5",
                }}
              >
                Share your emotions through voice with emotion detection
              </p>
            </div>
          </div>
        </div>

        {/* About Link */}
        <button
          onClick={goToAbout}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            border: "none",
            background: "none",
            color: "#4F3422",
            fontWeight: 600,
            fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
            cursor: "pointer",
            textDecoration: "underline",
            fontFamily: "Urbanist, sans-serif",
            transition: "color 0.3s ease",
            animation: isLoaded ? "fadeIn 1s ease-out 0.6s both" : "none",
          }}
          onMouseEnter={(e) => (e.currentTarget.style.color = "#642C2C")}
          onMouseLeave={(e) => (e.currentTarget.style.color = "#4F3422")}
        >
          <FaInfoCircle size={16} />
          About Beyond Words
        </button>
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

        @keyframes fadeInScale {
          from {
            opacity: 0;
            transform: scale(0.9);
          }
          to {
            opacity: 1;
            transform: scale(1);
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
      `}</style>
    </div>
  );
}
