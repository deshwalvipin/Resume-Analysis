import json
import os
import streamlit as st

st.set_page_config(page_title="Resume Analyzer", page_icon="🧠", layout="wide")

# ---------- Defaults in session ----------
defaults = {
    "page": "Home",
    "theme": "Dark",            # "Dark" | "Light"
    "language": "English",      # "English" | "Español" | "हिंदी"
    "accent": "#7c3aed",        # primary color
    "density": "Comfortable",   # "Comfortable" | "Compact"
    "animations": True,         # balloons/snow etc.
    "persist_history": False,   # save history.json
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)
st.session_state.setdefault("history", [])

# ---------- Simple i18n ----------
I18N = {
    "English": {
        "HOME_HERO_TITLE": "Make your resumes",
        "HOME_HERO_GLOW": "shine",
        "HOME_HERO_TAGLINE": "Upload a resume, extract key sections and skills, benchmark against a job description, and track improvements over time.",
        "NAV_HOME": "Home", "NAV_ANALYZE": "Analyze", "NAV_HISTORY": "History", "NAV_SETTINGS": "Settings",
        "ANALYZE_TITLE": "Analyze Resume",
        "HISTORY_TITLE": "History",
        "SETTINGS_TITLE": "Settings",
    },
    "Español": {
        "HOME_HERO_TITLE": "Haz que tu currículum",
        "HOME_HERO_GLOW": "brille",
        "HOME_HERO_TAGLINE": "Sube un currículum, extrae secciones y habilidades, compáralo con una oferta y sigue las mejoras.",
        "NAV_HOME": "Inicio", "NAV_ANALYZE": "Analizar", "NAV_HISTORY": "Historial", "NAV_SETTINGS": "Ajustes",
        "ANALYZE_TITLE": "Analizar Currículum",
        "HISTORY_TITLE": "Historial",
        "SETTINGS_TITLE": "Ajustes",
    },
    "हिंदी": {
        "HOME_HERO_TITLE": "अपने रिज़्यूमे को",
        "HOME_HERO_GLOW": "दमकाइए",
        "HOME_HERO_TAGLINE": "रिज़्यूमे अपलोड करें, सेक्शन/स्किल्स निकालें, जॉब डिस्क्रिप्शन से मिलाएँ और समय के साथ सुधार ट्रैक करें।",
        "NAV_HOME": "होम", "NAV_ANALYZE": "विश्लेषण", "NAV_HISTORY": "इतिहास", "NAV_SETTINGS": "सेटिंग्स",
        "ANALYZE_TITLE": "रिज़्यूमे विश्लेषण",
        "HISTORY_TITLE": "इतिहास",
        "SETTINGS_TITLE": "सेटिंग्स",
    },
}
def t(key: str) -> str:
    lang = st.session_state.get("language", "English")
    return I18N.get(lang, I18N["English"]).get(key, key)

# ---------- Theming (Dark/Light) ----------
def _density_px() -> str:
    return "0.65rem 0.9rem" if st.session_state.get("density") == "Compact" else "1rem 1.25rem"

