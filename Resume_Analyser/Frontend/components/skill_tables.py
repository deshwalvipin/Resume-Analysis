import streamlit as st

def show_skills(out: dict):
    st.subheader("Matched Skills")
    st.write(", ".join(out.get("matched_skills", [])) or "—")

    st.subheader("Missing Skills")
    st.write(", ".join(out.get("missing_skills", [])) or "—")

def show_gaps_and_tips(out: dict):
    st.subheader("Keyword Gaps")
    st.write(", ".join(out.get("keyword_gaps", [])) or "—")

    st.subheader("Rewrite Suggestions")
    for s in out.get("rewrite_suggestions", []):
        st.write("• " + s)

    st.subheader("ATS Flags")
    for f in out.get("ats_flags", []):
        st.write("• " + f)
