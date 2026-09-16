import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import UPLOAD_DIR
from app.models.schemas import UploadResponse
from app.pipeline.pdf_to_images import pdf_to_images

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_id = str(uuid.uuid4())
    dest_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        pages = pdf_to_images(dest_path)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not read PDF: {e}")

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        num_pages=len(pages),
        status="uploaded",
    )
