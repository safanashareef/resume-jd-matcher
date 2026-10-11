# Resume-JD Matcher

A FastAPI service that scores a resume against a job description and lists matched and missing skill keywords.

## Features
- Keyword extraction against a curated tech-skills list, with aliases (JS → JavaScript, Postgres → PostgreSQL)
- Match score: 70% keyword overlap + 30% TF-IDF cosine similarity (scikit-learn)
- PDF resume upload via `POST /match-pdf`
- Input validation with clear 400 errors
- 12 pytest tests, run automatically by GitHub Actions on every push

## Tech stack
Python, FastAPI, scikit-learn, pytest, GitHub Actions

## Run locally
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs` to try the API.

## Example
`POST /match`
```json
{
  "resume_text": "Python developer with FastAPI, SQL, Git and pytest experience. Built REST APIs with JWT authentication.",
  "jd_text": "Looking for a Python developer with REST API, SQL, Docker, AWS and Git experience."
}
```
Response:
```json
{
  "score": 58.1,
  "matched_keywords": ["git", "python", "rest api", "sql"],
  "missing_keywords": ["aws", "docker"]
}
```

## Run with Docker
```bash
docker build -t resume-jd-matcher .
docker run -p 8000:8000 resume-jd-matcher
```

## Run tests
```bash
pytest -v
```

## Known limitations and next steps
- Skills come from a fixed list, so uncommon skills are not detected
- Plain-text input only; PDF resume upload is planned
- Planned: LLM-based suggestions for rewriting resume bullets, Docker setup, deployed demo
