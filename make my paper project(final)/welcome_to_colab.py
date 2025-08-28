import easyocr
from pdf2image import convert_from_path
from PIL import Image
import matplotlib.pyplot as plt
from jiwer import wer, cer
import numpy as np

filename = 'love.png'

# Initialize reader (English)
reader = easyocr.Reader(['en'])

# If it's an image, load directly; if PDF, convert first page
if filename.lower().endswith((".png", ".jpg", ".jpeg")):
    img = Image.open(filename).convert("RGB")
elif filename.lower().endswith(".pdf"):
    pages = convert_from_path(filename, dpi=200)
    img   = pages[0]
else:
    raise ValueError("Unsupported file type")


def ocr_image(img):
    # If it's a PIL Image, convert to a NumPy array (RGB→BGR for OpenCV)
    if isinstance(img, Image.Image):
        arr = np.array(img)[:, :, ::-1]  # RGB to BGR
    else:
        arr = img  # assume already a NumPy array or path

    # Run EasyOCR
    lines = reader.readtext(arr, detail=0, paragraph=True)
    return "\n".join(lines)

# Now branch on extension as before:
if filename.lower().endswith(".pdf"):
    full_text = []
    for i, page in enumerate(pages, start=1):
        txt = ocr_image(page)
        full_text.append(f"--- Page {i} ---\n{txt}")
    ocr_output = "\n\n".join(full_text)
else:
    ocr_output = ocr_image(img)

print("=== OCR Output ===\n")
print(ocr_output)

# Branch on file type, run OCR, and print
ext = filename.lower().split('.')[-1]

if ext in ("png", "jpg", "jpeg"):
    hypothesis = ocr_image(img)

else:  # PDF
    all_pages = []
    for i, page in enumerate(pages, start=1):
        text = ocr_image(page)
        all_pages.append(f"--- Page {i} ---\n{text}\n")
    hypothesis = "\n".join(all_pages)

print("=== OCR Output ===\n")
print(hypothesis)

