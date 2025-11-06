import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";
import ErrorBoundary from "./components/ErrorBoundary";

// ==== IMPORT ALL PAGES ====
import Page1 from "./pages/page1";
import Page2 from "./pages/page2";
import Page3 from "./pages/page3";
import Page4 from "./pages/page4";
import Page5 from "./pages/page5";
import Page6 from "./pages/page6";
import Page7 from "./pages/page7";
import Page8 from "./pages/page8";
import Page9 from "./pages/page9";
import Page10 from "./pages/page10";

// ==== WRAPPERS (for page-to-page navigation props) ====

function Page1Wrapper() {
  const navigate = useNavigate();
  return <Page1 onSignIn={() => navigate("/page2")} />;
}

function Page2Wrapper() {
  const navigate = useNavigate();
  return <Page2 onNext={() => navigate("/page3")} />;
}

function Page3Wrapper() {
  const navigate = useNavigate();
  return <Page3 onNext={() => navigate("/page4")} />;
}

function Page4Wrapper() {
  const navigate = useNavigate();
  return <Page4 onNext={() => navigate("/page5")} />;
}

function Page5Wrapper() {
  const navigate = useNavigate();
  return <Page5 onNext={() => navigate("/page6")} />;
}
function Page6Wrapper() {
  const navigate = useNavigate();
  return (
    <Page6
      onAnalyze={() => navigate("/page8")} // Go to result page
      onBack={() => navigate("/page4")} // Go back if needed
    />
  );
}

function Page7Wrapper() {
  const navigate = useNavigate();
  return <Page7 onNext={() => navigate("/page8")} />;
}

function Page8Wrapper() {
  const navigate = useNavigate();
  return <Page8 onNext={() => navigate("/page9")} />;
}

function Page9Wrapper() {
  const navigate = useNavigate();
  return <Page9 onNext={() => navigate("/page10")} />;
}

function Page10Wrapper() {
  const navigate = useNavigate();
  return <Page10 onRestart={() => navigate("/")} />;
}

// ==== MAIN APP COMPONENT ====

export default function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Routes>
          <Route path="/" element={<Page1Wrapper />} />
          <Route path="/page2" element={<Page2Wrapper />} />
          <Route path="/page3" element={<Page3Wrapper />} />
          <Route path="/page4" element={<Page4Wrapper />} />
          <Route path="/page5" element={<Page5Wrapper />} />
          <Route path="/page6" element={<Page6Wrapper />} />
          <Route path="/page7" element={<Page7Wrapper />} />
          <Route path="/page8" element={<Page8Wrapper />} />
          <Route path="/page9" element={<Page9Wrapper />} />
          <Route path="/page10" element={<Page10Wrapper />} />
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}
