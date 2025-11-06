// src/components/PhoneFrame.jsx
import React, { useEffect, useState } from 'react';
import './PhoneFrame.css'; // small styles file below

/**
 * Props:
 *  - width: design width (default 404)
 *  - height: design height (default 814)
 *  - children: the page JSX (your Figma export)
 */
export default function PhoneFrame({ width = 404, height = 814, children, withShell = true }) {
  const [scale, setScale] = useState(1);

  useEffect(() => {
    function update() {
      const padding = 80; // space around the phone
      const availableW = window.innerWidth - padding;
      const availableH = window.innerHeight - padding;
      const sx = availableW / width;
      const sy = availableH / height;
      const s = Math.min(sx, sy, 1); // do not upscale beyond 1
      setScale(s);
    }
    update();
    window.addEventListener('resize', update);
    return () => window.removeEventListener('resize', update);
  }, [width, height]);

  return (
    <div className="app-center">
      <div className={withShell ? 'phone-shell' : ''} style={{ transform: `scale(${scale})`, transformOrigin: 'top left' }}>
        <div style={{ width, height, position: 'relative' }}>
          {children}
        </div>
      </div>
    </div>
  );
}

