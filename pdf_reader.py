"""PDF text extraction with OCR fallback and portable Tesseract setup."""

from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image
from pypdf import PdfReader
from pypdf.errors import PdfReadError


MIN_TEXT_CHARS = 30
MAX_DOCUMENT_CHARS = 80_000
OCR_LANGUAGES = "heb+ara+eng"

LOCAL_TESSDATA_PATH = Path(__file__).parent / "tessdata"
TEMP_TESSDATA_PATH = Path(tempfile.gettempdir()) / "formbridge_tessdata"
WINDOWS_TESSERACT_PATH = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")


class PDFProcessingError(Exception):
    """Base error for PDF processing failures."""


class PDFEmptyError(PDFProcessingError):
    """Raised when no text could be extracted."""


class PDFPasswordError(PDFProcessingError):
    """Raised when the PDF is password protected."""


class PDFCorruptedError(PDFProcessingError):
    """Raised when the PDF cannot be read."""


class DocumentTooLongError(PDFProcessingError):
    """Raised when extracted text exceeds the safe processing limit."""


class OCRNotAvailableError(PDFProcessingError):
    """Raised when Tesseract OCR is not available."""


class OCRLanguageMissingError(PDFProcessingError):
    """Raised when required OCR language files are missing."""


@dataclass
class ExtractionResult:
    text: str
    used_ocr: bool
    ocr_warning: str | None
    truncated: bool = False


def _sync_tessdata() -> None:
    """Copy local tessdata files to a temp path with an ASCII-only location."""
    TEMP_TESSDATA_PATH.mkdir(parents=True, exist_ok=True)
    for language_file in LOCAL_TESSDATA_PATH.glob("*.traineddata"):
        destination = TEMP_TESSDATA_PATH / language_file.name
        if not destination.exists() or destination.stat().st_mtime < language_file.stat().st_mtime:
            shutil.copy2(language_file, destination)


def _configure_tesseract() -> Path | None:
    """Detect Tesseract executable and configure pytesseract."""
    candidates: list[Path] = []

    env_path = os.getenv("TESSERACT_CMD")
    if env_path:
        candidates.append(Path(env_path))

    which_path = shutil.which("tesseract")
    if which_path:
        candidates.append(Path(which_path))

    if os.name == "nt":
        candidates.append(WINDOWS_TESSERACT_PATH)

    for candidate in candidates:
        if candidate.exists():
            pytesseract.pytesseract.tesseract_cmd = str(candidate)
            return candidate

    return None


def _verify_ocr_languages() -> None:
    """Ensure Hebrew, Arabic, and English tessdata files are available."""
    required = ("heb.traineddata", "ara.traineddata", "eng.traineddata")
    missing = [name for name in required if not (TEMP_TESSDATA_PATH / name).exists()]
    if missing:
        raise OCRLanguageMissingError(
            "Missing OCR language files: " + ", ".join(missing)
        )


def _truncate_text(text: str) -> tuple[str, bool]:
    if len(text) <= MAX_DOCUMENT_CHARS:
        return text, False
    return text[:MAX_DOCUMENT_CHARS], True


def extract_regular_text(pdf_bytes: bytes) -> str:
    """Extract embedded text from a PDF."""
    try:
        reader = PdfReader(BytesIO(pdf_bytes), strict=False)
    except PdfReadError as error:
        raise PDFCorruptedError("The PDF file appears to be corrupted.") from error

    if reader.is_encrypted:
        try:
            decrypt_result = reader.decrypt("")
            if decrypt_result == 0:
                raise PDFPasswordError("The PDF is password protected.")
        except PdfReadError as error:
            raise PDFPasswordError("The PDF is password protected.") from error

    extracted_pages: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            extracted_pages.append(page_text.strip())

    return "\n\n".join(extracted_pages)


def extract_text_with_ocr(pdf_bytes: bytes) -> str:
    """Run OCR on each PDF page when embedded text is insufficient."""
    tesseract_path = _configure_tesseract()
    if tesseract_path is None:
        raise OCRNotAvailableError("Tesseract OCR is not installed or not found.")

    _sync_tessdata()
    os.environ["TESSDATA_PREFIX"] = str(TEMP_TESSDATA_PATH)
    _verify_ocr_languages()

    try:
        document = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception as error:
        raise PDFCorruptedError("The PDF file could not be opened for OCR.") from error

    extracted_pages: list[str] = []
    try:
        for page in document:
            pixmap = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
            image = Image.open(BytesIO(pixmap.tobytes("png")))
            page_text = pytesseract.image_to_string(
                image,
                lang=OCR_LANGUAGES,
                config="--psm 6",
            )
            if page_text and page_text.strip():
                extracted_pages.append(page_text.strip())
    finally:
        document.close()

    return "\n\n".join(extracted_pages)


def extract_text_from_pdf(pdf_file) -> ExtractionResult:
    """
    Main entry point: try regular extraction, then OCR if needed.
    """
    pdf_file.seek(0)
    pdf_bytes = pdf_file.read()

    if not pdf_bytes:
        raise PDFCorruptedError("The uploaded file is empty.")

    regular_text = extract_regular_text(pdf_bytes)
    used_ocr = False
    ocr_warning: str | None = None

    if len(regular_text.strip()) >= MIN_TEXT_CHARS:
        final_text = regular_text
    else:
        ocr_text = extract_text_with_ocr(pdf_bytes)
        used_ocr = True
        ocr_warning = (
            "OCR was used because the PDF appears to be scanned or image-based. "
            "Some words, numbers, or dates may be inaccurate."
        )
        final_text = ocr_text

    if not final_text.strip():
        raise PDFEmptyError("No readable text could be extracted from the PDF.")

    final_text, truncated = _truncate_text(final_text.strip())
    return ExtractionResult(
        text=final_text,
        used_ocr=used_ocr,
        ocr_warning=ocr_warning,
        truncated=truncated,
    )


def get_tesseract_status() -> dict[str, object]:
    """Return Tesseract availability for UI diagnostics."""
    path = _configure_tesseract()
    _sync_tessdata()
    required = ("heb.traineddata", "ara.traineddata", "eng.traineddata")
    missing = [name for name in required if not (TEMP_TESSDATA_PATH / name).exists()]
    return {
        "available": path is not None,
        "path": str(path) if path else None,
        "missing_language_files": missing,
    }
