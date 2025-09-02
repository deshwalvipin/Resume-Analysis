import json
import pandas as pd
import streamlit as st
from io import StringIO

def _history_df():
    rows = st.session_state.history
    if not rows:
        return pd.DataFrame(columns=["ts", "filename", "summary", "score"])
    # Flatten to a simple table for list view
    return pd.DataFrame([{
        "ts": r.get("ts", ""),
        "filename": r.get("filename", ""),
        "summary": r.get("summary", ""),
        "score": r.get("score", 0.0),
    } for r in rows])

def view():
    st.subheader("History 🕘")

    df = _history_df()
    if df.empty:
        st.info("No analyses yet. Run one from the Analyze tab.")
        return

    st.dataframe(df, use_container_width=True, hide_index=True)

    # Select a row to view full details
    st.markdown("#### View details")
    idx = st.number_input("Enter row number (starting at 0)", min_value=0, max_value=len(st.session_state.history)-1, value=0, step=1)
    selected = st.session_state.history[int(idx)]

    st.write(f"**When:** {selected['ts']}")
    st.write(f"**File:** {selected['filename']}")
    st.write(f"**Summary:** {selected['summary']}")
    st.metric("Score", f"{selected.get('score', 0):.1f}")

    with st.expander("Full details (JSON)"):
        st.code(json.dumps(selected.get("details", {}), indent=2), language="json")

    # Export
    st.markdown("#### Export")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, file_name="history.csv")

    # Optional: clear history
    if st.button("Clear all history", type="secondary"):
        st.session_state.history = []
        st.success("History cleared.")
        st.rerun()
