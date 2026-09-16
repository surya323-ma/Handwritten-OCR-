"""Step 2b: Handwriting recognition with Microsoft TrOCR."""
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
from typing import List, Tuple
import torch

_MODEL_NAME = "microsoft/trocr-large-handwritten"

_processor = TrOCRProcessor.from_pretrained(_MODEL_NAME)
_model = VisionEncoderDecoderModel.from_pretrained(_MODEL_NAME)
_device = "cuda" if torch.cuda.is_available() else "cpu"
_model.to(_device)


def recognize_lines(line_images: List[Image.Image]) -> List[Tuple[str, float]]:
    """Run TrOCR on each cropped line image.

    Returns a list of (text, confidence) pairs. Confidence is derived
    from the mean token-level softmax probability of the generated
    sequence, as a rough proxy — not a calibrated accuracy score.
    """
    results = []
    for img in line_images:
        if img.mode != "RGB":
            img = img.convert("RGB")

        pixel_values = _processor(images=img, return_tensors="pt").pixel_values.to(_device)

        with torch.no_grad():
            out = _model.generate(
                pixel_values,
                output_scores=True,
                return_dict_in_generate=True,
                max_new_tokens=128,
            )

        text = _processor.batch_decode(out.sequences, skip_special_tokens=True)[0]

        # Rough confidence: mean max-softmax prob per generated token
        if out.scores:
            probs = [torch.softmax(s, dim=-1).max().item() for s in out.scores]
            confidence = sum(probs) / len(probs)
        else:
            confidence = 0.0

        results.append((text.strip(), round(confidence, 4)))

    return results
