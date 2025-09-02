import streamlit as st

def _goto(page: str):
    st.session_state.page = page
    st.rerun()

def view():
    # HERO
    with st.container():
        st.markdown(
            """
            <div class="glass" style="padding:2rem; text-align:center;">
              <div class="badge">🧠 Resume Analyzer</div>
              <h1 style="margin:.5rem 0 0 0; font-size:2.2rem;">
                Make your resumes <span class="gradient-text">shine</span> with data-driven insights
              </h1>
              <p style="color:var(--muted); max-width:860px; margin:.5rem auto 0;">
                Upload a resume, extract key sections and skills, benchmark against a job description, and
                track improvements over time — all in one simple workflow.
              </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")  # small gap

    # FEATURE CARDS (3 columns)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="glass" style="height:100%; border-left:3px solid var(--brand);">
              <h3>🔍 Smart Analysis</h3>
              <p style="color:var(--muted);">
                Parse PDF/DOCX, detect sections, skills &amp; gaps. Scores tailored to your roles.
              </p>
              <div class="badge">NLP · Scoring · Hints</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            """
            <div class="glass" style="height:100%; border-left:3px solid var(--ok);">
              <h3>📈 Version History</h3>
              <p style="color:var(--muted);">
                Compare edits over time and export a CSV of your iterations and scores.
              </p>
              <div class="badge">Diffs · Trends</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            """
            <div class="glass" style="height:100%; border-left:3px solid var(--brand-2);">
              <h3>⚙️ Customizable</h3>
              <p style="color:var(--muted);">
                Toggle advanced parsing, add API keys, and fine-tune your analysis to your needs.
              </p>
              <div class="badge">Config · Extensible</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")  # small gap

    # CTA ROW
    st.markdown('<div class="glass" style="padding:1.1rem;">', unsafe_allow_html=True)
    st.markdown("### Quick actions")
    a, b, c = st.columns([1,1,1], vertical_alignment="center")
    with a:
        st.markdown('<div class="cta">', unsafe_allow_html=True)
        if st.button("🚀 Start Analysis", use_container_width=True):
            _goto("Analyze")
        st.caption("Upload a resume & generate insights.")
        st.markdown('</div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="cta">', unsafe_allow_html=True)
        if st.button("🕘 View History", use_container_width=True):
            _goto("History")
        st.caption("See previous runs & export CSV.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="cta">', unsafe_allow_html=True)
        if st.button("🎛️ Open Settings", use_container_width=True):
            _goto("Settings")
        st.caption("Adjust parsing & preferences.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Fun touch:
    st.balloons()
