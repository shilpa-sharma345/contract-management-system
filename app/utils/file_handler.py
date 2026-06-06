import os
import uuid
from fastapi import UploadFile, HTTPException
import PyPDF2
from docx import Document

# -------------------------
# ALLOWED FILE TYPES
# -------------------------
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
UPLOAD_FOLDER = "uploads"


# -------------------------
# SAVE FILE TO DISK
# -------------------------
async def save_upload_file(file: UploadFile) -> str:
    # Check file extension
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF, DOC, DOCX allowed."
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Save file to disk
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return file_path


# -------------------------
# EXTRACT TEXT FROM FILE
# -------------------------
def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".doc", ".docx"]:
        return extract_text_from_docx(file_path)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type for text extraction"
        )


# -------------------------
# EXTRACT TEXT FROM PDF
# -------------------------
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


# -------------------------
# EXTRACT TEXT FROM DOCX
# -------------------------
def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text