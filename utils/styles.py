"""
CSS Styles for the Multimodal Construction Intelligence Platform.
"""

MAIN_CSS = """
<style>
/* ─── Google Fonts ─── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── Root Variables ─── */
:root {
    --bg-primary: #0E1117;
    --bg-secondary: #1A1F2E;
    --bg-card: #1E2435;
    --bg-card-hover: #252B3D;
    --accent-amber: #F5A623;
    --accent-amber-light: #FFD176;
    --accent-blue: #3B8CF8;
    --accent-green: #00C851;
    --accent-red: #FF4444;
    --accent-orange: #FF8C00;
    --accent-purple: #9C6FDE;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --border: rgba(255,255,255,0.07);
    --shadow-lg: 0 20px 60px rgba(0,0,0,0.5);
    --radius: 12px;
    --radius-sm: 8px;
}

/* ─── Global Reset ─── */
* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ─── Hide Streamlit Branding ─── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── Main Content Area ─── */
.main .block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1400px !important;
}

/* ─── Hero Header ─── */
.hero-header {
    background: linear-gradient(135deg, #1A1F2E 0%, #0E1117 40%, #1A2040 100%);
    border: 1px solid rgba(245,166,35,0.25);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(245,166,35,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #F5A623, #FFD176, #F5A623);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(245,166,35,0.12);
    border: 1px solid rgba(245,166,35,0.3);
    border-radius: 50px;
    padding: 0.3rem 0.9rem;
    font-size: 0.75rem;
    color: var(--accent-amber);
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ─── Metric Cards ─── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(245,166,35,0.3);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent-amber);
    border-radius: 3px 0 0 3px;
}
.metric-card.green::before { background: var(--accent-green); }
.metric-card.red::before { background: var(--accent-red); }
.metric-card.blue::before { background: var(--accent-blue); }
.metric-card.purple::before { background: var(--accent-purple); }
.metric-card.orange::before { background: var(--accent-orange); }

.metric-label {
    font-size: 0.72rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.1;
}
.metric-sub {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}

/* ─── Status Pills ─── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    border-radius: 50px;
    padding: 0.35rem 1rem;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.pill-compliant { background: rgba(0,200,81,0.15); color: #00C851; border: 1px solid rgba(0,200,81,0.3); }
.pill-at-risk { background: rgba(255,140,0,0.15); color: #FF8C00; border: 1px solid rgba(255,140,0,0.3); }
.pill-non-compliant { background: rgba(255,68,68,0.15); color: #FF4444; border: 1px solid rgba(255,68,68,0.3); }
.pill-critical { background: rgba(220,20,60,0.2); color: #DC143C; border: 1px solid rgba(220,20,60,0.4); }

/* ─── Hazard Cards ─── */
.hazard-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    border-left: 4px solid var(--accent-amber);
    transition: background 0.2s;
}
.hazard-card:hover { background: var(--bg-card-hover); }
.hazard-card.critical { border-left-color: #DC143C; }
.hazard-card.high { border-left-color: #FF4444; }
.hazard-card.medium { border-left-color: #FF8C00; }
.hazard-card.low { border-left-color: #FFD176; }

.hazard-title { font-weight: 600; font-size: 0.95rem; margin-bottom: 0.3rem; }
.hazard-remedy { font-size: 0.82rem; color: var(--text-secondary); }
.hazard-refs { font-size: 0.72rem; color: var(--text-muted); margin-top: 0.3rem; font-family: 'JetBrains Mono', monospace; }

/* ─── PPE Checklist ─── */
.ppe-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.85rem 1.25rem;
    margin-bottom: 0.6rem;
    transition: background 0.2s;
}
.ppe-item:hover { background: var(--bg-card-hover); }
.ppe-name { font-weight: 600; font-size: 0.9rem; }
.ppe-rate { font-size: 1.1rem; font-weight: 800; }
.ppe-notes { font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.15rem; }
.ppe-detected-yes { color: var(--accent-green); }
.ppe-detected-no { color: var(--accent-red); }

/* ─── Score Gauge ─── */
.score-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem;
}
.score-circle {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    font-size: 2.5rem;
    font-weight: 900;
    border: 6px solid;
    margin-bottom: 0.75rem;
}
.score-good { border-color: var(--accent-green); color: var(--accent-green); box-shadow: 0 0 30px rgba(0,200,81,0.2); }
.score-warning { border-color: var(--accent-orange); color: var(--accent-orange); box-shadow: 0 0 30px rgba(255,140,0,0.2); }
.score-danger { border-color: var(--accent-red); color: var(--accent-red); box-shadow: 0 0 30px rgba(255,68,68,0.2); }
.score-critical { border-color: #DC143C; color: #DC143C; box-shadow: 0 0 30px rgba(220,20,60,0.3); }

/* ─── Progress Bar ─── */
.progress-bar-container {
    background: rgba(255,255,255,0.07);
    border-radius: 50px;
    height: 10px;
    overflow: hidden;
    margin: 0.4rem 0;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, var(--accent-amber), var(--accent-amber-light));
    transition: width 0.6s ease;
}

/* ─── Section Headers ─── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.75rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
}
.section-icon {
    width: 32px;
    height: 32px;
    background: rgba(245,166,35,0.12);
    border: 1px solid rgba(245,166,35,0.25);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
}

/* ─── Weather Alert Banners ─── */
.weather-alert {
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid;
}
.weather-alert.red { background: rgba(255,68,68,0.08); border-color: rgba(255,68,68,0.3); }
.weather-alert.orange { background: rgba(255,140,0,0.08); border-color: rgba(255,140,0,0.3); }
.weather-alert.amber { background: rgba(255,179,0,0.08); border-color: rgba(255,179,0,0.3); }
.weather-alert.green { background: rgba(0,200,81,0.08); border-color: rgba(0,200,81,0.3); }

.alert-header {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.alert-list { margin: 0; padding-left: 1.2rem; }
.alert-list li { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.3rem; line-height: 1.5; }

/* ─── Crack Report ─── */
.crack-severity {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.5rem;
    border-radius: var(--radius);
    margin: 1rem 0;
}
.crack-badge {
    padding: 0.4rem 1rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
}

/* ─── Repair Cards ─── */
.repair-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.repair-title { font-weight: 700; font-size: 0.95rem; color: var(--accent-amber); }
.repair-desc { font-size: 0.82rem; color: var(--text-secondary); margin: 0.3rem 0; }
.repair-meta { display: flex; gap: 1rem; margin-top: 0.4rem; flex-wrap: wrap; }
.repair-tag {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
}
.tag-urgent { background: rgba(255,68,68,0.15); color: #FF4444; }
.tag-soon { background: rgba(255,140,0,0.15); color: #FF8C00; }
.tag-planned { background: rgba(59,140,248,0.15); color: #3B8CF8; }
.tag-cost { background: rgba(0,200,81,0.12); color: #00C851; }

/* ─── Chatbot ─── */
.chat-container {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    max-height: 480px;
    overflow-y: auto;
    margin-bottom: 1rem;
}
.chat-message {
    margin-bottom: 0.85rem;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
.chat-bubble {
    padding: 0.75rem 1rem;
    border-radius: 12px;
    font-size: 0.875rem;
    line-height: 1.6;
    max-width: 88%;
}
.chat-user .chat-bubble {
    background: rgba(245,166,35,0.12);
    border: 1px solid rgba(245,166,35,0.2);
    margin-left: auto;
    border-bottom-right-radius: 4px;
}
.chat-bot .chat-bubble {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
}
.chat-role {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.chat-user .chat-role { text-align: right; }

/* ─── Valuation Cards ─── */
.valuation-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.val-card {
    background: linear-gradient(135deg, var(--bg-card), var(--bg-secondary));
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease;
}
.val-card:hover { transform: translateY(-3px); }
.val-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent-amber), transparent);
}
.val-amount { font-size: 1.7rem; font-weight: 900; color: var(--accent-amber); }
.val-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.8px; margin-top: 0.3rem; font-weight: 600; }
.val-sub { font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.2rem; }

/* ─── Milestone Tracker ─── */
.milestone-track {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    margin: 1rem 0;
    flex-wrap: nowrap;
    overflow-x: auto;
}
.milestone-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
    flex: 1;
    min-width: 80px;
}
.milestone-dot {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    font-weight: 800;
    transition: all 0.3s;
}
.milestone-dot.done { background: var(--accent-green); color: white; box-shadow: 0 0 12px rgba(0,200,81,0.4); }
.milestone-dot.pending { background: rgba(255,255,255,0.08); border: 2px solid var(--border); color: var(--text-muted); }
.milestone-label { font-size: 0.62rem; text-align: center; color: var(--text-muted); font-weight: 500; line-height: 1.3; }
.milestone-label.done { color: var(--text-secondary); }
.milestone-connector { flex: 0.5; height: 2px; background: var(--border); }
.milestone-connector.done { background: var(--accent-green); }

/* ─── Sidebar Styling ─── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1rem 1.25rem !important;
}

/* ─── Streamlit widget overrides ─── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-sm) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-amber) !important;
    box-shadow: 0 0 0 1px rgba(245,166,35,0.3) !important;
}

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    border-radius: var(--radius-sm) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent-amber), #E8960F) !important;
    color: #0E1117 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s ease !important;
    font-size: 0.85rem !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(245,166,35,0.3) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-radius: var(--radius) !important;
    padding: 0.3rem !important;
    gap: 0.2rem !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-amber) !important;
    color: #0E1117 !important;
}

.stSlider > div > div { color: var(--accent-amber) !important; }

.stFileUploader > div {
    background: var(--bg-card) !important;
    border: 2px dashed rgba(245,166,35,0.3) !important;
    border-radius: var(--radius) !important;
    transition: border-color 0.2s;
}
.stFileUploader > div:hover { border-color: rgba(245,166,35,0.6) !important; }

.stAlert { border-radius: var(--radius-sm) !important; }

.stExpander {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}

.stDownloadButton > button {
    background: var(--bg-card) !important;
    color: var(--accent-amber) !important;
    border: 1px solid rgba(245,166,35,0.3) !important;
    font-weight: 600 !important;
    border-radius: var(--radius-sm) !important;
}
.stDownloadButton > button:hover {
    background: rgba(245,166,35,0.1) !important;
    border-color: rgba(245,166,35,0.6) !important;
}

/* ─── Sidebar Architecture ─── */
.arch-item {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.6rem 0.75rem;
    background: rgba(255,255,255,0.04);
    border-radius: var(--radius-sm);
    margin-bottom: 0.4rem;
    font-size: 0.78rem;
    line-height: 1.4;
}
.arch-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent-amber);
    margin-top: 3px;
    flex-shrink: 0;
}
.demo-banner {
    background: rgba(59,140,248,0.1);
    border: 1px solid rgba(59,140,248,0.3);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    font-size: 0.78rem;
    color: #93C5FD;
    margin-bottom: 1rem;
    line-height: 1.5;
}

/* ─── Image Preview ─── */
.img-preview-container {
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--border);
    margin: 0.75rem 0;
}

/* ─── Pollinations Render ─── */
.render-container {
    border-radius: var(--radius);
    overflow: hidden;
    border: 2px solid rgba(245,166,35,0.2);
    margin: 1rem 0;
    background: var(--bg-secondary);
}
.render-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    text-align: center;
    padding: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
}
</style>
"""
