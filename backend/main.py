"""
YojanaSetu - Backend Server (FastAPI)
Provides REST endpoints for:
- Multilingual RAG Chatbot (/api/chat) with Conversation History & Strict 4-Language Support
- Scheme Catalog & Search (/api/schemes)
- "Am I Eligible?" Evaluation (/api/check-eligibility)
- Supported Languages (/api/languages) - Strictly Hindi, English, Hinglish, Bengali
"""

import os
import json
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

from rag_engine import RAGEngine
from eligibility import EligibilityEngine

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "schemes.json"
DOCS_PATH = BASE_DIR / "scheme_documents"

app = FastAPI(
    title="YojanaSetu API",
    description="Multilingual AI-powered Indian Welfare Scheme Discovery and Eligibility Assistant",
    version="1.1.0"
)

# Enable CORS for local development and demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
rag_engine = RAGEngine(documents_dir=str(DOCS_PATH), schemes_json_path=str(DATA_PATH))
eligibility_engine = EligibilityEngine(schemes_json_path=str(DATA_PATH))

# In-memory schemes list
with open(DATA_PATH, "r", encoding="utf-8") as f:
    SCHEMES_LIST = json.load(f)


# --- Pydantic Models ---

class ChatMessage(BaseModel):
    sender: str
    text: str

class ChatRequest(BaseModel):
    message: str = Field(..., example="What is Ayushman Bharat PM-JAY?")
    language: Optional[str] = Field("auto", example="en")
    history: Optional[List[ChatMessage]] = Field(default_factory=list)

class ChatResponse(BaseModel):
    reply: str
    sources: List[Dict[str, str]]
    detected_language: str

class EligibilityProfile(BaseModel):
    age: int = Field(25, ge=0, le=120)
    gender: str = Field("male", example="female")
    occupation: str = Field("farmer", example="student")
    annual_income: float = Field(150000.0, ge=0)
    category: Optional[str] = "General"
    has_girl_child_under_10: Optional[bool] = False
    owns_pucca_house: Optional[bool] = False
    owns_agricultural_land: Optional[bool] = False


# --- Endpoints ---

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "YojanaSetu Citizen Welfare Assistant",
        "version": "1.1.0",
        "supported_languages": ["hi", "en", "hinglish", "bn"],
        "total_schemes_loaded": len(SCHEMES_LIST),
        "docs_url": "/docs"
    }


@app.get("/api/schemes")
def get_schemes(
    category: Optional[str] = Query(None, description="Filter schemes by category (e.g. Farmers, Health)"),
    search: Optional[str] = Query(None, description="Search keyword in scheme title, Hindi/Bengali names, or brief")
):
    """Retrieve all schemes with optional category filtering and keyword search."""
    results = SCHEMES_LIST

    if category and category.lower() != "all":
        results = [s for s in results if s.get("category", "").lower() == category.lower()]

    if search and search.strip():
        q = search.lower().strip()
        results = [
            s for s in results
            if q in s["name"].lower()
            or q in s.get("name_hi", "").lower()
            or q in s.get("name_bn", "").lower()
            or q in s.get("brief", "").lower()
            or q in s.get("category", "").lower()
            or any(q in b.lower() for b in s.get("benefits", []))
        ]

    return {
        "count": len(results),
        "schemes": results
    }


@app.get("/api/schemes/{scheme_id}")
def get_scheme_by_id(scheme_id: str):
    """Retrieve detailed information for a specific scheme."""
    for s in SCHEMES_LIST:
        if s["id"] == scheme_id:
            return s
    raise HTTPException(status_code=404, detail="Scheme not found")


@app.get("/api/categories")
def get_categories():
    """List unique scheme categories for filtering pills."""
    categories = sorted(list(set(s.get("category", "General") for s in SCHEMES_LIST)))
    return {"categories": ["All"] + categories}


@app.post("/api/chat", response_model=ChatResponse)
def chat_with_yojanasetu(payload: ChatRequest):
    """
    RAG-powered multilingual chat endpoint with conversation history.
    Strictly answers in requested language: Hindi, English, Hinglish, or Bengali.
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")

    history_list = [item.model_dump() for item in payload.history] if payload.history else []

    result = rag_engine.ask(
        query=payload.message,
        selected_language=payload.language,
        history=history_list
    )
    return ChatResponse(
        reply=result["reply"],
        sources=result["sources"],
        detected_language=result["detected_language"]
    )


@app.post("/api/check-eligibility")
def check_citizen_eligibility(profile: EligibilityProfile):
    """
    Evaluates citizen demographics and returns a list of qualifying schemes.
    """
    result = eligibility_engine.evaluate(profile.model_dump())
    return result


@app.get("/api/languages")
def get_supported_languages():
    """
    Returns available language options: ONLY Hindi, English, Hinglish, and Bengali.
    Tamil and Telugu are strictly excluded.
    """
    return {
        "languages": [
            {"code": "auto", "label": "Auto (স্বয়ংক্রিয় / स्वचालित)"},
            {"code": "hi", "label": "हिन्दी (Hindi)"},
            {"code": "en", "label": "English"},
            {"code": "hinglish", "label": "Hinglish (रोमन-हिन्दी)"},
            {"code": "bn", "label": "বাংলা (Bengali)"}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
