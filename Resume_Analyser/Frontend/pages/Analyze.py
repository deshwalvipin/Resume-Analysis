import streamlit as st
from services.api import analyze_resume
from components.metrics import show_score_metrics
from components.skill_tables import show_skills, show_gaps_and_tips

st.title("Analyze")

with st.container():
    resume_file = st.file_uploader("Upload resume (PDF/DOCX)", type=["pdf", "docx"])
    jd = st.text_area("Paste job description", height=220, placeholder="Paste JD here...")

run_col1, run_col2 = st.columns([1, 3])
with run_col1:
    run = st.button("Analyze", type="primary")

if run:
    if not resume_file:
        st.error("Please upload a resume file."); st.stop()
    if not jd.strip():
        st.error("Please paste a job description."); st.stop()

    with st.spinner("Scoring..."):
        try:
            out = analyze_resume(resume_file.getvalue(), resume_file.name, jd)
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()

    st.success("Done.")
    show_score_metrics(out)
    st.divider()
    show_skills(out)
    st.divider()
    show_gaps_and_tips(out)
