# Frontend/views/home.py
import streamlit as st
from utils.ui import t

def view():
    st.markdown("### Resume Analyzer")
    st.caption("Analyze how well your resume matches job requirements.")

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("🧠 **Smart Matching**  \nAI-powered matching.")
    with c2: st.markdown("📈 **Match Score**  \nDetailed % breakdown.")
    with c3: st.markdown("📝 **Improvement Tips**  \nActionable suggestions.")

    if st.button("Load Sample Data"):
        st.session_state["resume_text"] = (
            "John Doe — Data Analyst — Python, SQL, Power BI..."
        )
        st.session_state["jd_text"] = (
            "Data Analyst role requiring Python, SQL, BI, ETL, stats..."
        )
        st.success("Sample data loaded.")

    l, r = st.columns(2)
    with l:
        st.subheader("Your Resume")
        resume_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf","docx","txt"])
        st.text_area("…or paste resume text", key="resume_text", height=220)
    with r:
        st.subheader("Job Description")
        st.text_area("Paste the job description here…", key="jd_text", height=290)

    st.write("")
    if st.button("Start Smart Match"):
        st.session_state["page"] = "Analyze"
        st.rerun()
