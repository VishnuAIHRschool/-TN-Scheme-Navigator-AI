# ACTIVE AI ENGINE:
# app.py uses hybrid_rag_engine.ask_hybrid_ai() as the primary AI engine.
# hybrid_rag_engine combines rag_engine.py for ChromaDB Vector RAG and graph_rag_engine.py for Graph RAG.
# graph_rag_engine.py defaults to local NetworkX fallback and uses Neo4j AuraDB only when USE_NEO4J=true.
import html
import os
from typing import Any, List, Tuple

import pandas as pd
import streamlit as st

from rag_engine import ask_scheme_ai

try:
    from hybrid_rag_engine import ask_hybrid_ai
except Exception:
    ask_hybrid_ai = None

try:
    from language_utils import get_ui_text
except Exception:
    get_ui_text = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TN Scheme Navigator AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = "data/tn_scheme_details.csv"


# ============================================================
# BASIC UTILITIES
# ============================================================

def clean_value(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def esc(value: Any) -> str:
    return html.escape(clean_value(value))


def get_safe_column(row: pd.Series, column: str) -> str:
    if column not in row:
        return ""
    return clean_value(row.get(column, ""))


def safe_source_text(source: Any) -> str:
    if isinstance(source, dict):
        title = (
            source.get("title")
            or source.get("scheme_title")
            or source.get("name")
            or "Official source"
        )
        url = source.get("source_url") or source.get("url") or source.get("link") or ""
        return f"{title} - {url}" if url else str(title)

    return clean_value(source)


def fallback_ui_text(language: str):
    if language == "Tamil":
        return {
            "page_title": "அறிவு வரைபட RAG உதவியாளர்",
            "intro": "இந்த பக்கம் ChromaDB Vector RAG மற்றும் Neo4j Knowledge Graph RAG இரண்டையும் பயன்படுத்துகிறது.",
            "question_label": "உங்கள் கேள்வியை கேளுங்கள்",
            "placeholder": "உதாரணம்: விவசாயிகளுக்கான மானிய திட்டங்கள் எவை?",
            "button": "Hybrid Graph RAG மூலம் கேளுங்கள்",
            "answer_heading": "AI பதில்",
            "sources_heading": "அதிகாரப்பூர்வ ஆதாரங்கள்",
        }

    if language == "Bilingual":
        return {
            "page_title": "Knowledge Graph RAG Assistant / அறிவு வரைபட உதவியாளர்",
            "intro": "This page uses Vector RAG and Neo4j Graph RAG. / இந்த பக்கம் இரண்டு RAG முறைகளையும் பயன்படுத்துகிறது.",
            "question_label": "Ask your question / உங்கள் கேள்வியை கேளுங்கள்",
            "placeholder": "Example: Which schemes are sponsored by State? / மாநில அரசு நிதியுதவி வழங்கும் திட்டங்கள் எவை?",
            "button": "Ask Hybrid Graph RAG",
            "answer_heading": "Hybrid AI Answer / AI பதில்",
            "sources_heading": "Official Sources / அதிகாரப்பூர்வ ஆதாரங்கள்",
        }

    return {
        "page_title": "Knowledge Graph RAG Assistant",
        "intro": "This page uses both ChromaDB Vector RAG and Neo4j Knowledge Graph RAG.",
        "question_label": "Ask your Knowledge Graph question",
        "placeholder": "Example: Which schemes are sponsored by State?",
        "button": "Ask Hybrid Graph RAG",
        "answer_heading": "Hybrid AI Answer",
        "sources_heading": "Official References",
    }


def get_text(language: str):
    if get_ui_text:
        try:
            return get_ui_text(language)
        except Exception:
            return fallback_ui_text(language)
    return fallback_ui_text(language)


def get_language_note(language: str) -> str:
    if language == "Tamil":
        return "AI பதில் எளிய, குடிமக்களுக்கு புரியும் தமிழில் வழங்கப்படும்."
    if language == "Bilingual":
        return "AI answer will be provided in English and Tamil."
    return "AI answer will be provided in clear professional English."


# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data(show_spinner=False)
def load_scheme_data() -> pd.DataFrame:
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)
    df = df.fillna("")
    return df


def get_column_values(df: pd.DataFrame, column: str) -> List[str]:
    if df.empty or column not in df.columns:
        return []

    values = (
        df[column]
        .astype(str)
        .map(lambda x: x.strip())
        .replace("", pd.NA)
        .dropna()
        .unique()
        .tolist()
    )

    return sorted(values)


# ============================================================
# CSS
# ============================================================

