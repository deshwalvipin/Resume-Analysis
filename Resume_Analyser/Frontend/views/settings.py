import json
import os
import streamlit as st

# lightweight translation helper
def t(key: str) -> str:
    # Try to read from session_state.language (default English)
    lang = st.session_state.get("language", "English")
    I18N = {
        "English": {"SETTINGS_TITLE": "Settings"},
        "Español": {"SETTINGS_TITLE": "Ajustes"},
        "हिंदी": {"SETTINGS_TITLE": "सेटिंग्स"},
    }
    return I18N.get(lang, I18N["English"]).get(key, key)

SETTINGS_PATH = "history.json"  # used only for persistence demo

def _save_history():
    if not st.session_state.get("persist_history"):
        return
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(st.session_state.history, f, ensure_ascii=False, indent=2)
        st.toast("History saved to disk.", icon="💾")
    except Exception as e:
        st.error(f"Save failed: {e}")

def _load_history():
    if not st.session_state.get("persist_history"):
        return
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                st.session_state.history = json.load(f)
            st.toast("History loaded from disk.", icon="📂")
        except Exception as e:
            st.error(f"Load failed: {e}")

def view():
    st.subheader(t("SETTINGS_TITLE") + " ⚙️")

    # ========== Appearance ==========
    st.markdown("### Appearance")
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.session_state.theme = st.selectbox("Theme", ["Dark", "Light"], index=0 if st.session_state.theme=="Dark" else 1)
    with c2:
        st.session_state.accent = st.color_picker("Accent color", st.session_state.accent)
    with c3:
        st.session_state.density = st.selectbox("Density", ["Comfortable","Compact"], index=0 if st.session_state.density=="Comfortable" else 1)

    # Re-apply CSS instantly
    if st.button("Apply appearance", use_container_width=True):
        st.toast("Appearance updated.", icon="🎨")
        st.rerun()

    st.divider()

    # ========== Language ==========
    st.markdown("### Language")
    st.session_state.language = st.selectbox("App language", ["English","Español","हिंदी"],
                                             index=["English","Español","हिंदी"].index(st.session_state.language))
    st.caption("Translations are lightweight; add more keys in I18N dict inside app.py.")

    st.divider()

    # ========== Behavior ==========
    st.markdown("### Behavior")
    b1, b2 = st.columns(2)
    with b1:
        st.session_state.animations = st.toggle("Fun animations (balloons, etc.)", value=st.session_state.animations)
        st.session_state.persist_history = st.toggle("Persist history to disk (history.json)", value=st.session_state.persist_history)
    with b2:
        if st.button("Save history now", disabled=not st.session_state.persist_history, use_container_width=True):
            _save_history()
        if st.button("Load history from disk", disabled=not st.session_state.persist_history, use_container_width=True):
            _load_history()

    st.divider()

    # ========== Data ==========
    st.markdown("### Data")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export settings (JSON)", use_container_width=True):
            payload = {
                "theme": st.session_state.theme,
                "language": st.session_state.language,
                "accent": st.session_state.accent,
                "density": st.session_state.density,
                "animations": st.session_state.animations,
                "persist_history": st.session_state.persist_history,
            }
            st.download_button("⬇️ Download settings.json",
                               data=json.dumps(payload, indent=2).encode("utf-8"),
                               file_name="settings.json", use_container_width=True)
    with col2:
        uploaded = st.file_uploader("Import settings", type=["json"])
        if uploaded:
            try:
                cfg = json.load(uploaded)
                for k, v in cfg.items():
                    if k in ("theme","language","accent","density","animations","persist_history"):
                        st.session_state[k] = v
                st.success("Settings imported.")
                st.rerun()
            except Exception as e:
                st.error(f"Import failed: {e}")

    st.divider()

    # ========== Danger zone ==========
    st.markdown("### Danger zone")
    d1, d2 = st.columns(2)
    with d1:
        if st.button("Clear history", type="secondary", use_container_width=True):
            st.session_state.history = []
            if st.session_state.persist_history and os.path.exists(SETTINGS_PATH):
                try:
                    os.remove(SETTINGS_PATH)
                except Exception:
                    pass
            st.success("History cleared.")
    with d2:
        if st.button("Reset preferences", type="secondary", use_container_width=True):
            for k, v in {"theme":"Dark","language":"English","accent":"#7c3aed","density":"Comfortable",
                         "animations":True,"persist_history":False}.items():
                st.session_state[k] = v
            st.success("Preferences reset.")
            st.rerun()
