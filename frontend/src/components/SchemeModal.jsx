import React from 'react';
import { X, ExternalLink, CheckCircle2, FileText, Phone, Building2, Users } from 'lucide-react';

export default function SchemeModal({ scheme, onClose, onCheckEligibility }) {
  if (!scheme) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <span className="category-badge">{scheme.category}</span>
            <h2 style={{ fontSize: "1.45rem", marginBottom: "0.25rem" }}>{scheme.name}</h2>
            <div style={{ color: "var(--accent-saffron-light)", fontSize: "0.95rem" }}>
              {scheme.name_hi} {scheme.name_bn && `• ${scheme.name_bn}`}
            </div>
          </div>
          <button className="btn-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
          <div style={{ display: "flex", gap: "1.5rem", flexWrap: "wrap", background: "var(--bg-secondary)", padding: "0.85rem 1rem", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.85rem", color: "var(--text-secondary)" }}>
              <Building2 size={16} style={{ color: "var(--accent-saffron-light)" }} />
              <span>{scheme.ministry}</span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.85rem", color: "var(--text-secondary)" }}>
              <Users size={16} style={{ color: "var(--accent-emerald)" }} />
              <span>{scheme.target_audience}</span>
            </div>
          </div>

          <div>
            <h4 style={{ fontSize: "1rem", marginBottom: "0.5rem", color: "var(--text-primary)" }}>
              Scheme Overview
            </h4>
            <p style={{ fontSize: "0.92rem", color: "var(--text-secondary)", lineHeight: 1.6 }}>
              {scheme.brief}
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: "1rem", marginBottom: "0.5rem", color: "var(--text-primary)" }}>
              Key Benefits & Financial Assistance
            </h4>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.4rem" }}>
              {scheme.benefits?.map((b, i) => (
                <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: "0.5rem", fontSize: "0.88rem" }}>
                  <CheckCircle2 size={16} style={{ color: "var(--accent-emerald)", flexShrink: 0, marginTop: "2px" }} />
                  <span>{b}</span>
                </div>
              ))}
            </div>
          </div>

          {scheme.eligibility_rules && (
            <div style={{ background: "rgba(255, 140, 0, 0.05)", border: "1px solid rgba(255, 140, 0, 0.2)", padding: "1rem", borderRadius: "var(--radius-md)" }}>
              <h4 style={{ fontSize: "0.95rem", color: "var(--accent-saffron-light)", marginBottom: "0.4rem" }}>
                Eligibility Rules & Criteria
              </h4>
              <p style={{ fontSize: "0.88rem", color: "var(--text-primary)", lineHeight: 1.5 }}>
                {scheme.eligibility_rules.special_conditions}
              </p>
            </div>
          )}

          <div>
            <h4 style={{ fontSize: "1rem", marginBottom: "0.5rem", color: "var(--text-primary)", display: "flex", alignItems: "center", gap: "0.4rem" }}>
              <FileText size={16} style={{ color: "var(--accent-blue)" }} />
              Mandatory Documents Required
            </h4>
            <ul style={{ paddingLeft: "1.25rem", fontSize: "0.88rem", color: "var(--text-secondary)" }}>
              {scheme.documents_required?.map((doc, idx) => (
                <li key={idx} style={{ marginBottom: "0.25rem" }}>{doc}</li>
              ))}
            </ul>
          </div>

          {scheme.helpline && (
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.85rem", color: "var(--text-secondary)" }}>
              <Phone size={15} style={{ color: "var(--accent-emerald)" }} />
              <span>Official Helpline: <strong>{scheme.helpline}</strong></span>
            </div>
          )}

          <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
            <a
              href={scheme.official_url}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary"
              style={{ textDecoration: "none", flex: 1 }}
            >
              <ExternalLink size={18} />
              Visit Official Portal
            </a>
            <button
              className="btn-secondary"
              onClick={() => {
                onClose();
                onCheckEligibility(scheme);
              }}
            >
              Check My Eligibility
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
