# 🎤 YojanaSetu Demo Pitch & Judge Q&A Cheatsheet

Use this cheat-sheet during your 3-minute hackathon demo to impress the judges!

---

## ⏱️ 3-Minute Demo Script

### Minute 1: The Problem & The Solution
> *"Respected Judges, India has some of the most progressive welfare schemes in the world—from ₹5 Lakh health insurance under Ayushman Bharat to ₹20 Lakh collateral-free business loans under Mudra. However, the average citizen faces a huge barrier: complex 50-page bureaucratic guidelines written in formal English, no easy way to check eligibility, and fear of scams.*
> 
> *Introducing **YojanaSetu (योजनासेतु)**—an AI-powered, multilingual citizen welfare guide that operates like an empathetic local officer."*

### Minute 2: Live Feature Walkthrough
1. **Multilingual AI Sahayak (RAG)**:
   - Click the prompt chip or type in Hindi:
     ```
     मैं एक छोटा किसान हूँ, मुझे ₹6000 वाली योजना कैसे मिलेगी?
     ```
   - **Point to the Screen**: Show that the bot understands Hindi, explains the 3 installments of ₹2,000 under PM-KISAN, explains eligibility (land ownership, exclusion of tax-payers), and provides a **clickable official citation directly to `pmkisan.gov.in`**.
2. **Interactive "Am I Eligible?" Calculator**:
   - Switch to the **Am I Eligible?** tab.
   - Set: **Age 28, Female, Artisan / Craftsperson, Income ₹1,50,000**.
   - Click **Check My Eligible Schemes Now**.
   - **Show the Result**: Instantly highlights **PM Vishwakarma** (₹15,000 toolkit voucher + 5% loan) and **Ayushman Bharat** (₹5L healthcare cover) with precise justifications.
3. **Scheme Catalog & Search**:
   - Switch to **All Schemes** tab.
   - Click the **Business & Employment** category pill or type **"loan"** in the search bar.
   - Show how it filters to PM Mudra and PM SVANidhi with official portals and document requirements.

### Minute 3: Architecture & Social Impact
> *"Under the hood, YojanaSetu uses FastAPI, Google Gemini Flash, and grounded local RAG over verified government documents to ensure 100% factual accuracy with zero hallucinations. Even with zero internet or API quotas during peak hours, our offline-grounded fallback ensures the citizen always gets their answer.*
> 
> *YojanaSetu turns digital governance into true civic empowerment. Thank you!"*

---

## 💡 Top 3 Anticipated Judge Questions & Winning Answers

1. **Q: How do you prevent AI hallucinations when giving sensitive government advice?**
   - **A**: *"We use Retrieval-Augmented Generation (RAG). The AI is not answering from open internet training memory; its system prompt strictly limits answers to our curated, official scheme documents and forces official .gov.in source citations."*

2. **Q: How does this reach rural citizens who cannot type well?**
   - **A**: *"Our frontend supports natural mixed languages (Hinglish/vernacular), one-click quick prompt chips, and is architected to easily integrate with browser Web Speech APIs for speech-to-text in the future."*

3. **Q: Why did your team choose this architecture?**
   - **A**: *"FastAPI provides blazing-fast async endpoints and auto-generated Swagger documentation. A modular React frontend ensures crisp responsiveness on mobile and low-bandwidth connections."*
