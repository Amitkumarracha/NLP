import React, { useState, useEffect } from "react";

export default function Page3({ onNext }) {
  const [gender, setGender] = useState("");
  const [sleep, setSleep] = useState("");
  const [dayQuality, setDayQuality] = useState("");
  const [isLoaded, setIsLoaded] = useState(false);
  const [sleepFocused, setSleepFocused] = useState(false);

  // Load saved data on mount
  useEffect(() => {
    const saved = localStorage.getItem("userSurvey");
    if (saved) {
      try {
        const data = JSON.parse(saved);
        setGender(data.gender || "");
        setSleep(data.sleep || "");
        setDayQuality(data.dayQuality || "");
      } catch (e) {
        console.error("Failed to load survey data", e);
      }
    }
    setIsLoaded(true);
  }, []);

  // Save data and navigate
  const handleNext = () => {
    const surveyData = {
      gender,
      sleep,
      dayQuality,
      timestamp: new Date().toISOString(),
    };
    
    localStorage.setItem("userSurvey", JSON.stringify(surveyData));
    console.log("✅ Survey data saved:", surveyData);
    onNext?.();
  };

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
          top: "-10%",
          right: "-5%",
          width: "clamp(300px, 35vw, 500px)",
          height: "clamp(300px, 35vw, 500px)",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(100, 44, 44, 0.04) 0%, transparent 70%)",
          pointerEvents: "none",
        }}
      />
      
      <div
        style={{
          maxWidth: "650px",
          width: "100%",
          background: "white",
          borderRadius: "24px",
          padding: "clamp(2rem, 4vw, 2.75rem) clamp(1.75rem, 4vw, 2.5rem)",
          boxShadow: "0 20px 60px rgba(79, 52, 34, 0.12)",
          opacity: isLoaded ? 1 : 0,
          transform: isLoaded ? "translateY(0) scale(1)" : "translateY(30px) scale(0.95)",
          transition: "all 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
          position: "relative",
          zIndex: 1,
        }}
      >
        {/* Heading */}
        <h2
          style={{
            textAlign: "center",
            fontSize: "clamp(1.5rem, 3.5vw, 2rem)",
            fontWeight: "800",
            marginBottom: "0.75rem",
            animation: isLoaded ? "fadeInDown 1s ease-out 0.2s both" : "none",
          }}
        >
          Answer some quick questions
        </h2>

        <p
          style={{
            textAlign: "center",
            fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
            color: "#6E5844",
            marginBottom: "clamp(1.75rem, 3vw, 2.25rem)",
            animation: isLoaded ? "fadeInDown 1s ease-out 0.3s both" : "none",
          }}
        >
          Answer before we start your AI journey
        </p>

        {/* Gender */}
        <div
          style={{
            marginBottom: "clamp(1.25rem, 2.5vw, 1.5rem)",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.4s both" : "none",
          }}
        >
          <label
            style={{
              display: "block",
              fontWeight: "700",
              marginBottom: "0.75rem",
              fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
            }}
          >
            What's your gender?
          </label>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))",
              gap: "clamp(0.625rem, 1.5vw, 0.875rem)",
            }}
          >
            {["Male", "Female", "Other"].map((g) => (
              <button
                key={g}
                onClick={() => setGender(g)}
                style={{
                  padding: "clamp(0.75rem, 1.8vw, 0.875rem) 0",
                  borderRadius: "12px",
                  border: gender === g ? "3px solid #4F3422" : "2px solid #E6D8CF",
                  background: gender === g ? "linear-gradient(135deg, #4F3422 0%, #6E4C3A 100%)" : "#FAFAFA",
                  color: gender === g ? "#FFFFFF" : "#4F3422",
                  fontWeight: "700",
                  fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
                  cursor: "pointer",
                  transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                  boxShadow: gender === g ? "0 4px 12px rgba(79, 52, 34, 0.2)" : "none",
                }}
                onMouseEnter={(e) => {
                  if (gender !== g) {
                    e.currentTarget.style.borderColor = "#4F3422";
                    e.currentTarget.style.transform = "translateY(-2px)";
                    e.currentTarget.style.boxShadow = "0 4px 12px rgba(79, 52, 34, 0.1)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (gender !== g) {
                    e.currentTarget.style.borderColor = "#E6D8CF";
                    e.currentTarget.style.transform = "translateY(0)";
                    e.currentTarget.style.boxShadow = "none";
                  }
                }}
              >
                {g}
              </button>
            ))}
          </div>
        </div>

        {/* Sleep Hours */}
        <div
          style={{
            marginBottom: "clamp(1.25rem, 2.5vw, 1.5rem)",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.5s both" : "none",
          }}
        >
          <label
            style={{
              display: "block",
              fontWeight: "700",
              marginBottom: "0.75rem",
              fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
            }}
          >
            How many hours do you usually sleep?
          </label>
          <input
            type="number"
            placeholder="e.g., 7"
            value={sleep}
            onChange={(e) => setSleep(e.target.value)}
            onFocus={() => setSleepFocused(true)}
            onBlur={() => setSleepFocused(false)}
            style={{
              width: "100%",
              padding: "clamp(0.875rem, 1.8vw, 1rem) clamp(1rem, 2vw, 1.25rem)",
              borderRadius: "12px",
              border: sleepFocused ? "2px solid #4F3422" : "2px solid #E6D8CF",
              fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
              outline: "none",
              backgroundColor: sleepFocused ? "white" : "#FAFAFA",
              boxSizing: "border-box",
              transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
              boxShadow: sleepFocused ? "0 4px 12px rgba(79, 52, 34, 0.08)" : "none",
            }}
          />
        </div>

        {/* Day Quality */}
        <div
          style={{
            marginBottom: "clamp(1.75rem, 3vw, 2.25rem)",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.6s both" : "none",
          }}
        >
          <label
            style={{
              display: "block",
              fontWeight: "700",
              marginBottom: "0.75rem",
              fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
            }}
          >
            Rate the quality of your day
          </label>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(5, 1fr)",
              gap: "clamp(0.5rem, 1.2vw, 0.625rem)",
            }}
          >
            {[1, 2, 3, 4, 5].map((num) => (
              <button
                key={num}
                onClick={() => setDayQuality(num)}
                style={{
                  padding: "clamp(0.625rem, 1.5vw, 0.875rem) 0",
                  borderRadius: "50%",
                  aspectRatio: "1",
                  border: dayQuality === num ? "3px solid #4F3422" : "2px solid #E6D8CF",
                  background: dayQuality === num ? "linear-gradient(135deg, #4F3422 0%, #6E4C3A 100%)" : "#FAFAFA",
                  color: dayQuality === num ? "#FFFFFF" : "#4F3422",
                  fontWeight: "700",
                  fontSize: "clamp(1rem, 2vw, 1.25rem)",
                  cursor: "pointer",
                  transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                  boxShadow: dayQuality === num ? "0 4px 12px rgba(79, 52, 34, 0.2)" : "none",
                }}
                onMouseEnter={(e) => {
                  if (dayQuality !== num) {
                    e.currentTarget.style.borderColor = "#4F3422";
                    e.currentTarget.style.transform = "scale(1.1)";
                    e.currentTarget.style.boxShadow = "0 4px 12px rgba(79, 52, 34, 0.1)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (dayQuality !== num) {
                    e.currentTarget.style.borderColor = "#E6D8CF";
                    e.currentTarget.style.transform = "scale(1)";
                    e.currentTarget.style.boxShadow = "none";
                  }
                }}
              >
                {num}
              </button>
            ))}
          </div>
        </div>

        {/* Next Button */}
        <button
          onClick={handleNext}
          disabled={!gender || !sleep || !dayQuality}
          style={{
            width: "100%",
            background: (!gender || !sleep || !dayQuality)
              ? "#C9BEB4"
              : "linear-gradient(135deg, #4F3422 0%, #6E4C3A 100%)",
            color: "white",
            fontSize: "clamp(1rem, 1.8vw, 1.125rem)",
            fontWeight: 700,
            border: "none",
            borderRadius: "1000px",
            padding: "clamp(0.875rem, 1.8vw, 1rem) 0",
            cursor: (!gender || !sleep || !dayQuality) ? "not-allowed" : "pointer",
            boxShadow: (!gender || !sleep || !dayQuality)
              ? "none"
              : "0px 6px 20px rgba(79, 52, 34, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            opacity: (!gender || !sleep || !dayQuality) ? 0.6 : 1,
            transition: "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.7s both" : "none",
            position: "relative",
            overflow: "hidden",
          }}
          onMouseEnter={(e) => {
            if (gender && sleep && dayQuality) {
              e.currentTarget.style.transform = "translateY(-2px)";
              e.currentTarget.style.boxShadow = "0px 8px 30px rgba(79, 52, 34, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.15)";
            }
          }}
          onMouseLeave={(e) => {
            if (gender && sleep && dayQuality) {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0px 6px 20px rgba(79, 52, 34, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1)";
            }
          }}
        >
          {/* Button Shimmer */}
          {gender && sleep && dayQuality && (
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
          )}
          <span style={{ position: "relative", zIndex: 1 }}>Let's Go</span>
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
