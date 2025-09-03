from services.ai import extract_skill_bag, semantic_match, generate_suggestions
import io
import re
from collections import Counter
from typing import Tuple, Set, List

import streamlit as st

# ---------- File reading helpers ----------
def read_pdf(file) -> str:
    # Try pdfplumber first (best text fidelity), fallback to PyPDF2
    try:
        import pdfplumber
        text = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text).strip()
    except Exception:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file)
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages).strip()
        except Exception:
            return ""

def read_docx(file) -> str:
    try:
        import docx2txt
        # docx2txt expects a filepath or file-like; copy to BytesIO
        data = file.read()
        bio = io.BytesIO(data)
        text = docx2txt.process(bio)
        return (text or "").strip()
    except Exception:
        try:
            import docx
            doc = docx.Document(file)
            return "\n".join([p.text for p in doc.paragraphs]).strip()
        except Exception:
            return ""

def read_txt(file) -> str:
    try:
        raw = file.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="ignore")
        return raw.strip()
    except Exception:
        return ""

def get_text_from_upload(file) -> str:
    if file is None:
        return ""
    name = (file.name or "").lower()
    if name.endswith(".pdf"):
        return read_pdf(file)
    elif name.endswith(".docx"):
        return read_docx(file)
    elif name.endswith(".txt"):
        return read_txt(file)
    # Unknown extension → try naive read
    return read_txt(file)

# ---------- NLP-lite helpers ----------
STOPWORDS = {
    "and","or","with","the","to","a","in","for","of","on","at","is","are",
    "be","as","by","from","an","that","this","it","you","your","we","our",
    "will","can","able","etc","using","use","about","into","per","across",
    "such","via","over","under","within","their","they","them"
}

# Optional light normalization map to reduce variants
NORMALIZE_MAP = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "db": "database",
    "dbs": "database",
    "oop": "object oriented programming",
    "sqlserver": "sql server",
    "powerbi": "power bi",
    "tableau": "tableau",
    "gcp": "google cloud",
    "aws": "amazon web services",
    "azuredevops": "azure devops",
    "jira": "jira",
    "confluence": "confluence",
    "tfidf": "tf idf",
    "tf-idf": "tf idf",
    "tf": "tensorflow",
    "sklearn": "scikit learn",
    "scikit-learn": "scikit learn",
    "py": "python",
    "python3": "python",
    "js": "javascript",
    "ts": "typescript"
}

def normalize_token(tok: str) -> str:
    t = tok.lower().strip()
    t = re.sub(r"[^a-z0-9+#.\- ]", "", t)
    t = NORMALIZE_MAP.get(t, t)
    return t

def extract_keywords_blocks(text: str) -> Tuple[Set[str], Counter]:
    """
    Extracts unigrams + simple bigrams, filters stopwords/numbers,
    returns unique keyword set and a frequency Counter for weighting.
    """
    if not text:
        return set(), Counter()

    # Unigrams
    tokens = [normalize_token(t) for t in re.findall(r"\b[^\W_]+\b", text.lower())]
    tokens = [t for t in tokens if len(t) > 2 and t not in STOPWORDS]

    # Bigrams (simple & fast)
    bigrams = [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)]
    bigrams = [b for b in bigrams
               if all(w not in STOPWORDS and len(w) > 2 for w in b.split())]

    all_terms = tokens + bigrams
    freq = Counter(all_terms)
    return set(all_terms), freq

def match_resume_with_jd(resume_text: str, jd_text: str):
    res_set, res_freq = extract_keywords_blocks(resume_text)
    jd_set, jd_freq = extract_keywords_blocks(jd_text)

    matched = sorted(res_set.intersection(jd_set), key=lambda k: (-jd_freq[k], k))
    missing = sorted((jd_set - res_set), key=lambda k: (-jd_freq[k], k))

    # Basic score: % of JD terms covered (weighted by JD frequency)
    jd_total_weight = sum(jd_freq.values()) or 1
    covered_weight = sum(jd_freq[t] for t in matched)
    score = round(100 * covered_weight / jd_total_weight, 1)

    return matched, missing, score, jd_freq, res_freq

