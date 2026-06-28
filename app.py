import html
from pathlib import Path

import pandas as pd
import streamlit as st

from rag_engine import ask_scheme_ai


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="TN Scheme Navigator AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# App Constants
# ---------------------------------------------------------
APP_NAME = "TN Scheme Navigator AI"
APP_SUBTITLE = "AI-powered Tamil Nadu Government Scheme Assistant"
DATA_PATH = Path("data/tn_scheme_details.csv")


# ---------------------------------------------------------
# Custom CSS Styling - UI Only
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
    :root {
        --tn-navy: #071A3E;
        --tn-navy-2: #0B2F6B;
        --tn-blue: #123B7A;
        --tn-green: #167A3A;
        --tn-gold: #D99A1E;
        --tn-saffron: #F4A261;
        --tn-bg: #F5F7FA;
        --tn-bg-soft: #EEF3F8;
        --tn-card: #FFFFFF;
        --tn-text: #172033;
        --tn-muted: #475569;
        --tn-border: #E2E8F0;
        --tn-border-strong: #CBD5E1;
        --tn-shadow: 0 14px 36px rgba(15, 23, 42, 0.08);
        --tn-shadow-hover: 0 20px 48px rgba(15, 23, 42, 0.14);
        --sidebar-width: 286px;
    }

    html, body, [class*="css"] {
        font-family: Inter, Poppins, "Source Sans Pro", "Noto Sans Tamil", Arial, sans-serif;
        color: var(--tn-text);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(18, 59, 122, 0.08), transparent 30%),
            linear-gradient(180deg, var(--tn-bg) 0%, var(--tn-bg-soft) 100%);
        color: var(--tn-text);
    }

    .block-container {
        max-width: 1580px !important;
        padding-top: 1.05rem !important;
        padding-left: 1.7rem !important;
        padding-right: 1.7rem !important;
        padding-bottom: 2rem !important;
    }

    @media only screen and (max-width: 1100px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }

    /* -----------------------------------------------------
       Sidebar
    ----------------------------------------------------- */
    section[data-testid="stSidebar"] {
        width: var(--sidebar-width) !important;
        min-width: var(--sidebar-width) !important;
        background:
            radial-gradient(circle at top left, rgba(217, 154, 30, 0.18), transparent 28%),
            linear-gradient(180deg, #061633 0%, #071A3E 48%, #0B2F6B 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 12px 0 34px rgba(7, 26, 62, 0.18);
    }

    section[data-testid="stSidebar"] > div {
        width: var(--sidebar-width) !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    .sidebar-brand {
        padding: 0.7rem 0 1.05rem 0;
        margin-bottom: 0.9rem;
        border-bottom: 1px solid rgba(255,255,255,0.14);
    }

    .sidebar-logo-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .tn-logo {
        width: 56px;
        height: 56px;
        min-width: 56px;
        border-radius: 18px;
        background:
            linear-gradient(135deg, rgba(217,154,30,0.26), rgba(255,255,255,0.10)),
            rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.24);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow:
            inset 0 0 22px rgba(255,255,255,0.09),
            0 10px 24px rgba(0,0,0,0.18);
    }

    .tn-logo svg {
        width: 42px;
        height: 42px;
    }

    .sidebar-title {
        font-size: 1.12rem;
        font-weight: 900;
        line-height: 1.18;
        letter-spacing: -0.02em;
    }

    .sidebar-subtitle {
        color: rgba(255,255,255,0.82) !important;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-top: 0.8rem;
        font-weight: 500;
    }

    .sidebar-text {
        color: rgba(255,255,255,0.82) !important;
        font-size: 0.9rem;
        line-height: 1.55;
        margin-top: 0.7rem;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] .stRadio > label {
        font-size: 0.84rem !important;
        font-weight: 800 !important;
        color: rgba(255,255,255,0.74) !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 0.45rem;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        min-height: 46px;
        padding: 0.7rem 0.8rem !important;
        border-radius: 999px !important;
        margin: 0.18rem 0 !important;
        border: 1px solid transparent;
        background: transparent;
        transition: all 0.2s ease;
        font-size: 0.98rem !important;
        font-weight: 750 !important;
        line-height: 1.2;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.11) !important;
        border-color: rgba(255,255,255,0.15);
        transform: translateX(3px);
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background:
            linear-gradient(135deg, rgba(217, 154, 30, 0.28), rgba(22, 122, 58, 0.26)) !important;
        border-color: rgba(217, 154, 30, 0.75) !important;
        box-shadow:
            inset 0 0 18px rgba(255,255,255,0.05),
            0 10px 24px rgba(0,0,0,0.18);
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.14) !important;
        margin: 1.1rem 0 !important;
    }

    /* -----------------------------------------------------
       Header / Hero
    ----------------------------------------------------- */
    .portal-header {
        width: 100%;
        background:
            radial-gradient(circle at top right, rgba(217,154,30,0.22), transparent 25%),
            linear-gradient(135deg, #071A3E 0%, #0B2F6B 56%, #167A3A 100%);
        padding: 1.75rem 1.95rem;
        border-radius: 26px;
        color: white;
        box-shadow: 0 20px 52px rgba(7, 26, 62, 0.25);
        margin-bottom: 1.15rem;
        border: 1px solid rgba(255,255,255,0.12);
        position: relative;
        overflow: hidden;
    }

    .portal-header:after {
        content: "";
        position: absolute;
        right: -90px;
        top: -100px;
        width: 260px;
        height: 260px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }

    .header-row {
        display: flex;
        align-items: center;
        gap: 1.05rem;
        position: relative;
        z-index: 2;
    }

    .hero-logo {
        width: 76px;
        height: 76px;
        min-width: 76px;
        border-radius: 22px;
        background:
            linear-gradient(135deg, rgba(217,154,30,0.24), rgba(255,255,255,0.12)),
            rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.32);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 24px rgba(255,255,255,0.09);
    }

    .hero-logo svg {
        width: 54px;
        height: 54px;
    }

    .portal-title {
        font-size: clamp(2.1rem, 3vw, 3.15rem);
        line-height: 1.05;
        font-weight: 950;
        margin: 0;
        letter-spacing: -0.045em;
        color: #FFFFFF;
    }

    .portal-subtitle {
        font-size: clamp(1rem, 1.15vw, 1.16rem);
        margin-top: 0.5rem;
        opacity: 0.95;
        max-width: 960px;
        line-height: 1.55;
        font-weight: 520;
        color: rgba(255,255,255,0.94);
    }

    /* -----------------------------------------------------
       Cards / Layout
    ----------------------------------------------------- */
    .hero-card,
    .feature-card,
    .stat-card,
    .source-card,
    .response-card,
    .process-box,
    .footer {
        background: var(--tn-card);
        border: 1px solid var(--tn-border);
        box-shadow: var(--tn-shadow);
    }

    .hero-card {
        border-radius: 22px;
        padding: 1.4rem 1.5rem;
        min-height: 218px;
        height: 100%;
    }

    .hero-title {
        font-size: clamp(1.45rem, 1.8vw, 1.85rem);
        font-weight: 950;
        color: var(--tn-navy);
        margin-bottom: 0.65rem;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }

    .hero-text {
        color: #334155;
        line-height: 1.75;
        font-size: 1rem;
        font-weight: 480;
    }

    .section-heading {
        font-size: 1.34rem;
        font-weight: 950;
        color: var(--tn-navy);
        margin-top: 1.1rem;
        margin-bottom: 0.8rem;
        letter-spacing: -0.03em;
        line-height: 1.25;
    }

    .feature-card {
        border-radius: 20px;
        padding: 1.2rem;
        min-height: 176px;
        height: 100%;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--tn-shadow-hover);
        border-color: #C8D8F0;
    }

    .feature-icon {
        width: 50px;
        height: 50px;
        border-radius: 16px;
        background: linear-gradient(135deg, #EAF2FF 0%, #F8FAFC 100%);
        border: 1px solid #DDEBFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 0.85rem;
    }

    .feature-title {
        font-weight: 900;
        color: var(--tn-navy);
        margin-bottom: 0.45rem;
        font-size: 1.06rem;
        line-height: 1.3;
    }

    .feature-text {
        color: #475569;
        line-height: 1.62;
        font-size: 0.94rem;
        font-weight: 480;
    }

    .stat-card {
        border-radius: 18px;
        padding: 1rem 1.08rem;
        min-height: 98px;
        height: 100%;
    }

    .stat-number {
        font-size: 1.85rem;
        font-weight: 950;
        color: var(--tn-navy);
        margin-bottom: 0.12rem;
        letter-spacing: -0.03em;
    }

    .stat-label {
        color: #475569;
        font-size: 0.92rem;
        font-weight: 780;
        line-height: 1.35;
    }

    .process-box {
        border-radius: 20px;
        padding: 1.15rem 1.25rem;
        border-left: 6px solid var(--tn-gold);
        background:
            linear-gradient(90deg, rgba(217,154,30,0.10) 0%, rgba(255,255,255,1) 38%),
            #FFFFFF;
        color: var(--tn-text);
        line-height: 1.7;
    }

    .process-flow {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        align-items: center;
        margin-top: 0.8rem;
    }

    .process-step {
        display: inline-flex;
        align-items: center;
        padding: 0.46rem 0.72rem;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        color: #0F172A;
        border-radius: 999px;
        font-size: 0.88rem;
        font-weight: 780;
    }

    .process-arrow {
        color: var(--tn-blue);
        font-weight: 950;
    }

    .info-box {
        background: #EAF2FF;
        border: 1px solid #CFE1FF;
        border-left: 5px solid var(--tn-blue);
        border-radius: 17px;
        padding: 1rem 1.1rem;
        color: #102A56;
        line-height: 1.68;
        font-size: 0.99rem;
        font-weight: 480;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    }

    .warning-box {
        background: #FFF7E6;
        border: 1px solid #FFE0A3;
        border-left: 5px solid var(--tn-gold);
        border-radius: 17px;
        padding: 1rem 1.1rem;
        color: #5F4100;
        line-height: 1.65;
        font-size: 0.98rem;
        font-weight: 500;
    }

    /* -----------------------------------------------------
       Chatbot / Input Area
    ----------------------------------------------------- */
    .question-intro {
        background: #FFFFFF;
        border: 1px solid var(--tn-border);
        border-radius: 22px;
        box-shadow: var(--tn-shadow);
        padding: 1.1rem 1.2rem;
        margin-top: 0.85rem;
        margin-bottom: 0.75rem;
    }

    div[data-testid="stTextArea"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stSelectbox"] label {
        color: var(--tn-navy) !important;
        font-weight: 850 !important;
        font-size: 0.98rem !important;
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        border-radius: 16px !important;
        border: 1.5px solid #CBD5E1 !important;
        color: #172033 !important;
        background-color: #FFFFFF !important;
        font-size: 1rem !important;
        line-height: 1.55 !important;
        font-weight: 500 !important;
        -webkit-text-fill-color: #172033 !important;
        caret-color: #071A3E !important;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04) !important;
    }

    div[data-testid="stTextArea"] textarea::placeholder,
    div[data-testid="stTextInput"] input::placeholder {
        color: #64748B !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #64748B !important;
        font-weight: 500 !important;
    }

    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--tn-blue) !important;
        box-shadow:
            0 0 0 3px rgba(18, 59, 122, 0.14),
            0 10px 26px rgba(15, 23, 42, 0.07) !important;
        outline: none !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--tn-navy) 0%, var(--tn-blue) 100%);
        color: white !important;
        border: none;
        border-radius: 14px;
        padding: 0.7rem 1.15rem;
        font-weight: 900;
        font-size: 0.95rem;
        box-shadow: 0 10px 22px rgba(7, 26, 62, 0.22);
        transition: all 0.18s ease;
        min-height: 44px;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--tn-blue) 0%, var(--tn-green) 100%);
        color: white !important;
        transform: translateY(-1px);
        box-shadow: 0 14px 30px rgba(7, 26, 62, 0.28);
    }

    .stButton > button:focus {
        color: white !important;
        border: none !important;
        box-shadow: 0 0 0 3px rgba(217,154,30,0.30) !important;
    }

    .response-card {
        border-radius: 22px;
        padding: 1.35rem 1.45rem;
        border-left: 6px solid var(--tn-green);
        color: var(--tn-text);
        line-height: 1.78;
        font-size: 1rem;
        min-height: 170px;
        white-space: pre-wrap;
    }

    .response-card strong,
    .response-card b {
        color: var(--tn-navy);
    }

    .loading-card {
        background: #FFFFFF;
        border: 1px solid #DDEBFF;
        border-left: 6px solid var(--tn-gold);
        border-radius: 22px;
        padding: 1.2rem 1.35rem;
        box-shadow: var(--tn-shadow);
        color: var(--tn-navy);
        min-height: 112px;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        font-weight: 900;
        font-size: 1rem;
    }

    .loading-dot {
        width: 12px;
        height: 12px;
        background: var(--tn-gold);
        border-radius: 999px;
        display: inline-block;
        animation: pulse 1.1s infinite ease-in-out;
    }

    @keyframes pulse {
        0% { opacity: 0.35; transform: scale(0.9); }
        50% { opacity: 1; transform: scale(1.18); }
        100% { opacity: 0.35; transform: scale(0.9); }
    }

    /* -----------------------------------------------------
       Scheme Cards
    ----------------------------------------------------- */
    .source-card {
        border-radius: 21px;
        padding: 1.18rem 1.25rem;
        margin-bottom: 1rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }

    .source-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--tn-shadow-hover);
        border-color: #C8D8F0;
    }

    .source-title {
        color: var(--tn-navy);
        font-weight: 950;
        font-size: 1.1rem;
        margin-bottom: 0.55rem;
        line-height: 1.35;
        letter-spacing: -0.01em;
    }

    .source-meta {
        color: #334155;
        line-height: 1.72;
        font-size: 0.95rem;
        font-weight: 480;
    }

    .source-meta strong {
        color: var(--tn-navy);
        font-weight: 850;
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.38rem;
        margin: 0.72rem 0 0.78rem 0;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.32rem 0.64rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 850;
        border: 1px solid transparent;
        line-height: 1.2;
    }

    .badge-state { background: #EAF2FF; color: #123B7A; border-color: #CFE1FF; }
    .badge-central { background: #F0FDF4; color: #167A3A; border-color: #BBF7D0; }
    .badge-grant { background: #FFF7E6; color: #8A5300; border-color: #FFE0A3; }
    .badge-subsidy { background: #ECFDF5; color: #047857; border-color: #A7F3D0; }
    .badge-training { background: #F5F3FF; color: #5B21B6; border-color: #DDD6FE; }
    .badge-loan { background: #FEF2F2; color: #B91C1C; border-color: #FECACA; }
    .badge-farmer { background: #F0FDF4; color: #166534; border-color: #BBF7D0; }
    .badge-msme { background: #EFF6FF; color: #1D4ED8; border-color: #BFDBFE; }
    .badge-student { background: #FAF5FF; color: #7E22CE; border-color: #E9D5FF; }
    .badge-default { background: #F3F4F6; color: #374151; border-color: #E5E7EB; }

    .official-link {
        display: inline-block;
        margin-top: 0.84rem;
        padding: 0.6rem 0.9rem;
        background: var(--tn-navy);
        color: white !important;
        border-radius: 12px;
        text-decoration: none !important;
        font-weight: 900;
        font-size: 0.88rem;
        box-shadow: 0 8px 18px rgba(7, 26, 62, 0.18);
    }

    .official-link:hover {
        background: var(--tn-blue);
        color: white !important;
    }

    /* -----------------------------------------------------
       Footer
    ----------------------------------------------------- */
    .footer {
        margin-top: 1.5rem;
        padding: 1.05rem 1.25rem;
        border-radius: 18px;
        text-align: center;
        color: #475569;
        line-height: 1.65;
        font-size: 0.92rem;
        font-weight: 480;
    }

    .footer strong {
        color: var(--tn-navy);
        font-weight: 900;
    }

    /* Reduce default Streamlit gaps */
    div[data-testid="stVerticalBlock"] {
        gap: 0.75rem;
    }

    div[data-testid="column"] {
        min-width: 0;
    }

    /* Mobile */
    @media only screen and (max-width: 768px) {
        section[data-testid="stSidebar"] {
            width: 100% !important;
            min-width: 100% !important;
        }

        .portal-header {
            padding: 1.25rem;
            border-radius: 20px;
        }

        .header-row {
            align-items: flex-start;
        }

        .hero-logo {
            width: 58px;
            height: 58px;
            min-width: 58px;
            border-radius: 18px;
        }

        .hero-logo svg {
            width: 42px;
            height: 42px;
        }

        .portal-title {
            font-size: 1.8rem;
        }

        .hero-card,
        .feature-card,
        .source-card,
        .response-card,
        .process-box {
            border-radius: 18px;
        }
    }
</style>
"""


# ---------------------------------------------------------
# Inline Logo - Local Safe SVG
# Agriculture + Gopuram + Sun + AI Node
# ---------------------------------------------------------
LOGO_SVG = """
<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="TN Scheme Navigator AI Logo">
    <circle cx="50" cy="50" r="45" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.32)" stroke-width="2"/>
    <path d="M22 66C34 58 44 58 50 72C57 55 70 53 82 61" stroke="#7EE08A" stroke-width="5" stroke-linecap="round"/>
    <path d="M32 63C42 56 48 57 52 70" stroke="#D99A1E" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M39 52H61V76H39V52Z" fill="#F8FAFC" opacity="0.95"/>
    <path d="M35 52L50 36L65 52H35Z" fill="#D99A1E"/>
    <path d="M44 52V45H56V52" fill="#F4A261"/>
    <path d="M46 76V62H54V76" fill="#071A3E" opacity="0.92"/>
    <path d="M31 35C35 25 43 20 50 20C57 20 65 25 69 35" stroke="#F4A261" stroke-width="4" stroke-linecap="round"/>
    <circle cx="75" cy="26" r="5" fill="#7EE08A"/>
    <circle cx="82" cy="40" r="3.5" fill="#D99A1E"/>
    <path d="M75 26L82 40" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/>
</svg>
"""


# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------
def inject_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def clean_value(value, default="Not available"):
    if value is None:
        return default

    text = str(value).strip()

    if not text or text.lower() in ["nan", "none", "null"]:
        return default

    return text


def esc(value):
    return html.escape(clean_value(value))


@st.cache_data(show_spinner=False)
def load_scheme_data():
    if not DATA_PATH.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(DATA_PATH)
    except Exception:
        return pd.DataFrame()


def get_column_values(df, column_name):
    if df.empty or column_name not in df.columns:
        return []

    values = (
        df[column_name]
        .dropna()
        .astype(str)
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .unique()
        .tolist()
    )

    return sorted(values)


def detect_badges(text):
    text = clean_value(text, "").lower()
    badges = []

    if "state" in text:
        badges.append(("State Scheme", "badge-state"))

    if "central" in text:
        badges.append(("Central Scheme", "badge-central"))

    if "grant" in text:
        badges.append(("Grant", "badge-grant"))

    if "subsidy" in text:
        badges.append(("Subsidy", "badge-subsidy"))

    if "training" in text:
        badges.append(("Training", "badge-training"))

    if "loan" in text or "credit" in text:
        badges.append(("Loan", "badge-loan"))

    if "farmer" in text or "farmers" in text or "agriculture" in text:
        badges.append(("Farmer", "badge-farmer"))

    if "msme" in text or "micro" in text or "small enterprise" in text:
        badges.append(("MSME", "badge-msme"))

    if "student" in text or "students" in text:
        badges.append(("Student", "badge-student"))

    if not badges:
        badges.append(("Scheme", "badge-default"))

    return badges[:6]


def render_badges(text):
    badges = detect_badges(text)
    badge_html = ""

    for label, badge_class in badges:
        badge_html += f'<span class="badge {badge_class}">{html.escape(label)}</span>'

    return f'<div class="badge-row">{badge_html}</div>'


def render_portal_header():
    st.markdown(
        f"""
        <div class="portal-header">
            <div class="header-row">
                <div class="hero-logo">{LOGO_SVG}</div>
                <div>
                    <h1 class="portal-title">{APP_NAME}</h1>
                    <div class="portal-subtitle">{APP_SUBTITLE}</div>
                    <div class="portal-subtitle">
                        Search, understand, and explore Tamil Nadu Government schemes using Gen AI + RAG.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_card(icon, title, text):
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{html.escape(title)}</div>
            <div class="feature-text">{html.escape(text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(number, label):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{html.escape(str(number))}</div>
            <div class="stat-label">{html.escape(label)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="footer">
            <strong>Built for Tamil Nadu Scheme Discovery using Gen AI + RAG</strong><br>
            This AI assistant is for informational support. Please verify final details from official government sources.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_process_box():
    st.markdown(
        """
        <div class="process-box">
            <strong>How the portal works</strong>
            <div class="process-flow">
                <span class="process-step">Official scheme page</span>
                <span class="process-arrow">→</span>
                <span class="process-step">Scraper</span>
                <span class="process-arrow">→</span>
                <span class="process-step">CSV</span>
                <span class="process-arrow">→</span>
                <span class="process-step">Embeddings</span>
                <span class="process-arrow">→</span>
                <span class="process-step">Chroma Vector DB</span>
                <span class="process-arrow">→</span>
                <span class="process-step">LangChain RAG</span>
                <span class="process-arrow">→</span>
                <span class="process-step">Streamlit AI Portal</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_loading_card():
    st.markdown(
        """
        <div class="loading-card">
            <span class="loading-dot"></span>
            <span>Generating verified scheme guidance...</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_answer_card(answer):
    safe_answer = html.escape(clean_value(answer, "No answer generated."))
    safe_answer = safe_answer.replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="response-card">
            {safe_answer}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_source_cards(sources):
    if not sources:
        st.markdown(
            """
            <div class="warning-box">
                No official source references were returned for this answer.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    shown_urls = set()

    for item in sources:
        url = clean_value(item.get("source_url"), "")

        if not url or url in shown_urls:
            continue

        shown_urls.add(url)

        scheme_title = esc(item.get("scheme_title"))
        department = esc(item.get("department"))
        beneficiaries = esc(item.get("beneficiaries"))
        benefit_type = esc(item.get("benefit_type"))

        badge_text = f"{scheme_title} {department} {benefit_type} {beneficiaries}"

        st.markdown(
            f"""
            <div class="source-card">
                <div class="source-title">{scheme_title}</div>
                {render_badges(badge_text)}
                <div class="source-meta">
                    <strong>Department:</strong> {department}<br>
                    <strong>Beneficiary:</strong> {beneficiaries}<br>
                    <strong>Benefit Type:</strong> {benefit_type}
                </div>
                <a class="official-link" href="{html.escape(url)}" target="_blank">
                    Open Official Scheme Page
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# Pages
# ---------------------------------------------------------
def home_page(df):
    render_portal_header()

    left_col, right_col = st.columns([1.65, 1], gap="large")

    with left_col:
        st.markdown(
            """
            <div class="hero-card">
                <div class="hero-title">Citizen-friendly AI for Tamil Nadu schemes</div>
                <div class="hero-text">
                    TN Scheme Navigator AI helps farmers, students, MSMEs, women, entrepreneurs,
                    and citizens quickly understand government scheme information using a
                    Retrieval-Augmented Generation workflow.
                    <br><br>
                    The portal retrieves relevant scheme data, generates simple explanations,
                    and shows official source links for verification.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        total_schemes = len(df) if not df.empty else 0
        total_departments = len(get_column_values(df, "concerned_department"))
        total_beneficiaries = len(get_column_values(df, "beneficiaries"))

        stat_col_1, stat_col_2 = st.columns(2, gap="medium")

        with stat_col_1:
            render_stat_card(total_schemes, "Schemes indexed")
            render_stat_card(total_beneficiaries, "Beneficiary types")

        with stat_col_2:
            render_stat_card(total_departments, "Departments")
            render_stat_card("RAG", "AI search engine")

    st.markdown('<div class="section-heading">Portal Features</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        render_feature_card(
            "🔎",
            "Search Schemes",
            "Ask natural language questions and discover relevant government schemes.",
        )

    with c2:
        render_feature_card(
            "✅",
            "Check Eligibility",
            "Understand beneficiaries, eligibility notes, and benefit details.",
        )

    with c3:
        render_feature_card(
            "🏢",
            "Department-wise Schemes",
            "Explore schemes by department, benefit type, and beneficiary group.",
        )

    with c4:
        render_feature_card(
            "🤖",
            "AI Scheme Assistant",
            "Get simplified answers with official source links for verification.",
        )

    st.markdown('<div class="section-heading">How it works</div>', unsafe_allow_html=True)
    render_process_box()


def assistant_page():
    render_portal_header()

    st.markdown('<div class="section-heading">AI Scheme Assistant</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
            Ask about schemes for farmers, MSMEs, students, women, entrepreneurs, eligibility,
            training, grants, subsidies, seeds, soil health, pest management, or how to apply.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="question-intro">
            <strong>Start with a sample question or type your own scheme query below.</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    example_col_1, example_col_2, example_col_3 = st.columns(3, gap="medium")

    with example_col_1:
        if st.button("🌾 Funding for Training to Farmers"):
            st.session_state["question"] = "What is the funding pattern for Training to Farmers?"

    with example_col_2:
        if st.button("👨‍🌾 Beneficiaries"):
            st.session_state["question"] = "Who are the beneficiaries of Training to Farmers?"

    with example_col_3:
        if st.button("📄 How to apply"):
            st.session_state["question"] = "How can farmers avail Training to Farmers scheme?"

    default_question = st.session_state.get("question", "")

    question = st.text_area(
        "Enter your question",
        value=default_question,
        height=125,
        placeholder="Ask about schemes for farmers, MSMEs, students, women, entrepreneurs, or eligibility...",
    )

    ask_button = st.button("Ask TN Scheme Navigator AI")

    if ask_button:
        if not question.strip():
            st.warning("Please enter a question.")
            return

        st.markdown('<div class="section-heading">AI Answer</div>', unsafe_allow_html=True)

        answer_placeholder = st.empty()

        with answer_placeholder.container():
            render_loading_card()

        try:
            answer, sources = ask_scheme_ai(question)
        except Exception as error:
            answer_placeholder.empty()
            st.error("Unable to generate answer. Please make sure you have run the scraper and ingest files.")
            st.code(
                "python scrape_schemes.py\npython ingest.py\nstreamlit run app.py",
                language="bash",
            )
            st.exception(error)
            return

        answer_placeholder.empty()
        render_answer_card(answer)

        st.markdown('<div class="section-heading">Official References</div>', unsafe_allow_html=True)
        render_source_cards(sources)


def scheme_explorer_page(df):
    render_portal_header()

    st.markdown('<div class="section-heading">Scheme Explorer</div>', unsafe_allow_html=True)

    if df.empty:
        st.markdown(
            """
            <div class="warning-box">
                No scheme CSV found. Please run <strong>python scrape_schemes.py</strong> first.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    search_text = st.text_input(
        "Search schemes",
        placeholder="Search by scheme name, beneficiary, benefit type, department, or keyword...",
    )

    filter_col_1, filter_col_2, filter_col_3 = st.columns(3, gap="medium")

    department_values = ["All"] + get_column_values(df, "concerned_department")
    beneficiary_values = ["All"] + get_column_values(df, "beneficiaries")
    benefit_values = ["All"] + get_column_values(df, "types_of_benefits")

    with filter_col_1:
        selected_department = st.selectbox("Department", department_values)

    with filter_col_2:
        selected_beneficiary = st.selectbox("Beneficiary", beneficiary_values)

    with filter_col_3:
        selected_benefit = st.selectbox("Benefit Type", benefit_values)

    filtered_df = df.copy()

    if selected_department != "All" and "concerned_department" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["concerned_department"].astype(str).str.strip() == selected_department
        ]

    if selected_beneficiary != "All" and "beneficiaries" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["beneficiaries"].astype(str).str.strip() == selected_beneficiary
        ]

    if selected_benefit != "All" and "types_of_benefits" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["types_of_benefits"].astype(str).str.strip() == selected_benefit
        ]

    if search_text.strip():
        search_lower = search_text.lower()
        combined_text = filtered_df.astype(str).agg(" ".join, axis=1).str.lower()
        filtered_df = filtered_df[combined_text.str.contains(search_lower, na=False)]

    st.markdown(
        f"""
        <div class="info-box">
            Showing <strong>{len(filtered_df)}</strong> scheme result(s).
        </div>
        """,
        unsafe_allow_html=True,
    )

    for _, row in filtered_df.head(25).iterrows():
        scheme_title = esc(row.get("scheme_title"))
        department = esc(row.get("concerned_department"))
        beneficiaries = esc(row.get("beneficiaries"))
        benefit_type = esc(row.get("types_of_benefits"))
        funding_pattern = esc(row.get("funding_pattern"))
        how_to_avail = esc(row.get("how_to_avail"))
        source_url = clean_value(row.get("source_url"), "")

        badge_text = (
            f"{scheme_title} {department} {beneficiaries} {benefit_type} "
            f"{funding_pattern} {clean_value(row.get('sponsored_by'), '')}"
        )

        link_html = ""
        if source_url:
            link_html = (
                f'<a class="official-link" href="{html.escape(source_url)}" '
                f'target="_blank">Open Official Scheme Page</a>'
            )

        st.markdown(
            f"""
            <div class="source-card">
                <div class="source-title">{scheme_title}</div>
                {render_badges(badge_text)}
                <div class="source-meta">
                    <strong>Department:</strong> {department}<br>
                    <strong>Beneficiary:</strong> {beneficiaries}<br>
                    <strong>Benefit Type:</strong> {benefit_type}<br>
                    <strong>Funding Pattern:</strong> {funding_pattern}<br>
                    <strong>How to Apply:</strong> {how_to_avail}
                </div>
                {link_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


def about_page():
    render_portal_header()

    st.markdown('<div class="section-heading">About this Gen AI RAG Application</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Built for public scheme discovery</div>
            <div class="hero-text">
                TN Scheme Navigator AI is a learning project that demonstrates how Gen AI can help citizens
                understand government schemes using official source data, retrieval, and simple explanations.
                <br><br>
                The application does not replace official government guidance. It supports discovery,
                awareness, and first-level understanding.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-heading">Technology Stack</div>', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.columns(4, gap="medium")

    with t1:
        render_feature_card("🐍", "Python", "Core programming language for scraping, RAG, and UI.")

    with t2:
        render_feature_card("🧠", "LangChain", "Used to build the Retrieval-Augmented Generation pipeline.")

    with t3:
        render_feature_card("🗂️", "ChromaDB", "Stores scheme embeddings for semantic retrieval.")

    with t4:
        render_feature_card("📊", "Streamlit", "Creates the citizen-friendly web interface.")

    st.markdown('<div class="section-heading">Responsible AI Disclaimer</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="warning-box">
            This AI assistant is for informational support only. Users should verify final eligibility,
            scheme validity, subsidy amount, documents required, and application process from official
            Tamil Nadu Government sources before taking action.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Main App
# ---------------------------------------------------------
def main():
    inject_css()

    df = load_scheme_data()

    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <div class="sidebar-logo-row">
                    <div class="tn-logo">{LOGO_SVG}</div>
                    <div class="sidebar-title">TN Scheme<br>Navigator AI</div>
                </div>
                <div class="sidebar-subtitle">
                    AI-powered Tamil Nadu Government Scheme Assistant.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        selected_page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "🤖 AI Scheme Assistant",
                "📚 Scheme Explorer",
                "ℹ️ About",
            ],
        )

        st.markdown("---")

        if df.empty:
            st.markdown(
                """
                <div class="sidebar-text">
                    ⚠️ Scheme data not found.<br>
                    Run scraper and ingest first.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="sidebar-text">
                    ✅ Scheme data loaded<br>
                    Total schemes indexed: <strong>{len(df)}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown(
            """
            <div class="sidebar-text">
                Built using LangChain, RAG, ChromaDB, OpenAI, and Streamlit.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if selected_page == "🏠 Home":
        home_page(df)
    elif selected_page == "🤖 AI Scheme Assistant":
        assistant_page()
    elif selected_page == "📚 Scheme Explorer":
        scheme_explorer_page(df)
    elif selected_page == "ℹ️ About":
        about_page()

    render_footer()


if __name__ == "__main__":
    main()