"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1
"""

import streamlit as st
import json
import time
import requests
from datetime import datetime
from io import BytesIO
import urllib.parse

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Local Imports ───────────────────────────────────────────────────────────
from utils.styles import MAIN_CSS
from utils.demo_data import DEMO_PPE_REPORT, DEMO_CRACK_REPORT, WEATHER_PROTOCOLS
from utils.helpers import (
    get_gemini_model, image_to_pil, extract_json,
    run_ppe_audit, run_crack_diagnostics,
    calculate_project_metrics, run_chatbot, get_demo_chat_response,
    COST_MATRIX
)

# ─── Inject CSS ──────────────────────────────────────────────────────────────
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "ppe_report" not in st.session_state:
    st.session_state.ppe_report = None
if "crack_report" not in st.session_state:
    st.session_state.crack_report = None
if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = None
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem 0 1.25rem 0;'>
        <div style='font-size:2.5rem;'>🏗️</div>
        <div style='font-size:1rem; font-weight:800; color:#F5A623; letter-spacing:-0.3px;'>Construction AI</div>
        <div style='font-size:0.72rem; color:#64748B; margin-top:0.2rem;'>Multimodal Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # ── API Key Input ──
    st.markdown("### 🔑 Gemini API Key")
    api_key_input = st.text_input(
        "Enter your Google Gemini API key",
        type="password",
        placeholder="AIza...",
        help="Get your free key at https://makersuite.google.com/app/apikey",
        key="api_key_field",
        label_visibility="collapsed"
    )

    if api_key_input:
        with st.spinner("Validating API key…"):
            try:
                model = get_gemini_model(api_key_input)
                # Quick validation call
                test = model.generate_content("Reply with just: OK")
                st.session_state.gemini_model = model
                st.session_state.api_key_valid = True
                st.success("✅ API key validated — AI mode active")
            except Exception as e:
                st.session_state.api_key_valid = False
                st.session_state.gemini_model = None
                st.error(f"❌ Invalid key: {str(e)[:60]}")
    else:
        st.session_state.api_key_valid = False
        st.session_state.gemini_model = None
        st.markdown("""
        <div class='demo-banner'>
            🎭 <strong>Demonstration Mode</strong><br>
            Running with pre-built AI responses. Add a Gemini API key above to enable live multimodal analysis.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Architecture Overview ──
    st.markdown("### 🧱 Tech Architecture")
    arch_items = [
        ("🐍", "Python 3.9+ · FastAPI-ready"),
        ("🎨", "Streamlit · Responsive UI"),
        ("🤖", "Google Gemini 1.5 Flash/Pro"),
        ("🖼️", "Pillow · Multimodal Vision"),
        ("🎲", "Pollinations AI · 3D Renders"),
        ("📋", "JSON Data Contracts"),
        ("☁️", "Streamlit Cloud Deploy"),
    ]
    for icon, text in arch_items:
        st.markdown(f"""
        <div class='arch-item'>
            <span>{icon}</span>
            <span style='color:#94A3B8;'>{text}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Feature Navigation ──
    st.markdown("### 📋 Module Coverage")
    epics = [
        ("✅", "Epic 1", "Environment & Prerequisites"),
        ("🦺", "Epic 2", "PPE Vision & Crack Diagnostics"),
        ("📊", "Epic 3", "Planning & Valuation"),
        ("🔗", "Epic 4", "Multimodal AI & JSON Contracts"),
        ("💬", "Epic 5", "Chatbot & Weather Advisory"),
        ("☁️", "Epic 6", "Interface & Deployment"),
    ]
    for icon, epic, title in epics:
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:0.5rem; padding:0.4rem 0; font-size:0.78rem;'>
            <span style='font-size:1rem;'>{icon}</span>
            <span style='color:#F5A623; font-weight:700; min-width:52px;'>{epic}</span>
            <span style='color:#64748B;'>{title}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown(f"""
    <div style='font-size:0.7rem; color:#334155; text-align:center; line-height:1.6;'>
        Platform ID: 6ac4c98d1dcde6d7857c1642<br>
        Skill Wallet Capstone · Project 1<br>
        {datetime.now().strftime("%d %b %Y, %H:%M")}
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='hero-header'>
    <div class='hero-badge'>⚡ Generative AI · Real Estate Decision Support</div>
    <h1 class='hero-title'>Multimodal Construction Intelligence Platform</h1>
    <p class='hero-subtitle'>AI-powered site safety audits, structural diagnostics, cost estimation & weather-aware protocols — built for Indian construction professionals.</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺  Site Safety & PPE Audit",
    "🔬  Crack Diagnostics",
    "📊  Planning & Valuation",
    "💬  Site Assistant & Weather"
])


