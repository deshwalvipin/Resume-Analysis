import streamlit as st

def show_score_metrics(out: dict):
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Fit", out.get("fit_score"))
    c2.metric("Keyword", out.get("keyword_score"))
    c3.metric("Semantic", out.get("semantic_score"))
    c4.metric("Readability", out.get("readability_score"))
    c5.metric("ATS", out.get("ats_score"))
