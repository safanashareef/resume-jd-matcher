from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_match_success():
    response = client.post(
        "/match",
        json={"resume_text": "Python SQL", "jd_text": "Python SQL Docker"},
    )
    assert response.status_code == 200
    assert "docker" in response.json()["missing_keywords"]


def test_match_empty_resume_returns_400():
    response = client.post(
        "/match", json={"resume_text": "", "jd_text": "Python"}
    )
    assert response.status_code == 400


def test_match_pdf_rejects_non_pdf():
    response = client.post(
        "/match-pdf",
        files={"resume": ("resume.txt", b"hello", "text/plain")},
        data={"jd_text": "Python"},
    )
    assert response.status_code == 400


def test_match_pdf_rejects_corrupt_pdf():
    response = client.post(
        "/match-pdf",
        files={"resume": ("resume.pdf", b"not a real pdf", "application/pdf")},
        data={"jd_text": "Python"},
    )
    assert response.status_code == 400
