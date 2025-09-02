import streamlit as st

def view():
    st.subheader("Settings ⚙️")
    st.checkbox("Enable advanced parsing", value=True, key="adv_parsing")
    st.text_input("API key (example)", type="password", key="api_key")
    st.caption("These settings are just placeholders. Wire your real config here.")
