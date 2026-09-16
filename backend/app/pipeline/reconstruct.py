"""Step 3: Reconstruct reading order and split into question/answer blocks.

Detected lines come back sorted top-to-bottom already (see
ocr_detect.detect_text_lines). This step joins consecutive lines into
paragraphs and splits the page into per-question chunks by looking
for a "Q# n" / "Q.n" / "n)" style marker at the start of a line —
matching the handwriting convention seen in the sample sheets.
"""
import re
from typing import List, Tuple

_Q_MARKER = re.compile(r"^\s*Q[\.#]?\s*[:\-]?\s*(\d+)", re.IGNORECASE)


def join_lines(lines: List[str]) -> str:
    return " ".join(l.strip() for l in lines if l.strip())


def split_into_questions(lines: List[str]) -> List[Tuple[int, str]]:
    """Group raw OCR lines into (question_number, joined_text) blocks."""
    blocks: List[Tuple[int, List[str]]] = []
    current_q = 0
    current_lines: List[str] = []

    for line in lines:
        match = _Q_MARKER.match(line)
        if match:
            if current_lines:
                blocks.append((current_q, current_lines))
            current_q = int(match.group(1))
            remainder = line[match.end():].strip(" :.-")
            current_lines = [remainder] if remainder else []
        else:
            current_lines.append(line)

    if current_lines:
        blocks.append((current_q, current_lines))

    return [(q, join_lines(ls)) for q, ls in blocks if q > 0]
