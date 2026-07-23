import streamlit as st

# ──────────────────────────────────────────────────────────────
#  Vibrant & Modern Colorful SaaS Design System for SnapClass
# ──────────────────────────────────────────────────────────────

_BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

/* ── Global Reset & Page Shell ─────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
    color: #0F172A !important;
}

.stApp {
    background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%) !important;
    color: #0F172A !important;
}

/* Hide default Streamlit header/footer/menu */
#MainMenu, footer, header {
    visibility: hidden !important;
    height: 0 !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1020px !important;
}

/* ── Headings ──────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #0F172A !important;
    letter-spacing: -0.03em !important;
}

h1 { font-size: 2.2rem !important; font-weight: 800 !important; }
h2 { font-size: 1.5rem !important; font-weight: 800 !important; }
h3 { font-size: 1.2rem !important; font-weight: 700 !important; }

p, span, label, div {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
}

/* ── Card Containers ───────────────────────────────────────── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 18px !important;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.05), 0 8px 10px -6px rgba(15, 23, 42, 0.03) !important;
    padding: 1.5rem !important;
}

/* ── Primary, Secondary & Tertiary Buttons ──────────────────── */
button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.93rem !important;
    padding: 0.65rem 1.35rem !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
    transition: all 0.2s ease !important;
    letter-spacing: -0.01em !important;
}

button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.45) !important;
    transform: translateY(-2px) !important;
}

button[kind="primary"]:active {
    transform: translateY(0px) !important;
}

button[kind="secondary"] {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.93rem !important;
    padding: 0.65rem 1.35rem !important;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04) !important;
    transition: all 0.2s ease !important;
}

button[kind="secondary"]:hover {
    border-color: #6366F1 !important;
    background-color: #EEF2FF !important;
    color: #4338CA !important;
    transform: translateY(-1px) !important;
}

button[kind="tertiary"] {
    background-color: transparent !important;
    color: #4F46E5 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 0.85rem !important;
    transition: all 0.15s ease !important;
}

button[kind="tertiary"]:hover {
    color: #4338CA !important;
    background-color: #EEF2FF !important;
}

/* Disabled button styling */
button:disabled, button[disabled] {
    background-color: #F1F5F9 !important;
    color: #94A3B8 !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
    opacity: 0.7 !important;
}

/* ── Form Controls & Selectbox Fixes ────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
    color: #0F172A !important;
    font-size: 0.94rem !important;
    padding: 0.65rem 0.9rem !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3.5px rgba(99, 102, 241, 0.18) !important;
}

/* Fix Selectbox input container & popover menu */
.stSelectbox > div > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
    color: #0F172A !important;
}

.stSelectbox div[role="button"], .stSelectbox span, .stSelectbox input {
    color: #0F172A !important;
    font-weight: 600 !important;
}

/* Selectbox Dropdown Menu (Baseweb Popover Fix) */
div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 14px !important;
    box-shadow: 0 12px 28px -5px rgba(15, 23, 42, 0.15) !important;
}

li[role="option"], div[data-baseweb="option"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    font-weight: 600 !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
}

li[role="option"]:hover, div[data-baseweb="option"]:hover {
    background-color: #EEF2FF !important;
    color: #4F46E5 !important;
}

/* Fix password toggle adornment styling */
.stTextInput button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #64748B !important;
}

/* ── Streamlit Dialog / Modal Theme Overrides ─────────────── */
div[role="dialog"], div[data-testid="stModal"], div[data-baseweb="modal"] {
    background-color: #FFFFFF !important;
    border: 2px solid #6366F1 !important;
    border-radius: 22px !important;
    box-shadow: 0 25px 50px -12px rgba(99, 102, 241, 0.25) !important;
    color: #0F172A !important;
}

div[role="dialog"] * {
    color: #0F172A !important;
}

div[role="dialog"] p {
    color: #334155 !important;
}

div[role="dialog"] button[aria-label="Close"] {
    color: #64748B !important;
}

