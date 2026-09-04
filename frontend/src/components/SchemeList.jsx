import React, { useState, useEffect } from 'react';
import { Search, Filter, ExternalLink, ArrowRight, CheckCircle, Eye } from 'lucide-react';
import { fetchSchemes, fetchCategories } from '../services/api';
import SchemeModal from './SchemeModal';

export default function SchemeList({ onCheckEligibility }) {
  const [schemes, setSchemes] = useState([]);
  const [categories, setCategories] = useState(["All"]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [activeModalScheme, setActiveModalScheme] = useState(null);

  useEffect(() => {
    async function loadInitial() {
      setLoading(true);
      const [cats, scs] = await Promise.all([
        fetchCategories(),
        fetchSchemes("All", "")
      ]);
      setCategories(cats);
      setSchemes(scs);
      setLoading(false);
    }
    loadInitial();
  }, []);

  const handleFilter = async (cat, search) => {
    setLoading(true);
    const data = await fetchSchemes(cat, search);
    setSchemes(data);
    setLoading(false);
  };

  const onCategoryClick = (cat) => {
    setSelectedCategory(cat);
    handleFilter(cat, searchQuery);
  };

  const onSearchChange = (e) => {
    const val = e.target.value;
    setSearchQuery(val);
    handleFilter(selectedCategory, val);
  };

  return (
    <div>
      <div className="catalog-controls">
        <div className="search-input-box">
          <Search size={20} style={{ color: "var(--accent-saffron-light)" }} />
          <input
            type="text"
            placeholder="Search schemes by name, keyword (e.g. Kisan, loan, hospital, housing, Beti)..."
            value={searchQuery}
            onChange={onSearchChange}
          />
          {searchQuery && (
            <button
              className="btn-secondary"
              style={{ padding: "0.25rem 0.75rem", fontSize: "0.75rem" }}
              onClick={() => {
                setSearchQuery("");
                handleFilter(selectedCategory, "");
              }}
            >
              Clear
            </button>
          )}
        </div>

        <div className="category-pills">
          {categories.map((cat) => (
            <button
              key={cat}
              className={`category-pill ${selectedCategory === cat ? "active" : ""}`}
              onClick={() => onCategoryClick(cat)}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: "center", padding: "4rem 0", color: "var(--text-secondary)" }}>
          Loading official schemes repository...
        </div>
      ) : schemes.length === 0 ? (
        <div className="glass-panel" style={{ textAlign: "center", padding: "3rem", margin: "2rem auto", maxWidth: "600px" }}>
          <h3 style={{ marginBottom: "0.5rem" }}>No matching schemes found</h3>
          <p style={{ color: "var(--text-secondary)", fontSize: "0.95rem" }}>
            Try adjusting your search terms or clearing category filters.
          </p>
        </div>
      ) : (
        <div className="schemes-grid">
          {schemes.map((scheme) => (
            <div key={scheme.id} className="scheme-card">
              <div className="card-top">
                <span className="category-badge">{scheme.category}</span>
                <h3 className="scheme-card-title">{scheme.name}</h3>
                <div className="scheme-card-sub">
                  {scheme.name_hi} {scheme.name_bn && `• ${scheme.name_bn}`}
                </div>
                <p className="scheme-card-brief">{scheme.brief}</p>

                <ul className="card-benefits-list">
                  {scheme.benefits?.slice(0, 2).map((b, i) => (
                    <li key={i}>
                      <CheckCircle size={14} style={{ color: "var(--accent-emerald)", flexShrink: 0, marginTop: "2px" }} />
                      <span>{b}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="card-footer">
                <button
                  className="btn-secondary"
                  onClick={() => setActiveModalScheme(scheme)}
                >
                  <Eye size={14} />
                  Details
                </button>

                <a
                  href={scheme.official_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-link"
                >
                  Apply Official <ExternalLink size={13} />
                </a>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeModalScheme && (
        <SchemeModal
          scheme={activeModalScheme}
          onClose={() => setActiveModalScheme(null)}
          onCheckEligibility={onCheckEligibility}
        />
      )}
    </div>
  );
}
