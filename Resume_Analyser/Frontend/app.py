import streamlit as st
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠", layout="wide")
st.markdown(
    """
    <style>
    .block-container { padding-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI-Powered Resume Analyzer")
st.write(
    "Use the **Analyze** page (left sidebar) to upload a resume and compare against a job description. "
    "Add or remove pages in the **pages/** folder as you like."
)
st.info("Tip: You can tweak components under `frontend/components/` or the API URL in `frontend/services/api.py`.")
