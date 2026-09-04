import React, { useState } from 'react';
import { CheckCircle2, AlertCircle, ArrowRight, ExternalLink, Sparkles, UserCheck } from 'lucide-react';
import { checkEligibility } from '../services/api';

export default function EligibilityWizard() {
  const [profile, setProfile] = useState({
    age: 25,
    gender: "male",
    occupation: "farmer",
    annual_income: 180000,
    has_girl_child_under_10: false,
    owns_pucca_house: false,
    owns_agricultural_land: true
  });

  const [results, setResults] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsEvaluating(true);
    try {
      const res = await checkEligibility(profile);
      setResults(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsEvaluating(false);
    }
  };

  return (
    <div className="wizard-card glass-panel">
      <div style={{ textAlign: "center", marginBottom: "2rem" }}>
        <div className="hero-pill">
          <UserCheck size={15} />
          Instant AI Eligibility Matcher
        </div>
        <h2 style={{ fontSize: "1.85rem", marginBottom: "0.5rem" }}>
          Am I Eligible? (पात्रता कैलकुलेटर)
        </h2>
        <p style={{ color: "var(--text-secondary)", fontSize: "0.95rem" }}>
          Provide basic details to find out exactly which of the 10 Central Government welfare schemes you qualify for.
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="form-group">
            <label>Age (उम्र)</label>
            <input
              type="number"
              min="0"
              max="110"
              value={profile.age}
              onChange={(e) => setProfile({ ...profile, age: parseInt(e.target.value) || 0 })}
              required
            />
          </div>

          <div className="form-group">
            <label>Gender (लिंग)</label>
            <select
              value={profile.gender}
              onChange={(e) => setProfile({ ...profile, gender: e.target.value })}
            >
              <option value="male">Male (पुरुष)</option>
              <option value="female">Female (महिला)</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label>Primary Occupation / Category (व्यवसाय / वर्ग)</label>
            <select
              value={profile.occupation}
              onChange={(e) => setProfile({ ...profile, occupation: e.target.value })}
            >
              <option value="farmer">Farmer / Agriculture (किसान)</option>
              <option value="student">Student (छात्र/छात्रा)</option>
              <option value="artisan">Artisan / Craftsperson (विश्वकर्मा / कारीगर)</option>
              <option value="street_vendor">Street Vendor / Hawker (रेहड़ी-पटरी विक्रेता)</option>
              <option value="unorganized_worker">Daily Wager / Unorganized Worker (मजदूर)</option>
              <option value="entrepreneur">Micro Business / Entrepreneur (व्यापारी)</option>
              <option value="unemployed">Unemployed / Job Seeker</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label>Total Annual Family Income (वार्षिक पारिवारिक आय ₹)</label>
            <input
              type="number"
              min="0"
              step="10000"
              value={profile.annual_income}
              onChange={(e) => setProfile({ ...profile, annual_income: parseFloat(e.target.value) || 0 })}
              required
            />
          </div>

          <div className="checkbox-group">
            <span style={{ fontSize: "0.85rem", color: "var(--accent-saffron-light)", fontWeight: 700 }}>
              Additional Family & Asset Details:
            </span>

            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={profile.owns_agricultural_land}
                onChange={(e) => setProfile({ ...profile, owns_agricultural_land: e.target.checked })}
              />
              Family owns cultivable agricultural land (कृषि भूमि स्वामी)
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={profile.has_girl_child_under_10}
                onChange={(e) => setProfile({ ...profile, has_girl_child_under_10: e.target.checked })}
              />
              Have a girl child aged 10 years or younger (10 वर्ष से कम आयु की बेटी)
            </label>

            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={profile.owns_pucca_house}
                onChange={(e) => setProfile({ ...profile, owns_pucca_house: e.target.checked })}
              />
              Already own a permanent pucca house anywhere in India (पक्का मकान)
            </label>
          </div>
        </div>

        <button type="submit" className="btn-primary" disabled={isEvaluating}>
          <Sparkles size={18} />
          {isEvaluating ? "Evaluating Criteria..." : "Check My Eligible Schemes Now"}
        </button>
      </form>

      {results && (
        <div className="results-box">
          <div className="results-header">
            <div>
              <h3 style={{ fontSize: "1.3rem" }}>Eligibility Evaluation Results</h3>
              <p style={{ fontSize: "0.88rem", color: "var(--text-secondary)" }}>
                Based on current central government guidelines
              </p>
            </div>
            <div className="match-count-badge">
              {results.eligible_schemes_count} Qualified Schemes
            </div>
          </div>

          {results.eligible_schemes_count === 0 ? (
            <div style={{ textAlign: "center", padding: "2rem 0", color: "var(--text-secondary)" }}>
              No direct matches found for this specific profile. Try verifying family income or trade status.
            </div>
          ) : (
            results.eligible_schemes.map((scheme) => (
              <div key={scheme.id} className="match-card">
                <div className="match-card-title">
                  <span>{scheme.name}</span>
                  <a
                    href={scheme.official_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-link"
                    style={{ fontSize: "0.82rem" }}
                  >
                    Apply Now <ExternalLink size={13} />
                  </a>
                </div>

                <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", margin: "0.4rem 0" }}>
                  {scheme.brief}
                </div>

                <div style={{ marginTop: "0.6rem" }}>
                  <span style={{ fontSize: "0.78rem", fontWeight: 700, color: "var(--accent-emerald)" }}>
                    WHY YOU QUALIFY:
                  </span>
                  <ul style={{ paddingLeft: "1.2rem", fontSize: "0.85rem", marginTop: "0.2rem" }}>
                    {scheme.reasons.map((r, i) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                </div>

                {scheme.documents_required && scheme.documents_required.length > 0 && (
                  <div style={{ marginTop: "0.6rem", fontSize: "0.8rem", color: "var(--text-muted)" }}>
                    <strong>Required Documents:</strong> {scheme.documents_required.join(", ")}
                  </div>
                )}
              </div>
            ))
          )}

          {results.potential_schemes && results.potential_schemes.length > 0 && (
            <div style={{ marginTop: "1.5rem" }}>
              <h4 style={{ fontSize: "1rem", color: "var(--accent-saffron-light)", marginBottom: "0.75rem", display: "flex", alignItems: "center", gap: "0.4rem" }}>
                <AlertCircle size={16} />
                Potential Schemes (Subject to Additional Conditions):
              </h4>
              {results.potential_schemes.map((s) => (
                <div key={s.id} style={{ background: "rgba(255, 140, 0, 0.04)", border: "1px solid rgba(255, 140, 0, 0.2)", borderRadius: "var(--radius-md)", padding: "0.85rem 1.15rem", marginBottom: "0.75rem" }}>
                  <div style={{ fontWeight: 600, fontSize: "0.95rem" }}>{s.name}</div>
                  <div style={{ fontSize: "0.84rem", color: "var(--text-secondary)", marginTop: "0.25rem" }}>
                    {s.reasons.join(" • ")}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
