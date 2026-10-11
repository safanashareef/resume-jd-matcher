from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app.matcher import match
from app.pdf_utils import extract_pdf_text

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


@app.post("/match-pdf")
async def match_pdf(resume: UploadFile = File(...), jd_text: str = Form(...)):
    if not (resume.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Resume must be a PDF file")
    data = await resume.read()
    try:
        return match(extract_pdf_text(data), jd_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
