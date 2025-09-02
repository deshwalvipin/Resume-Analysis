# views/home.py
import streamlit as st

# --- lightweight i18n fallback (works even if app.t isn't imported) ---
_I18N_LOCAL = {
    "English": {
        "BADGE": "🧠 Resume Analyzer",
        "TITLE_PREFIX": "",
        "TITLE_CORE": "Make your resumes",
        "TITLE_GLOW": "shine",
        "TAGLINE": "Upload a resume, extract key sections and skills, benchmark against a job description, and track improvements over time — all in one simple workflow.",
        "CTA_ANALYZE": "Analyze",
        "CTA_HISTORY": "History",
        "CTA_SETTINGS": "Settings",
        "CTA_ANALYZE_CAP": "Upload a resume & generate insights.",
        "CTA_HISTORY_CAP": "See previous runs & export CSV.",
        "CTA_SETTINGS_CAP": "Adjust parsing & preferences.",
        "FEATURE_1_TITLE": "🔍 Smart Analysis",
        "FEATURE_1_BODY": "Parse PDF/DOCX, detect sections, skills & gaps. Scores tailored to your roles.",
        "FEATURE_1_BADGE": "NLP · Scoring · Hints",
        "FEATURE_2_TITLE": "📈 Version History",
        "FEATURE_2_BODY": "Compare edits over time and export a CSV of your iterations and scores.",
        "FEATURE_2_BADGE": "Diffs · Trends",
        "FEATURE_3_TITLE": "⚙️ Customizable",
        "FEATURE_3_BODY": "Toggle advanced parsing, add API keys, and fine-tune your analysis to your needs.",
        "FEATURE_3_BADGE": "Config · Extensible",
        "QUICK_ACTIONS": "Quick actions",
    },
    "Español": {
        "BADGE": "🧠 Analizador de CV",
        "TITLE_PREFIX": "",
        "TITLE_CORE": "Haz que tu currículum",
        "TITLE_GLOW": "brille",
        "TAGLINE": "Sube un currículum, extrae secciones y habilidades, compáralo con una oferta y sigue las mejoras, todo en un mismo flujo.",
        "CTA_ANALYZE": "Analizar",
        "CTA_HISTORY": "Historial",
        "CTA_SETTINGS": "Ajustes",
        "CTA_ANALYZE_CAP": "Sube un CV y genera insights.",
        "CTA_HISTORY_CAP": "Mira ejecuciones previas y exporta CSV.",
        "CTA_SETTINGS_CAP": "Ajusta el análisis a tu gusto.",
        "FEATURE_1_TITLE": "🔍 Análisis inteligente",
        "FEATURE_1_BODY": "Parsea PDF/DOCX, detecta secciones, habilidades y brechas. Puntuaciones para tus roles.",
        "FEATURE_1_BADGE": "NLP · Scoring · Consejos",
        "FEATURE_2_TITLE": "📈 Historial de versiones",
        "FEATURE_2_BODY": "Compara ediciones en el tiempo y exporta un CSV.",
        "FEATURE_2_BADGE": "Differences · Tendencias",
        "FEATURE_3_TITLE": "⚙️ Personalizable",
        "FEATURE_3_BODY": "Activa análisis avanzado, añade claves API y ajusta la evaluación a tus necesidades.",
        "FEATURE_3_BADGE": "Config · Extensible",
        "QUICK_ACTIONS": "Acciones rápidas",
    },
    "हिंदी": {
        "BADGE": "🧠 रिज़्यूमे विश्लेषक",
        "TITLE_PREFIX": "",
        "TITLE_CORE": "अपने रिज़्यूमे को",
        "TITLE_GLOW": "दमकाइए",
        "TAGLINE": "रिज़्यूमे अपलोड करें, मुख्य सेक्शन/स्किल्स निकालें, जॉब डिस्क्रिप्शन से मिलाएँ और समय के साथ सुधार ट्रैक करें — सब एक ही जगह।",
        "CTA_ANALYZE": "विश्लेषण",
        "CTA_HISTORY": "इतिहास",
        "CTA_SETTINGS": "सेटिंग्स",
        "CTA_ANALYZE_CAP": "रिज़्यूमे अपलोड करें और इनसाइट्स पाएँ।",
        "CTA_HISTORY_CAP": "पिछली रनिंग देखें और CSV एक्सपोर्ट करें।",
        "CTA_SETTINGS_CAP": "पार्सिंग और प्रेफरेंसेज़ समायोजित करें।",
        "FEATURE_1_TITLE": "🔍 स्मार्ट विश्लेषण",
        "FEATURE_1_BODY": "PDF/DOCX पार्स करें, सेक्शन, स्किल्स और गैप्स पहचानें। भूमिकाओं के अनुरूप स्कोर।",
        "FEATURE_1_BADGE": "NLP · स्कोरिंग · सुझाव",
        "FEATURE_2_TITLE": "📈 संस्करण इतिहास",
        "FEATURE_2_BODY": "समय के साथ बदलावों की तुलना करें और CSV निर्यात करें।",
        "FEATURE_2_BADGE": "डिफ़्स · ट्रेंड्स",
        "FEATURE_3_TITLE": "⚙️ अनुकूलन",
        "FEATURE_3_BODY": "एडवांस्ड पार्सिंग, API कीज़ और स्कोरिंग को अपनी ज़रूरत अनुसार ट्यून करें।",
        "FEATURE_3_BADGE": "कॉन्फ़िग · एक्सटेंसिबल",
        "QUICK_ACTIONS": "त्वरित क्रियाएँ",
    },
}

