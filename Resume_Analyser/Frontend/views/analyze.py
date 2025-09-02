import io
import time
from datetime import datetime
import streamlit as st

# -------- Replace this with your real analysis --------
def analyze_resume(file_bytes: bytes, filename: str) -> dict:
    """
    Stub analysis function. Return a dict of results.
    Replace with your real pipeline (e.g., PDF/Docx parsing, NER, scoring, LLM prompts, etc.)
    """
    # Simulate work
    time.sleep(0.5)

    # Example output
    return {
        "summary": f"Parsed {filename}. Detected 4 sections; extracted 12 skills.",
        "score": 78.5,   # e.g., match score to a JD
        "details": {
            "name": "Candidate Name",
            "email": "candidate@example.com",
            "skills": ["Python", "Pandas", "NLP", "Streamlit"],
            "experience_years": 2,
            "notes": "Good data tooling; could add project outcomes & metrics."
        }
    }
# ------------------------------------------------------

def view():
    st.subheader("Analyze Resume 🔍")

    uploaded = st.file_uploader("Upload a resume (PDF/DOCX)", type=["pdf", "docx"])
    col_a, col_b = st.columns([1,1])
    with col_a:
        run_btn = st.button("Run Analysis", use_container_width=True, disabled=(uploaded is None))
    with col_b:
        clear_btn = st.button("Clear", use_container_width=True)

    if clear_btn:
        st.session_state.pop("last_result", None)
        st.experimental_set_query_params()  # harmless; clears URL params if any
        st.success("Cleared.")

    if run_btn and uploaded:
        file_bytes = uploaded.read()
        with st.spinner("Analyzing…"):
            result = analyze_resume(file_bytes, uploaded.name)

        # Save last result in session (for showing below)
        st.session_state.last_result = result

        # Save into global history
        st.session_state.history.append({
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filename": uploaded.name,
            "summary": result.get("summary", ""),
            "score": float(result.get("score", 0.0)),
            "details": result.get("details", {})
        })

        st.success("Analysis complete and saved to History ✅")

    # Show current result (if any)
    if "last_result" in st.session_state:
        res = st.session_state.last_result
        st.markdown("### Result")
        st.write(res.get("summary", ""))
        st.metric("Score", f"{res.get('score', 0):.1f}")

        with st.expander("Details"):
            details = res.get("details", {})
            st.json(details)
