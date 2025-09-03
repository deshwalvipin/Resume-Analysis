# Frontend/services/ai.py
import os
import numpy as np
from openai import OpenAI

_EMBED_MODEL = "text-embedding-3-small"
_CHAT_MODEL  = "gpt-4o-mini"

def _client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    return OpenAI(api_key=key)

# ---- LLM skill extraction ----
def extract_skill_bag(text: str, max_items: int = 60) -> list[str]:
    """
    Ask the LLM to extract a clean, de-duplicated list of skills/keywords/tools/frameworks.
    Returns lowercase strings.
    """
    cli = _client()
    prompt = f"""Extract a concise, de-duplicated list of SKILLS/TOOLS/KEYWORDS from the text.
- Prefer nouns/bigrams ("data visualization", "feature engineering", "Power BI")
- Include programming languages, libraries, cloud, DBs, ML topics, domain terms
- Return ONLY a JSON array of strings (max {max_items} items). No commentary.

TEXT:
{text}
"""
    resp = cli.chat.completions.create(
        model=_CHAT_MODEL,
        temperature=0.2,
        messages=[{"role":"user","content":prompt}]
    )
    import json
    content = resp.choices[0].message.content
    try:
        items = json.loads(content)
        items = [str(x).strip().lower() for x in items if str(x).strip()]
        # normalize tiny punctuation variants
        items = list(dict.fromkeys(items))[:max_items]
        return items
    except Exception:
        # fallback: naive token split if JSON parsing fails
        return list(set([w.strip(" ,.;:").lower() for w in text.split() if len(w)>2]))[:max_items]

# ---- Embeddings & similarity ----
def embed_texts(texts: list[str]) -> np.ndarray:
    if not texts:
        return np.zeros((0, 1536))
    cli = _client()
    out = cli.embeddings.create(model=_EMBED_MODEL, input=texts)
    vecs = np.array([d.embedding for d in out.data], dtype=np.float32)
    # normalize for cosine
    norms = np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9
    return vecs / norms

def semantic_match(jd_skills: list[str], resume_chunks: list[str], threshold: float = 0.78):
    """
    For each JD skill, find the best matching resume phrase by cosine similarity.
    Returns dicts: matched, missing, scores
    """
    if not jd_skills:
        return [], jd_skills, {}

    # Chunk resume (skills list or sentences)
    chunks = resume_chunks if resume_chunks else []
    if not chunks:
        return [], jd_skills, {}

    # Embedding matrices
    e_jd = embed_texts(jd_skills)
    e_rs = embed_texts(chunks)

    # cosine = dot(e_jd, e_rs.T) because both are normalized
    sims = e_jd @ e_rs.T  # shape [len(jd), len(resume)]
    matched, missing, best_scores = [], [], {}
    for i, sk in enumerate(jd_skills):
        j = int(np.argmax(sims[i])) if e_rs.size else -1
        score = float(sims[i, j]) if j >= 0 else 0.0
        best_scores[sk] = score
        if score >= threshold:
            matched.append(sk)
        else:
            missing.append(sk)
    return matched, missing, best_scores

# ---- Suggestions (LLM) ----
def generate_suggestions(resume_text: str, jd_text: str, missing_skills: list[str], matched_skills: list[str]) -> str:
    cli = _client()
    prompt = f"""You are a resume coach. Compare the resume with the job description.

- Missing skills to prioritize: {missing_skills[:20]}
- Already matched strengths: {matched_skills[:15]}

Write a concise, actionable plan:
1) Top 5 changes to the SUMMARY (bullet list)
2) 3–5 STAR bullets to add under EXPERIENCE (start each with a strong verb)
3) Keywords to insert naturally (comma-separated)
4) Optional: short project idea (2–3 lines) that showcases 2–3 missing skills.

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    resp = cli.chat.completions.create(
        model=_CHAT_MODEL,
        temperature=0.4,
        messages=[{"role":"user","content":prompt}]
    )
    return resp.choices[0].message.content
