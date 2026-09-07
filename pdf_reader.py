from io import BytesIO
from pathlib import Path
import os
import shutil
import tempfile

import pymupdf
import pytesseract
from PIL import Image
from pypdf import PdfReader


# מיקום תוכנת Tesseract במחשב
TESSERACT_PATH = Path(
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# תיקיית השפות שנמצאת בתוך הפרויקט
LOCAL_TESSDATA_PATH = Path(__file__).parent / "tessdata"

# תיקייה זמנית עם נתיב באנגלית בלבד
TEMP_TESSDATA_PATH = (
    Path(tempfile.gettempdir()) / "formbridge_tessdata"
)

# יצירת התיקייה הזמנית
TEMP_TESSDATA_PATH.mkdir(
    parents=True,
    exist_ok=True
)

# העתקת קובצי השפות לתיקייה הזמנית
for language_file in LOCAL_TESSDATA_PATH.glob("*.traineddata"):
    destination = TEMP_TESSDATA_PATH / language_file.name

    shutil.copy2(
        language_file,
        destination
    )

# הגדרת מיקום תוכנת Tesseract
if TESSERACT_PATH.exists():
    pytesseract.pytesseract.tesseract_cmd = str(
        TESSERACT_PATH
    )

# הגדרת מיקום קובצי השפות
os.environ["TESSDATA_PREFIX"] = str(
    TEMP_TESSDATA_PATH
)


def extract_regular_text(pdf_bytes):
    """
    ניסיון ראשון: חילוץ טקסט רגיל מתוך PDF.
    """

    reader = PdfReader(BytesIO(pdf_bytes))
    extracted_pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text and page_text.strip():
            extracted_pages.append(page_text)

    return "\n\n".join(extracted_pages)


def extract_text_with_ocr(pdf_bytes):
    """
    אם ה-PDF הוא סריקה, הפונקציה מפעילה OCR.
    """

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    extracted_pages = []

    try:
        for page in document:
            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2),
                alpha=False
            )

            image_bytes = pixmap.tobytes("png")
            image = Image.open(
                BytesIO(image_bytes)
            )

            page_text = pytesseract.image_to_string(
                image,
                lang="heb+ara+eng",
                config="--psm 6"
            )

            if page_text and page_text.strip():
                extracted_pages.append(page_text)

    finally:
        document.close()

    return "\n\n".join(extracted_pages)


def extract_text_from_pdf(pdf_file):
    """
    הפונקציה הראשית:
    מנסה קריאת PDF רגילה, ואם אין טקסט מפעילה OCR.
    """

    pdf_file.seek(0)
    pdf_bytes = pdf_file.read()

    regular_text = extract_regular_text(pdf_bytes)

    if len(regular_text.strip()) >= 30:
        return regular_text

    return extract_text_with_ocr(pdf_bytes)