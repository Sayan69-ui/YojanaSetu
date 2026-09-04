"""
YojanaSetu RAG Engine
High-fidelity grounded retrieval and multi-turn conversational reasoning for Indian Government Schemes.
Strictly supports ONLY 4 languages: Hindi, English, Hinglish, and Bengali.
Ensures comprehensive, structured scheme explanations without generic/vague summaries.
"""

import os
import re
import glob
import json
import requests
from typing import List, Dict, Any, Optional, Tuple


class RAGEngine:
    def __init__(self, documents_dir: str, schemes_json_path: str):
        self.documents_dir = documents_dir
        self.schemes_json_path = schemes_json_path
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

        # Load structured scheme database
        self.schemes_data: Dict[str, Dict[str, Any]] = {}
        if os.path.exists(schemes_json_path):
            with open(schemes_json_path, "r", encoding="utf-8") as f:
                raw_schemes = json.load(f)
                for s in raw_schemes:
                    self.schemes_data[s["id"]] = s

        # Load multilingual verified scheme profiles (en, hi, hinglish, bn)
        self.schemes_i18n: Dict[str, Dict[str, Any]] = {}
        i18n_path = os.path.join(os.path.dirname(schemes_json_path), "schemes_i18n.json")
        if os.path.exists(i18n_path):
            with open(i18n_path, "r", encoding="utf-8") as f:
                self.schemes_i18n = json.load(f)

        # Load markdown documents for full text grounding
        self.doc_texts: Dict[str, str] = {}
        self._load_markdown_documents()

        # Multi-language keywords and aliases mapping to scheme IDs
        self.concept_aliases: Dict[str, List[str]] = {
            "pm-kisan": [
                "kisan", "pm-kisan", "pmkisan", "farmer", "farmers", "agriculture", "fasal", "kheti", "6000",
                "installment", "cultivable", "landholder", "dbt",
                "किसान", "खेती", "कृषि", "फसल", "जमीन", "खाता", "सम्मान निधि", "६०००",
                "কৃষক", "কিষাণ", "চাষি", "কৃষি", "জমি", "টাকা", "অনুদানের", "সম্মান নিধি"
            ],
            "ayushman-bharat": [
                "ayushman", "pmjay", "pm-jay", "health", "hospital", "swasthya", "ilaj", "bimari", "doctor",
                "cashless", "5 lakh", "5,00,000", "golden card", "hospitalization", "nha", "secc",
                "आयुष्मान", "स्वास्थ्य", "इलाज", "अस्पताल", "बीमारी", "कार्ड", "कैशलेस", "पांच लाख", "5 लाख",
                "আয়ুষ্মান", "স্বাস্থ্য", "হাসপাতাল", "চিকিৎসা", "বীমা", "কার্ড", "৫ লক্ষ", "পাঁচ লাখ", "ক্যাশলেস"
            ],
            "pmay": [
                "awas", "pmay", "pmay-g", "pmay-u", "housing", "pucca", "makan", "ghar", "home", "subsidy",
                "gramin", "urban", "clss", "blc",
                "आवास", "मकान", "घर", "पक्का", "सब्सिडी", "शहरी", "ग्रामीण",
                "আবাস", "বাড়ি", "ঘর", "পাকা বাড়ি", "আবাসন", "গ্রামীণ", "নগর"
            ],
            "pm-mudra": [
                "mudra", "pmmy", "loan", "business", "vyapar", "karobar", "shishu", "kishore", "tarun",
                "dukan", "shop", "enterprise", "collateral free", "working capital", "msme",
                "मुद्रा", "लोन", "व्यापार", "दुकान", "कारोबार", "ऋण", "शिशु", "किशोर", "तरुण", "बिना गारंटी",
                "মুদ্রা", "ঋণ", "ব্যবসা", "দোকান", "লোন", "বিনামূল্যে বন্ধক"
            ],
            "sukanya-samriddhi": [
                "sukanya", "ssy", "beti", "girl", "daughter", "child", "education", "shaadi", "marriage",
                "80c", "tax free", "post office", "8.2%",
                "सुकन्या", "बेटी", "बच्ची", "विवाह", "शादी", "लड़की", "बालिका", "सुकन्या समृद्धि",
                "সুকন্যা", "মেয়ে", "কন্যা", "কন্যাশ্রী", "বিবাহ", "পড়াশোনা", "সুকন্যা সমৃদ্ধি"
            ],
            "pm-ujjwala": [
                "ujjwala", "pmuy", "gas", "cylinder", "lpg", "rasoi", "chulha", "smokeless", "connection",
                "subsidy", "clean fuel", "bpl women",
                "उज्ज्वला", "गैस", "सिलेंडर", "चूल्हा", "रसोई", "एलपीजी",
                "উজ্জ্বলা", "গ্যাস", "সিলিন্ডার", "রান্না", "এলপিজি"
            ],
            "atal-pension": [
                "atal", "apy", "pension", "budhapa", "monthly pension", "unorganized", "retirement",
                "pfrda", "pran", "1000", "5000",
                "अटल", "पेंशन", "बुढ़ापा", "रिटायरमेंट", "अटल पेंशन",
                "অটল", "পেনশন", "অবসর", "বার্ধক্য"
            ],
            "pm-vishwakarma": [
                "vishwakarma", "artisan", "karigar", "craftsperson", "carpenter", "blacksmith", "lohar",
                "darzi", "tailor", "tools", "15000", "stipend", "traditional trades",
                "विश्वकर्मा", "कारीगर", "टूलकिट", "दर्जी", "बढ़ई", "लोहार", "हस्तशिल्प", "शिल्पकार",
                "বিশ্বকর্মা", "কারিগর", "ছুতোর", "কামার", "দর্জি", "টুলকিট", "হস্তশিল্পী"
            ],
            "national-scholarship": [
                "scholarship", "nsp", "chhatravritti", "student", "college", "school", "education",
                "fees", "merit", "post matric", "pre matric", "csss",
                "छात्रवृत्ति", "स्कॉलरशिप", "विद्यार्थी", "छात्र", "छात्रा", "कॉलेज", "पढ़ाई",
                "স্কলারশিপ", "বৃত্তি", "ছাত্র", "ছাত্রী", "কলেজ", "পড়াশোনা", "মেধা"
            ],
            "pm-svanidhi": [
                "svanidhi", "vendor", "street vendor", "thela", "rehri", "patri", "hawker", "10000",
                "working capital", "street food", "urban local body", "ulb",
                "स्वनिधि", "वेंडर", "ठेला", "रेहड़ी", "पटरी", "फेरीवाला", "पीएम स्वनिधि",
                "স্বনিধি", "হকার", "বিক্রেতা", "রাস্তার দোকান", "ঠেলাওয়ালা"
            ],
        }

    def _load_markdown_documents(self):
        """Map scheme IDs to their detailed markdown documentation."""
        file_mapping = {
            "pm_kisan": "pm-kisan",
            "ayushman_bharat": "ayushman-bharat",
            "pmay": "pmay",
            "pm_mudra": "pm-mudra",
            "sukanya_samriddhi": "sukanya-samriddhi",
            "pm_ujjwala": "pm-ujjwala",
            "atal_pension": "atal-pension",
            "pm_vishwakarma": "pm-vishwakarma",
            "national_scholarship": "national-scholarship",
            "pm_svanidhi": "pm-svanidhi",
        }
        for file_key, scheme_id in file_mapping.items():
            path = os.path.join(self.documents_dir, f"{file_key}.md")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.doc_texts[scheme_id] = f.read()

    def detect_language(self, text: str) -> str:
        """
        Detects among the 4 strictly supported languages:
        1. 'bn' (Bengali / বাংলা)
        2. 'hi' (Hindi / हिन्दी)
        3. 'hinglish' (Hinglish / Roman Hindi)
        4. 'en' (English)
        """
        # 1. Check Bengali script (Unicode: U+0980 to U+09FF)
        if re.search(r'[\u0980-\u09FF]', text):
            return "bn"

        # 2. Check Devanagari script (Unicode: U+0900 to U+097F)
        if re.search(r'[\u0900-\u097F]', text):
            return "hi"

        # 3. Check for Hinglish markers (Roman Hindi words)
        hinglish_words = {
            "kya", "kaise", "milega", "chahiye", "kisan", "yojana", "paisa", "paise",
            "loan", "ghar", "makan", "beti", "padhai", "mujhe", "mera", "meri", "mere",
            "namaste", "aap", "karein", "karna", "kare", "hota", "hoti", "hai", "hain",
            "ke", "ki", "ko", "se", "mein", "me", "par", "liye", "aur", "ya", "batao",
            "bataiye", "dijiye", "bhi", "toh", "to", "kaun", "kab", "kisko", "milta",
            "milti", "sakte", "sakta", "karo", "lakh", "crore", "hoga", "shuru", "wale"
        }
        words = set(re.findall(r'[a-zA-Z]+', text.lower()))
        matched = words.intersection(hinglish_words)
        strong_markers = {"kaise", "milega", "chahiye", "batao", "bataiye", "mujhe", "karein", "milti"}
        if len(matched) >= 2 or len(words.intersection(strong_markers)) >= 1:
            return "hinglish"

        # 4. Default to English
        return "en"

    def _resolve_response_language(self, query: str, selected_language: Optional[str]) -> str:
        """
        Language Resolution Rule:
        If user explicitly selected 'hi', 'en', 'hinglish', or 'bn', that choice MUST be followed.
        If user selected 'auto' (or unspecified), detect the language of the query.
        Defaults to 'en' if ambiguous. Never returns Tamil/Telugu.
        """
        valid_languages = ["hi", "en", "hinglish", "bn"]
        if selected_language and selected_language.lower() in valid_languages:
            return selected_language.lower()

        # Auto detection
        detected = self.detect_language(query)
        return detected if detected in valid_languages else "en"

    def _match_scheme(self, query: str) -> Optional[Tuple[str, int]]:
        """Scores query against all 10 schemes using names, aliases, and keywords."""
        query_clean = query.lower().strip()
        query_words = set(re.findall(r'\w+', query_clean))

        best_scheme_id = None
        best_score = 0

        for scheme_id, scheme in self.schemes_data.items():
            score = 0
            name_en = scheme["name"].lower()
            name_hi = scheme.get("name_hi", "").lower()
            name_bn = scheme.get("name_bn", "").lower()

            if scheme_id in query_clean:
                score += 15
            if ("pm-jay" in query_clean or "pmjay" in query_clean or "ayushman" in query_clean or "আয়ুষ্মান" in query_clean or "आयुष्मान" in query_clean) and scheme_id == "ayushman-bharat":
                score += 25
            if ("pm-kisan" in query_clean or "pmkisan" in query_clean or "किसान" in query_clean or "কিষাণ" in query_clean) and scheme_id == "pm-kisan":
                score += 25
            if ("mudra" in query_clean or "मुद्रा" in query_clean or "মুদ্রা" in query_clean) and scheme_id == "pm-mudra":
                score += 25
            if ("svanidhi" in query_clean or "स्वनिधि" in query_clean or "স্বনিধি" in query_clean) and scheme_id == "pm-svanidhi":
                score += 25
            if ("ujjwala" in query_clean or "उज्ज्वला" in query_clean or "উজ্জ্বলা" in query_clean) and scheme_id == "pm-ujjwala":
                score += 25
            if ("sukanya" in query_clean or "सुकन्या" in query_clean or "সুকন্যা" in query_clean) and scheme_id == "sukanya-samriddhi":
                score += 25
            if ("vishwakarma" in query_clean or "विश्वकर्मा" in query_clean or "বিশ্বকর্মা" in query_clean) and scheme_id == "pm-vishwakarma":
                score += 25
            if ("awas" in query_clean or "आवास" in query_clean or "আবাস" in query_clean) and scheme_id == "pmay":
                score += 25
            if ("pension" in query_clean or "अटल" in query_clean or "অটল" in query_clean) and scheme_id == "atal-pension":
                score += 25
            if ("scholarship" in query_clean or "छात्रवृत्ति" in query_clean or "স্কলারশিপ" in query_clean) and scheme_id == "national-scholarship":
                score += 25

            # Exact title matches
            if name_en in query_clean:
                score += 15
            if name_hi and name_hi in query_clean:
                score += 18
            if name_bn and name_bn in query_clean:
                score += 18

            # Alias matching
            aliases = self.concept_aliases.get(scheme_id, [])
            for alias in aliases:
                if alias.lower() in query_clean or alias in query:
                    score += 6

            # Word overlaps with brief
            brief_words = set(re.findall(r'\w+', scheme.get("brief", "").lower()))
            overlap = len(query_words.intersection(brief_words))
            score += overlap

            if score > best_score:
                best_score = score
                best_scheme_id = scheme_id

        # Require a threshold score of at least 4
        if best_score >= 4:
            return best_scheme_id, best_score
        return None

    def _find_scheme_from_history(self, history: List[Dict[str, str]]) -> Optional[str]:
        """Scans conversation history in reverse to find the active scheme being discussed."""
        if not history:
            return None

        for item in reversed(history):
            text = item.get("text", "")
            match = self._match_scheme(text)
            if match:
                return match[0]
        return None

    def _detect_query_intent(self, query: str) -> str:
        """Determines if user is asking for general overview, eligibility, benefits, documents, or how to apply."""
        q = query.lower()

        # Documents intent
        doc_words = ["document", "documents", "paper", "papers", "aadhaar", "proof", "दस्तावेज", "कागजात", "कागज़", "কাগজপত্র", "নথিপত্র"]
        if any(w in q for w in doc_words):
            return "documents"

        # Eligibility intent
        elig_words = ["eligible", "eligibility", "who can", "who is", "criteria", "qualification", "qualify", "patra", "patrata", "कौन पात्र", "पात्रता", "কারা সুবিধা", "যোগ্যতা"]
        if any(w in q for w in elig_words):
            return "eligibility"

        # Benefits intent
        benefit_words = ["benefit", "benefits", "advantage", "paisa", "rupees", "kitna", "amount", "लाभ", "फायदे", "कितने पैसे", "সুবিধা", "টাকা"]
        if any(w in q for w in benefit_words):
            return "benefits"

        # Apply intent
        apply_words = ["apply", "how to apply", "process", "register", "registration", "portal", "आवेदन", "कैसे करें", "আবেদন", "কিভাবে আবেদন"]
        if any(w in q for w in apply_words):
            return "apply"

        return "overview"

    def _call_gemini_rest(self, system_instruction: str, prompt: str) -> Optional[str]:
        """Direct REST API call to Gemini 1.5 Flash."""
        api_key = os.getenv("GEMINI_API_KEY", "").strip() or self.api_key
        if not api_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_instruction}\n\n{prompt}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1000
            }
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=12)
            if res.status_code == 200:
                data = res.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
            else:
                print(f"[RAGEngine] Gemini HTTP {res.status_code}: {res.text[:120]}")
        except Exception as e:
            print(f"[RAGEngine] Gemini REST exception: {e}")
        return None

    def ask(self, query: str, selected_language: Optional[str] = "auto", history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Main query processing entrypoint.
        1. Resolves language (strict adherence to user selection or query language).
        2. Identifies scheme from query or previous conversation history.
        3. Formulates detailed, grounded response with official citations.
        """
        history = history or []

        # 1. Resolve exact target language
        target_lang = self._resolve_response_language(query, selected_language)

        # 2. Retrieve scheme
        scheme_match = self._match_scheme(query)
        scheme_id = None

        if scheme_match:
            scheme_id = scheme_match[0]
        else:
            # Check if this is a follow-up referring to a previously discussed scheme
            scheme_id = self._find_scheme_from_history(history)

        # 3. Handle unknown / unverified scheme query
        if not scheme_id or scheme_id not in self.schemes_data:
            unknown_reply = self._generate_unknown_scheme_response(query, target_lang)
            return {
                "reply": unknown_reply,
                "sources": [],
                "detected_language": target_lang
            }

        scheme = self.schemes_data[scheme_id]
        doc_text = self.doc_texts.get(scheme_id, scheme.get("brief", ""))
        intent = self._detect_query_intent(query)

        # Localized source title
        i18n_scheme = self.schemes_i18n.get(scheme_id, {}).get(target_lang, {})
        source_title = i18n_scheme.get("name", scheme["name"])
        sources = [{
            "title": source_title,
            "url": scheme["official_url"]
        }]

        # 4. Attempt Gemini LLM Generation
        lang_names = {
            "hi": "Hindi (हिन्दी) using Devanagari script",
            "en": "English",
            "hinglish": "natural Indian Hinglish using Roman/English script (e.g., 'Ye scheme eligible families ko...')",
            "bn": "Bengali (বাংলা) using Bengali script"
        }
        target_lang_desc = lang_names.get(target_lang, "English")

        system_instruction = f"""You are YojanaSetu — AI Sahayak, an Indian Government Scheme Assistant.

The user's requested response language is: {target_lang_desc}

You MUST generate the final answer ONLY in the requested language ({target_lang}).

Supported languages:
- Hindi
- English
- Hinglish
- Bengali

Never answer in Tamil or Telugu.

For Hindi, use Devanagari script.
For English, use English.
For Hinglish, use Roman script and natural Indian Hinglish.
For Bengali, use Bengali script.

The retrieved documents may be written in English or another language. Translate and explain the verified information into the requested language before producing the final response.

Do not hallucinate government scheme information.
Use only information supported by retrieved sources.
If information is unavailable, clearly state that it could not be verified.

Structure scheme answers clearly:
- Scheme Name (e.g. 🟢 {source_title})
- **What is it? / क्या है यह योजना? / এটি কি?** (Simple explanation & main purpose)
- **Who can benefit? / कौन पात्र है? / কারা সুবিধা পাবেন?** (Eligibility criteria & conditions)
- **Major Benefits / मुख्य लाभ / প্রধান সুবিধাগুলি** (Clear bullet points with exact figures)
- **Required Documents / आवश्यक दस्तावेज / প্রয়োজনীয় নথিপত্র** (Exact checklist)
- **How to Apply / आवेदन कैसे करें / কিভাবে আবেদন করবেন** (Clear steps & official portal)
- **Official Source & Helpline / आधिकारिक स्रोत / অফিসিয়াল পোর্টাল ও হেল্পলাইন**
"""

        # Context assembly including structured metadata and raw guidelines
        structured_context = f"""
SCHEME METADATA:
ID: {scheme['id']}
Name (English): {scheme['name']}
Name (Hindi): {scheme.get('name_hi', '')}
Name (Bengali): {scheme.get('name_bn', '')}
Ministry: {scheme.get('ministry', '')}
Target Audience: {scheme.get('target_audience', '')}
Overview: {scheme.get('brief', '')}
Benefits: {json.dumps(scheme.get('benefits', []), ensure_ascii=False)}
Eligibility Rules: {json.dumps(scheme.get('eligibility_rules', {}), ensure_ascii=False)}
Required Documents: {json.dumps(scheme.get('documents_required', []), ensure_ascii=False)}
Official URL: {scheme.get('official_url', '')}
Helpline: {scheme.get('helpline', '')}

DETAILED GUIDELINES:
{doc_text}
"""

        # History context string
        history_str = ""
        if history:
            recent = history[-4:]
            history_str = "Recent Conversation History:\n" + "\n".join([f"{item['sender'].capitalize()}: {item['text']}" for item in recent]) + "\n\n"

        user_prompt = f"""{history_str}Official Government Scheme Context:
{structured_context}

Citizen's Question:
{query}

Formulate the complete, grounded answer in {target_lang_desc} now:"""

        gemini_reply = self._call_gemini_rest(system_instruction, user_prompt)
        if gemini_reply:
            return {
                "reply": gemini_reply,
                "sources": sources,
                "detected_language": target_lang
            }

        # 5. Guaranteed Comprehensive Grounded Fallback (Offline / Zero-Key Safety Net)
        # Pulls directly from our verified multilingual dictionary
        fallback_reply = self._generate_structured_grounded_response(scheme_id, intent, target_lang)
        return {
            "reply": fallback_reply,
            "sources": sources,
            "detected_language": target_lang
        }

    def _generate_unknown_scheme_response(self, query: str, lang: str) -> str:
        """Returns a transparent message when the scheme cannot be found among verified sources."""
        if lang == "hi":
            return f"""⚠️ **सत्यापित जानकारी उपलब्ध नहीं है**

मुझे अपने आधिकारिक ज्ञानकोष में **"{query}"** से संबंधित किसी सत्यापित केंद्र सरकार की योजना का विवरण नहीं मिला।

कृपया योजना का सही नाम जांचें या आप निम्नलिखित में से किसी योजना के बारे में पूछ सकते हैं:
• **पीएम-किसान** (किसानों के लिए ₹6,000 सहायता)
• **आयुष्मान भारत (PM-JAY)** (₹5 लाख मुफ्त स्वास्थ्य सुरक्षा)
• **प्रधानमंत्री आवास योजना (PMAY)** (पक्के मकान हेतु सब्सिडी)
• **पीएम मुद्रा योजना (PMMY)** (बिना गारंटी व्यापार ऋण)
• **सुकन्या समृद्धि योजना (SSY)** (बेटियों के लिए उच्च ब्याज बचत)
• **पीएम उज्ज्वला योजना** (मुफ्त एलपीजी गैस कनेक्शन)
• **अटल पेंशन योजना (APY)** (आजीवन मासिक पेंशन)
• **पीएम विश्वकर्मा योजना** (कारीगरों हेतु टूलकिट व 5% ऋण)
• **राष्ट्रीय छात्रवृत्ति पोर्टल (NSP)** (छात्रों हेतु स्कॉलरशिप)
• **पीएम स्वनिधि** (स्ट्रीट वेंडर्स हेतु कार्यशील पूंजी)"""

        elif lang == "bn":
            return f"""⚠️ **যাচাইকৃত তথ্য পাওয়া যায়নি**

আমার তথ্যভাণ্ডারে **"{query}"** সম্পর্কিত কোনো অনুমোদিত কেন্দ্রীয় সরকারি প্রকল্পের বিবরণ পাওয়া যায়নি।

অনুগ্রহ করে প্রকল্পের সঠিক নাম পরীক্ষা করুন অথবা নিম্নলিখিত প্রধান প্রকল্পগুলি সম্পর্কে জিজ্ঞাসা করতে পারেন:
• **পিএম কিষাণ** (কৃষকদের জন্য ₹৬,০০০ অনুদান)
• **আয়ুষ্মান ভারত (PM-JAY)** (₹৫ লক্ষ ক্যাশলেস স্বাস্থ্য বীমা)
• **প্রধানমন্ত্রী আবাস যোজনা (PMAY)** (পাকা বাড়ি নির্মাণের সহায়তা)
• **প্রধানমন্ত্রী মুদ্রা যোজনা** (ব্যবসার জন্য বন্ধকমুক্ত ঋণ)
• **সুকন্যা সমৃদ্ধি যোজনা** (কন্যা সন্তানের জন্য সঞ্চয় প্রকল্প)
• **প্রধানমন্ত্রী উজ্জ্বলা যোজনা** (বিনামূল্যে এলপিজি সংযোগ)
• **অটল পেনশন যোজনা (APY)** (নিশ্চিত মাসিক পেনশন)
• **প্রধানমন্ত্রী বিশ্বকর্মা যোজনা** (কারিগরদের জন্য ₹১৫,০০০ টুলকিট অনুদান)
• **জাতীয় স্কলারশিপ পোর্টাল (NSP)** (শিক্ষার্থীদের জন্য বৃত্তি)
• **পিএম স্বনিধি** (হকারদের জন্য ওয়ার্কিং ক্যাপিটাল ঋণ)"""

        elif lang == "hinglish":
            return f"""⚠️ **Verified Information Not Found**

Mujhe verified central government records me **"{query}"** se related official scheme ki details nahi mili.

Kripya scheme ka correct name check karein ya aap in official schemes ke baare me pooch sakte hain:
• **PM-KISAN** (Farmers ke liye ₹6,000 direct benefit)
• **Ayushman Bharat (PM-JAY)** (₹5 Lakh free health cover)
• **PMAY Housing** (Pucca ghar banane ke liye subsidy)
• **PM Mudra Yojana** (Collateral-free business loan up to ₹20 Lakh)
• **Sukanya Samriddhi** (Girl child savings & education)
• **PM Ujjwala Yojana** (Free LPG connection for women)
• **Atal Pension Yojana** (Guaranteed monthly pension after 60)
• **PM Vishwakarma** (Artisans ke liye toolkit & 5% loan)
• **National Scholarship Portal** (Students education support)
• **PM SVANidhi** (Street vendors working capital loan)"""

        else:
            return f"""⚠️ **Verified Information Not Found**

I could not find verified government details for **"{query}"** in our official scheme database.

Please check the scheme name or feel free to ask about any of the 10 central schemes we cover:
• **PM-KISAN** (Income support for farmers)
• **Ayushman Bharat (PM-JAY)** (₹5 Lakh free health assurance)
• **PMAY (Housing for All)** (Financial assistance for pucca housing)
• **PM Mudra Yojana (PMMY)** (Collateral-free enterprise credit up to ₹20 Lakh)
• **Sukanya Samriddhi Yojana (SSY)** (Savings for girl child education & marriage)
• **PM Ujjwala Yojana** (Free LPG connection for poor households)
• **Atal Pension Yojana (APY)** (Guaranteed lifelong monthly pension)
• **PM Vishwakarma** (Holistic support and toolkit for traditional artisans)
• **National Scholarship Portal (NSP)** (Scholarships for meritorious students)
• **PM SVANidhi** (Working capital credit for street vendors)"""

    def _generate_structured_grounded_response(self, scheme_id: str, intent: str, lang: str) -> str:
        """
        Uses verified multilingual scheme knowledge to construct a comprehensive,
        structured guide in the requested language (bn, hi, hinglish, or en).
        """
        i18n_scheme = self.schemes_i18n.get(scheme_id, {}).get(lang)
        # Fallback to English if translation missing
        if not i18n_scheme:
            i18n_scheme = self.schemes_i18n.get(scheme_id, {}).get("en", {})

        name = i18n_scheme.get("name", scheme_id)
        what_is_it = i18n_scheme.get("what_is_it", "")
        ministry = i18n_scheme.get("ministry", "")
        who_can_benefit = i18n_scheme.get("who_can_benefit", "")
        conditions = i18n_scheme.get("conditions", "")
        benefits = i18n_scheme.get("benefits", [])
        documents = i18n_scheme.get("documents", [])
        how_to_apply = i18n_scheme.get("how_to_apply", "")
        url = i18n_scheme.get("url", "https://india.gov.in")
        helpline = i18n_scheme.get("helpline", "")

        benefits_bullets = "\n".join([f"• {b}" for b in benefits])
        docs_bullets = "\n".join([f"• {d}" for d in documents])

        # 1. BENGALI
        if lang == "bn":
            title = f"🟢 {name}"
            if intent == "documents":
                return f"""{title}

**প্রয়োজনীয় নথিপত্র (Required Documents):**
{docs_bullets}

📌 **আবেদনের নির্দেশনা:**
• সমস্ত নথিতে নাম ও তথ্যের সাথে আধার কার্ড ও ব্যাংক অ্যাকাউন্টের মিল থাকা বাধ্যতামূলক।
• অনলাইন আবেদন বা স্ট্যাটাস যাচাইয়ের জন্য অফিসিয়াল পোর্টালে যান: [{name}]({url})
• অফিসিয়াল হেল্পলাইন: **{helpline}**"""

            if intent == "eligibility":
                return f"""{title}

**কারা সুবিধা পাবেন? (Who can benefit?):**
• **মূল সুবিধাভোগী:** {who_can_benefit}
• **শর্তাবলী ও বিধিনিষেধ:** {conditions}

📌 **যোগ্যতা যাচাই:**
• নিজের পরিবারের নাম বা যোগ্যতা যাচাই করতে অফিসিয়াল পোর্টাল দেখুন: [{name}]({url})
• জাতীয় হেল্পলাইন নম্বর: **{helpline}**"""

            if intent == "benefits":
                return f"""{title}

**প্রধান সুবিধা ও আর্থিক সহায়তা (Major Benefits):**
{benefits_bullets}

📌 **সুবিধা প্রদান পদ্ধতি:**
• সমস্ত আর্থিক সুবিধা সরাসরি সুবিধাভোগীর ব্যাংক অ্যাকাউন্টে (DBT) বা হাসপাতালে ক্যাশলেস মাধ্যমে প্রদান করা হয়।
• বিস্তারিত তথ্যের জন্য পোর্টাল: [{name}]({url})"""

            # Full Overview Guide
            return f"""{title}

**এটি কি? (What is it?)**
{what_is_it}
• **মন্ত্রণালয়:** {ministry}
• **মূল উদ্দেশ্য:** যোগ্য নাগরিকদের সামাজিক ও আর্থিক সুরক্ষা নিশ্চিত করা।

**কারা সুবিধা পাবেন? (Who can benefit?)**
• **যোগ্য নাগরিক:** {who_can_benefit}
• **শর্তাবলী:** {conditions}

**প্রধান সুবিধাগুলি (Major Benefits):**
{benefits_bullets}

**প্রয়োজনীয় নথিপত্র (Required Documents):**
{docs_bullets}

**কিভাবে আবেদন করবেন (How to Apply):**
{how_to_apply}

**অফিসিয়াল পোর্টাল ও হেল্পলাইন:**
• অফিসিয়াল পোর্টাল: [{name}]({url})
• হেল্পলাইন নম্বর: **{helpline}**"""

        # 2. HINDI
        elif lang == "hi":
            title = f"🟢 {name}"
            if intent == "documents":
                return f"""{title}

**आवश्यक दस्तावेज (Required Documents):**
{docs_bullets}

📌 **आवेदन निर्देश:**
• सभी दस्तावेजों में नाम और जन्मतिथि आधार कार्ड के अनुसार होनी चाहिए।
• ऑनलाइन आवेदन या स्थिति जांच के लिए आधिकारिक पोर्टल पर जाएं: [{name}]({url})
• आधिकारिक हेल्पलाइन: **{helpline}**"""

            if intent == "eligibility":
                return f"""{title}

**कौन पात्र है? (Eligibility Criteria):**
• **लक्षित वर्ग:** {who_can_benefit}
• **पात्रता की शर्तें व अपवाद:** {conditions}

📌 **पात्रता की जांच:**
• अपना नाम या पात्रता सूची आधिकारिक पोर्टल पर देखें: [{name}]({url})
• हेल्पलाइन नंबर: **{helpline}**"""

            if intent == "benefits":
                return f"""{title}

**मुख्य लाभ एवं वित्तीय सहायता (Major Benefits):**
{benefits_bullets}

📌 **लाभ वितरण मोड:**
• सभी वित्तीय सहायता सीधे आधार से जुड़े बैंक खाते में (DBT) या अस्पताल में कैशलेस माध्यम से दी जाती है।
• आधिकारिक पोर्टल: [{name}]({url})"""

            # Full Overview Guide
            return f"""{title}

**योजना क्या है? (What is it?)**
{what_is_it}
• **संबंधित मंत्रालय:** {ministry}
• **प्रमुख उद्देश्य:** पात्र नागरिकों को आर्थिक सुरक्षा और सशक्तिकरण प्रदान करना।

**कौन लाभ उठा सकता है? (Who can benefit?)**
• **पात्र नागरिक:** {who_can_benefit}
• **पात्रता शर्तें:** {conditions}

**मुख्य लाभ (Major Benefits):**
{benefits_bullets}

**आवश्यक दस्तावेज (Required Documents):**
{docs_bullets}

**आवेदन कैसे करें (How to Apply):**
{how_to_apply}

**आधिकारिक हेल्पलाइन एवं पोर्टल:**
• आधिकारिक पोर्टल: [{name}]({url})
• संपर्क नंबर: **{helpline}**"""

        # 3. HINGLISH
        elif lang == "hinglish":
            title = f"🟢 {name}"
            if intent == "documents":
                return f"""{title}

**Required Documents (Zaroori Documents):**
{docs_bullets}

📌 **Important Instructions:**
• Saare documents me details aapke Aadhaar card aur active bank passbook se match honi chahiye.
• Online status check aur application ke liye official portal visit karein: [{name}]({url})
• Official Helpline: **{helpline}**"""

            if intent == "eligibility":
                return f"""{title}

**Kaun Eligible Hai? (Who can benefit):**
• **Target Beneficiaries:** {who_can_benefit}
• **Eligibility Conditions & Exclusions:** {conditions}

📌 **Official Verification:**
• Apni eligibility check karne ke liye official portal visit karein: [{name}]({url})
• Helpline Number: **{helpline}**"""

            if intent == "benefits":
                return f"""{title}

**Main Benefits (Yojana ke Fayde):**
{benefits_bullets}

📌 **Disbursement:**
• Benefits directly bank account me Direct Benefit Transfer (DBT) ya hospital me cashless network ke zariye milte hain.
• Official Portal: [{name}]({url})"""

            # Full Overview Guide
            return f"""{title}

**Yojana Kya Hai? (What is it):**
{what_is_it}
• **Ministry:** {ministry}
• **Purpose:** Eligible citizens ko financial support aur social security provide karna.

**Kaun Benefit Le Sakta Hai? (Eligibility):**
• **Eligible Categories:** {who_can_benefit}
• **Conditions:** {conditions}

**Major Benefits (Mukhya Labh):**
{benefits_bullets}

**Required Documents (Zaroori Kagazat):**
{docs_bullets}

**Apply Kaise Karein (Application Steps):**
{how_to_apply}

**Official Portal & Helpline:**
• Official Portal Link: [{name}]({url})
• Helpline Number: **{helpline}**"""

        # 4. ENGLISH
        else:
            title = f"🟢 {name}"
            if intent == "documents":
                return f"""{title}

**Required Documents:**
{docs_bullets}

📌 **Important Guidelines:**
• Ensure your name and details match your Aadhaar Card and active bank account.
• Access online application and document verification at: [{name}]({url})
• Official Helpline: **{helpline}**"""

            if intent == "eligibility":
                return f"""{title}

**Who can benefit? (Eligibility Criteria):**
• **Target Beneficiaries:** {who_can_benefit}
• **Specific Conditions & Exclusions:** {conditions}

📌 **Verify Eligibility:**
• Confirm your household eligibility directly on the portal: [{name}]({url})
• Official Helpline: **{helpline}**"""

            if intent == "benefits":
                return f"""{title}

**Major Benefits & Financial Assistance:**
{benefits_bullets}

📌 **Mode of Assistance:**
• Benefits are disbursed directly via Direct Benefit Transfer (DBT) into verified bank accounts or through cashless hospital networks.
• Official Portal: [{name}]({url})"""

            # Full Overview Guide
            return f"""{title}

**What is it?**
{what_is_it}
• **Administering Ministry:** {ministry}
• **Primary Objective:** Empowering eligible citizens through direct financial protection, enterprise assistance, and welfare support.

**Who can benefit?**
• **Target Citizens:** {who_can_benefit}
• **Eligibility Conditions & Limitations:** {conditions}

**Major Benefits:**
{benefits_bullets}

**Required Documents:**
{docs_bullets}

**How to Apply:**
{how_to_apply}

**Official Helpline & Portal:**
• Official Portal: [{name}]({url})
• National Toll-Free Helpline: **{helpline}**"""
