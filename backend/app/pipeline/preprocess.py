"""Step 1b: Image preprocessing — CLAHE contrast enhancement + denoise.

Handwritten answer sheets are often photographed rather than scanned,
so lighting is uneven. CLAHE (Contrast Limited Adaptive Histogram
Equalization) boosts local contrast without blowing out bright areas,
which noticeably helps faint pencil / light-pen handwriting.
"""
import cv2
import numpy as np
from PIL import Image


def preprocess_image(pil_img: Image.Image) -> Image.Image:
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    denoised = cv2.fastNlMeansDenoising(enhanced, h=10)

    # Mild adaptive threshold helps separate ink from paper texture
    # without fully binarizing (keeps some grayscale nuance for TrOCR).
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 25, 15,
    )

    result_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(result_rgb)