def t(key: str) -> str:
    lang = st.session_state.get("language", "English")
    return _I18N_LOCAL.get(lang, _I18N_LOCAL["English"]).get(key, key)

# --- navigation helper ---
def _goto(page: str):
    st.session_state.page = page
    st.rerun()

def view():
    # HERO
    with st.container():
        st.markdown(
            f"""
            <div class="glass" style="padding:2rem; text-align:center;">
              <div class="badge">{t("BADGE")}</div>
              <h1 style="margin:.5rem 0 0 0; font-size:2.2rem;">
                {t("TITLE_PREFIX")}{t("TITLE_CORE")} <span class="gradient-text">{t("TITLE_GLOW")}</span>
              </h1>
              <p style="color:var(--muted); max-width:860px; margin:.5rem auto 0;">
                {t("TAGLINE")}
              </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    # FEATURE CARDS
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="glass" style="height:100%; border-left:3px solid var(--brand);">
              <h3>{t("FEATURE_1_TITLE")}</h3>
              <p style="color:var(--muted);">{t("FEATURE_1_BODY")}</p>
              <div class="badge">{t("FEATURE_1_BADGE")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="glass" style="height:100%; border-left:3px solid var(--ok);">
              <h3>{t("FEATURE_2_TITLE")}</h3>
              <p style="color:var(--muted);">{t("FEATURE_2_BODY")}</p>
              <div class="badge">{t("FEATURE_2_BADGE")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="glass" style="height:100%; border-left:3px solid var(--brand-2);">
              <h3>{t("FEATURE_3_TITLE")}</h3>
              <p style="color:var(--muted);">{t("FEATURE_3_BODY")}</p>
              <div class="badge">{t("FEATURE_3_BADGE")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    # CTA ROW
    st.markdown('<div class="glass" style="padding:1.1rem;">', unsafe_allow_html=True)
    st.markdown(f"### {t('QUICK_ACTIONS')}")
    a, b, c = st.columns([1,1,1], vertical_alignment="center")

    with a:
        st.markdown('<div class="cta">', unsafe_allow_html=True)
        if st.button("🚀 " + t("CTA_ANALYZE"), use_container_width=True):
            _goto("Analyze")
        st.caption(t("CTA_ANALYZE_CAP"))
        st.markdown('</div>', unsafe_allow_html=True)

    with b:
        st.markdown('<div class="cta">', unsafe_allow_html=True)
        if st.button("🕘 " + t("CTA_HISTORY"), use_container_width=True):
            _goto("History")
        st.caption(t("CTA_HISTORY_CAP"))
        st.markdown('</div>', unsafe_allow_html=True)

    with c:
        st.markdown('<div class="cta">', unsafe_allow_html=True)
        if st.button("🎛️ " + t("CTA_SETTINGS"), use_container_width=True):
            _goto("Settings")
        st.caption(t("CTA_SETTINGS_CAP"))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # fun animation (honors Settings toggle)
    if st.session_state.get("animations", True):
        st.balloons()
