import React, { useState } from 'react';
import Navbar from './components/Navbar';
import ChatBot from './components/ChatBot';
import SchemeList from './components/SchemeList';
import EligibilityWizard from './components/EligibilityWizard';
import SplashScreen from './components/SplashScreen';
import { Sparkles, ShieldCheck, HeartHandshake, Award } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState("chat");
  const [language, setLanguage] = useState("auto");
  const [showSplash, setShowSplash] = useState(true);

  return (
    <div className="app-layout">
      {showSplash && <SplashScreen onFinish={() => setShowSplash(false)} />}

      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        language={language}
        setLanguage={setLanguage}
      />

      <main className="app-container">
        {activeTab === "chat" && (
          <section className="hero-banner">
            <div className="hero-pill">
              <Sparkles size={14} />
              AI Powered Citizen Welfare Bridge
            </div>
            <h1 className="hero-title">
              Yojana<span className="hero-title-highlight">Setu</span> (योजनासेतु)
            </h1>
            <p className="hero-desc">
              Your multilingual conversational guide to Indian Government welfare schemes.
              Get grounded answers, discover eligible financial subsidies, and access official application portals.
            </p>

            <div style={{ display: "flex", justifyContent: "center", gap: "2rem", marginTop: "1.5rem", flexWrap: "wrap" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.85rem", color: "var(--text-secondary)" }}>
                <ShieldCheck size={16} style={{ color: "var(--accent-emerald)" }} />
                <span>100% Grounded in Official Portals</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.85rem", color: "var(--text-secondary)" }}>
                <HeartHandshake size={16} style={{ color: "var(--accent-saffron-light)" }} />
                <span>Multilingual (Hindi, English & Regional)</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.85rem", color: "var(--text-secondary)" }}>
                <Award size={16} style={{ color: "var(--accent-blue)" }} />
                <span>Instant Eligibility Calculator</span>
              </div>
            </div>
          </section>
        )}

        {activeTab === "chat" && <ChatBot language={language} />}
        
        {activeTab === "schemes" && (
          <div>
            <div style={{ marginBottom: "2rem", textAlign: "center" }}>
              <h2 style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>
                Explore Central Government Schemes (कल्याणकारी योजनाएं)
              </h2>
              <p style={{ color: "var(--text-secondary)", maxWidth: "680px", margin: "0 auto" }}>
                Browse comprehensive guidelines, financial assistance amounts, and direct application links for 10 flagship initiatives.
              </p>
            </div>
            <SchemeList onCheckEligibility={() => setActiveTab("eligible")} />
          </div>
        )}

        {activeTab === "eligible" && <EligibilityWizard />}
      </main>

      <footer style={{ borderTop: "1px solid var(--border-color)", padding: "2rem", textAlign: "center", color: "var(--text-muted)", fontSize: "0.85rem" }}>
        <p>
          🇮🇳 <strong>YojanaSetu</strong> — Built for civic empowerment.
          All scheme information is retrieved and cited directly from official <code style={{ color: "var(--accent-saffron-light)" }}>.gov.in</code> repositories.
        </p>
      </footer>
    </div>
  );
}
