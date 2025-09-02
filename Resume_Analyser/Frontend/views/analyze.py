import time
from datetime import datetime
import json
import streamlit as st

# ---------- UTIL ----------
def badge(text: str):
    st.markdown(f'<span class="badge">{text}</span>', unsafe_allow_html=True)

def glass_start(pad="1.25rem 1.5rem"):
    st.markdown(f'<div class="glass" style="padding:{pad};">', unsafe_allow_html=True)

def glass_end():
    st.markdown("</div>", unsafe_allow_html=True)

# -------- Replace with your real pipeline --------
def analyze_resume(file_bytes: bytes, filename: str) -> dict:
    """
    Stub analysis function. Replace with your real logic (PDF/DOCX parsing, scoring, etc.)
    Return:
      {
        "summary": str,
        "score": float,
        "details": { ... any JSON-serializable content ... }
      }
    """
    # Simulate compute time
    time.sleep(0.8)

    # Example output
    return {
        "summary": f"Parsed **{filename}** — detected 4 sections, extracted 12 skills, 3 quantified impacts.",
        "score": 82.3,
        "details": {
            "name": "Candidate Name",
            "email": "candidate@example.com",
            "skills": ["Python", "Pandas", "NLP", "Streamlit", "SQL", "Docker"],
            "experience_years": 2,
            "suggestions": [
                "Add outcome metrics to recent role bullets (e.g., % improvements).",
                "Place Skills section above Education.",
                "Tailor keywords to target JD (e.g., Airflow, dbt)."
            ]
        }
    }
# -------------------------------------------------

def view():
    st.subheader("Analyze Resume 🔍")

    # --- Row: Upload + Tips ---
    c1, c2 = st.columns([1.2, 1], vertical_alignment="top")

    with c1:
        glass_start()
        st.markdown("### Upload & Run")
        badge("PDF / DOCX")
        uploaded = st.file_uploader("Choose a resume file", type=["pdf", "docx"], label_visibility="collapsed")
        run = st.button("🚀 Run Analysis", use_container_width=True, disabled=(uploaded is None))
        clear = st.button("🧹 Clear Current Result", use_container_width=True)

        if clear:
            st.session_state.pop("last_result", None)
            st.toast("Cleared current result.", icon="🧼")

        if run and uploaded:
            file_bytes = uploaded.read()
            with st.spinner("Analyzing…"):
                # Optional: tiny progress feedback
                prog = st.progress(0.0)
                for p in (0.25, 0.55, 0.85):
                    time.sleep(0.2)
                    prog.progress(p)
                result = analyze_resume(file_bytes, uploaded.name)
                prog.progress(1.0)

            # Save last result in session + global history
            st.session_state.last_result = result
            st.session_state.history.append({
                "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": uploaded.name,
                "summary": result.get("summary", ""),
                "score": float(result.get("score", 0.0)),
                "details": result.get("details", {})
            })
            st.success("Analysis complete and saved to History ✅")
            st.balloons()
        glass_end()

    with c2:
        glass_start()
        st.markdown("### Tips for Best Results")
        badge("Pro Tip")
        st.markdown(
            """
            - Use a **simple layout** (single column) for better parsing.  
            - Prefer **PDF** exported from Word/Docs (not scanned images).  
            - Add **metrics** in bullets (e.g., *reduced costs by 18%*).  
            - Tailor keywords to the **job description** you’re targeting.  
            """
        )
        st.divider()
        st.markdown("### Settings Snapshot")
        b1, b2, b3 = st.columns(3)
        with b1: badge("Advanced parsing ✅" if st.session_state.get("adv_parsing", True) else "Advanced parsing ❌")
        with b2: badge("Dark UI")
        with b3: badge("Export CSV in History")
        glass_end()

    # --- Row: Results ---
    if "last_result" in st.session_state:
        res = st.session_state.last_result
        st.markdown("")
        glass_start(pad="1.5rem")
        st.markdown("### Result Overview")
        st.write(res.get("summary", ""))

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Score", f"{res.get('score', 0):.1f}")
        with m2:
            # Example: rough band label
            score = float(res.get("score", 0))
            band = "Excellent" if score >= 85 else "Good" if score >= 70 else "Needs Work"
            st.metric("Band", band)
        with m3:
            details = res.get("details", {})
            yrs = details.get("experience_years", "—")
            st.metric("Experience", f"{yrs} yrs")

        st.divider()

        with st.expander("Details (JSON)"):
            st.json(res.get("details", {}))

        # Quick exports
        col_a, col_b = st.columns(2)
        with col_a:
            as_json = json.dumps(res, indent=2).encode("utf-8")
            st.download_button("⬇️ Download Result (JSON)", as_json, file_name="analysis_result.json", use_container_width=True)
        with col_b:
            txt = f"Summary:\n{res.get('summary','')}\n\nScore: {res.get('score',0):.1f}"
            st.download_button("⬇️ Download Summary (TXT)", txt, file_name="analysis_summary.txt", use_container_width=True)
        glass_end()
