# Handwritten Answer Sheet OCR — Full Project

FYP project: converts scanned handwritten student answer sheets (PDF) into
digital, machine-readable text, preserving original wording and structure.

## Structure

```
backend/     FastAPI + PaddleOCR + TrOCR + Ollama(Qwen2.5) pipeline
frontend/    Next.js + Tailwind UI (sidebar, PDF preview, answer cards)
render.yaml  3-service Render blueprint (backend, ollama, frontend)
```

## Pipeline (backend/app/pipeline/)

1. `pdf_to_images.py` — PDF → page images (pdf2image)
2. `preprocess.py` — CLAHE contrast + denoise (OpenCV)
3. `ocr_detect.py` — line/region detection (PaddleOCR, detection-only)
4. `trocr_recognize.py` — handwriting recognition (TrOCR)
5. `reconstruct.py` — reading-order joining + Q#-marker splitting
6. `llm_refine.py` — conservative cleanup pass (Qwen 2.5 via Ollama)

## Run locally

**Backend**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```
Requires Ollama running locally with `ollama pull qwen2.5:7b` (or edit
`OLLAMA_MODEL` in `.env` to a smaller variant, e.g. `qwen2.5:3b`).

**Frontend**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```
Visit http://localhost:3000.

## Deploy

`render.yaml` defines three services — backend, a dedicated Ollama service
with a persistent disk for model weights, and the Next.js frontend. Push
to a connected GitHub repo and use Render's "New Blueprint" flow, or
`render blueprint launch` via the CLI. Update the `envVars` URLs to match
the actual service subdomains Render assigns on first deploy.

For a lighter/free-tier demo, swap `qwen2.5:7b` for `qwen2.5:3b` (or
`1.5b`) in `ollama.Dockerfile` and `backend/.env`.
