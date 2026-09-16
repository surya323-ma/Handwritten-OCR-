"""Step 4: LLM-based post-processing via a local Ollama Qwen 2.5 model.

The refinement prompt is deliberately conservative: fix obvious OCR
artifacts (spacing, stray characters, obvious misreads) but do NOT
rewrite, rephrase, or "improve" the student's actual answer. This
preserves grading integrity — the model is a cleanup pass, not an
editor.
"""
import ollama
from app.config import OLLAMA_HOST, OLLAMA_MODEL

_client = ollama.Client(host=OLLAMA_HOST)

_SYSTEM_PROMPT = (
    "You clean up OCR output from a handwritten student answer sheet. "
    "Fix obvious character-recognition mistakes, spacing, and punctuation. "
    "Do NOT rewrite, rephrase, summarize, or correct the student's factual "
    "content or wording — preserve their original meaning and phrasing "
    "exactly, even if the answer itself is wrong or awkwardly worded. "
    "Return ONLY the cleaned text, with no preamble or explanation."
)


def refine_text(raw_text: str) -> str:
    if not raw_text.strip():
        return raw_text

    response = _client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        options={"temperature": 0.1},
    )
    return response["message"]["content"].strip()