def apply_theme_css():
    theme = st.session_state.get("theme", "Dark")
    accent = st.session_state.get("accent", "#7c3aed")

    if theme == "Light":
        bg1, bg2 = "#eef2ff", "#e2e8f0"         # soft indigo -> gray
        card = "rgba(255,255,255,0.7)"
        text, muted = "#111827", "#6b7280"
        glass = "rgba(255,255,255,0.6)"
        border = "rgba(0,0,0,0.08)"
        metric_val, metric_delta = "#111827", "#166534"
    else:  # Dark
        bg1, bg2 = "#0f172a", "#1e293b"
        card = "#0b1220"
        text, muted = "#e2e8f0", "#94a3b8"
        glass = "rgba(255,255,255,0.06)"
        border = "rgba(255,255,255,0.12)"
        metric_val, metric_delta = "#e5e7eb", "#a7f3d0"

    st.markdown(f"""
    <style>
    :root {{
      --bg1:{bg1};
      --bg2:{bg2};
      --card:{card};
      --glass:{glass};
      --glass-border:{border};
      --text:{text};
      --muted:{muted};
      --brand:{accent};
      --brand-2:#06b6d4;
      --ok:#22c55e;
      --warn:#f59e0b;
      --danger:#ef4444;
    }}
    html, body, [data-testid="stAppViewContainer"] {{
      background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 100%) !important;
      color: var(--text);
    }}
    #MainMenu, footer, header {{visibility:hidden;}}

    .block-container {{ padding-top: 2rem; }}
    .glass {{
      background: var(--glass);
      border: 1px solid var(--glass-border);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-radius: 16px;
      padding: {_density_px()};
      box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }}

    .taskbar {{ display:flex; gap:.75rem; align-items:center; margin:.75rem 0 1rem 0; }}
    .taskbar .stButton > button {{
      width:100%; border-radius:9999px; border:1px solid var(--glass-border);
      background: linear-gradient(135deg, color-mix(in srgb, var(--brand), transparent 85%), color-mix(in srgb, var(--brand-2), transparent 88%));
      color: var(--text); padding:.6rem 1rem; font-weight:600; transition: all .2s ease; 
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
    }}
    .taskbar .stButton > button:hover {{ transform: translateY(-1px); border-color: rgba(255,255,255,0.25); }}
    .taskbar .active .stButton > button {{
      background: linear-gradient(135deg, var(--brand), var(--brand-2)); border-color: transparent;
      color: white;
    }}

    .cta .stButton > button {{
      width:100%; border-radius:16px; border:1px solid var(--glass-border);
      background: linear-gradient(135deg, color-mix(in srgb, var(--brand), transparent 82%), color-mix(in srgb, var(--brand-2), transparent 86%));
      color: var(--text); padding: 1rem 1.25rem; font-size:1.05rem; font-weight:700; transition: all .2s ease;
    }}
    .cta .stButton > button:hover {{ transform: translateY(-2px) scale(1.01); border-color: rgba(255,255,255,0.25); }}

    .badge {{
      display:inline-block; padding:.25rem .6rem; border-radius:9999px;
      background: rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.15); font-size:.75rem; color:var(--muted);
    }}
    .gradient-text {{
      background: linear-gradient(90deg, color-mix(in srgb, var(--brand), #a78bfa 50%), var(--brand-2), #34d399);
      -webkit-background-clip:text; background-clip:text; color:transparent; animation:hue 6s linear infinite;
    }}
    @keyframes hue {{ 0% {{filter:hue-rotate(0deg)}} 100% {{filter:hue-rotate(360deg)}} }}
    [data-testid="stMetricValue"] {{ color: {metric_val}; }}
    [data-testid="stMetricDelta"] {{ color: {metric_delta}; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme_css()

# ---------- (your nav + pages go below like before) ----------


import streamlit as st
from views.home import view as view_home
# Frontend/app.py
from views.analysis import view_analysis as view_analyze
from views.history import view as view_history
from views.settings import view as view_settings

st.set_page_config(page_title="Resume Analyzer", page_icon="🧠", layout="wide")

# Hide sidebar + chrome
st.markdown("""
<style>
[data-testid="stSidebar"], section[data-testid="stSidebar"] {display:none!important;}
div[data-testid="collapsedControl"] {display:none!important;}
#MainMenu, footer, header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# Global app state
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "history" not in st.session_state:
    # Each item: {"ts": "...", "filename": "...", "summary": "...", "score": float, "details": {...}}
    st.session_state.history = []

def goto(page: str):
    st.session_state.page = page
    st.rerun()

def task_bar():
    pages = [("Home", t("NAV_HOME")), ("Analyze", t("NAV_ANALYZE")),
             ("History", t("NAV_HISTORY")), ("Settings", t("NAV_SETTINGS"))]
    cols = st.columns(len(pages), vertical_alignment="center")
    with st.container():
        st.markdown('<div class="taskbar">', unsafe_allow_html=True)
        for (key, label), col in zip(pages, cols):
            with col:
                active = (st.session_state.page == key)
                st.markdown(f'<div class="{ "active" if active else "" }">', unsafe_allow_html=True)
                if st.button(("✅ " if active else "") + label, use_container_width=True, key=f"nav_{key}"):
                    st.session_state.page = key
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="glass"></div>', unsafe_allow_html=True)
task_bar()

page = st.session_state.page
if page == "Home":
    view_home()
elif page == "Analyze":
    view_analyze()
elif page == "History":
    view_history()
elif page == "Settings":
    view_settings()
