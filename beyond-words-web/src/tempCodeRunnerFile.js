import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(<App />);

import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import Page1 from "./pages/page1";
import Page2 from "./pages/page2";
import Page3 from "./pages/page3";
import Page4 from "./pages/page4";
import Page5 from "./pages/page5";
import Page6 from "./pages/page6";
import Page7 from "./pages/page7";
import Page8 from "./pages/page8";

function Page1Wrapper() {
  const navigate = useNavigate();
  return <Page1 onSignIn={() => navigate("/page2")} />;
}

export default function beyond-words-web() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Page1Wrapper />} />
        <Route path="/page2" element={<Page2 />} />
        <Route path="/page3" element={<Page3 />} />
        <Route path="/page4" element={<Page4 />} />
        <Route path="/page5" element={<Page5 />} />
        <Route path="/page6" element={<Page6 />} />
        <Route path="/page8" element={<Page8 />} />
        <Route path="/page9" element={<Page9 />} />
      </Routes>
    </Router>
  );
}
