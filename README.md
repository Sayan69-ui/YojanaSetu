# 🇮🇳 YojanaSetu (योजनासेतु)
### Multilingual AI-Powered Citizen Welfare Scheme Discovery & Eligibility Assistant

**YojanaSetu** is an AI assistant built for Indian citizens to bridge the gap between complex government welfare schemes and the people who need them most. Built within an 8-hour hackathon, it features grounded retrieval (RAG), native multilingual support, an instant eligibility calculator, and verified citations directly to official government portals.

---

## 🌟 Key Features

1. **Multilingual Chatbot (AI Sahayak)**: Converses naturally in Hindi, English, Hinglish, and Bengali using Google Gemini Flash.
2. **Grounded RAG (Retrieval-Augmented Generation)**: Answers are strictly derived from official scheme guidelines, eliminating hallucinations.
3. **Official Source Citations**: Every answer includes direct links to official `.gov.in` websites and helplines.
4. **Scheme Catalog & Smart Search**: Real-time filtering and keyword search across 10 flagship central government schemes.
5. **Interactive "Am I Eligible?" Calculator**: Evaluates citizen demographics (Age, Gender, Occupation, Income, Land/Housing ownership) against eligibility rules.
6. **Zero-Downtime Fallback Architecture**: Built-in offline grounded retrieval ensures seamless demo performance even during network interruptions.

---

## 🏛️ The 10 Flagship Schemes Covered

| # | Scheme | Target Beneficiaries | Key Benefit | Official Portal |
|---|---|---|---|---|
| 1 | **PM-KISAN** | Landholding Farmers | ₹6,000/year in 3 DBT installments | [pmkisan.gov.in](https://pmkisan.gov.in) |
| 2 | **Ayushman Bharat (PM-JAY)** | Low-income Families | ₹5 Lakh cashless health cover/year | [pmjay.gov.in](https://pmjay.gov.in) |
| 3 | **PMAY (Housing for All)** | Homeless / Kutcha House Dwellers | Up to ₹1.3L grant or ₹2.67L interest subsidy | [pmaymis.gov.in](https://pmaymis.gov.in) |
| 4 | **PM Mudra Yojana (PMMY)** | Micro-enterprises & Small Businesses | Collateral-free loans up to ₹20 Lakh | [mudra.org.in](https://www.mudra.org.in) |
| 5 | **Sukanya Samriddhi (SSY)** | Girl Child (Aged ≤ 10) | 8.2% guaranteed interest + triple tax exemption | [indiapost.gov.in](https://www.indiapost.gov.in) |
| 6 | **PM Ujjwala Yojana 2.0** | Rural & BPL Women | Free LPG connection + ₹300 refill subsidy | [pmuy.gov.in](https://www.pmuy.gov.in) |
| 7 | **Atal Pension Yojana (APY)** | Unorganized Sector Workers | Guaranteed ₹1,000 - ₹5,000/month pension | [npscra.nsdl.co.in](https://www.npscra.nsdl.co.in) |
| 8 | **PM Vishwakarma** | 18 Traditional Trades / Artisans | ₹15k toolkit voucher + 5% concessional credit | [pmvishwakarma.gov.in](https://pmvishwakarma.gov.in) |
| 9 | **National Scholarship Portal** | Underprivileged & Meritorious Students | ₹10,000 to ₹50,000/year education support | [scholarships.gov.in](https://scholarships.gov.in) |
| 10 | **PM SVANidhi** | Street Vendors & Hawkers | Collateral-free ₹10k-₹50k loan with 7% subsidy | [pmsvanidhi.mohua.gov.in](https://pmsvanidhi.mohua.gov.in) |

---

## 👥 Team Roles & Responsibilities

- **Member 1 (AI / RAG)**: Document chunking, vector indexing, Gemini system prompts, and citation extraction (`backend/rag_engine.py`).
- **Member 2 (Backend & Multilingual)**: FastAPI endpoints (`/api/chat`, `/api/schemes`, `/api/check-eligibility`), CORS configuration, and language routing (`backend/main.py`).
- **Member 3 (Frontend / UI)**: Responsive UI, Chat interface, Scheme Cards, and Eligibility Wizard (`frontend/src/components/*`).
- **Member 4 (Integration, Antigravity, Testing & Demo Lead)**: System architecture, API contracts, environment setup, cross-stack integration, testing, and pitch readiness.

---

## 🚀 Quick Start Guide

### 1. Start the Backend Server (FastAPI)
```bash
cd backend
python -m pip install -r requirements.txt
python main.py
```
- API will run at: `https://yojanasetu-9yfn.onrender.com`
- Interactive Swagger Documentation: `https://yojanasetu-9yfn.onrender.com/docs`

### 2. Start the Frontend Application (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
- Web Application will run at: `https://sayan69-ui.github.io/YojanaSetu/`

---

## 🎯 3 Showstopper Scenarios for Judges Demo

1. **Farmer Scenario (Hindi)**:
   - Ask: *"मैं एक छोटा किसान हूँ, मुझे सरकार से आर्थिक सहायता कैसे मिल सकती है?"*
   - Shows: Native Hindi comprehension, details on ₹6,000 PM-KISAN, and direct link to `pmkisan.gov.in`.
2. **Healthcare & Family Protection**:
   - Ask: *"How can my family get free hospital treatment under Ayushman Bharat?"*
   - Shows: Grounded retrieval detailing the ₹5 Lakh cashless coverage, empanelled hospitals, and `pmjay.gov.in`.
3. **Instant "Am I Eligible?" Wizard**:
   - Go to the **Am I Eligible?** tab, select *Age 28, Female, Artisan/Craftsperson, Annual Income ₹1,50,000*.
   - Shows: Automatic matching with PM Vishwakarma (₹15,000 toolkit voucher + 5% loan) and Ayushman Bharat with clear justification.

## Disclaimer 
Open website using your own internet . Might face some issue if accessed via college's wifi .