# ---------- Actionable suggestions ----------
def suggest_edits(missing: List[str], jd_text: str, top_k: int = 15) -> List[str]:
    """
    Return concise, actionable edit suggestions to close the gap.
    """
    if not missing:
        return ["Your resume already aligns well. Consider emphasizing quantifiable outcomes and mirroring the employer’s language in bullet points."]

    suggestions = []
    picked = missing[:top_k]
    for term in picked:
        # Heuristics to place terms
        if any(k in term for k in ["python","r","sql","tableau","power bi","excel","tensorflow","pytorch","spark","hadoop","aws","azure","google cloud","linux","git","docker","kubernetes","react","node"]):
            where = "Skills / Tech Stack"
        elif any(k in term for k in ["lead","manage","stakeholder","communication","presentation","collaboration","agile","scrum","kanban","mentoring","ownership"]):
            where = "Summary or Experience bullets"
        elif any(k in term for k in ["etl","pipeline","dashboard","api","model","deployment","monitoring","ab test","a/b test","metrics","forecast","optimization"]):
            where = "Experience bullets (impact-focused)"
        else:
            where = "Summary, Skills, or relevant Experience"

        # Bullet template
        suggestions.append(
            f"Add **{term}** in **{where}** — e.g., “Delivered {term} across project X, resulting in Y% improvement / $Z savings.”"
        )

    # General tailoring reminders
    suggestions.append("Mirror the JD phrasing for high-priority items (exact wording helps ATS and recruiters).")
    suggestions.append("Prioritize 4–6 most critical gaps; don’t keyword-stuff. Tie each to a measurable outcome.")
    return suggestions

# ---------- UI helpers (chips + results layout) ----------
def styled_chip(word, color="#2ecc71", text_color="white"):
    return f"""
    <span style="
        background-color:{color};
        color:{text_color};
        padding:4px 10px;
        border-radius:16px;
        margin:3px 6px 3px 0;
        display:inline-block;
        font-size:14px;
        line-height:22px;
        white-space:nowrap;">
        {word}
    </span>
    """

def display_results(matched, missing, score, jd_freq):
    st.markdown("### 📊 Overall Match Score")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Resume vs JD Match", f"{score}%")
    with col2:
        if score >= 70:
            st.success("Great alignment! ✅")
        elif score >= 40:
            st.warning("Some improvements needed ⚠️")
        else:
            st.error("Low alignment ❌ — needs tailoring")

    st.markdown("---")

    # Matches (green chips)
    with st.container():
        st.markdown("### ✅ Matches Found")
        if matched:
            chips_html = " ".join([styled_chip(m, "#27ae60") for m in matched[:30]])
            st.markdown(chips_html, unsafe_allow_html=True)
        else:
            st.warning("No direct keyword matches found. Try mirroring JD phrasing.")

    # Missing (red chips, with JD frequency)
    with st.container():
        st.markdown("### ❌ Missing from Resume (high → low priority)")
        if missing:
            chips_html = " ".join([styled_chip(f"{m} ({jd_freq[m]})", "#e74c3c") for m in missing[:20]])
            st.markdown(chips_html, unsafe_allow_html=True)
            st.info("Tip: Focus on the first 5–8 items to improve ATS fit.")
        else:
            st.success("You’ve covered all major JD keywords!")

    # Quick guidance (collapsed by default)
    with st.container():
        st.markdown("### 💡 Tailoring Tips")
        with st.expander("Open tips"):
            st.markdown(
                """
- Use **exact JD phrases** where true (helps ATS).
- Add **measurable outcomes**: %, $, time saved, SLAs met.
- Keep to **1–2 pages**, remove low-impact lines to make room.
- Prioritise **relevant** skills/experience first.
                """
            )