def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+Tamil:wght@400;500;600;700;800&display=swap');

        :root {
            --navy: #071b2f;
            --navy-2: #0b2540;
            --green: #0f766e;
            --green-dark: #14532d;
            --green-soft: #ecfdf5;
            --gold: #f59e0b;
            --gold-soft: #fff7ed;
            --slate: #0f172a;
            --muted: #475569;
            --border: #dbe4ee;
            --surface: #ffffff;
            --surface-2: #f8fafc;
            --danger: #b91c1c;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', 'Noto Sans Tamil', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 10% 5%, rgba(15, 118, 110, 0.14), transparent 26%),
                radial-gradient(circle at 92% 8%, rgba(245, 158, 11, 0.16), transparent 24%),
                linear-gradient(135deg, #f8fafc 0%, #f0fdf4 45%, #eff6ff 100%);
        }

        .main .block-container {
            padding-top: 1.35rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at top left, rgba(245, 158, 11, 0.18), transparent 26%),
                linear-gradient(180deg, #071b2f 0%, #0b2540 42%, #064e3b 100%);
            border-right: 1px solid rgba(255,255,255,0.14);
            width: 330px !important;
        }

        section[data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }

        .sidebar-brand-card {
            padding: 18px 16px;
            border-radius: 24px;
            background: rgba(255,255,255,0.09);
            border: 1px solid rgba(255,255,255,0.14);
            box-shadow: 0 18px 44px rgba(0,0,0,0.22);
            margin: 6px 0 18px 0;
        }

        .sidebar-logo {
            width: 54px;
            height: 54px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #f59e0b, #10b981);
            font-size: 30px;
            margin-bottom: 12px;
            box-shadow: 0 12px 26px rgba(0,0,0,0.24);
        }

        .sidebar-title {
            font-size: 27px;
            font-weight: 900;
            line-height: 1.06;
            letter-spacing: -0.04em;
            color: #ffffff;
            margin-bottom: 8px;
        }

        .sidebar-subtitle {
            font-size: 13px;
            line-height: 1.55;
            color: #d1fae5 !important;
        }

        .sidebar-info-card {
            padding: 15px 15px;
            border-radius: 20px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.13);
            margin-top: 14px;
            font-size: 13px;
            line-height: 1.6;
            color: #d1fae5;
        }

        .sidebar-section-title {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #fde68a !important;
            font-weight: 900;
            margin: 12px 0 8px 0;
        }

        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stRadio label {
            font-size: 13px !important;
            font-weight: 800 !important;
            letter-spacing: 0.01em;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.11);
            border-radius: 16px;
            padding: 11px 12px;
            margin-bottom: 9px;
            min-height: 46px;
            transition: all 0.20s ease;
            box-shadow: 0 8px 18px rgba(0,0,0,0.12);
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(245, 158, 11, 0.60);
            transform: translateX(2px);
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(135deg, rgba(245,158,11,0.28), rgba(16,185,129,0.20));
            border: 1px solid rgba(253, 230, 138, 0.95);
            box-shadow: 0 12px 26px rgba(0,0,0,0.22);
        }

        /* Header */
        .portal-header {
            position: relative;
            overflow: hidden;
            background:
                linear-gradient(135deg, rgba(7, 27, 47, 0.98), rgba(15, 81, 50, 0.96)),
                url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=1600&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            border-radius: 30px;
            padding: 38px 40px;
            color: #ffffff;
            box-shadow: 0 24px 65px rgba(15, 23, 42, 0.23);
            margin-bottom: 26px;
            border: 1px solid rgba(255,255,255,0.18);
        }

        .portal-header:after {
            content: "";
            position: absolute;
            right: -120px;
            top: -140px;
            width: 330px;
            height: 330px;
            border-radius: 50%;
            background: rgba(245,158,11,0.22);
            filter: blur(2px);
        }

        .portal-content {
            position: relative;
            z-index: 1;
        }

        .portal-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(251, 191, 36, 0.18);
            color: #fde68a;
            border: 1px solid rgba(251, 191, 36, 0.42);
            border-radius: 999px;
            padding: 8px 14px;
            font-size: 12px;
            font-weight: 900;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            margin-bottom: 15px;
        }

        .portal-title {
            font-size: clamp(36px, 5vw, 54px);
            line-height: 1.03;
            font-weight: 900;
            margin: 0 0 14px 0;
            letter-spacing: -0.055em;
        }

        .portal-subtitle {
            max-width: 900px;
            font-size: 17px;
            line-height: 1.7;
            color: #e2e8f0;
            margin: 0;
            font-weight: 500;
        }

        .header-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 22px;
        }

        .header-chip {
            display: inline-flex;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.11);
            border: 1px solid rgba(255,255,255,0.16);
            color: #f8fafc;
            font-size: 12px;
            font-weight: 800;
        }

        /* Typography */
        .section-heading {
            font-size: 28px;
            font-weight: 900;
            color: #0f172a;
            margin: 28px 0 14px 0;
            letter-spacing: -0.035em;
        }

        .section-subheading {
            font-size: 16px;
            color: #475569;
            line-height: 1.7;
            margin-bottom: 18px;
        }

        .mini-label {
            font-size: 12px;
            font-weight: 900;
            color: #0f766e;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        /* Cards */
        .info-box {
            background: rgba(255,255,255,0.92);
            border: 1px solid #dbeafe;
            border-left: 6px solid #0f766e;
            border-radius: 20px;
            padding: 20px 22px;
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.07);
            color: #334155;
            font-size: 16px;
            line-height: 1.75;
            margin-bottom: 20px;
        }

        .question-card {
            background:
                linear-gradient(135deg, rgba(255,255,255,0.96), rgba(240,253,244,0.96));
            border: 1px solid rgba(15, 118, 110, 0.18);
            border-radius: 26px;
            padding: 24px;
            box-shadow: 0 20px 55px rgba(15,23,42,0.10);
            margin: 18px 0 22px 0;
        }

        .question-card-title {
            font-size: 22px;
            color: #0f172a;
            font-weight: 900;
            letter-spacing: -0.03em;
            margin-bottom: 8px;
        }

        .question-card-text {
            font-size: 15px;
            color: #475569;
            line-height: 1.65;
            margin-bottom: 18px;
        }

        .feature-card {
            background: rgba(255,255,255,0.94);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 24px;
            padding: 24px;
            min-height: 198px;
            box-shadow: 0 16px 38px rgba(15, 23, 42, 0.08);
            transition: 0.20s ease;
        }

        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 20px 48px rgba(15, 23, 42, 0.12);
        }

        .feature-icon {
            font-size: 32px;
            margin-bottom: 12px;
        }

        .feature-title {
            font-size: 19px;
            font-weight: 900;
            color: #0f172a;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }

        .feature-text {
            color: #475569;
            line-height: 1.65;
            font-size: 15px;
        }

        .stat-card {
            background: linear-gradient(135deg, #ffffff, #f8fafc);
            border-radius: 22px;
            padding: 22px;
            border: 1px solid rgba(15,23,42,0.08);
            box-shadow: 0 14px 30px rgba(15,23,42,0.08);
            min-height: 118px;
        }

        .stat-value {
            color: #0f766e;
            font-size: 36px;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 8px;
        }

        .stat-label {
            color: #334155;
            font-size: 14px;
            font-weight: 800;
        }

        .answer-card {
            background:
                linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 24px;
            padding: 26px 28px;
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 20px 52px rgba(15, 23, 42, 0.11);
            color: #1e293b;
            line-height: 1.85;
            font-size: 16px;
            white-space: pre-wrap;
            margin-top: 10px;
        }

        .answer-title-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 12px;
        }

        .route-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 13px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 900;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            border: 1px solid rgba(15,118,110,0.26);
            background: #ecfdf5;
            color: #047857;
        }

        .route-badge.hybrid {
            background: #eef2ff;
            color: #3730a3;
            border-color: #c7d2fe;
        }

        .route-badge.graph {
            background: #fff7ed;
            color: #c2410c;
            border-color: #fed7aa;
        }

        .route-badge.vector {
            background: #ecfdf5;
            color: #047857;
            border-color: #a7f3d0;
        }

        .source-card {
            background: #ffffff;
            border-radius: 20px;
            padding: 17px 18px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 12px 28px rgba(15,23,42,0.07);
            margin-bottom: 13px;
            color: #334155;
            line-height: 1.65;
        }

        .source-card a {
            color: #0f766e !important;
            font-weight: 800;
            text-decoration: none;
        }

        .scheme-card {
            background:
                linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
            border-radius: 24px;
            padding: 22px 24px;
            border: 1px solid rgba(15,23,42,0.08);
            box-shadow: 0 16px 38px rgba(15,23,42,0.08);
            margin-bottom: 18px;
        }

        .scheme-title {
            color: #0f172a;
            font-size: 21px;
            font-weight: 900;
            letter-spacing: -0.03em;
            margin-bottom: 12px;
        }

        .scheme-meta-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px 16px;
            margin-bottom: 12px;
        }

        .scheme-meta {
            color: #475569;
            font-size: 14px;
            line-height: 1.55;
        }

        .scheme-meta strong {
            color: #0f172a;
        }

        .scheme-desc {
            color: #334155;
            line-height: 1.7;
            font-size: 15px;
            margin-top: 12px;
        }

        .badge {
            display: inline-block;
            padding: 7px 11px;
            border-radius: 999px;
            background: #ecfdf5;
            color: #047857;
            border: 1px solid #a7f3d0;
            font-size: 12px;
            font-weight: 900;
            margin: 4px 5px 4px 0;
        }

        .badge.gold {
            background: #fffbeb;
            color: #b45309;
            border-color: #fde68a;
        }

        .badge.blue {
            background: #eff6ff;
            color: #1d4ed8;
            border-color: #bfdbfe;
        }

        .badge.purple {
            background: #f5f3ff;
            color: #6d28d9;
            border-color: #ddd6fe;
        }

        .loading-card {
            background:
                linear-gradient(135deg, #ffffff, #f0fdf4);
            border-radius: 24px;
            padding: 24px;
            border: 1px dashed #0f766e;
            color: #334155;
            font-weight: 800;
            box-shadow: 0 14px 34px rgba(15,23,42,0.08);
            line-height: 1.65;
        }

        .footer {
            color: #64748b;
            font-size: 13px;
            text-align: center;
            padding: 30px 0 8px 0;
        }

        /* Inputs */
        .stTextArea textarea,
        .stTextInput input {
            background: #f8fafc !important;
            color: #0f172a !important;
            border: 1px solid #9ca3af !important;
            border-radius: 16px !important;
            box-shadow: inset 0 1px 2px rgba(15,23,42,0.04);
            font-size: 15px !important;
            line-height: 1.6 !important;
        }

        .stTextArea textarea:focus,
        .stTextInput input:focus {
            border: 2px solid #0f766e !important;
            box-shadow: 0 0 0 4px rgba(15,118,110,0.12) !important;
        }

        .stTextArea textarea::placeholder,
        .stTextInput input::placeholder {
            color: #64748b !important;
            opacity: 1 !important;
        }

        .stSelectbox div[data-baseweb="select"] {
            background-color: #f8fafc !important;
            color: #0f172a !important;
            border-radius: 16px !important;
            border-color: #cbd5e1 !important;
        }

        .stButton > button {
            width: 100%;
            border-radius: 16px;
            border: 1px solid rgba(15, 118, 110, 0.24);
            background: linear-gradient(135deg, #0f766e, #14532d);
            color: white !important;
            font-weight: 900;
            padding: 0.78rem 1.1rem;
            box-shadow: 0 12px 26px rgba(15, 118, 110, 0.22);
            transition: all 0.20s ease;
        }

        .stButton > button:hover {
            border-color: #f59e0b;
            background: linear-gradient(135deg, #115e59, #064e3b);
            color: white !important;
            transform: translateY(-1px);
            box-shadow: 0 16px 34px rgba(15, 118, 110, 0.28);
        }

        .stButton > button:active {
            transform: translateY(0px);
        }

        div[data-testid="stMetricValue"] {
            color: #0f766e;
            font-weight: 900;
        }

        hr {
            border-color: rgba(148, 163, 184, 0.28);
        }

        @media (max-width: 900px) {
            .portal-header {
                padding: 28px 24px;
                border-radius: 24px;
            }

            .scheme-meta-grid {
                grid-template-columns: 1fr;
            }

            .portal-title {
                font-size: 36px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# RENDER COMPONENTS
# ============================================================

def render_sidebar_brand():
    st.sidebar.markdown(
        """
        <div class="sidebar-brand-card">
            <div class="sidebar-logo">🌾</div>
            <div class="sidebar-title">TN Scheme<br>Navigator AI</div>
            <div class="sidebar-subtitle">
                Hybrid Vector RAG + Neo4j Graph RAG assistant for Tamil Nadu Government schemes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(language: str) -> str:
    render_sidebar_brand()

    st.sidebar.markdown('<div class="sidebar-section-title">Navigation</div>', unsafe_allow_html=True)

    selected_page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "🤖 AI Scheme Assistant",
            "📚 Scheme Explorer",
            "🕸️ Knowledge Graph RAG",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

    st.sidebar.markdown('<div class="sidebar-section-title">App Context</div>', unsafe_allow_html=True)

    st.sidebar.markdown(
        f"""
        <div class="sidebar-info-card">
            <strong>Response language</strong><br>
            {esc(language)}<br><br>
            <strong>AI architecture</strong><br>
            Vector RAG · Graph RAG · Hybrid Routing<br><br>
            <strong>Stack</strong><br>
            Streamlit · LangChain · OpenAI · ChromaDB · Neo4j AuraDB · NetworkX
        </div>
        """,
        unsafe_allow_html=True,
    )

    return selected_page


def render_portal_header():
    st.markdown(
        """
        <div class="portal-header">
            <div class="portal-content">
                <div class="portal-eyebrow">Government-tech AI assistant</div>
                <div class="portal-title">TN Scheme Navigator AI</div>
                <p class="portal-subtitle">
                    A production-style Hybrid RAG application for Tamil Nadu Government schemes.
                    It combines semantic search, knowledge graph reasoning, official references,
                    and Tamil-friendly AI responses.
                </p>
                <div class="header-chip-row">
                    <span class="header-chip">🔎 ChromaDB Vector RAG</span>
                    <span class="header-chip">🕸️ Neo4j Graph RAG</span>
                    <span class="header-chip">தமிழ் + English</span>
                    <span class="header-chip">✅ Official Source Links</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_card(icon: str, title: str, text: str):
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{esc(title)}</div>
            <div class="feature-text">{esc(text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(value: Any, label: str):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-value">{esc(value)}</div>
            <div class="stat-label">{esc(label)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_loading_card():
    st.markdown(
        """
        <div class="loading-card">
            🔎 <strong>Generating verified AI response...</strong><br>
            Searching semantic vector data, knowledge graph relationships, and official references.
        </div>
        """,
        unsafe_allow_html=True,
    )


def route_class(route: str) -> str:
    route_clean = clean_value(route).lower()
    if "graph" in route_clean:
        return "graph"
    if "hybrid" in route_clean:
        return "hybrid"
    return "vector"


def render_route_badge(route: str):
    css_class = route_class(route)
    route_label = clean_value(route).upper() if route else "VECTOR"
    icon = "🕸️" if css_class == "graph" else "⚡" if css_class == "hybrid" else "🔎"

    st.markdown(
        f"""
        <div class="route-badge {css_class}">
            {icon} AI Route Used: {esc(route_label)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_answer_card(answer: str):
    st.markdown(
        f"""
        <div class="answer-card">
            {esc(answer)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_source_cards(sources: List[Any]):
    if not sources:
        st.info("No official source references were returned.")
        return

    for index, source in enumerate(sources, start=1):
        source_text = safe_source_text(source)

        if "http" in source_text:
            parts = source_text.split("http", 1)
            title = parts[0].strip(" -")
            url = "http" + parts[1].strip()

            st.markdown(
                f"""
                <div class="source-card">
                    <div class="mini-label">Official Reference {index}</div>
                    <strong>{esc(title) if title else "Official source"}</strong><br>
                    <a href="{esc(url)}" target="_blank">Open official source</a>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="source-card">
                    <div class="mini-label">Official Reference {index}</div>
                    {esc(source_text)}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_footer():
    st.markdown(
        """
        <div class="footer">
            Built by Vishnukumar · TN Scheme Navigator AI · Hybrid Graph RAG Project
        </div>
        """,
        unsafe_allow_html=True,
    )


def detect_badges(row: pd.Series) -> List[str]:
    text = " ".join([clean_value(v) for v in row.values]).lower()
    badges = []

    if "farmer" in text or "farmers" in text or "விவசாய" in text:
        badges.append("Farmer Support")
    if "grant" in text:
        badges.append("Grant")
    if "subsidy" in text:
        badges.append("Subsidy")
    if "seed" in text or "seeds" in text:
        badges.append("Seed Support")
    if "training" in text:
        badges.append("Training")
    if "soil" in text:
        badges.append("Soil Health")
    if "state" in text:
        badges.append("State Sponsored")
    if "central" in text:
        badges.append("Central Sponsored")

    return badges[:6]


def badge_class(badge: str) -> str:
    b = badge.lower()
    if "grant" in b or "subsidy" in b or "sponsored" in b:
        return "gold"
    if "seed" in b or "soil" in b:
        return "blue"
    if "training" in b:
        return "purple"
    return ""


def render_badges(badges: List[str]):
    badge_html = "".join(
        [
            f'<span class="badge {badge_class(badge)}">{esc(badge)}</span>'
            for badge in badges
        ]
    )
    st.markdown(badge_html, unsafe_allow_html=True)


def render_question_shell(title: str, text: str):
    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-card-title">{esc(title)}</div>
            <div class="question-card-text">{esc(text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# AI CALL HELPERS
# ============================================================

def run_vector_ai(question: str, language: str = "English") -> Tuple[str, List[Any]]:
    response = ask_scheme_ai(question, language)

    if isinstance(response, tuple):
        if len(response) >= 2:
            return response[0], response[1]
        if len(response) == 1:
            return response[0], []

    return str(response), []


def run_hybrid_ai(question: str, language: str) -> Tuple[str, List[Any], str]:
    if ask_hybrid_ai is None:
        answer, sources = run_vector_ai(question, language)
        return answer, sources, "vector"

    response = ask_hybrid_ai(question, language)

    if isinstance(response, tuple):
        if len(response) == 3:
            return response[0], response[1], response[2]
        if len(response) == 2:
            return response[0], response[1], "hybrid"

    return str(response), [], "hybrid"


# ============================================================
# SESSION STATE HELPERS
# ============================================================

def set_assistant_question(question: str):
    st.session_state["assistant_question"] = question


def set_graph_question(question: str):
    st.session_state["graph_question"] = question


# ============================================================
# PAGES
# ============================================================

def home_page(df: pd.DataFrame):
    render_portal_header()

    st.markdown('<div class="section-heading">Project Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    total_schemes = len(df) if not df.empty else 0
    departments = len(get_column_values(df, "concerned_department"))
    beneficiaries = len(get_column_values(df, "beneficiaries"))
    benefits = len(get_column_values(df, "types_of_benefits"))

    with col1:
        render_stat_card(total_schemes, "Schemes Loaded")
    with col2:
        render_stat_card(departments, "Departments")
    with col3:
        render_stat_card(beneficiaries, "Beneficiary Groups")
    with col4:
        render_stat_card(benefits, "Benefit Types")

    st.markdown('<div class="section-heading">What This App Does</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        render_feature_card(
            "🔎",
            "Semantic Scheme Search",
            "Uses ChromaDB and OpenAI embeddings to find scheme information by meaning, not just exact keywords.",
        )

    with c2:
        render_feature_card(
            "🕸️",
            "Knowledge Graph Reasoning",
            "Uses Neo4j AuraDB to understand relationships between schemes, departments, sponsors, beneficiaries, and benefits.",
        )

    with c3:
        render_feature_card(
            "தமிழ்",
            "Tamil + English AI",
            "Supports English, Tamil, and bilingual responses so scheme information is easier for citizens to understand.",
        )

    st.markdown('<div class="section-heading">Production Architecture</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
            <strong>Data Collection:</strong> Tamil Nadu Government scheme data is scraped and structured into CSV.<br>
            <strong>Vector Layer:</strong> Scheme text is embedded and stored in ChromaDB for semantic retrieval.<br>
            <strong>Graph Layer:</strong> Scheme relationships are stored in Neo4j AuraDB for Cypher-based reasoning.<br>
            <strong>Hybrid AI Layer:</strong> LangChain and OpenAI generate final answers with official references.
        </div>
        """,
        unsafe_allow_html=True,
    )


def assistant_page(language: str):
    render_portal_header()

    st.markdown('<div class="section-heading">AI Scheme Assistant</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="info-box">
            Ask a scheme-related question in English or Tamil. The assistant will search the available scheme data
            and provide a clear answer in the selected response language.
            <br><br>
            <strong>Selected language:</strong> {esc(language)}<br>
            <strong>Response style:</strong> {esc(get_language_note(language))}
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_question_shell(
        "Ask your scheme question",
        "Use the quick prompts below or type your own question. The AI will return a readable answer with official references when available.",
    )

    example_col_1, example_col_2, example_col_3 = st.columns(3, gap="medium")

    with example_col_1:
        st.button(
            "🌾 Farmer Schemes",
            key="assistant_farmer_schemes",
            on_click=set_assistant_question,
            args=("What schemes are available for farmers?",),
        )

    with example_col_2:
        st.button(
            "💰 Subsidy Schemes",
            key="assistant_subsidy_schemes",
            on_click=set_assistant_question,
            args=("Which schemes provide subsidy benefits for farmers?",),
        )

    with example_col_3:
        st.button(
            "தமிழ் கேள்வி",
            key="assistant_tamil_question",
            on_click=set_assistant_question,
            args=("விவசாயிகளுக்கான மானிய திட்டங்கள் எவை?",),
        )

    question = st.text_area(
        "Question / கேள்வி",
        key="assistant_question",
        height=145,
        placeholder="Example: What agriculture schemes are available for farmers?",
    )

    ask_clicked = st.button("Ask AI Scheme Assistant", key="ask_scheme_assistant")

    if ask_clicked:
        if not question.strip():
            st.warning("Please enter a question.")
            return

        answer_placeholder = st.empty()

        with answer_placeholder.container():
            render_loading_card()

        try:
            answer, sources, route = run_hybrid_ai(question, language)
        except Exception as error:
            answer_placeholder.empty()
            st.error("Unable to generate answer.")
            st.exception(error)
            return

        answer_placeholder.empty()

        st.markdown('<div class="section-heading">AI Answer</div>', unsafe_allow_html=True)
        render_route_badge(route)
        render_answer_card(answer)

        st.markdown('<div class="section-heading">Official References</div>', unsafe_allow_html=True)
        render_source_cards(sources)


def scheme_explorer_page(df: pd.DataFrame):
    render_portal_header()

    st.markdown('<div class="section-heading">Scheme Explorer</div>', unsafe_allow_html=True)

    if df.empty:
        st.error("Scheme CSV file not found or empty. Please run scrape_schemes.py first.")
        return

    st.markdown(
        """
        <div class="info-box">
            Explore the structured scheme dataset directly. Use filters to narrow results by department,
            beneficiary, benefit type, and keyword.
        </div>
        """,
        unsafe_allow_html=True,
    )

    filter_col_1, filter_col_2, filter_col_3 = st.columns(3, gap="medium")

    with filter_col_1:
        department_options = ["All"] + get_column_values(df, "concerned_department")
        selected_department = st.selectbox("Department", department_options)

    with filter_col_2:
        beneficiary_options = ["All"] + get_column_values(df, "beneficiaries")
        selected_beneficiary = st.selectbox("Beneficiary", beneficiary_options)

    with filter_col_3:
        benefit_options = ["All"] + get_column_values(df, "types_of_benefits")
        selected_benefit = st.selectbox("Benefit Type", benefit_options)

    search_text = st.text_input(
        "Search scheme title, description, benefit, or keyword",
        placeholder="Search by seed, grant, subsidy, training, soil, irrigation...",
    )

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
        searchable_cols = [
            col for col in [
                "scheme_title",
                "description",
                "beneficiaries",
                "types_of_benefits",
                "funding_pattern",
                "how_to_avail",
                "sponsored_by",
            ]
            if col in filtered_df.columns
        ]

        mask = pd.Series(False, index=filtered_df.index)
        for col in searchable_cols:
            mask = mask | filtered_df[col].astype(str).str.lower().str.contains(search_lower, na=False)

        filtered_df = filtered_df[mask]

    st.markdown(
        f"""
        <div class="info-box">
            <strong>{len(filtered_df)}</strong> scheme record(s) found based on your filter.
        </div>
        """,
        unsafe_allow_html=True,
    )

    for _, row in filtered_df.iterrows():
        scheme_title = get_safe_column(row, "scheme_title") or "Untitled Scheme"
        department = get_safe_column(row, "concerned_department")
        beneficiary = get_safe_column(row, "beneficiaries")
        benefit = get_safe_column(row, "types_of_benefits")
        sponsor = get_safe_column(row, "sponsored_by")
        funding = get_safe_column(row, "funding_pattern")
        description = get_safe_column(row, "description")
        source_url = get_safe_column(row, "source_url")

        st.markdown(
            f"""
            <div class="scheme-card">
                <div class="scheme-title">{esc(scheme_title)}</div>
                <div class="scheme-meta-grid">
                    <div class="scheme-meta"><strong>Department:</strong> {esc(department) if department else "Not available"}</div>
                    <div class="scheme-meta"><strong>Beneficiaries:</strong> {esc(beneficiary) if beneficiary else "Not available"}</div>
                    <div class="scheme-meta"><strong>Benefit Type:</strong> {esc(benefit) if benefit else "Not available"}</div>
                    <div class="scheme-meta"><strong>Sponsored By:</strong> {esc(sponsor) if sponsor else "Not available"}</div>
                    <div class="scheme-meta"><strong>Funding Pattern:</strong> {esc(funding) if funding else "Not available"}</div>
                </div>
                <div class="scheme-desc">
                    {esc(description[:520]) if description else "Description not available."}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        badges = detect_badges(row)
        if badges:
            render_badges(badges)

        if source_url:
            st.markdown(f"[Open official source]({source_url})")

        st.markdown("<br>", unsafe_allow_html=True)


def graph_rag_page(language: str):
    render_portal_header()

    ui = get_text(language)

    st.markdown(
        f'<div class="section-heading">{ui["page_title"]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="info-box">
            {ui["intro"]}
            <br><br>
            <strong>Smart AI flow:</strong><br>
            <strong>Vector RAG</strong> handles meaning-based questions.<br>
            <strong>Graph RAG</strong> handles relationship-based questions like sponsor, department, beneficiary, benefit type, grant, subsidy, and scheme connections.<br>
            <strong>Hybrid RAG</strong> combines both for richer answers.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if ask_hybrid_ai is None:
        st.warning(
            "hybrid_rag_engine.py is not available or has an import error. "
            "This page will fall back to Vector RAG only."
        )

    render_question_shell(
        "Ask a relationship-based scheme question",
        "Use the prompt buttons below or ask your own question. This page is best for questions involving scheme relationships, sponsors, beneficiaries, departments, grants, subsidies, and keywords.",
    )

    example_col_1, example_col_2, example_col_3 = st.columns(3, gap="medium")

    with example_col_1:
        st.button(
            "🏛️ State Sponsored Schemes",
            key="graph_state_sponsored",
            on_click=set_graph_question,
            args=("Which schemes are sponsored by State?",),
        )

    with example_col_2:
        st.button(
            "👨‍🌾 Farmer Grant Schemes",
            key="graph_farmer_grants",
            on_click=set_graph_question,
            args=("Which schemes are for farmers and provide grants?",),
        )

    with example_col_3:
        st.button(
            "🌱 Seed Support Schemes",
            key="graph_seed_support",
            on_click=set_graph_question,
            args=("Which schemes are related to seed support?",),
        )

    example_col_4, example_col_5, example_col_6 = st.columns(3, gap="medium")

    with example_col_4:
        st.button(
            "💰 Subsidy Schemes",
            key="graph_subsidy_schemes",
            on_click=set_graph_question,
            args=("Which schemes provide subsidy benefits?",),
        )

    with example_col_5:
        st.button(
            "🧪 Soil Health Schemes",
            key="graph_soil_health",
            on_click=set_graph_question,
            args=("Which schemes are connected to soil health?",),
        )

    with example_col_6:
        st.button(
            "தமிழ் கேள்வி",
            key="graph_tamil_question",
            on_click=set_graph_question,
            args=("விவசாயிகளுக்கான மானிய திட்டங்கள் எவை?",),
        )

    question = st.text_area(
        ui["question_label"],
        key="graph_question",
        height=150,
        placeholder=ui["placeholder"],
    )

    ask_button = st.button(ui["button"], key="ask_hybrid_graph_rag")

    if ask_button:
        if not question.strip():
            st.warning("Please enter a question.")
            return

        st.markdown(
            f'<div class="section-heading">{ui["answer_heading"]}</div>',
            unsafe_allow_html=True,
        )

        answer_placeholder = st.empty()

        with answer_placeholder.container():
            render_loading_card()

        try:
            answer, sources, route = run_hybrid_ai(question, language)
        except Exception as error:
            answer_placeholder.empty()
            st.error("Unable to generate Hybrid Graph RAG answer.")
            st.exception(error)
            return

        answer_placeholder.empty()

        render_route_badge(route)
        render_answer_card(answer)

        st.markdown(
            f'<div class="section-heading">{ui["sources_heading"]}</div>',
            unsafe_allow_html=True,
        )

        render_source_cards(sources)


def about_page():
    render_portal_header()

    st.markdown('<div class="section-heading">About This Project</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
            <strong>TN Scheme Navigator AI</strong> is a Hybrid Graph RAG application built to help users search,
            understand, and verify Tamil Nadu Government scheme information.
            <br><br>
            It combines semantic search, graph reasoning, bilingual AI response generation, and official source references.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-heading">Technology Stack</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")

    with c1:
        st.markdown(
            """
            <div class="source-card">
                <div class="mini-label">AI + Retrieval</div>
                <strong>Frontend:</strong> Streamlit<br>
                <strong>AI Orchestration:</strong> LangChain<br>
                <strong>LLM:</strong> OpenAI<br>
                <strong>Vector DB:</strong> ChromaDB<br>
                <strong>Embeddings:</strong> OpenAI Embeddings
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="source-card">
                <div class="mini-label">Graph + Observability</div>
                <strong>Knowledge Graph:</strong> Neo4j AuraDB<br>
                <strong>Graph Query:</strong> Cypher<br>
                <strong>Graph Analysis:</strong> NetworkX<br>
                <strong>Observability:</strong> LangSmith<br>
                <strong>Data Collection:</strong> BeautifulSoup + Requests
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-heading">Quality and Safety Notes</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
            This tool is designed for learning, exploration, and citizen-friendly information discovery.
            It should not be treated as the final legal or eligibility authority.
            Users should always verify eligibility, benefit details, and application process from the official government source link.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN APP
# ============================================================

def main():
    inject_css()

    df = load_scheme_data()

    language = st.sidebar.selectbox(
        "Response Language / பதில் மொழி",
        ["English", "Tamil", "Bilingual"],
        index=0,
    )

    selected_page = render_sidebar(language)

    if selected_page == "🏠 Home":
        home_page(df)
    elif selected_page == "🤖 AI Scheme Assistant":
        assistant_page(language)
    elif selected_page == "📚 Scheme Explorer":
        scheme_explorer_page(df)
    elif selected_page == "🕸️ Knowledge Graph RAG":
        graph_rag_page(language)
    elif selected_page == "ℹ️ About":
        about_page()

    render_footer()


if __name__ == "__main__":
    main()