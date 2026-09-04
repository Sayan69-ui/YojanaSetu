import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, ExternalLink, RefreshCw, ShieldCheck } from 'lucide-react';
import { sendChatMessage } from '../services/api';

export default function ChatBot({ language }) {
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      sender: "bot",
      text: "🙏 **নমস্কার / नमस्ते! Welcome to YojanaSetu (योजनासेतु)**.\n\nI am **AI Sahayak**, your dedicated Citizen Welfare Assistant for Indian Government Schemes.\n\nAsk me anything in **हिन्दी (Hindi), English, Hinglish (रोमन-हिन्दी), or বাংলা (Bengali)** and I will respond in the requested language.\n\n*Examples:*\n- *\"What is Ayushman Bharat PM-JAY?\" (English)*\n- *\"पीएम किसान योजना क्या है और ₹6000 का लाभ कैसे मिलता है?\" (हिन्दी)*\n- *\"Mujhe business ke liye bina guarantee ka loan chahiye, kaise milega?\" (Hinglish)*\n- *\"আমি একজন কৃষক, পিএম কিষাণ প্রকল্পে অনুদান পাওয়ার নিয়ম কি?\" (বাংলা)*",
      sources: [
        { title: "PM-KISAN Portal", url: "https://pmkisan.gov.in" },
        { title: "Ayushman Bharat PMJAY", url: "https://pmjay.gov.in" }
      ]
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const quickPrompts = [
    { label: "🏥 Ayushman Bharat PM-JAY", prompt: "What is Ayushman Bharat PM-JAY?" },
    { label: "🌾 किसान सहायता (हिन्दी)", prompt: "पीएम किसान योजना क्या है और कौन इसके लिए पात्र है?" },
    { label: "💼 Mudra Loan (Hinglish)", prompt: "Mujhe small business ke liye Mudra loan chahiye, eligibility aur documents kya hain?" },
    { label: "🌾 কৃষক সহায়তা (বাংলা)", prompt: "আমি একজন চাষি, পিএম কিষাণ প্রকল্পে ₹৬০০০ অনুদান পাওয়ার নিয়ম কি?" },
    { label: "🏠 PMAY Housing (English)", prompt: "What is Pradhan Mantri Awas Yojana (PMAY) and how can I apply?" },
    { label: "👧 সুকন্যা সমৃদ্ধি (বাংলা)", prompt: "সুকন্যা সমৃদ্ধি যোজনায় সুদের হার এবং সঞ্চয়ের নিয়ম কি?" }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (textToSend) => {
    const query = (textToSend || input).trim();
    if (!query || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      sender: "user",
      text: query
    };

    // Prepare conversation history for follow-up context
    const currentHistory = messages
      .filter((m) => m.id !== "welcome")
      .slice(-8)
      .map((m) => ({
        sender: m.sender,
        text: m.text
      }));

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await sendChatMessage(query, language, currentHistory);
      const botMessage = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: response.reply,
        sources: response.sources || [],
        detected_language: response.detected_language
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: "bot",
          text: "⚠️ Sorry, there was an issue retrieving verified scheme information. Please ensure the backend server is running.",
          sources: []
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Helper to render formatted markdown
  const renderFormattedText = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    return lines.map((line, idx) => {
      let content = line;

      // Header 3
      if (content.startsWith('### ')) {
        return <h3 key={idx} style={{ color: "var(--accent-saffron-light)", margin: "0.6rem 0 0.3rem 0", fontSize: "1.15rem" }}>{content.replace('### ', '')}</h3>;
      }
      // Header 2
      if (content.startsWith('## ')) {
        return <h2 key={idx} style={{ fontSize: "1.25rem", margin: "0.75rem 0 0.35rem 0", color: "var(--text-primary)" }}>{content.replace('## ', '')}</h2>;
      }

      // Bullet point
      const isBullet = content.startsWith('- ') || content.startsWith('* ') || content.startsWith('• ');
      if (isBullet) {
        content = content.replace(/^[-*•]\s+/, '');
      }

      // Render bold tokens and links
      const parts = content.split(/(\*\*.*?\*\*|\[.*?\]\(.*?\))/g);
      const renderedParts = parts.map((part, pIdx) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return <strong key={pIdx} style={{ color: "var(--text-primary)" }}>{part.slice(2, -2)}</strong>;
        }
        const linkMatch = part.match(/\[(.*?)\]\((.*?)\)/);
        if (linkMatch) {
          return (
            <a key={pIdx} href={linkMatch[2]} target="_blank" rel="noopener noreferrer" className="btn-link" style={{ display: "inline" }}>
              {linkMatch[1]} <ExternalLink size={12} style={{ display: "inline", verticalAlign: "middle" }} />
            </a>
          );
        }
        return part;
      });

      if (isBullet) {
        return (
          <li key={idx} style={{ marginLeft: "1.25rem", listStyleType: "disc", margin: "0.25rem 0" }}>
            {renderedParts}
          </li>
        );
      }

      if (!content.trim()) {
        return <div key={idx} style={{ height: "0.5rem" }} />;
      }

      return <p key={idx} style={{ margin: "0.25rem 0" }}>{renderedParts}</p>;
    });
  };

  return (
    <div className="chat-window glass-panel">
      <div className="chat-header">
        <div className="chat-header-info">
          <div className="status-dot" />
          <div>
            <h2 style={{ fontSize: "1.05rem", display: "flex", alignItems: "center", gap: "0.4rem" }}>
              YojanaSetu — AI Sahayak
              <ShieldCheck size={16} style={{ color: "var(--accent-emerald)" }} />
            </h2>
            <span style={{ fontSize: "0.78rem", color: "var(--text-secondary)" }}>
              Verified Knowledge Base • 10 Government Schemes • Grounded RAG
            </span>
          </div>
        </div>

        <button
          className="btn-secondary"
          onClick={() => setMessages([messages[0]])}
          title="Restart Conversation"
        >
          <RefreshCw size={14} />
          Clear
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((m) => (
          <div key={m.id} className={`chat-bubble ${m.sender}`}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.4rem", opacity: 0.85 }}>
              {m.sender === "bot" ? <Bot size={16} /> : <User size={16} />}
              <span style={{ fontSize: "0.75rem", fontWeight: 700, textTransform: "uppercase" }}>
                {m.sender === "bot" ? "AI Sahayak" : "Citizen"}
              </span>
            </div>

            <div>{renderFormattedText(m.text)}</div>

            {m.sources && m.sources.length > 0 && (
              <div className="source-tags-box">
                <span style={{ fontSize: "0.72rem", color: "var(--text-muted)", fontWeight: 600 }}>
                  OFFICIAL CITATIONS:
                </span>
                {m.sources.map((src, sIdx) => (
                  <a
                    key={sIdx}
                    href={src.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="source-badge"
                  >
                    <ExternalLink size={12} />
                    {src.title}
                  </a>
                ))}
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="chat-bubble bot" style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
            <Sparkles size={16} style={{ color: "var(--accent-saffron-light)", animation: "spin 2s linear infinite" }} />
            <span style={{ fontSize: "0.88rem", color: "var(--text-secondary)" }}>
              Retrieving verified government guidelines & formulating response...
            </span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="quick-chips-bar">
        {quickPrompts.map((item, i) => (
          <button
            key={i}
            className="quick-chip"
            onClick={() => handleSend(item.prompt)}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="chat-input-bar">
        <input
          type="text"
          placeholder="Ask in Hindi, English, Hinglish, or বাংলা (e.g. What is PM-JAY? / मुझे लोन चाहिए)..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <button
          className="btn-send"
          onClick={() => handleSend()}
          disabled={!input.trim() || isLoading}
          title="Send query"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}
