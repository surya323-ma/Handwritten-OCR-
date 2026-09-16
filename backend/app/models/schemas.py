from pydantic import BaseModel
from typing import List, Optional


class ExtractedAnswer(BaseModel):
    question_number: int
    text: str
    confidence: float  # 0-1


class PageResult(BaseModel):
    page_number: int
    raw_text: str
    answers: List[ExtractedAnswer]


class ProcessResponse(BaseModel):
    file_id: str
    filename: str
    pages: List[PageResult]


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    num_pages: int
    status: str


class JobStatus(BaseModel):
    file_id: str
    status: str  # "queued" | "processing" | "done" | "error"
    progress: Optional[int] = None
    detail: Optional[str] = None
