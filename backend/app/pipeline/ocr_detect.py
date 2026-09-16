"""Step 2a: Line/region detection with PaddleOCR (detection-only)."""
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
from typing import List, Tuple

# lang='en' det model; rec is disabled since TrOCR handles recognition.
_paddle = PaddleOCR(use_angle_cls=True, lang="en", show_log=False, rec=False)

BBox = Tuple[int, int, int, int]  # x_min, y_min, x_max, y_max


def detect_text_lines(pil_img: Image.Image) -> List[BBox]:
    """Return bounding boxes for each detected line of handwriting,
    ordered top-to-bottom, left-to-right (natural reading order for
    single-column answer sheets)."""
    img_np = np.array(pil_img)
    result = _paddle.ocr(img_np, cls=True, rec=False)

    boxes: List[BBox] = []
    for line in result[0] or []:
        pts = line[0] if isinstance(line, (list, tuple)) else line
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        boxes.append((int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))))

    boxes.sort(key=lambda b: (b[1], b[0]))
    return boxes


def crop_lines(pil_img: Image.Image, boxes: List[BBox]) -> List[Image.Image]:
    return [pil_img.crop(box) for box in boxes]
