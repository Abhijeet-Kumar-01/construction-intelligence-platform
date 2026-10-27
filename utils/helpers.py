"""
Utility helpers: Gemini API wrappers, cost calculations, prompt builders.
"""

import json
import re
import math
from datetime import datetime
from io import BytesIO
from PIL import Image


# ─────────────────────────────────────────────
# Gemini API helpers
# ─────────────────────────────────────────────

def get_gemini_model(api_key: str, model_name: str = "gemini-1.5-flash"):
    """Initialise and return a Gemini GenerativeModel."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(model_name)
    except Exception as e:
        raise RuntimeError(f"Failed to initialise Gemini: {e}")


def image_to_pil(uploaded_file) -> Image.Image:
    """Convert Streamlit UploadedFile to PIL Image."""
    return Image.open(BytesIO(uploaded_file.read()))


def pil_to_bytes(img: Image.Image, fmt: str = "JPEG") -> bytes:
    buf = BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def extract_json(text: str) -> dict:
    """Extract the first JSON block from a model response string."""
    # Try ```json ... ``` fenced block first
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    # Fallback: find raw { ... }
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No JSON object found in model response.")


# ─────────────────────────────────────────────
# PPE Audit prompt
# ─────────────────────────────────────────────

PPE_SYSTEM_PROMPT = """
You are a certified construction site safety auditor with expertise in OSHA 29 CFR 1926 and Indian Standard IS 456:2000, IS 3696, and NBC 2016 Part 7 regulations.

Analyse the provided construction site photograph and return ONLY a valid JSON object (no markdown, no prose) in the exact schema below:

{
  "safety_score": <integer 0-100>,
  "overall_status": <"COMPLIANT" | "AT RISK" | "NON-COMPLIANT" | "CRITICAL VIOLATION">,
  "ppe_detection": {
    "helmets": {"detected": <bool>, "compliant_workers": <int>, "total_workers": <int>, "compliance_rate": "<string>%", "notes": "<string>"},
    "high_vis_vests": {"detected": <bool>, "compliant_workers": <int>, "total_workers": <int>, "compliance_rate": "<string>%", "notes": "<string>"},
    "steel_toe_boots": {"detected": <bool>, "compliant_workers": <int>, "total_workers": <int>, "compliance_rate": "<string>%", "notes": "<string>"},
    "safety_harnesses": {"detected": <bool>, "compliant_workers": <int>, "total_workers": <int>, "compliance_rate": "<string>%", "notes": "<string>"},
    "safety_gloves": {"detected": <bool>, "compliant_workers": <int>, "total_workers": <int>, "compliance_rate": "<string>%", "notes": "<string>"}
  },
  "site_hazards": [
    {"hazard": "<string>", "severity": "<Low|Medium|High|Critical>", "osha_reference": "<string>", "is_reference": "<string>", "corrective_remedy": "<string>"}
  ],
  "compliance_standards": ["<string>"],
  "recommendation_summary": "<string>",
  "audit_timestamp": "<ISO 8601 timestamp>"
}

Be precise: count visible workers and their PPE status. Identify all visible hazards. Assign safety_score based on overall compliance level.
"""


def run_ppe_audit(model, image: Image.Image) -> dict:
    """Run PPE audit using Gemini multimodal API."""
    import google.generativeai as genai
    response = model.generate_content(
        [PPE_SYSTEM_PROMPT, image],
        generation_config=genai.GenerationConfig(temperature=0.1, max_output_tokens=2048)
    )
    raw = response.text
    result = extract_json(raw)
    result["demo_mode"] = False
    return result


# ─────────────────────────────────────────────
# Crack Diagnostics prompt
# ─────────────────────────────────────────────

CRACK_SYSTEM_PROMPT = """
You are a senior structural engineer with expertise in concrete diagnostics per IS 456:2000, IS 13920, and ACI 318-19.

Analyse the provided image of a concrete/wall surface and return ONLY a valid JSON object (no markdown, no prose):

{
  "defect_type": "<Hairline Crack|Settlement Crack|Structural Shear Crack|Thermal Expansion Crack|Spalling|No Defect Detected>",
  "severity_level": "<Low|Medium|High|Critical>",
  "crack_width_mm": <float>,
  "crack_length_estimate_cm": <float>,
  "orientation": "<Horizontal|Vertical|Diagonal|Map/Crazing|Multiple>",
  "root_causes": ["<string>"],
  "affected_zone": "<string describing location/structural element>",
  "structural_risk": "<string describing risk to structural integrity>",
  "recommended_repairs": [
    {
      "repair": "<repair technique name>",
      "description": "<detailed procedure>",
      "urgency": "<Immediate|Within 7 days|Within 30 days|Planned Maintenance>",
      "estimated_cost_inr": "<cost range string in INR>"
    }
  ],
  "monitoring_protocol": "<string>",
  "is_standard_reference": "<string>",
  "requires_structural_engineer": <bool>
}

