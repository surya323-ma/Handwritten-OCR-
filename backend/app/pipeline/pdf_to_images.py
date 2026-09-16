"""Step 1: Convert an uploaded PDF into per-page images."""
from pdf2image import convert_from_path
from typing import List
from PIL import Image
import os


def pdf_to_images(pdf_path: str, dpi: int = 300) -> List[Image.Image]:
    """Render each PDF page to a PIL Image at the given DPI.

    Higher DPI improves handwriting legibility for OCR at the cost
    of processing time — 300 is a reasonable default for lined
    notebook-paper scans.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(pdf_path)
    return convert_from_path(pdf_path, dpi=dpi)


def save_page_images(images: List[Image.Image], out_dir: str, file_id: str) -> List[str]:
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, img in enumerate(images):
        path = os.path.join(out_dir, f"{file_id}_page_{i+1}.png")
        img.save(path)
        paths.append(path)
    return paths
