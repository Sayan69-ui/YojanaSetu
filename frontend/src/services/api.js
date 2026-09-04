/**
 * YojanaSetu API Client
 * Centralized API integration module for the frontend.
 */

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function fetchSchemes(category = "All", search = "") {
  try {
    const params = new URLSearchParams();
    if (category && category !== "All") params.append("category", category);
    if (search && search.trim()) params.append("search", search.trim());
    
    const res = await fetch(`${API_BASE}/api/schemes?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    const data = await res.json();
    return data.schemes || [];
  } catch (err) {
    console.warn("[API] fetchSchemes warning:", err.message);
    return [];
  }
}

export async function fetchSchemeDetails(schemeId) {
  try {
    const res = await fetch(`${API_BASE}/api/schemes/${schemeId}`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("[API] fetchSchemeDetails error:", err);
    throw err;
  }
}

export async function sendChatMessage(message, language = "auto", history = []) {
  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, language, history })
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("[API] sendChatMessage error:", err);
    return {
      reply: "We are currently having trouble connecting to the YojanaSetu intelligence server. Please ensure the backend is running at http://localhost:8000.",
      sources: [],
      detected_language: "en"
    };
  }
}

export async function checkEligibility(profile) {
  try {
    const res = await fetch(`${API_BASE}/api/check-eligibility`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(profile)
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("[API] checkEligibility error:", err);
    return {
      eligible_schemes_count: 0,
      eligible_schemes: [],
      potential_schemes_count: 0,
      potential_schemes: []
    };
  }
}

export async function fetchCategories() {
  try {
    const res = await fetch(`${API_BASE}/api/categories`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    const data = await res.json();
    return data.categories || ["All"];
  } catch (err) {
    return ["All", "Farmers", "Health", "Housing", "Business & Employment", "Women & Child", "Pension & Social Security", "Students & Education"];
  }
}
