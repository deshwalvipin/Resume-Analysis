import streamlit as st

st.set_page_config(page_title="Resume Analyzer", page_icon="🧠", layout="wide")
# --- Global CSS theme ---
st.markdown("""
<style>
:root{
  --bg1:#0f172a; /* slate-900 */
  --bg2:#1e293b; /* slate-800 */
  --card:#0b1220; /* very dark */
  --glass: rgba(255,255,255,0.06);
  --glass-border: rgba(255,255,255,0.12);
  --text:#e2e8f0; /* slate-200 */
  --muted:#94a3b8; /* slate-400 */
  --brand:#7c3aed; /* violet-600 */
  --brand-2:#06b6d4; /* cyan-500 */
  --ok:#22c55e; /* green-500 */
  --warn:#f59e0b; /* amber-500 */
  --danger:#ef4444; /* red-500 */
}

html, body, [data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 100%) !important;
  color: var(--text);
}

/* Hide Streamlit chrome (keep if you like it clean) */
#MainMenu, footer, header {visibility:hidden;}

/* Glass containers */
.block-container {
  padding-top: 2rem;
}
.glass {
  background: var(--glass);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

/* Task bar */
.taskbar {
  display:flex;
  gap:.75rem;
  align-items:center;
  margin: .75rem 0 1rem 0;
}
.taskbar .stButton > button {
  width:100%;
  border-radius: 9999px;
  border: 1px solid var(--glass-border);
  background: linear-gradient(135deg, rgba(124,58,237,.15), rgba(6,182,212,.12));
  color: var(--text);
  padding:.6rem 1rem;
  font-weight:600;
  transition: all .2s ease;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
}
.taskbar .stButton > button:hover {
  transform: translateY(-1px);
  border-color: rgba(255,255,255,0.25);
}
.taskbar .active .stButton > button {
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  border-color: transparent;
}

/* Big CTA buttons on Home */
.cta .stButton > button {
  width:100%;
  border-radius: 16px;
  border: 1px solid var(--glass-border);
  background: linear-gradient(135deg, rgba(124,58,237,.18), rgba(6,182,212,.14));
  color: var(--text);
  padding: 1rem 1.25rem;
  font-size: 1.05rem;
  font-weight:700;
  transition: all .2s ease;
}
.cta .stButton > button:hover {
  transform: translateY(-2px) scale(1.01);
  border-color: rgba(255,255,255,0.25);
}

/* Small pill badges */
.badge {
  display:inline-block;
  padding:.25rem .6rem;
  border-radius:9999px;
  background: rgba(255,255,255,.08);
  border:1px solid rgba(255,255,255,.15);
  font-size:.75rem; color:var(--muted);
}

/* Subtle animated gradient text for headline */
.gradient-text {
  background: linear-gradient(90deg, #a78bfa, #22d3ee, #34d399);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: hue 6s linear infinite;
}
@keyframes hue {
  0% {filter:hue-rotate(0deg)}
  100% {filter:hue-rotate(360deg)}
}

/* Tables, metrics contrast */
[data-testid="stMetricValue"] { color: #e5e7eb; }
[data-testid="stMetricDelta"] { color: #a7f3d0; }
</style>
""", unsafe_allow_html=True)

import streamlit as st
from views.home import view as view_home
from views.analyze import view as view_analyze
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
    pages = ["Home", "Analyze", "History", "Settings"]
    cols = st.columns(len(pages), vertical_alignment="center")
    with st.container():
        st.markdown('<div class="taskbar">', unsafe_allow_html=True)
        for i, (col, name) in enumerate(zip(cols, pages)):
            with col:
                active = (st.session_state.page == name)
                # Wrap each button in a div so we can mark the active one
                st.markdown(f'<div class="{ "active" if active else "" }">', unsafe_allow_html=True)
                label = f"{'✅ ' if active else ''}{name}"
                if st.button(label, use_container_width=True, key=f"nav_{name}"):
                    goto(name)
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="glass"></div>', unsafe_allow_html=True)  # thin separator glow
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
