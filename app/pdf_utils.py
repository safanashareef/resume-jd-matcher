import io

from pypdf import PdfReader
from pypdf.errors import PyPdfError


def extract_pdf_text(data: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(data))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except (PyPdfError, ValueError):
        raise ValueError("Could not read the PDF file")
    if not text.strip():
        raise ValueError("No text found in the PDF (is it a scanned image?)")
    return text