Provide precise engineering assessment. Crack width < 0.3mm = Hairline; 0.3-1mm = Medium; 1-3mm = High; >3mm = Critical.
"""


def run_crack_diagnostics(model, image: Image.Image) -> dict:
    """Run crack diagnostics using Gemini multimodal API."""
    import google.generativeai as genai
    response = model.generate_content(
        [CRACK_SYSTEM_PROMPT, image],
        generation_config=genai.GenerationConfig(temperature=0.1, max_output_tokens=2048)
    )
    raw = response.text
    result = extract_json(raw)
    result["demo_mode"] = False
    return result


# ─────────────────────────────────────────────
# Construction Cost & Valuation Calculator
# ─────────────────────────────────────────────

# Cost per sqft in INR by structure type and city tier
COST_MATRIX = {
    "Residential Apartment": {"Tier 1": 3800, "Tier 2": 2800, "Tier 3": 1900},
    "Commercial Office": {"Tier 1": 5500, "Tier 2": 4200, "Tier 3": 3000},
    "Industrial Warehouse": {"Tier 1": 2200, "Tier 2": 1700, "Tier 3": 1200},
    "Luxury Villa": {"Tier 1": 7500, "Tier 2": 5500, "Tier 3": 4000},
    "Hospital / Healthcare": {"Tier 1": 8500, "Tier 2": 6500, "Tier 3": 4500},
    "Educational Institution": {"Tier 1": 4500, "Tier 2": 3500, "Tier 3": 2500},
}

# Market multiplier for real estate valuation
MARKET_MULTIPLIER = {
    "Tier 1": 2.8,   # Mumbai, Delhi, Bengaluru, Chennai
    "Tier 2": 1.9,   # Pune, Hyderabad, Ahmedabad, Jaipur
    "Tier 3": 1.4,   # Smaller cities
}

# Steel and cement ratios
STEEL_KG_PER_SQFT = {"Residential Apartment": 4.5, "Commercial Office": 6.0, "Industrial Warehouse": 3.5, "Luxury Villa": 5.5, "Hospital / Healthcare": 7.0, "Educational Institution": 5.0}
CEMENT_BAGS_PER_SQFT = {"Residential Apartment": 0.55, "Commercial Office": 0.7, "Industrial Warehouse": 0.45, "Luxury Villa": 0.65, "Hospital / Healthcare": 0.8, "Educational Institution": 0.6}


def calculate_project_metrics(
    structure_type: str,
    builtup_sqft: float,
    location_tier: str,
    completion_pct: float
) -> dict:
    """Calculate cost, valuation and material metrics."""
    cost_per_sqft = COST_MATRIX.get(structure_type, {}).get(location_tier, 3000)
    total_budget = builtup_sqft * cost_per_sqft
    capex_incurred = total_budget * (completion_pct / 100)
    market_mult = MARKET_MULTIPLIER.get(location_tier, 1.5)
    asset_valuation = total_budget * market_mult * (0.4 + 0.6 * completion_pct / 100)

    # Materials
    steel_total_kg = builtup_sqft * STEEL_KG_PER_SQFT.get(structure_type, 5.0)
    steel_used_kg = steel_total_kg * (completion_pct / 100)
    cement_total_bags = builtup_sqft * CEMENT_BAGS_PER_SQFT.get(structure_type, 0.6)
    cement_used_bags = cement_total_bags * (completion_pct / 100)

    def to_display(amount_inr):
        if amount_inr >= 1e7:
            return f"₹{amount_inr/1e7:.2f} Cr"
        elif amount_inr >= 1e5:
            return f"₹{amount_inr/1e5:.2f} L"
        else:
            return f"₹{amount_inr:,.0f}"

    # Milestones
    milestones = [
        {"name": "Foundation & Excavation", "threshold": 15},
        {"name": "Structural Framework", "threshold": 35},
        {"name": "Masonry & Roofing", "threshold": 55},
        {"name": "MEP & Finishing", "threshold": 75},
        {"name": "Handover Ready", "threshold": 95},
    ]
    completed_milestones = [m for m in milestones if completion_pct >= m["threshold"]]

    return {
        "cost_per_sqft": cost_per_sqft,
        "total_budget_inr": total_budget,
        "total_budget_display": to_display(total_budget),
        "capex_incurred_inr": capex_incurred,
        "capex_incurred_display": to_display(capex_incurred),
        "asset_valuation_inr": asset_valuation,
        "asset_valuation_display": to_display(asset_valuation),
        "steel_total_mt": round(steel_total_kg / 1000, 2),
        "steel_used_mt": round(steel_used_kg / 1000, 2),
        "cement_total_bags": round(cement_total_bags),
        "cement_used_bags": round(cement_used_bags),
        "milestones": milestones,
        "completed_milestones": len(completed_milestones),
        "total_milestones": len(milestones),
    }


# ─────────────────────────────────────────────
# Chatbot helpers
# ─────────────────────────────────────────────

CHATBOT_SYSTEM_PROMPT = """You are ConstructBot, an expert AI assistant specialising in construction engineering, Indian building codes (IS 456, IS 13920, NBC 2016), OSHA safety regulations, real estate valuation, and project planning. 