# ───────────────────────────────────────────────────────────────────────────────
# TAB 1 — PPE SAFETY AUDIT
# ───────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <div class='section-header'>
        <div class='section-icon'>🦺</div>
        <div>
            <div class='section-title'>Site Safety & PPE Compliance Audit</div>
            <div style='font-size:0.75rem; color:#64748B; margin-top:0.1rem;'>OSHA 29 CFR 1926 · IS 456:2000 · IS 3696 · NBC 2016</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_upload, col_info = st.columns([3, 2])

    with col_upload:
        uploaded_ppe = st.file_uploader(
            "Upload construction site photo",
            type=["jpg", "jpeg", "png", "webp"],
            key="ppe_uploader",
            help="Upload a clear photo of your construction site for PPE analysis"
        )

        if uploaded_ppe:
            st.image(uploaded_ppe, caption="Uploaded Site Photo", use_column_width=True)
            uploaded_ppe.seek(0)

    with col_info:
        st.markdown("""
        <div style='background:rgba(245,166,35,0.06); border:1px solid rgba(245,166,35,0.2); border-radius:12px; padding:1.25rem; height:100%;'>
            <div style='font-weight:700; margin-bottom:0.75rem; color:#F5A623;'>📋 What Gets Analysed</div>
            <div style='font-size:0.82rem; color:#94A3B8; line-height:1.8;'>
                ✓ &nbsp;<strong>Hard Hats</strong> — IS 2925 compliance<br>
                ✓ &nbsp;<strong>High-Vis Vests</strong> — IS 15809 retro-reflectivity<br>
                ✓ &nbsp;<strong>Steel-Toe Boots</strong> — IS 15298 standard<br>
                ✓ &nbsp;<strong>Safety Harnesses</strong> — IS 3521 (height work)<br>
                ✓ &nbsp;<strong>Safety Gloves</strong> — IS 6994<br><br>
                <strong style='color:#F5A623;'>Output:</strong> Safety score (0–100), hazard severity matrix with OSHA citations, corrective action plan.
            </div>
        </div>
        """, unsafe_allow_html=True)

    analyze_btn = st.button("🔍 Run PPE Safety Audit", key="btn_ppe_audit", use_container_width=True)

    if analyze_btn:
        with st.spinner("🤖 AI analysing site safety and PPE compliance…"):
            time.sleep(0.5)
            try:
                if st.session_state.api_key_valid and uploaded_ppe:
                    uploaded_ppe.seek(0)
                    img = image_to_pil(uploaded_ppe)
                    result = run_ppe_audit(st.session_state.gemini_model, img)
                else:
                    result = DEMO_PPE_REPORT
                    if not uploaded_ppe:
                        st.info("ℹ️ No image uploaded — showing demonstration report. Upload a photo for live analysis.")
                st.session_state.ppe_report = result
            except Exception as e:
                st.error(f"Analysis failed: {e}. Showing demo data.")
                st.session_state.ppe_report = DEMO_PPE_REPORT

    # ── Render PPE Report ──
    if st.session_state.ppe_report:
        report = st.session_state.ppe_report

        if report.get("demo_mode"):
            st.markdown("""
            <div class='demo-banner' style='margin-bottom:0.75rem;'>
                🎭 <strong>Demonstration Report</strong> — This is sample output. Upload a site photo + API key for live analysis.
            </div>""", unsafe_allow_html=True)

        # Score + Status
        score = report.get("safety_score", 0)
        status = report.get("overall_status", "UNKNOWN")

        score_class = "score-good" if score >= 80 else ("score-warning" if score >= 50 else "score-danger")
        if "CRITICAL" in status:
            score_class = "score-critical"

        pill_class = {
            "COMPLIANT": "pill-compliant",
            "AT RISK": "pill-at-risk",
            "NON-COMPLIANT": "pill-non-compliant",
            "CRITICAL VIOLATION": "pill-critical"
        }.get(status, "pill-at-risk")

        col_score, col_status = st.columns([1, 3])
        with col_score:
            st.markdown(f"""
            <div class='score-container'>
                <div class='score-circle {score_class}'>{score}</div>
                <div style='font-size:0.75rem; color:#64748B; font-weight:600;'>SAFETY SCORE</div>
            </div>
            """, unsafe_allow_html=True)
        with col_status:
            st.markdown(f"""
            <div style='padding:1rem 0;'>
                <div style='margin-bottom:0.5rem;'>
                    <span class='status-pill {pill_class}'>● {status}</span>
                </div>
                <div style='font-size:0.85rem; color:#94A3B8; line-height:1.7; max-width:500px;'>
                    {report.get("recommendation_summary", "")}
                </div>
                <div style='margin-top:0.75rem; font-size:0.72rem; color:#475569;'>
                    Standards: {", ".join(report.get("compliance_standards", []))}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # PPE Checklist
        st.markdown("<div class='section-header'><div class='section-icon'>✅</div><div class='section-title'>PPE Detection Checklist</div></div>", unsafe_allow_html=True)

        ppe_icons = {"helmets": "⛑️", "high_vis_vests": "🦺", "steel_toe_boots": "👢", "safety_harnesses": "🔒", "safety_gloves": "🧤"}
        ppe_labels = {"helmets": "Hard Hats", "high_vis_vests": "Hi-Vis Vests", "steel_toe_boots": "Steel-Toe Boots", "safety_harnesses": "Safety Harnesses", "safety_gloves": "Safety Gloves"}

        ppe_data = report.get("ppe_detection", {})
        for key, data in ppe_data.items():
            rate_str = data.get("compliance_rate", "0%")
            try:
                rate_num = int(rate_str.replace("%", ""))
            except:
                rate_num = 0
            detected = data.get("detected", False)
            icon = ppe_icons.get(key, "📋")
            label = ppe_labels.get(key, key.replace("_", " ").title())
            color = "#00C851" if rate_num >= 80 else ("#FF8C00" if rate_num >= 50 else "#FF4444")
            det_class = "ppe-detected-yes" if detected else "ppe-detected-no"

            st.markdown(f"""
            <div class='ppe-item'>
                <div>
                    <div class='ppe-name'>{icon} {label}</div>
                    <div class='ppe-notes'>{data.get("notes", "")}</div>
                </div>
                <div style='text-align:right;'>
                    <div class='ppe-rate' style='color:{color};'>{rate_str}</div>
                    <div style='font-size:0.72rem;' class='{det_class}'>
                        {"✓ Detected" if detected else "✗ Not Detected"}
                        &nbsp;·&nbsp; {data.get("compliant_workers", 0)}/{data.get("total_workers", 0)} workers
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Hazards
        hazards = report.get("site_hazards", [])
        if hazards:
            st.markdown("<div class='section-header'><div class='section-icon'>⚠️</div><div class='section-title'>Identified Site Hazards</div></div>", unsafe_allow_html=True)
            for hazard in hazards:
                sev = hazard.get("severity", "Medium").lower()
                sev_colors = {"critical": "#DC143C", "high": "#FF4444", "medium": "#FF8C00", "low": "#FFD176"}
                sev_color = sev_colors.get(sev, "#FF8C00")
                st.markdown(f"""
                <div class='hazard-card {sev}'>
                    <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;'>
                        <div class='hazard-title'>⚠️ {hazard.get("hazard", "")}</div>
                        <span class='status-pill' style='background:rgba(255,255,255,0.05); border:1px solid {sev_color}; color:{sev_color}; white-space:nowrap;'>{hazard.get("severity","").upper()}</span>
                    </div>
                    <div class='hazard-remedy'>🔧 {hazard.get("corrective_remedy", "")}</div>
                    <div class='hazard-refs'>{hazard.get("osha_reference", "")} &nbsp;|&nbsp; {hazard.get("is_reference", "")}</div>
                </div>
                """, unsafe_allow_html=True)

        # Download
        st.markdown("<br>", unsafe_allow_html=True)
        col_dl1, col_dl2 = st.columns([1, 3])
        with col_dl1:
            st.download_button(
                label="⬇️ Download JSON Report",
                data=json.dumps(report, indent=2),
                file_name=f"ppe_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )


# ───────────────────────────────────────────────────────────────────────────────
# TAB 2 — CRACK DIAGNOSTICS
# ───────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("""
    <div class='section-header'>
        <div class='section-icon'>🔬</div>
        <div>
            <div class='section-title'>Concrete Crack Diagnostics & Structural Integrity</div>
            <div style='font-size:0.75rem; color:#64748B; margin-top:0.1rem;'>IS 456:2000 · IS 13920 · ACI 318-19 · Structural Engineering Standards</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_crack_up, col_crack_info = st.columns([3, 2])

    with col_crack_up:
        uploaded_crack = st.file_uploader(
            "Upload concrete / wall surface photo",
            type=["jpg", "jpeg", "png", "webp"],
            key="crack_uploader",
            help="Upload a clear close-up photo of the crack or concrete defect"
        )
        if uploaded_crack:
            st.image(uploaded_crack, caption="Uploaded Surface Photo", use_column_width=True)
            uploaded_crack.seek(0)

    with col_crack_info:
        st.markdown("""
        <div style='background:rgba(59,140,248,0.06); border:1px solid rgba(59,140,248,0.2); border-radius:12px; padding:1.25rem; height:100%;'>
            <div style='font-weight:700; margin-bottom:0.75rem; color:#3B8CF8;'>🔬 Defect Classification</div>
            <div style='font-size:0.82rem; color:#94A3B8; line-height:1.9;'>
                ↔ <strong>Hairline</strong> — &lt; 0.1mm, cosmetic<br>
                ↔ <strong>Settlement</strong> — Foundation movement<br>
                ↔ <strong>Structural Shear</strong> — Load/seismic related<br>
                ↔ <strong>Thermal Expansion</strong> — Temperature cycles<br>
                ↔ <strong>Spalling</strong> — Rebar corrosion / freeze<br><br>
                <strong style='color:#3B8CF8;'>Output:</strong> Crack width (mm), repair recommendations with INR cost estimates, urgency classification.
            </div>
        </div>
        """, unsafe_allow_html=True)

    analyze_crack_btn = st.button("🔍 Run Crack Diagnostics", key="btn_crack", use_container_width=True)

    if analyze_crack_btn:
        with st.spinner("🤖 AI classifying defect and assessing structural integrity…"):
            time.sleep(0.5)
            try:
                if st.session_state.api_key_valid and uploaded_crack:
                    uploaded_crack.seek(0)
                    img = image_to_pil(uploaded_crack)
                    result = run_crack_diagnostics(st.session_state.gemini_model, img)
                else:
                    result = DEMO_CRACK_REPORT
                    if not uploaded_crack:
                        st.info("ℹ️ No image uploaded — showing demonstration report. Upload a photo for live analysis.")
                st.session_state.crack_report = result
            except Exception as e:
                st.error(f"Analysis failed: {e}. Showing demo data.")
                st.session_state.crack_report = DEMO_CRACK_REPORT

    # ── Render Crack Report ──
    if st.session_state.crack_report:
        rep = st.session_state.crack_report

        if rep.get("demo_mode"):
            st.markdown("""<div class='demo-banner'>🎭 <strong>Demonstration Report</strong> — Upload a crack photo + API key for live analysis.</div>""", unsafe_allow_html=True)

        sev = rep.get("severity_level", "Medium")
        sev_colors_map = {"Low": "#00C851", "Medium": "#FF8C00", "High": "#FF4444", "Critical": "#DC143C"}
        sev_color = sev_colors_map.get(sev, "#FF8C00")
        sev_bg = f"rgba({{'Low':'0,200,81', 'Medium':'255,140,0', 'High':'255,68,68', 'Critical':'220,20,60'}}.get(sev, '255,140,0'), 0.1)"

        # Main defect header
        col_defect, col_metrics = st.columns([3, 2])
        with col_defect:
            st.markdown(f"""
            <div style='background:{sev_bg}; border:1px solid {sev_color}40; border-radius:12px; padding:1.25rem; margin-bottom:1rem;'>
                <div style='font-size:0.72rem; color:{sev_color}; font-weight:700; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:0.4rem;'>Defect Classification</div>
                <div style='font-size:1.4rem; font-weight:800; color:#F8FAFC;'>{rep.get("defect_type", "Unknown Defect")}</div>
                <div style='font-size:0.82rem; color:#94A3B8; margin-top:0.3rem;'>{rep.get("orientation", "")} · Zone: {rep.get("affected_zone", "")}</div>
                <div style='margin-top:0.75rem; font-size:0.82rem; color:#94A3B8;'>
                    <strong style='color:#F8FAFC;'>Structural Risk:</strong> {rep.get("structural_risk", "")}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if rep.get("requires_structural_engineer"):
                st.warning("⚠️ **Structural Engineer Required** — This defect classification mandates assessment by a Licensed Structural Engineer per IS 456:2000.")

        with col_metrics:
            st.markdown(f"""
            <div class='metric-grid' style='grid-template-columns:1fr 1fr;'>
                <div class='metric-card red'>
                    <div class='metric-label'>Crack Width</div>
                    <div class='metric-value'>{rep.get("crack_width_mm", 0)}</div>
                    <div class='metric-sub'>millimetres</div>
                </div>
                <div class='metric-card orange'>
                    <div class='metric-label'>Length Est.</div>
                    <div class='metric-value'>{rep.get("crack_length_estimate_cm", 0)}</div>
                    <div class='metric-sub'>centimetres</div>
                </div>
                <div class='metric-card' style='border-left-color:{sev_color};'>
                    <div class='metric-label'>Severity</div>
                    <div class='metric-value' style='font-size:1.1rem; color:{sev_color};'>{sev}</div>
                    <div class='metric-sub'>Risk Level</div>
                </div>
                <div class='metric-card blue'>
                    <div class='metric-label'>Repairs</div>
                    <div class='metric-value'>{len(rep.get("recommended_repairs", []))}</div>
                    <div class='metric-sub'>recommended</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Root Causes
        causes = rep.get("root_causes", [])
        if causes:
            st.markdown("<div class='section-header'><div class='section-icon'>🔎</div><div class='section-title'>Root Cause Analysis</div></div>", unsafe_allow_html=True)
            causes_html = "".join([f"<li>{c}</li>" for c in causes])
            st.markdown(f"""
            <div style='background:#1E2435; border:1px solid rgba(255,255,255,0.07); border-radius:10px; padding:1rem 1.5rem;'>
                <ul class='alert-list'>{causes_html}</ul>
            </div>
            """, unsafe_allow_html=True)

        # Repair Recommendations
        repairs = rep.get("recommended_repairs", [])
        if repairs:
            st.markdown("<div class='section-header'><div class='section-icon'>🔧</div><div class='section-title'>Recommended Engineering Repairs</div></div>", unsafe_allow_html=True)
            for repair in repairs:
                urgency = repair.get("urgency", "")
                tag_class = "tag-urgent" if "Immediate" in urgency else ("tag-soon" if "7" in urgency else "tag-planned")
                st.markdown(f"""
                <div class='repair-card'>
                    <div class='repair-title'>🔩 {repair.get("repair", "")}</div>
                    <div class='repair-desc'>{repair.get("description", "")}</div>
                    <div class='repair-meta'>
                        <span class='repair-tag {tag_class}'>⏱ {urgency}</span>
                        <span class='repair-tag tag-cost'>💰 {repair.get("estimated_cost_inr", "")}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Monitoring Protocol
        if rep.get("monitoring_protocol"):
            st.info(f"📡 **Monitoring Protocol:** {rep.get('monitoring_protocol')}")

        st.markdown(f"""
        <div style='font-size:0.72rem; color:#475569; margin-top:0.5rem;'>
            📚 Standards Reference: {rep.get("is_standard_reference", "")}
        </div>
        """, unsafe_allow_html=True)

        col_dl2a, col_dl2b = st.columns([1, 3])
        with col_dl2a:
            st.download_button(
                label="⬇️ Download Diagnostic Report",
                data=json.dumps(rep, indent=2),
                file_name=f"crack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )


# ───────────────────────────────────────────────────────────────────────────────
# TAB 3 — PLANNING & REAL ESTATE VALUATION
# ───────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class='section-header'>
        <div class='section-icon'>📊</div>
        <div>
            <div class='section-title'>Project Planning & Real Estate Valuation</div>
            <div style='font-size:0.75rem; color:#64748B; margin-top:0.1rem;'>Live cost estimation in INR · Material requirements · Asset valuation · 3D Architectural Rendering</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Input Panel
    col_inp1, col_inp2 = st.columns(2)
    with col_inp1:
        structure_type = st.selectbox(
            "🏢 Structure Type",
            options=list(COST_MATRIX.keys()),
            index=0
        )
        location_tier = st.selectbox(
            "📍 Location Tier",
            options=["Tier 1", "Tier 2", "Tier 3"],
            index=0,
            help="Tier 1: Mumbai, Delhi, Bengaluru, Chennai, Hyderabad | Tier 2: Pune, Ahmedabad, Jaipur | Tier 3: Smaller cities"
        )

    with col_inp2:
        builtup_sqft = st.number_input(
            "📐 Built-up Area (sq.ft)",
            min_value=500,
            max_value=500000,
            value=5000,
            step=100,
            format="%d"
        )
        completion_pct = st.slider(
            "🏗️ Completion Percentage",
            min_value=0,
            max_value=100,
            value=45,
            step=1,
            format="%d%%"
        )

    calc_btn = st.button("📊 Calculate Project Metrics", key="btn_calc", use_container_width=True)

    # Auto-calculate on input change too
    metrics = calculate_project_metrics(structure_type, builtup_sqft, location_tier, completion_pct)

    # ── Valuation Cards ──
    st.markdown("""
    <div class='section-header'><div class='section-icon'>💰</div><div class='section-title'>Financial Overview</div></div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='valuation-grid'>
        <div class='val-card'>
            <div class='val-amount'>{metrics['total_budget_display']}</div>
            <div class='val-label'>Total Project Budget</div>
            <div class='val-sub'>₹{metrics['cost_per_sqft']:,}/sqft · {location_tier} {structure_type}</div>
        </div>
        <div class='val-card'>
            <div class='val-amount' style='color:#3B8CF8;'>{metrics['capex_incurred_display']}</div>
            <div class='val-label'>CapEx Incurred</div>
            <div class='val-sub'>{completion_pct}% completion · Invested to date</div>
        </div>
        <div class='val-card'>
            <div class='val-amount' style='color:#00C851;'>{metrics['asset_valuation_display']}</div>
            <div class='val-label'>Current Market Valuation</div>
            <div class='val-sub'>Real estate market estimate · {location_tier} multiplier</div>
        </div>
        <div class='val-card'>
            <div class='val-amount' style='color:#9C6FDE;'>₹{metrics['cost_per_sqft']:,}</div>
            <div class='val-label'>Cost Per Sq.Ft</div>
            <div class='val-sub'>{structure_type} · {location_tier} benchmark</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Progress Bar ──
    st.markdown(f"""
    <div style='margin:1.25rem 0;'>
        <div style='display:flex; justify-content:space-between; margin-bottom:0.4rem;'>
            <span style='font-size:0.82rem; font-weight:600;'>Project Completion</span>
            <span style='font-size:0.82rem; color:#F5A623; font-weight:700;'>{completion_pct}%</span>
        </div>
        <div class='progress-bar-container' style='height:14px;'>
            <div class='progress-bar-fill' style='width:{completion_pct}%;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Material Requirements ──
    col_mat1, col_mat2 = st.columns(2)
    with col_mat1:
        st.markdown("""
        <div class='section-header'><div class='section-icon'>🏗️</div><div class='section-title'>Steel Requirements</div></div>
        """, unsafe_allow_html=True)
        steel_pct = int((metrics['steel_used_mt'] / metrics['steel_total_mt'] * 100)) if metrics['steel_total_mt'] > 0 else 0
        st.markdown(f"""
        <div class='metric-card' style='margin-bottom:0.75rem;'>
            <div class='metric-label'>Total Steel Requirement</div>
            <div class='metric-value'>{metrics['steel_total_mt']} MT</div>
            <div class='metric-sub'>Metric tonnes for complete structure</div>
        </div>
        <div class='metric-card green'>
            <div class='metric-label'>Steel Used So Far</div>
            <div class='metric-value'>{metrics['steel_used_mt']} MT</div>
            <div class='metric-sub'>{steel_pct}% consumed · ₹58,000/MT average</div>
        </div>
        <div class='progress-bar-container'>
            <div class='progress-bar-fill' style='width:{steel_pct}%; background:linear-gradient(90deg,#3B8CF8,#60A5FA);'></div>
        </div>
        """, unsafe_allow_html=True)

    with col_mat2:
        st.markdown("""
        <div class='section-header'><div class='section-icon'>🏛️</div><div class='section-title'>Cement Requirements</div></div>
        """, unsafe_allow_html=True)
        cement_pct = int((metrics['cement_used_bags'] / metrics['cement_total_bags'] * 100)) if metrics['cement_total_bags'] > 0 else 0
        st.markdown(f"""
        <div class='metric-card' style='margin-bottom:0.75rem;'>
            <div class='metric-label'>Total Cement Requirement</div>
            <div class='metric-value'>{metrics['cement_total_bags']:,}</div>
            <div class='metric-sub'>50kg bags for complete structure</div>
        </div>
        <div class='metric-card orange'>
            <div class='metric-label'>Cement Used So Far</div>
            <div class='metric-value'>{metrics['cement_used_bags']:,}</div>
            <div class='metric-sub'>{cement_pct}% consumed · ₹380/bag average</div>
        </div>
        <div class='progress-bar-container'>
            <div class='progress-bar-fill' style='width:{cement_pct}%; background:linear-gradient(90deg,#F5A623,#FFD176);'></div>
        </div>
        """, unsafe_allow_html=True)

    # ── Milestone Tracker ──
    st.markdown("""
    <div class='section-header'><div class='section-icon'>🎯</div><div class='section-title'>Construction Milestone Progress</div></div>
    """, unsafe_allow_html=True)

    milestones = metrics["milestones"]
    completed_count = metrics["completed_milestones"]

    milestone_html = "<div class='milestone-track'>"
    for i, m in enumerate(milestones):
        done = completion_pct >= m["threshold"]
        dot_class = "done" if done else "pending"
        label_class = "done" if done else ""
        symbol = "✓" if done else str(i + 1)
        milestone_html += f"""
        <div class='milestone-node'>
            <div class='milestone-dot {dot_class}'>{symbol}</div>
            <div class='milestone-label {label_class}'>{m["name"]}<br><span style='color:#F5A623;font-size:0.58rem;'>{m["threshold"]}%+</span></div>
        </div>
        """
        if i < len(milestones) - 1:
            conn_class = "done" if done else ""
            milestone_html += f"<div class='milestone-connector {conn_class}'></div>"
    milestone_html += "</div>"
    st.markdown(milestone_html, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center; font-size:0.8rem; color:#94A3B8; margin-top:0.5rem;'>
        <strong style='color:#F5A623;'>{completed_count}</strong> of {metrics["total_milestones"]} milestones completed
    </div>
    """, unsafe_allow_html=True)

    # ── 3D Architectural Rendering via Pollinations AI ──
    st.markdown("""
    <div class='section-header'><div class='section-icon'>🎨</div><div class='section-title'>Conceptual 3D Architectural Rendering</div></div>
    """, unsafe_allow_html=True)

    render_col1, render_col2 = st.columns([3, 1])
    with render_col1:
        custom_prompt = st.text_area(
            "Rendering description (optional — leave blank for auto-generated)",
            placeholder=f"E.g. Modern {structure_type.lower()} building exterior, glass facade, landscaping, {location_tier} Indian city skyline...",
            height=80,
            key="render_prompt"
        )
    with render_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        render_btn = st.button("🎨 Generate 3D Render", key="btn_render", use_container_width=True)

    if render_btn:
        if custom_prompt.strip():
            prompt_text = custom_prompt.strip()
        else:
            prompt_text = (
                f"Photorealistic 3D architectural rendering of a modern {structure_type.lower()} building, "
                f"contemporary Indian architecture, glass and concrete facade, landscaped surroundings, "
                f"professional architectural visualization, golden hour lighting, {location_tier} urban context, "
                f"ultra-high detail, 8K render quality"
            )

        encoded = urllib.parse.quote(prompt_text)
        image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=576&seed=42&nologo=true"

        with st.spinner("🎨 Generating architectural render via Pollinations AI…"):
            try:
                resp = requests.get(image_url, timeout=30)
                if resp.status_code == 200:
                    st.markdown(f"""
                    <div class='render-container'>
                        <div class='render-label'>AI-Generated Conceptual Render · Pollinations Flux · Prompt: "{prompt_text[:80]}..."</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.image(BytesIO(resp.content), caption=f"Conceptual 3D Render — {structure_type}, {location_tier}", use_column_width=True)
                    st.markdown(f"<div style='font-size:0.72rem; color:#475569; margin-top:0.3rem;'>Prompt: {prompt_text}</div>", unsafe_allow_html=True)
                else:
                    st.warning(f"Rendering service returned status {resp.status_code}. Try again shortly.")
            except Exception as e:
                st.error(f"Rendering failed: {e}. Please check your internet connection.")


# ───────────────────────────────────────────────────────────────────────────────
# TAB 4 — SITE ASSISTANT & WEATHER ADVISORY
# ───────────────────────────────────────────────────────────────────────────────
with tab4:
    col_weather, col_chat = st.columns([1, 1], gap="large")

    # ── WEATHER PANEL ──
    with col_weather:
        st.markdown("""
        <div class='section-header'>
            <div class='section-icon'>🌦️</div>
            <div>
                <div class='section-title'>Weather-Aware Safety Protocols</div>
                <div style='font-size:0.75rem; color:#64748B; margin-top:0.1rem;'>Dynamic daily site safety advisories</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        weather_icons = {"High Wind": "🌬️", "Heavy Rain": "🌧️", "Extreme Heat": "☀️", "Normal": "✅"}
        selected_weather = st.selectbox(
            "Current Site Weather Condition",
            options=list(WEATHER_PROTOCOLS.keys()),
            format_func=lambda x: f"{weather_icons.get(x, '')} {x}",
            key="weather_selector"
        )

        protocol = WEATHER_PROTOCOLS[selected_weather]
        alert_level = protocol["alert_level"]
        color = protocol["color"]
        alert_css = {"RED": "red", "ORANGE": "orange", "AMBER": "amber", "GREEN": "green"}.get(alert_level, "amber")

        # Alert Level Banner
        st.markdown(f"""
        <div class='weather-alert {alert_css}' style='margin-top:0.75rem;'>
            <div class='alert-header' style='color:{color};'>
                {weather_icons.get(selected_weather, "⚠️")} ALERT LEVEL: {alert_level}
                &nbsp;·&nbsp; {selected_weather.upper()}
            </div>
            <div style='font-size:0.78rem; color:#94A3B8;'>{protocol["osha_threshold"]}</div>
            <div style='font-size:0.72rem; color:#64748B; margin-top:0.2rem;'>{protocol["is_standard"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Suspended Operations
        if protocol["suspended_operations"]:
            st.markdown(f"""
            <div class='weather-alert red' style='margin-bottom:0.75rem;'>
                <div class='alert-header' style='color:#FF4444;'>🚫 SUSPENDED OPERATIONS</div>
                <ul class='alert-list'>
                    {''.join([f"<li>{op}</li>" for op in protocol["suspended_operations"]])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:rgba(0,200,81,0.08); border:1px solid rgba(0,200,81,0.2); border-radius:10px; padding:0.75rem 1rem; margin-bottom:0.75rem; font-size:0.82rem; color:#00C851;'>
                ✅ No operations suspended under current conditions
            </div>
            """, unsafe_allow_html=True)

        # Active Safety Measures
        st.markdown(f"""
        <div class='weather-alert {alert_css}'>
            <div class='alert-header' style='color:{color};'>✅ ACTIVE SAFETY MEASURES</div>
            <ul class='alert-list'>
                {''.join([f"<li>{m}</li>" for m in protocol["active_measures"]])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── CHATBOT PANEL ──
    with col_chat:
        st.markdown("""
        <div class='section-header'>
            <div class='section-icon'>💬</div>
            <div>
                <div class='section-title'>ConstructBot — Site Engineering Assistant</div>
                <div style='font-size:0.75rem; color:#64748B; margin-top:0.1rem;'>Multi-turn AI chatbot · IS standards · OSHA · Cost advisory</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick Suggestion Buttons
        st.markdown("<div style='display:flex; gap:0.4rem; flex-wrap:wrap; margin-bottom:0.75rem;'>", unsafe_allow_html=True)
        quick_btns = [
            ("🦺 PPE Requirements", "What are the mandatory PPE requirements for a construction site in India?"),
            ("🔬 Crack Repair Guide", "Explain the concrete crack repair methods and their cost in INR"),
            ("💰 Budget Estimate", "How do I estimate construction cost for a 3000 sqft residential apartment in Mumbai?"),
            ("🌧️ Rain Protocol", "What precautions should I take during heavy rain on a construction site?"),
        ]
        for label, question in quick_btns:
            if st.button(label, key=f"quick_{label[:5]}", use_container_width=False):
                st.session_state.chat_history.append({"role": "user", "content": question})
                with st.spinner("ConstructBot is thinking…"):
                    if st.session_state.api_key_valid:
                        response = run_chatbot(st.session_state.gemini_model, st.session_state.chat_history[:-1], question)
                    else:
                        response = get_demo_chat_response(question)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

        # Chat Display
        if st.session_state.chat_history:
            chat_html = "<div class='chat-container'>"
            for msg in st.session_state.chat_history:
                role = msg["role"]
                content = msg["content"]
                role_class = "chat-user" if role == "user" else "chat-bot"
                role_label = "You" if role == "user" else "🤖 ConstructBot"
                # Escape content for HTML but preserve basic markdown-like formatting
                safe_content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
                chat_html += f"""
                <div class='chat-message {role_class}'>
                    <div class='chat-role'>{role_label}</div>
                    <div class='chat-bubble'>{safe_content}</div>
                </div>
                """
            chat_html += "</div>"
            st.markdown(chat_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='chat-container' style='display:flex; align-items:center; justify-content:center; min-height:200px;'>
                <div style='text-align:center; color:#475569;'>
                    <div style='font-size:2rem; margin-bottom:0.5rem;'>🤖</div>
                    <div style='font-weight:600; color:#64748B;'>ConstructBot Ready</div>
                    <div style='font-size:0.78rem; margin-top:0.3rem;'>Ask me anything about construction engineering, safety, or costs</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Chat Input
        col_chat_in, col_send = st.columns([5, 1])
        with col_chat_in:
            user_input = st.text_input(
                "Ask ConstructBot",
                placeholder="E.g. What is the ideal concrete mix ratio for M25 grade?",
                label_visibility="collapsed",
                key="chat_input"
            )
        with col_send:
            send_btn = st.button("Send", key="btn_send", use_container_width=True)

        if (send_btn or user_input) and user_input.strip():
            msg = user_input.strip()
            st.session_state.chat_history.append({"role": "user", "content": msg})
            with st.spinner("ConstructBot is thinking…"):
                if st.session_state.api_key_valid:
                    response = run_chatbot(st.session_state.gemini_model, st.session_state.chat_history[:-1], msg)
                else:
                    response = get_demo_chat_response(msg)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

        # Clear Chat
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Conversation", key="btn_clear", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        # Status indicator
        if not st.session_state.api_key_valid:
            st.markdown("""
            <div style='background:rgba(59,140,248,0.06); border:1px solid rgba(59,140,248,0.2); border-radius:8px; padding:0.6rem 0.9rem; font-size:0.75rem; color:#93C5FD; margin-top:0.5rem;'>
                🎭 Demo mode — Add Gemini API key in sidebar for live AI responses
            </div>
            """, unsafe_allow_html=True)
