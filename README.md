# 🏗️ Multimodal Construction Intelligence Platform

**Skill Wallet Capstone Project 1** · Platform ID: `6ac4c98d1dcde6d7857c1642`

> An AI-powered decision-support system for Indian construction professionals — analysing site photos for PPE compliance, classifying concrete cracks, estimating costs in INR, and providing weather-aware daily protocols.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

### 3. (Optional) Configure API Key
Add your Google Gemini API key in the sidebar to enable live AI analysis. The app runs in **demonstration mode** without a key.

---

## 📋 Features

| Module | Epic | Description |
|--------|------|-------------|
| 🦺 PPE Safety Audit | Epic 2 | Multimodal vision analysis of construction site photos for OSHA & IS 456 PPE compliance |
| 🔬 Crack Diagnostics | Epic 2 | Structural crack classification with repair recommendations (epoxy injection, CFRP, jacketing) |
| 📊 Planning & Valuation | Epic 3 | INR cost estimation, CapEx tracking, steel/cement requirements, Pollinations AI 3D renders |
| 💬 Site Assistant | Epic 5 | Multi-turn Gemini-powered chatbot for construction engineering Q&A |
| 🌦️ Weather Advisory | Epic 5 | Dynamic safety protocols for High Wind, Heavy Rain, Extreme Heat conditions |

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit 1.39 + Custom CSS |
| **AI Engine** | Google Gemini 1.5 Flash/Pro (multimodal) |
| **Image Processing** | Pillow (PIL) |
| **3D Rendering** | Pollinations AI / Flux API |
| **Data Format** | JSON Data Contracts |
| **Deployment** | Streamlit Community Cloud |

---

## 🏗️ Project Structure

```
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Theme & server config
└── utils/
    ├── __init__.py
    ├── helpers.py          # Gemini API, prompts, calculators
    ├── demo_data.py        # Fallback demonstration data
    └── styles.py           # CSS design system
```

---

## 🔑 API Key Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a free API key
3. Paste it in the sidebar **Gemini API Key** field
4. The app will validate and switch to live AI mode

> **Note:** The app runs fully in demonstration mode without an API key — great for exploration.

---

## ☁️ Streamlit Cloud Deployment

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file**: `app.py`
5. Add `GOOGLE_API_KEY` as a secret (optional)

---

## 📐 Standards & Compliance References

- **OSHA 29 CFR 1926** — Construction Safety Standards
- **IS 456:2000** — Plain & Reinforced Concrete Code
- **IS 3696** — Safety Code for Scaffolding
- **IS 13920** — Ductile Detailing for Seismic Zones
- **NBC 2016 Part 7** — National Building Code Safety
- **ACI 318-19** — Building Code for Concrete Structures

---

## 📄 License

MIT License · Built for Skill Wallet Capstone Program
