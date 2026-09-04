import React, { useState, useEffect } from 'react';
import logoImg from '../assets/yojanasetu-logo.png';

export default function SplashScreen({ onFinish }) {
  const [fadingOut, setFadingOut] = useState(false);

  useEffect(() => {
    // Start fade out at ~3.6s so transition is complete by 4.0s
    const fadeTimer = setTimeout(() => {
      setFadingOut(true);
    }, 3600);

    // Completely finish and unmount at 4.0s
    const finishTimer = setTimeout(() => {
      if (onFinish) onFinish();
    }, 4000);

    return () => {
      clearTimeout(fadeTimer);
      clearTimeout(finishTimer);
    };
  }, [onFinish]);

  return (
    <div 
      className={`splash-overlay ${fadingOut ? 'splash-fade-out' : ''}`}
      aria-label="YojanaSetu Loading Screen"
      role="status"
    >
      {/* Background ambient lighting */}
      <div className="splash-ambient-glow" />
      <div className="splash-grid-pattern" />

      <div className="splash-content">
        {/* Official Logo Container */}
        <div className="splash-logo-wrapper">
          <div className="splash-logo-card">
            <img
              src={logoImg}
              alt="YojanaSetu Logo"
              className="splash-logo-image"
            />
          </div>
        </div>

        {/* Website / Brand Name */}
        <h1 className="splash-title">
          Yojana<span className="splash-title-accent">Setu</span>
        </h1>

        {/* Brand Subtitle */}
        <p className="splash-subtitle">Citizen Welfare Assistant</p>

        {/* Official Hindi Tagline */}
        <p className="splash-tagline">सरकारी योजनाएँ, अब आसान भाषा में।</p>

        {/* Animated Progress Line */}
        <div className="splash-progress-track">
          <div className="splash-progress-fill" />
        </div>

        {/* Subtle Status Note */}
        <p className="splash-status-text">Connecting you to the right scheme...</p>
      </div>
    </div>
  );
}
