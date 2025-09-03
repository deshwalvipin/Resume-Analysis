# Frontend/app.py
import streamlit as st
from utils.ui import apply_theme_css, t

from views.home import view as view_home
from views.analysis import view_analysis as view_analyze
from views.history import view as view_history
from views.settings import view as view_settings

# ---- ONE page_config only ----
st.set_page_config(page_title="Resume Analyzer", page_icon="🧠", layout="wide")

# ---- Defaults ----
defaults = {
    "page": "Home",
    "theme": "Dark",
    "language": "English",
    "accent": "#7c3aed",
    "density": "Comfortable",
    "animations": True,
    "persist_history": False,
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)
st.session_state.setdefault("history", [])

# ---- Theme ----
apply_theme_css()

# ---- (Optional) hide the default sidebar ----
st.markdown("""
<style>
[data-testid="stSidebar"], section[data-testid="stSidebar"] {display:none!important;}
div[data-testid="collapsedControl"] {display:none!important;}
#MainMenu, footer, header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

def task_bar():
    pages = [("Home", t("NAV_HOME")), ("Analyze", t("NAV_ANALYZE")),
             ("History", t("NAV_HISTORY")), ("Settings", t("NAV_SETTINGS"))]
    cols = st.columns(len(pages), vertical_alignment="center")
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

# ---- Router ----
page = st.session_state.page
if page == "Home":
    view_home()
elif page == "Analyze":
    view_analyze()
elif page == "History":
    view_history()
elif page == "Settings":
    view_settings()
