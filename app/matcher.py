import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.keywords import ALIASES, SKILLS


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_keywords(text: str) -> set:
    text = clean(text)
    terms = {skill: skill for skill in SKILLS}
    terms.update(ALIASES)
    found = set()
    for term, canonical in terms.items():
        pattern = r"(?<![a-z0-9+#.])" + re.escape(term) + r"(?![a-z0-9+#])"
        if re.search(pattern, text):
            found.add(canonical)
    return found


def text_similarity(resume_text: str, jd_text: str) -> float:
    try:
        vectors = TfidfVectorizer(stop_words="english").fit_transform(
            [clean(resume_text), clean(jd_text)]
        )
        return float(cosine_similarity(vectors[0], vectors[1])[0][0])
    except ValueError:
        return 0.0


def match(resume_text: str, jd_text: str) -> dict:
    if not resume_text.strip() or not jd_text.strip():
        raise ValueError("Both resume and job description are required")

    resume_kw = extract_keywords(resume_text)
    jd_kw = extract_keywords(jd_text)

    matched = sorted(jd_kw & resume_kw)
    missing = sorted(jd_kw - resume_kw)

    keyword_score = len(matched) / len(jd_kw) if jd_kw else 0.0
    similarity = text_similarity(resume_text, jd_text)
    score = round((0.7 * keyword_score + 0.3 * similarity) * 100, 1)

    return {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }