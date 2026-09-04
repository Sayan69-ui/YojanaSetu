import React from 'react';
import { MessageSquare, Layers, CheckCircle2, Globe } from 'lucide-react';
import logoImg from '../assets/yojanasetu-logo.png';

export default function Navbar({ activeTab, setActiveTab, language, setLanguage }) {
  // STRICTLY only 4 supported languages + Auto
  const languages = [
    { code: "auto", label: "Auto (স্বয়ংক্রিয় / स्वचालित)" },
    { code: "hi", label: "हिन्दी (Hindi)" },
    { code: "en", label: "English" },
    { code: "hinglish", label: "Hinglish (रोमन-हिन्दी)" },
    { code: "bn", label: "বাংলা (Bengali)" }
  ];

  return (
    <header className="navbar">
      <div className="nav-brand" onClick={() => setActiveTab("chat")} title="YojanaSetu Home">
        <div className="brand-icon-box" style={{ background: "#ffffff", padding: "4px", overflow: "hidden" }}>
          <img src={logoImg} alt="YojanaSetu Logo" style={{ width: "100%", height: "100%", objectFit: "contain" }} />
        </div>
        <div>
          <div className="brand-title">
            YojanaSetu
            <span className="brand-badge">Gov AI</span>
          </div>
          <div className="brand-subtitle">योजनासेतु • Citizen Welfare Assistant</div>
        </div>
      </div>

      <nav className="nav-tabs">
        <button
          className={`nav-tab-btn ${activeTab === "chat" ? "active" : ""}`}
          onClick={() => setActiveTab("chat")}
        >
          <MessageSquare size={17} />
          AI Sahayak
        </button>
        <button
          className={`nav-tab-btn ${activeTab === "schemes" ? "active" : ""}`}
          onClick={() => setActiveTab("schemes")}
        >
          <Layers size={17} />
          All Schemes
        </button>
        <button
          className={`nav-tab-btn ${activeTab === "eligible" ? "active" : ""}`}
          onClick={() => setActiveTab("eligible")}
        >
          <CheckCircle2 size={17} />
          Am I Eligible?
        </button>
      </nav>

      <div className="nav-right">
        <div className="lang-selector-box">
          <Globe size={16} style={{ color: "var(--accent-saffron-light)" }} />
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            {languages.map((l) => (
              <option key={l.code} value={l.code}>
                {l.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </header>
  );
}