You provide precise, actionable answers to construction professionals in India. Always cite relevant IS standards or OSHA regulations where applicable. Keep answers concise but technically rich. Use bullet points for lists. Format costs in INR (Lakhs/Crores). Always recommend consulting a licensed structural engineer for safety-critical matters."""


def run_chatbot(model, conversation_history: list, user_message: str) -> str:
    """Run a chatbot turn using Gemini."""
    import google.generativeai as genai
    # Build conversation with system prompt injected
    messages = [CHATBOT_SYSTEM_PROMPT, "\n\n"]
    for turn in conversation_history:
        role_prefix = "User: " if turn["role"] == "user" else "Assistant: "
        messages.append(f"{role_prefix}{turn['content']}\n")
    messages.append(f"User: {user_message}\nAssistant:")

    full_prompt = "".join(messages)
    response = model.generate_content(
        full_prompt,
        generation_config=genai.GenerationConfig(temperature=0.7, max_output_tokens=1024)
    )
    return response.text.strip()


def get_demo_chat_response(user_message: str) -> str:
    """Return a realistic demo response when no API key is set."""
    user_lower = user_message.lower()
    if any(w in user_lower for w in ["ppe", "helmet", "safety", "harness"]):
        return """**PPE Requirements on Indian Construction Sites (IS 3696 & NBC 2016):**

- **Hard Hats**: Mandatory for all personnel per IS 2925. Class B for electrical zones.
- **High-Vis Vests**: Retro-reflective per IS 15809 — minimum Class 2 in active zones.
- **Safety Harnesses**: Full-body harness + double lanyard required above 1.8m (IS 3521).
- **Steel-Toe Boots**: IS 15298 compliance for all site workers.
- **Gloves**: Cut-resistant per IS 6994 for manual handling.

> **OSHA Reference**: 29 CFR 1926 Subpart E mandates PPE selection based on hazard assessment.

Would you like a specific PPE checklist for a particular trade?"""
    elif any(w in user_lower for w in ["crack", "structural", "repair", "concrete"]):
        return """**Concrete Crack Classification & Repair Guide (IS 456:2000):**

| Crack Width | Classification | Action Required |
|-------------|---------------|-----------------|
| < 0.1 mm | Hairline | Monitor quarterly |
| 0.1–0.3 mm | Fine | Seal with elastomeric sealant |
| 0.3–1.0 mm | Medium | Epoxy injection grouting |
| > 1.0 mm | Wide/Structural | Structural engineer assessment + CFRP/jacketing |

**Key Remediation Techniques:**
- **Epoxy Injection**: ₹18,000–35,000/running metre — for structural cracks
- **CFRP Wrapping**: ₹45,000–90,000/column — restores tensile capacity  
- **Concrete Jacketing**: ₹1.2L–2.5L/element — full section restoration

Always engage a Licensed Structural Engineer for cracks exceeding 0.3mm in load-bearing elements."""
    elif any(w in user_lower for w in ["cost", "budget", "valuation", "price", "estimate"]):
        return """**Construction Cost Benchmarks — India 2024-25:**

| Structure Type | Tier 1 (₹/sqft) | Tier 2 (₹/sqft) | Tier 3 (₹/sqft) |
|----------------|------------------|------------------|------------------|
| Residential Apt | ₹3,800 | ₹2,800 | ₹1,900 |
| Commercial Office | ₹5,500 | ₹4,200 | ₹3,000 |
| Luxury Villa | ₹7,500 | ₹5,500 | ₹4,000 |
| Hospital | ₹8,500 | ₹6,500 | ₹4,500 |

**Valuation Multipliers**: Tier 1 cities command 2.8x construction cost as market value.

Use the **Planning & Valuation** tab for a detailed project-specific estimate with material quantities."""
    elif any(w in user_lower for w in ["weather", "rain", "wind", "heat", "temperature"]):
        return """**Weather-Aware Construction Protocols:**

**Heavy Rain (>50mm/day):**
- Halt all open excavations > 1.5m depth
- Cover fresh concrete (< 24h old) with polythene
- De-energise all temporary electrical near water

**High Wind (> 45 km/h per IS 875 Part 3):**
- Suspend all crane operations immediately
- Secure loose formwork and sheeting
- Ground all AWP and scissor lifts

**Extreme Heat (> 40°C):**
- Reschedule concrete pours to 05:00–09:00 hrs
- Mandatory water breaks every 30 minutes
- Use fly ash/GGBS to reduce heat of hydration

Check the **Site Assistant** tab for live weather-specific protocols."""
    else:
        return f"""Thank you for your question about **"{user_message}"**.

As ConstructBot, I can help you with:

- 🏗️ **Structural Engineering** — IS 456, IS 13920, NBC 2016 compliance
- 🦺 **Site Safety** — PPE requirements, OSHA regulations, hazard assessment
- 💰 **Cost Estimation** — Construction budgets, real estate valuation in INR
- 🌦️ **Weather Protocols** — Daily safety advisories based on site conditions
- 📋 **Project Planning** — Milestones, material requirements, scheduling

*Please note: This is demonstration mode. Connect a **Google Gemini API key** in the sidebar for full AI-powered responses tailored to your specific query.*

Could you provide more details about your specific construction challenge?"""
