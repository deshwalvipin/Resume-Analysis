from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Dict
from collections import Counter
from tempfile import NamedTemporaryFile
import pdfminer.high_level, docx2txt, re
import spacy
from sentence_transformers import SentenceTransformer, util
from textstat import flesch_reading_ease
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Resume Analyzer API")

# CORS for local Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

# Load NLP models
nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Basic skill taxonomy (extend later)
SKILLS = {
    "python": ["python", "pandas", "numpy"],
    "ml": ["machine learning", "scikit-learn", "xgboost", "svm"],
    "sql": ["sql", "postgres", "mysql"],
    "cloud": ["aws", "gcp", "azure", "sagemaker", "bigquery"]
}

def _save_tmp(upload: UploadFile) -> str:
    with NamedTemporaryFile(delete=False, suffix=upload.filename[upload.filename.rfind('.'):]) as tmp:
        upload.file.seek(0)
        tmp.write(upload.file.read())
        return tmp.name

def extract_text(upload: UploadFile) -> str:
    name = upload.filename.lower()
    tmp_path = _save_tmp(upload)
    if name.endswith(".pdf"):
        return pdfminer_high_level_extract(tmp_path)
    elif name.endswith(".docx"):
        return docx2txt.process(tmp_path) or ""
    else:
        upload.file.seek(0)
        return upload.file.read().decode(errors="ignore")

def pdfminer_high_level_extract(path: str) -> str:
    try:
        return pdfminer.high_level.extract_text(path) or ""
    except Exception:
        return ""

def noun_keywords(text: str) -> Counter:
    doc = nlp(text.lower())
    toks = [t.lemma_ for t in doc if t.pos_ in {"NOUN", "PROPN"} and t.is_alpha and not t.is_stop]
    return Counter(toks)

def semantic_score(resume_text: str, jds: List[str]) -> float:
    if not jds: return 0.0
    r = embedder.encode(resume_text, convert_to_tensor=True)
    sims = []
    for jd in jds:
        j = embedder.encode(jd, convert_to_tensor=True)
        sims.append(float(util.cos_sim(r, j)))
    return max(sims) * 100

def map_readability(re: float) -> float:
    return max(0.0, min(100.0, re))

def extract_skills(text: str) -> Dict[str, List[str]]:
    found, missing = [], []
    t = text.lower()
    for k, synonyms in SKILLS.items():
        present = any(s in t for s in synonyms)
        (found if present else missing).append(k)
    return {"matched": found, "missing": missing}

def ats_checks(text: str):
    flags, low = [], text.lower()
    if "skills" not in low: flags.append("Add a dedicated 'Skills' section.")
    if not re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text): flags.append("Add a professional email.")
    if not re.search(r"\b20\d{2}\b", text): flags.append("Add years for roles (YYYY).")
    if "experience" not in low and "work" not in low: flags.append("Add 'Experience' section header.")
    return flags

@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), jds: List[str] = Form(...)):
    res_text = extract_text(resume)
    kw_res = noun_keywords(res_text)
    kw_jd = noun_keywords(" ".join(jds))

    overlap = sum((kw_res & kw_jd).values()) / max(1, sum(kw_jd.values()))
    keyword_score = round(min(100.0, overlap * 100.0), 1)
    sem = round(semantic_score(res_text, jds), 1)
    readability_score = round(map_readability(flesch_reading_ease(res_text or "a")), 1)

    flags = ats_checks(res_text)
    ats_score = max(0.0, 100.0 - 10.0 * len(flags))

    jd_top = [w for w, c in kw_jd.most_common(20)]
    res_vocab = set(kw_res.keys())
    keyword_gaps = [w for w in jd_top if w not in res_vocab][:10]

    fit = round(0.45*keyword_score + 0.35*sem + 0.10*readability_score + 0.10*ats_score, 1)
    suggestions = []
    if keyword_gaps:
        suggestions.append(f"Add context for: {', '.join(keyword_gaps[:5])}.")
    suggestions.append("Use impact bullets: verb + metric + outcome (e.g., 'Built X reducing Y by 15%').")

    return {
        "fit_score": fit,
        "keyword_score": keyword_score,
        "semantic_score": sem,
        "readability_score": readability_score,
        "ats_score": ats_score,
        "matched_skills": extract_skills(res_text)["matched"],
        "missing_skills": extract_skills(res_text)["missing"],
        "keyword_gaps": keyword_gaps,
        "rewrite_suggestions": suggestions,
        "ats_flags": flags
    }
