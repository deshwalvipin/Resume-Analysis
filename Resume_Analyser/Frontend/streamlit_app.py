import streamlit as st, requests

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠", layout="centered")
st.title("AI-Powered Resume Analyzer")

with st.sidebar:
    st.markdown("**Backend**: FastAPI on port 8000\n\n**Frontend**: Streamlit on port 8501")

resume_file = st.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf","docx"])
jd = st.text_area("Paste one job description", height=220, placeholder="Paste JD here...")

if st.button("Analyze") and resume_file and jd.strip():
    files = {"resume": (resume_file.name, resume_file.getvalue(), resume_file.type or "application/octet-stream")}
    data = [("jds", jd)]
    with st.spinner("Scoring..."):
        r = requests.post(API_URL, files=files, data=data, timeout=120)
    if r.ok:
        out = r.json()
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Fit", out["fit_score"])
        c2.metric("Keyword", out["keyword_score"])
        c3.metric("Semantic", out["semantic_score"])
        c4.metric("Readability", out["readability_score"])
        c5.metric("ATS", out["ats_score"])

        st.subheader("Matched Skills"); st.write(", ".join(out["matched_skills"]) or "—")
        st.subheader("Missing Skills"); st.write(", ".join(out["missing_skills"]) or "—")
        st.subheader("Keyword Gaps");  st.write(", ".join(out["keyword_gaps"]) or "—")
        st.subheader("Rewrite Suggestions"); [st.write("• " + s) for s in out["rewrite_suggestions"]]
        st.subheader("ATS Flags");          [st.write("• " + f) for f in out["ats_flags"]]
    else:
        st.error(f"{r.status_code} – {r.text}")
