"""
Eligibility Matching Engine for YojanaSetu
Evaluates citizen profile against 10 Indian welfare schemes.
"""

import json
from typing import List, Dict, Any


class EligibilityEngine:
    def __init__(self, schemes_json_path: str):
        with open(schemes_json_path, "r", encoding="utf-8") as f:
            self.schemes = json.load(f)

    def evaluate(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Profile schema:
        {
          "age": int,
          "gender": str ("male", "female", "other"),
          "occupation": str ("farmer", "artisan", "student", "street_vendor", "unorganized_worker", "business_owner", "unemployed", "other"),
          "annual_income": float,
          "has_girl_child_under_10": bool (optional),
          "owns_pucca_house": bool (optional),
          "owns_agricultural_land": bool (optional)
        }
        """
        age = profile.get("age", 25)
        gender = profile.get("gender", "any").lower()
        occupation = profile.get("occupation", "other").lower().replace(" ", "_")
        income = profile.get("annual_income", 200000.0)
        has_girl_child = profile.get("has_girl_child_under_10", False)
        owns_pucca_house = profile.get("owns_pucca_house", False)
        owns_land = profile.get("owns_agricultural_land", False)

        eligible: List[Dict[str, Any]] = []
        potential: List[Dict[str, Any]] = []

        for s in self.schemes:
            sid = s["id"]
            rules = s.get("eligibility_rules", {})
            min_age = rules.get("min_age", 0)
            max_age = rules.get("max_age", 120)
            req_gender = rules.get("gender", "any").lower()
            max_income = rules.get("max_income")
            target_occupations = rules.get("occupations", [])

            reasons = []
            is_match = True
            is_potential = False

            # 1. Age check
            if age < min_age or age > max_age:
                if sid == "sukanya-samriddhi" and has_girl_child:
                    # Special check: age of girl child matters, parent can apply
                    reasons.append("Eligible on behalf of girl child aged ≤ 10")
                else:
                    is_match = False

            # 2. Gender check
            if req_gender != "any" and req_gender != gender:
                if sid == "sukanya-samriddhi" and has_girl_child:
                    pass  # Parent can be male or female
                elif sid == "pm-ujjwala" and gender != "female":
                    is_match = False
                    is_potential = True
                    reasons.append("Scheme is registered in the name of an adult female member of the household")

            # 3. Income check
            if max_income is not None and income > max_income:
                is_match = False

            # Scheme-specific matching logic
            if sid == "pm-kisan":
                if "farmer" in occupation or "agriculture" in occupation or owns_land:
                    is_match = True
                    reasons.append("You are engaged in agriculture and landholding")
                else:
                    is_match = False

            elif sid == "ayushman-bharat":
                if income <= 250000 or occupation in ["unorganized_worker", "laborer", "artisan", "street_vendor", "unemployed", "farmer"]:
                    is_match = True
                    reasons.append("Income within eligible bracket for SECC / NFSA healthcare coverage")

            elif sid == "pmay":
                if not owns_pucca_house and income <= 600000:
                    is_match = True
                    reasons.append("No pucca house owned and annual household income is within EWS/LIG slab")
                elif owns_pucca_house:
                    is_match = False

            elif sid == "pm-mudra":
                if age >= 18 and age <= 65 and occupation in ["entrepreneur", "business_owner", "artisan", "street_vendor", "trader", "self_employed", "other"]:
                    is_match = True
                    reasons.append("Eligible for collateral-free business/working capital loans up to ₹20 lakh")

            elif sid == "sukanya-samriddhi":
                if has_girl_child:
                    is_match = True
                    reasons.append("You have a daughter aged 10 or younger (highest 8.2% guaranteed interest)")
                else:
                    is_potential = True
                    reasons.append("Eligible if you have a girl child aged 10 or younger")
                    is_match = False

            elif sid == "pm-ujjwala":
                if (gender == "female" or is_potential) and income <= 200000:
                    if gender == "female":
                        is_match = True
                        reasons.append("Adult woman in eligible income bracket for free LPG connection & ₹300 subsidy")
                else:
                    is_match = False

            elif sid == "atal-pension":
                if 18 <= age <= 40:
                    is_match = True
                    reasons.append(f"At age {age}, you can lock in a guaranteed lifetime pension of ₹1,000 to ₹5,000/month")
                else:
                    is_match = False

            elif sid == "pm-vishwakarma":
                if occupation in ["artisan", "craftsperson", "carpenter", "blacksmith", "potter", "mason", "tailor", "barber"]:
                    is_match = True
                    reasons.append("Your trade qualifies for ₹15,000 toolkit voucher and 5% concessional credit")
                else:
                    is_potential = True
                    reasons.append("Applicable if you or a family member practice one of the 18 recognized traditional crafts")

            elif sid == "national-scholarship":
                if occupation == "student" and income <= 250000:
                    is_match = True
                    reasons.append("Enrolled student with family income under ₹2.5L qualifies for pre/post-matric & higher education scholarships")
                else:
                    is_match = False

            elif sid == "pm-svanidhi":
                if occupation in ["street_vendor", "hawker", "vendor", "small_seller"]:
                    is_match = True
                    reasons.append("Eligible for ₹10,000 to ₹50,000 collateral-free working capital loan with 7% interest subsidy")
                else:
                    is_match = False

            # Construct result entry
            entry = {
                "id": s["id"],
                "name": s["name"],
                "name_hi": s.get("name_hi", s["name"]),
                "category": s["category"],
                "brief": s["brief"],
                "official_url": s["official_url"],
                "documents_required": s.get("documents_required", []),
                "reasons": reasons
            }

            if is_match and reasons:
                eligible.append(entry)
            elif is_potential:
                potential.append(entry)

        return {
            "eligible_schemes_count": len(eligible),
            "eligible_schemes": eligible,
            "potential_schemes_count": len(potential),
            "potential_schemes": potential
        }
