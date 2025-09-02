import json
from datetime import datetime
import pandas as pd
import streamlit as st

# ---------- UTIL ----------
def badge(text: str):
    st.markdown(f'<span class="badge">{text}</span>', unsafe_allow_html=True)

def glass_start(pad="1.25rem 1.5rem"):
    st.markdown(f'<div class="glass" style="padding:{pad};">', unsafe_allow_html=True)

def glass_end():
    st.markdown("</div>", unsafe_allow_html=True)

def to_df():
    rows = st.session_state.get("history", [])
    if not rows:
        return pd.DataFrame(columns=["ts", "filename", "summary", "score"])
    return pd.DataFrame(rows)

def view():
    st.subheader("History 🕘")

    df = to_df()
    if df.empty:
        glass_start()
        st.info("No analyses yet. Run one from the Analyze tab.")
        glass_end()
        return

    # --- Stats / Filters ---
    glass_start()
    st.markdown("### Overview")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Runs", len(df))
    with c2:
        avg = df["score"].astype(float).mean() if not df.empty else 0.0
        st.metric("Average Score", f"{avg:.1f}")
    with c3:
        mx = df["score"].astype(float).max()
        st.metric("Best Score", f"{mx:.1f}")
    with c4:
        # last run timestamp
        try:
            last_ts = max(pd.to_datetime(df["ts"]))
            st.metric("Last Run", last_ts.strftime("%Y-%m-%d %H:%M"))
        except Exception:
            st.metric("Last Run", "—")

    st.divider()

    # Filters
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1.2])
    with col_f1:
        name_filter = st.text_input("Filter by filename")
    with col_f2:
        min_score = st.number_input("Min score", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
    with col_f3:
        sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Score ⬆", "Score ⬇"])

    # Apply filters
    fdf = df.copy()
    if name_filter:
        fdf = fdf[fdf["filename"].str.contains(name_filter, case=False, na=False)]
    fdf["score"] = fdf["score"].astype(float)
    fdf = fdf[fdf["score"] >= float(min_score)]

    # Sort
    if sort_by == "Newest":
        fdf = fdf.sort_values("ts", ascending=False)
    elif sort_by == "Oldest":
        fdf = fdf.sort_values("ts", ascending=True)
    elif sort_by == "Score ⬆":
        fdf = fdf.sort_values("score", ascending=True)
    elif sort_by == "Score ⬇":
        fdf = fdf.sort_values("score", ascending=False)

    # Show table
    st.markdown("#### Runs")
    st.dataframe(
        fdf[["ts", "filename", "summary", "score"]],
        use_container_width=True,
        hide_index=True
    )

    # Tiny trend (score over time)
    try:
        tdf = fdf.copy()
        tdf["ts_dt"] = pd.to_datetime(tdf["ts"])
        tdf = tdf.sort_values("ts_dt")
        st.line_chart(tdf.set_index("ts_dt")["score"])
    except Exception:
        pass

    # Export CSV
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered CSV", csv, file_name="history_filtered.csv", use_container_width=True)

    glass_end()

    st.markdown("")

    # --- Details Viewer / Actions ---
    glass_start()
    st.markdown("### View Details")
    if len(fdf) == 0:
        st.info("No rows match the current filters.")
        glass_end()
        return

    # Select by row number in filtered view
    idx = st.number_input(
        "Row index (from the filtered table, starting at 0)",
        min_value=0,
        max_value=len(fdf) - 1,
        value=0,
        step=1
    )
    sel = fdf.iloc[int(idx)]

    # Pretty summary
    st.markdown(f"**When:** {sel['ts']}")
    st.markdown(f"**File:** {sel['filename']}")
    badge(f"Score {float(sel['score']):.1f}")

    st.divider()
    st.markdown("**Summary**")
    st.write(sel.get("summary", ""))

    st.markdown("**Details (JSON)**")
    # Look up original details by matching timestamp + filename
    raw = next(
        (r for r in st.session_state.history if r["ts"] == sel["ts"] and r["filename"] == sel["filename"]),
        None
    )
    st.code(json.dumps(raw.get("details", {}) if raw else {}, indent=2), language="json")

    st.divider()

    # Row actions
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        if st.button("🗑️ Delete Selected Row", use_container_width=True, type="secondary"):
            st.session_state.history = [r for _, r in df.iterrows() if not (
                r["ts"] == sel["ts"] and r["filename"] == sel["filename"]
            )]
            st.toast("Deleted.", icon="🗑️")
            st.rerun()
    with col_b:
        if st.button("🧼 Clear All History", use_container_width=True):
            st.session_state.history = []
            st.toast("History cleared.", icon="🧼")
            st.rerun()
    with col_c:
        st.caption("Use filters above to narrow the table.")

    glass_end()
