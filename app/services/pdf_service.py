# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )
import io

import pymupdf
import pytesseract
from PIL import Image


def _ocr_page(page) -> str:
    pix = page.get_pixmap(
        matrix=pymupdf.Matrix(2, 2),
        alpha=False,
    )

    image_bytes = pix.tobytes("png")

    image = Image.open(
        io.BytesIO(image_bytes)
    )

    text = pytesseract.image_to_string(
        image,
        lang="eng",
    )

    return text.strip()


def extract_pdf_pages(file_path: str,) -> list[dict]:

    document = pymupdf.open(file_path)

    pages = []

    try:
        for index, page in enumerate(document):

            # 1. Try normal text extraction first
            text = page.get_text("text").strip()

            print(
                f"Page {index + 1}: "
                f"{len(text)} characters extracted normally"
            )

            # 2. OCR fallback
            if not text:
                print(
                    f"Page {index + 1}: "
                    "No text layer found. Running OCR..."
                )

                text = _ocr_page(page)

                print(
                    f"Page {index + 1}: "
                    f"{len(text)} characters extracted using OCR"
                )

            # 3. Skip completely empty pages
            if not text:
                print(
                    f"Page {index + 1}: "
                    "No readable text found even after OCR."
                )

                continue

            pages.append(
                {
                    "page_number":
                        index + 1,

                    "text":
                        text,
                }
            )

    finally:
        document.close()

    return pages