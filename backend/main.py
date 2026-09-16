from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.routes import upload, process

app = FastAPI(
    title="Handwritten Answer Sheet OCR API",
    description="Converts scanned handwritten student answer sheets into digital text.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, tags=["upload"])
app.include_router(process.router, tags=["process"])


@app.get("/health")
async def health():
    return {"status": "ok"}