# ---------- Main Streamlit view function ----------
# ---------- Streamlit UI ----------
def view_analysis():
    st.title("📊 Resume Analysis")

    st.caption("Upload your resume and job description (PDF/DOCX/TXT) or paste text. We'll find matches, gaps, and tell you exactly what to do next.")

    col1, col2 = st.columns(2, vertical_alignment="top")
    with col1:
        st.subheader("📄 Resume")
        resume_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf","docx","txt"], key="resume_file")
        resume_text = st.text_area("…or paste resume text", height=220, key="resume_text")

        if resume_file and not resume_text:
            extracted = get_text_from_upload(resume_file)
            if not extracted:
                st.warning("Couldn't read the uploaded resume. Try a different format or paste the text.")
            else:
                resume_text = extracted

    with col2:
        st.subheader("📌 Job Description")
        jd_file = st.file_uploader("Upload JD (PDF/DOCX/TXT)", type=["pdf","docx","txt"], key="jd_file")
        jd_text = st.text_area("…or paste JD text", height=220, key="jd_text")

        if jd_file and not jd_text:
            extracted = get_text_from_upload(jd_file)
            if not extracted:
                st.warning("Couldn't read the uploaded JD. Try a different format or paste the text.")
            else:
                jd_text = extracted

    st.divider()
    if st.button("Analyze 🔎", use_container_width=True):
        if not resume_text or not jd_text:
            st.error("Please provide both resume and job description (upload or paste) before analyzing.")
            return

        matched, missing, score, jd_freq, res_freq = match_resume_with_jd(resume_text, jd_text)

                # Clean, professional layout
        display_results(matched, missing, score, jd_freq)

        st.markdown("### 🚀 What To Do Next")
        actions = suggest_edits(missing, jd_text)
        for a in actions:
            st.markdown(f"- {a}")

        with st.expander("See keyword weighting details (advanced)"):
            st.write("**Top JD terms (by frequency):**")
            jd_top = Counter({k: jd_freq[k] for k in jd_freq}).most_common(30)
            st.write(jd_top)
            st.write("**Top Resume terms (by frequency):**")
            res_top = Counter({k: res_freq[k] for k in res_freq}).most_common(30)
            st.write(res_top)
    st.markdown("### 🔮 AI Matching & Suggestions")

ai_cols = st.columns([1,1,1])
with ai_cols[0]:
    run_ai = st.button("Run AI Match", type="primary")

with ai_cols[1]:
    suggest_ai = st.button("Generate AI Suggestions")

with ai_cols[2]:
    threshold = st.slider("Semantic threshold", 0.60, 0.90, 0.78, 0.01, help="Higher = stricter matching")

# Cache extraction to avoid re-billing on rerun
@st.cache_data(show_spinner=False)
def _extract_bags(resume_text, jd_text):
    jd_skills = extract_skill_bag(jd_text)
    rs_skills = extract_skill_bag(resume_text)
    return jd_skills, rs_skills

if run_ai or suggest_ai:
    if not resume_text or not jd_text:
        st.warning("Please provide both Resume and Job Description.")
    else:
        with st.spinner("Extracting skills with AI…"):
            jd_skills, rs_skills = _extract_bags(resume_text, jd_text)

        st.write("**JD skills (AI):**", ", ".join(jd_skills[:30]))
        st.write("**Resume skills (AI):**", ", ".join(rs_skills[:30]))

        with st.spinner("Computing semantic matches…"):
            matched, missing, scores = semantic_match(jd_skills, rs_skills, threshold=threshold)

        m1, m2, m3 = st.columns(3)
        m1.metric("Matched (semantic)", len(matched))
        m2.metric("Missing (priority)", len(missing))
        m3.metric("Match %", round(100*len(matched)/max(1,len(jd_skills))))

        st.subheader("Matched Skills")
        if matched:
            st.write(", ".join(sorted(matched)))
        else:
            st.caption("No strong semantic matches at current threshold.")

        st.subheader("Missing / Low-Score Skills")
        if missing:
            st.write(", ".join(sorted(missing)))
            # small table with scores
            import pandas as pd
            st.dataframe(
                pd.DataFrame(
                    [{"skill": s, "similarity": round(scores.get(s, 0.0), 3)} for s in missing]
                ).sort_values("similarity", ascending=False),
                use_container_width=True, height=280
            )
        else:
            st.caption("Great! Nothing critical appears missing.")

        if suggest_ai:
            with st.spinner("Drafting tailored suggestions…"):
                advice = generate_suggestions(resume_text, jd_text, missing, matched)
            st.markdown("### ✍️ AI Suggestions")
            st.write(advice)

