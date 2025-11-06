import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            width: "100vw",
            height: "100vh",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "#F7F4F2",
            fontFamily: "Urbanist, sans-serif",
            padding: "20px",
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontSize: 80,
              marginBottom: 20,
            }}
          >
            😔
          </div>
          <h1
            style={{
              fontSize: 28,
              fontWeight: 800,
              color: "#4F3422",
              marginBottom: 15,
            }}
          >
            Oops! Something went wrong
          </h1>
          <p
            style={{
              fontSize: 16,
              color: "#6E5844",
              marginBottom: 30,
              maxWidth: 400,
            }}
          >
            We're sorry for the inconvenience. Please try refreshing the page or
            go back to the home screen.
          </p>
          <div style={{ display: "flex", gap: 15 }}>
            <button
              onClick={() => window.location.reload()}
              style={{
                padding: "14px 28px",
                borderRadius: 30,
                border: "none",
                background: "#4F3422",
                color: "white",
                fontSize: 16,
                fontWeight: 700,
                cursor: "pointer",
                boxShadow: "0 3px 8px rgba(0,0,0,0.15)",
              }}
            >
              Refresh Page
            </button>
            <button
              onClick={() => (window.location.href = "/")}
              style={{
                padding: "14px 28px",
                borderRadius: 30,
                border: "2px solid #4F3422",
                background: "transparent",
                color: "#4F3422",
                fontSize: 16,
                fontWeight: 700,
                cursor: "pointer",
              }}
            >
              Go Home
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