div[role="dialog"] button[aria-label="Close"]:hover {
    color: #0F172A !important;
    background-color: #F1F5F9 !important;
    border-radius: 50% !important;
}

/* ── Alert Boxes (Vibrant Colored Badges) ──────────────────── */
.stAlert {
    border-radius: 14px !important;
    font-weight: 600 !important;
    padding: 0.9rem 1.2rem !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03) !important;
}

div[data-testid="stAlert"] p {
    font-size: 0.93rem !important;
    font-weight: 700 !important;
}

/* Warning alert fix */
div[data-testid="stAlert"]:has(div:contains("⚠️")),
.stAlert:has(.st-ae) {
    background-color: #FEF3C7 !important;
    border: 1.5px solid #FCD34D !important;
    color: #78350F !important;
}

div[data-testid="stAlert"]:has(div:contains("⚠️")) p {
    color: #78350F !important;
}

/* Info alert fix */
div[data-testid="stAlert"]:has(div:contains("ℹ️")) {
    background-color: #E0F2FE !important;
    border: 1.5px solid #7DD3FC !important;
    color: #0369A1 !important;
}

div[data-testid="stAlert"]:has(div:contains("ℹ️")) p {
    color: #0369A1 !important;
}

/* Success alert fix */
div[data-testid="stAlert"]:has(div:contains("✅")),
div[data-testid="stAlert"]:has(div:contains("🎉")) {
    background-color: #D1FAE5 !important;
    border: 1.5px solid #6EE7B7 !important;
    color: #047857 !important;
}

div[data-testid="stAlert"]:has(div:contains("✅")) p,
div[data-testid="stAlert"]:has(div:contains("🎉")) p {
    color: #047857 !important;
}

/* Error alert fix */
div[data-testid="stAlert"]:has(div:contains("❌")),
div[data-testid="stAlert"]:has(div:contains("Error")) {
    background-color: #FEE2E2 !important;
    border: 1.5px solid #FCA5A5 !important;
    color: #B91C1C !important;
}

div[data-testid="stAlert"]:has(div:contains("❌")) p {
    color: #B91C1C !important;
}

/* ── Divider & Camera Frame ────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1.5px solid #E2E8F0 !important;
    margin: 1.35rem 0 !important;
}

.stCameraInput {
    max-width: 580px !important;
    margin: 0 auto !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    border: 3px solid #6366F1 !important;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2) !important;
}

/* ── Responsive Mobile Layouts ─────────────────────────────── */
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 1rem !important;
    }
    
    h1 { font-size: 1.75rem !important; }
    h2 { font-size: 1.3rem !important; }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 1.1rem !important;
    }
}
</style>
"""

_HOME_HERO_CSS = """
<style>
.snap-portal-card-student {
    background: #FFFFFF;
    border: 1.5px solid #DDD6FE;
    border-top: 5px solid #8B5CF6;
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.08);
    transition: all 0.22s ease;
    margin-bottom: 1rem;
}
.snap-portal-card-student:hover {
    border-color: #8B5CF6;
    box-shadow: 0 14px 30px rgba(139, 92, 246, 0.18);
    transform: translateY(-3px);
}

.snap-portal-card-teacher {
    background: #FFFFFF;
    border: 1.5px solid #A5F3FC;
    border-top: 5px solid #06B6D4;
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 6px 20px rgba(6, 182, 212, 0.08);
    transition: all 0.22s ease;
    margin-bottom: 1rem;
}
.snap-portal-card-teacher:hover {
    border-color: #06B6D4;
    box-shadow: 0 14px 30px rgba(6, 182, 212, 0.18);
    transform: translateY(-3px);
}
</style>
"""


def style_base_layout():
    """Inject vibrant light SaaS theme system."""
    st.markdown(_BASE_CSS, unsafe_allow_html=True)


def style_background_home():
    """Inject portal hero card styles."""
    st.markdown(_HOME_HERO_CSS, unsafe_allow_html=True)


def style_background_dashboard():
    """No-op compatibility function."""
    pass