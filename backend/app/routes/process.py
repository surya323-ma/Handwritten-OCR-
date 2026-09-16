import os
from fastapi import APIRouter, HTTPException
from app.config import UPLOAD_DIR
from app.models.schemas import ProcessResponse, PageResult, ExtractedAnswer
from app.pipeline.pdf_to_images import pdf_to_images
from app.pipeline.preprocess import preprocess_image
from app.pipeline.ocr_detect import detect_text_lines, crop_lines
from app.pipeline.trocr_recognize import recognize_lines
from app.pipeline.reconstruct import split_into_questions
from app.pipeline.llm_refine import refine_text

router = APIRouter()


@router.post("/process/{file_id}", response_model=ProcessResponse)
async def process_pdf(file_id: str, filename: str = "document.pdf"):
    pdf_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="File not found — upload it first")

    pages = pdf_to_images(pdf_path)
    page_results = []

    for page_num, page_img in enumerate(pages, start=1):
        clean_img = preprocess_image(page_img)
        boxes = detect_text_lines(clean_img)
        line_imgs = crop_lines(clean_img, boxes)
        recognized = recognize_lines(line_imgs)  # [(text, confidence), ...]

        raw_lines = [text for text, _ in recognized]
        confidences = [conf for _, conf in recognized]
        raw_text = " ".join(raw_lines)

        blocks = split_into_questions(raw_lines)
        answers = []
        for q_num, block_text in blocks:
            refined = refine_text(block_text)
            avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
            answers.append(ExtractedAnswer(
                question_number=q_num,
                text=refined,
                confidence=round(avg_conf, 4),
            ))

        page_results.append(PageResult(
            page_number=page_num,
            raw_text=raw_text,
            answers=answers,
        ))

    return ProcessResponse(file_id=file_id, filename=filename, pages=page_results)
