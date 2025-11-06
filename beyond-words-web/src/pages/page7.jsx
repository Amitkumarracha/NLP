import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaPaperPlane, FaMicrophone, FaStop, FaTrash, FaArrowLeft } from "react-icons/fa";

export default function Page7() {
  const navigate = useNavigate();
  
  // Load saved conversation history
  const loadHistory = () => {
    try {
      const saved = localStorage.getItem("chatHistory");
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (e) {
      console.error("Failed to load chat history", e);
    }
    return [
      {
        sender: "bot",
        text: "Hi! I'm your mental wellness assistant 💬\nI can understand both text and voice. How are you feeling today?",
        emotion: "calm",
      },
    ];
  };
  
  const [messages, setMessages] = useState(loadHistory);
  const [input, setInput] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [currentEmotion, setCurrentEmotion] = useState("neutral");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:8000";

  // Save conversation history whenever messages change
  useEffect(() => {
    if (messages.length > 1) {
      localStorage.setItem("chatHistory", JSON.stringify(messages));
    }
  }, [messages]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Clear chat history
  const clearHistory = () => {
    if (window.confirm("Clear all conversation history?")) {
      const initialMessage = [{
        sender: "bot",
        text: "Hi! I'm your mental wellness assistant 💬\nI can understand both text and voice. How are you feeling today?",
        emotion: "calm",
      }];
      setMessages(initialMessage);
      localStorage.removeItem("chatHistory");
    }
  };

  // Send text message with emotion analysis
  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMsg = { sender: "user", text: input, emotion: "analyzing" };
    setMessages((prev) => [...prev, userMsg]);
    const messageText = input;
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(`${backendUrl}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: messageText,
          emotion_context: currentEmotion,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        
        setMessages((prev) =>
          prev.map((msg, idx) =>
            idx === prev.length - 1
              ? { ...msg, emotion: data.detected_emotion }
              : msg
          )
        );
        
        setCurrentEmotion(data.detected_emotion);

        setTimeout(() => {
          setMessages((prev) => [
            ...prev,
            { sender: "bot", text: data.response, emotion: "calm" },
          ]);
          setIsLoading(false);
        }, 500);
      }
    } catch (error) {
      console.error("Error:", error);
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: "I'm here to listen. Tell me more about how you're feeling.", emotion: "calm" },
        ]);
        setIsLoading(false);
      }, 500);
    }
  };

  // Voice recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        await processVoiceMessage(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Could not access microphone.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processVoiceMessage = async (audioBlob) => {
    setIsLoading(true);
    setMessages((prev) => [...prev, { sender: "user", text: "🎤 Voice message...", emotion: "analyzing" }]);

    try {
      const formData = new FormData();
      formData.append("file", audioBlob, "voice.webm");

      const response = await fetch(`${backendUrl}/predict`, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        const transcription = data.transcription || "[Audio analyzed]";
        const emotion = data.final_emotion || data.emotion_ensemble || "neutral";
        
        setMessages((prev) =>
          prev.map((msg, idx) =>
            idx === prev.length - 1
              ? { ...msg, text: transcription, emotion: emotion }
              : msg
          )
        );
        
        setCurrentEmotion(emotion);

        const chatResponse = await fetch(`${backendUrl}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: transcription,
            emotion_context: emotion,
          }),
        });

        if (chatResponse.ok) {
          const chatData = await chatResponse.json();
          setTimeout(() => {
            setMessages((prev) => [...prev, { sender: "bot", text: chatData.response, emotion: "calm" }]);
            setIsLoading(false);
          }, 500);
        }
      }
    } catch (error) {
      console.error("Error processing voice:", error);
      setMessages((prev) =>
        prev.map((msg, idx) =>
          idx === prev.length - 1
            ? { ...msg, text: "[Audio processing failed]", emotion: "neutral" }
            : msg
        )
      );
      setIsLoading(false);
    }
  };

  const getEmotionColor = (emotion) => {
    const colors = {
      happy: "#F8D26A",
      sad: "#7BA3CC",
      angry: "#B23A48",
      fearful: "#8B7AA8",
      calm: "#5F8C52",
      surprised: "#E8A87C",
      disgust: "#A67C52",
      neutral: "#C9BEB4",
    };
    return colors[emotion] || colors.neutral;
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        background: "#F7F4F2",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "clamp(1rem, 2vw, 2rem)",
        boxSizing: "border-box",
        fontFamily: "Urbanist, sans-serif",
      }}
    >
      <div
        style={{
          maxWidth: "900px",
          width: "100%",
          height: "clamp(500px, 80vh, 700px)",
          backgroundColor: "white",
          borderRadius: "24px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          color: "#4F3422",
          boxShadow: "0 20px 60px rgba(79, 52, 34, 0.15)",
          overflow: "hidden",
        }}
      >
        {/* Top bar */}
        <div
          style={{
            padding: "clamp(1rem, 2vw, 1.5rem) clamp(1.5rem, 3vw, 2rem)",
            fontSize: "clamp(1.125rem, 2vw, 1.25rem)",
            fontWeight: "600",
            borderBottom: "2px solid #E6D8CF",
            display: "flex",
            alignItems: "center",
            gap: "1rem",
            justifyContent: "space-between",
            background: "#F7F4F2",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
            <button
              onClick={() => navigate(-1)}
              style={{
                border: "none",
                background: "white",
                fontSize: "clamp(1.125rem, 2vw, 1.25rem)",
                cursor: "pointer",
                color: "#4F3422",
                width: "clamp(2rem, 5vw, 2.5rem)",
                height: "clamp(2rem, 5vw, 2.5rem)",
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                transition: "all 0.3s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "#4F3422";
                e.currentTarget.style.color = "white";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "white";
                e.currentTarget.style.color = "#4F3422";
              }}
            >
              <FaArrowLeft />
            </button>
            <span>Emotion-Aware Chat</span>
          </div>
          <button
            onClick={clearHistory}
            style={{
              border: "none",
              background: "white",
              color: "#B23A48",
              cursor: "pointer",
              fontSize: "clamp(1rem, 2vw, 1.125rem)",
              width: "clamp(2rem, 5vw, 2.5rem)",
              height: "clamp(2rem, 5vw, 2.5rem)",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              transition: "all 0.3s ease",
            }}
            title="Clear chat history"
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "#B23A48";
              e.currentTarget.style.color = "white";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "white";
              e.currentTarget.style.color = "#B23A48";
            }}
          >
            <FaTrash />
          </button>
        </div>

        {/* Current emotion indicator */}
        <div
          style={{
            padding: "clamp(0.5rem, 1vw, 0.75rem) clamp(1rem, 2vw, 1.5rem)",
            backgroundColor: "#FFF",
            borderBottom: "1px solid #E6D8CF",
            fontSize: "clamp(0.875rem, 1.5vw, 1rem)",
            color: "#8B7355",
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
          }}
        >
          Current mood:
          <span
            style={{
              padding: "clamp(0.25rem, 0.5vw, 0.375rem) clamp(0.75rem, 1.5vw, 1rem)",
              borderRadius: "12px",
              backgroundColor: getEmotionColor(currentEmotion),
              color: "#FFF",
              fontWeight: 600,
              fontSize: "clamp(0.75rem, 1.5vw, 0.875rem)",
              textTransform: "capitalize",
            }}
          >
            {currentEmotion}
          </span>
        </div>

        {/* Chat window */}
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            padding: "clamp(1rem, 2vw, 1.5rem)",
            display: "flex",
            flexDirection: "column",
            gap: "0.75rem",
            background: "#FAFAFA",
          }}
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              style={{
                alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                backgroundColor: msg.sender === "user" ? getEmotionColor(msg.emotion) : "#FFF",
                color: msg.sender === "user" ? "#FFF" : "#4F3422",
                padding: "clamp(0.75rem, 1.5vw, 1rem) clamp(1rem, 2vw, 1.25rem)",
                borderRadius: "16px",
                maxWidth: "70%",
                whiteSpace: "pre-line",
                boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                position: "relative",
                fontSize: "clamp(0.875rem, 1.5vw, 1rem)",
                lineHeight: "1.5",
              }}
            >
              {msg.text}
              {msg.emotion && msg.sender === "user" && msg.emotion !== "analyzing" && (
                <div
                  style={{
                    fontSize: "clamp(0.625rem, 1vw, 0.75rem)",
                    marginTop: "0.25rem",
                    opacity: 0.8,
                    textTransform: "capitalize",
                  }}
                >
                  {msg.emotion}
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div
              style={{
                alignSelf: "flex-start",
                color: "#8B7355",
                fontSize: "clamp(0.875rem, 1.5vw, 1rem)",
                fontStyle: "italic",
              }}
            >
              Thinking...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input section */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            padding: "clamp(1rem, 2vw, 1.25rem)",
            borderTop: "2px solid #E6D8CF",
            backgroundColor: "#FFF",
            gap: "clamp(0.5rem, 1vw, 0.75rem)",
          }}
        >
          <input
            type="text"
            placeholder="Type or speak your message"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isRecording}
            style={{
              flex: 1,
              padding: "clamp(0.75rem, 1.5vw, 1rem)",
              borderRadius: "25px",
              border: "2px solid #E6D8CF",
              outline: "none",
              fontSize: "clamp(0.875rem, 1.5vw, 1rem)",
              opacity: isRecording ? 0.5 : 1,
              transition: "all 0.3s ease",
            }}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            onFocus={(e) => (e.target.style.borderColor = "#4F3422")}
            onBlur={(e) => (e.target.style.borderColor = "#E6D8CF")}
          />
          
          <button
            onClick={isRecording ? stopRecording : startRecording}
            style={{
              backgroundColor: isRecording ? "#B23A48" : "#5F8C52",
              border: "none",
              color: "white",
              borderRadius: "50%",
              width: "clamp(2.5rem, 6vw, 3rem)",
              height: "clamp(2.5rem, 6vw, 3rem)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              transition: "all 0.3s ease",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.1)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
          >
            {isRecording ? <FaStop size={16} /> : <FaMicrophone size={16} />}
          </button>

          <button
            onClick={sendMessage}
            disabled={isRecording}
            style={{
              backgroundColor: "#4F3422",
              border: "none",
              color: "white",
              borderRadius: "50%",
              width: "clamp(2.5rem, 6vw, 3rem)",
              height: "clamp(2.5rem, 6vw, 3rem)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              opacity: isRecording ? 0.5 : 1,
              transition: "all 0.3s ease",
            }}
            onMouseEnter={(e) => {
              if (!isRecording) e.currentTarget.style.transform = "scale(1.1)";
            }}
            onMouseLeave={(e) => {
              if (!isRecording) e.currentTarget.style.transform = "scale(1)";
            }}
          >
            <FaPaperPlane size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
