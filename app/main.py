from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.matcher import match

app = FastAPI(title="Resume-JD Matcher")


class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/match")
def match_endpoint(req: MatchRequest):
    try:
        return match(req.resume_text, req.jd_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))