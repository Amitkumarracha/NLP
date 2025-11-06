import React, { useState, useEffect } from "react";
import { FaMicrophone, FaStop, FaArrowLeft } from "react-icons/fa";

export default function Page6({ onAnalyze, onBack }) {
  const [recording, setRecording] = useState(false);
  const [audioData, setAudioData] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  // Start recording with WAV format
  const startRecording = async () => {
    try {
      console.log("🎙️ Requesting microphone permission...");
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      console.log("✅ Microphone access granted.");

      // Try to use WAV format, fallback to webm if not supported
      let mimeType = 'audio/wav';
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        console.log("⚠️ WAV not supported, checking alternatives...");

        // Try different formats
        const formats = [
          'audio/webm;codecs=pcm',
          'audio/webm;codecs=opus',
          'audio/webm',
          'audio/ogg;codecs=opus',
          'audio/mp4'
        ];

        mimeType = formats.find(fmt => MediaRecorder.isTypeSupported(fmt)) || 'audio/webm';
        console.log("📝 Using format:", mimeType);
      }

      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      const chunks = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) chunks.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: mimeType });

        // If we got webm, convert to WAV in the browser
        if (mimeType.includes('webm') || mimeType.includes('ogg')) {
          console.log("🔄 Converting to WAV format...");
          try {
            const wavBlob = await convertToWav(blob);
            const url = URL.createObjectURL(wavBlob);
            console.log("✅ Converted to WAV. Size:", wavBlob.size, "bytes");
            setAudioData({ blob: wavBlob, url });
          } catch (err) {
            console.error("❌ Conversion failed:", err);
            // Fallback to original blob
            const url = URL.createObjectURL(blob);
            setAudioData({ blob, url });
          }
        } else {
          const url = URL.createObjectURL(blob);
          console.log("🎧 Recording stopped. Audio size:", blob.size, "bytes");
          setAudioData({ blob, url });
        }
      };

      mediaRecorder.start();
      console.log("⏺️ Recording started.");
      setRecording({ mediaRecorder, stream });
    } catch (err) {
      console.error("❌ Microphone access error:", err);
      alert("Please allow microphone permission to record audio.");
    }
  };

  // Convert WebM/OGG to WAV using Web Audio API
  const convertToWav = async (blob) => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const arrayBuffer = await blob.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    // Convert to WAV
    const wavBlob = audioBufferToWav(audioBuffer);
    return wavBlob;
  };

  // Convert AudioBuffer to WAV Blob
  const audioBufferToWav = (audioBuffer) => {
    const numChannels = 1; // Mono
    const sampleRate = audioBuffer.sampleRate;
    const format = 1; // PCM
    const bitDepth = 16;

    // Get audio data (convert to mono if needed)
    let audioData;
    if (audioBuffer.numberOfChannels === 1) {
      audioData = audioBuffer.getChannelData(0);
    } else {
      // Mix to mono
      const left = audioBuffer.getChannelData(0);
      const right = audioBuffer.getChannelData(1);
      audioData = new Float32Array(left.length);
      for (let i = 0; i < left.length; i++) {
        audioData[i] = (left[i] + right[i]) / 2;
      }
    }

    const dataLength = audioData.length * (bitDepth / 8);
    const buffer = new ArrayBuffer(44 + dataLength);
    const view = new DataView(buffer);

    // Write WAV header
    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    writeString(0, 'RIFF');
    view.setUint32(4, 36 + dataLength, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true); // fmt chunk size
    view.setUint16(20, format, true); // audio format (PCM)
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * numChannels * (bitDepth / 8), true); // byte rate
    view.setUint16(32, numChannels * (bitDepth / 8), true); // block align
    view.setUint16(34, bitDepth, true);
    writeString(36, 'data');
    view.setUint32(40, dataLength, true);

    // Write audio data
    const volume = 0.8;
    let offset = 44;
    for (let i = 0; i < audioData.length; i++) {
      const sample = Math.max(-1, Math.min(1, audioData[i]));
      view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
      offset += 2;
    }

    return new Blob([buffer], { type: 'audio/wav' });
  };

  // Stop recording (clean stop)
  const stopRecording = () => {
    if (recording?.mediaRecorder) {
      recording.mediaRecorder.stop();
      recording.stream.getTracks().forEach((track) => track.stop());
      console.log("🛑 Recording and stream stopped.");
      setRecording(false);
    }
  };

  // Upload + Analyze
  const handleAnalyze = async () => {
    if (!audioData) {
      alert("Please record something first!");
      return;
    }

    const btn = document.getElementById("analyzeBtn");
    btn.innerText = "Analyzing...";
    btn.style.opacity = "0.7";

    try {
      const backendUrl =
        process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:8000";

      const formData = new FormData();
      formData.append("file", audioData.blob, "recording.wav");

      const res = await fetch(`${backendUrl}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Response not OK");

      const result = await res.json();
      localStorage.setItem("emotionResult", JSON.stringify(result));
      onAnalyze?.(result);
    } catch (err) {
      console.error("❌ Error uploading audio:", err);
      alert("Failed to analyze audio. Make sure the backend is running!");
    } finally {
      btn.innerText = "Analyze";
      btn.style.opacity = "1";
    }
  };

  // UI
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
      }}
    >
      <div
        style={{
          maxWidth: "550px",
          width: "100%",
          background: "white",
          borderRadius: "24px",
          padding: "clamp(2.25rem, 4.5vw, 3.25rem) clamp(1.5rem, 3vw, 2.25rem)",
          boxShadow: "0 20px 60px rgba(79, 52, 34, 0.12)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "clamp(1.75rem, 3.5vw, 2.5rem)",
          position: "relative",
          opacity: isLoaded ? 1 : 0,
          transform: isLoaded ? "translateY(0) scale(1)" : "translateY(30px) scale(0.95)",
          transition: "all 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
        }}
      >
        {/* Back Button */}
        <button
          onClick={onBack}
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
        <div
          style={{
            textAlign: "center",
            color: "#4F3422",
            animation: isLoaded ? "fadeInDown 1s ease-out 0.2s both" : "none",
          }}
        >
          <h2
            style={{
              fontWeight: 700,
              fontSize: "clamp(1.375rem, 3.5vw, 1.75rem)",
              marginBottom: "0.75rem",
            }}
          >
            {recording ? "Listening..." : "Tap the Mic to Record"}
          </h2>
          <p
            style={{
              fontSize: "clamp(0.9rem, 1.8vw, 1rem)",
              color: "#6E5844",
              lineHeight: "1.5",
            }}
          >
            Speak your thoughts clearly to analyze your emotion.
          </p>
        </div>

        {/* Mic Button */}
        <div
          onClick={recording ? stopRecording : startRecording}
          style={{
            width: "clamp(110px, 18vw, 160px)",
            height: "clamp(110px, 18vw, 160px)",
            borderRadius: "50%",
            background: recording
              ? "linear-gradient(135deg, #B23A48 0%, #D64456 100%)"
              : "linear-gradient(135deg, #4F3422 0%, #6E4C3A 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            boxShadow: recording
              ? "0 0 35px 10px rgba(178, 58, 72, 0.35)"
              : "0 10px 35px rgba(79, 52, 34, 0.25)",
            transition: "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
            animation: isLoaded ? "fadeInScale 1s ease-out 0.4s both" : "none",
          }}
          onMouseEnter={(e) => {
            if (!recording) {
              e.currentTarget.style.transform = "scale(1.05)";
              e.currentTarget.style.boxShadow = "0 12px 45px rgba(79, 52, 34, 0.35)";
            }
          }}
          onMouseLeave={(e) => {
            if (!recording) {
              e.currentTarget.style.transform = "scale(1)";
              e.currentTarget.style.boxShadow = "0 10px 35px rgba(79, 52, 34, 0.25)";
            }
          }}
        >
          {recording ? (
            <FaStop size={window.innerWidth < 768 ? 36 : 44} color="white" />
          ) : (
            <FaMicrophone size={window.innerWidth < 768 ? 36 : 44} color="white" />
          )}
        </div>

        {/* Playback */}
        {audioData && (
          <div
            style={{
              width: "100%",
              textAlign: "center",
            }}
          >
            <audio
              controls
              src={audioData.url}
              style={{
                width: "100%",
                maxWidth: "400px",
                borderRadius: "12px",
              }}
            />
          </div>
        )}

        {/* Analyze Button */}
        <button
          onClick={handleAnalyze}
          id="analyzeBtn"
          style={{
            width: "100%",
            maxWidth: "280px",
            padding: "clamp(0.875rem, 1.8vw, 1.125rem) clamp(2rem, 3.5vw, 2.75rem)",
            background: "linear-gradient(135deg, #4F3422 0%, #6E4C3A 100%)",
            borderRadius: "1000px",
            border: "none",
            color: "white",
            fontFamily: "Urbanist",
            fontWeight: 800,
            fontSize: "clamp(1rem, 1.8vw, 1.125rem)",
            cursor: "pointer",
            boxShadow: "0px 6px 20px rgba(79, 52, 34, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            transition: "all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
            animation: isLoaded ? "fadeInUp 1s ease-out 0.6s both" : "none",
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
          <span style={{ position: "relative", zIndex: 1 }}>Analyze</span>
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