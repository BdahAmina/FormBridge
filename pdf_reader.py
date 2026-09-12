"""PDF text extraction with OCR fallback and portable Tesseract setup."""

from __future__ import annotations

import os
import re
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
OCR_LANGUAGES = "heb+eng"

LOCAL_TESSDATA_PATH = Path(__file__).parent / "tessdata"
TEMP_TESSDATA_PATH = Path(tempfile.gettempdir()) / "formbridge_tessdata"
WINDOWS_TESSERACT_PATH = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

_HEBREW_RE = re.compile(r"[\u0590-\u05FF]")
_ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
_LTR_RUN_RE = re.compile(r"[A-Za-z0-9]+(?:[./:\-*+][A-Za-z0-9]+)*")
_REVERSED_MARKERS = (
    "חוטיב",
    "ימואלה",
    "ףינס",
    "תוריש",
    "םולשת",
    "הפוקת",
    "םוכס",
    "הנעמ",
    "דובכל",
)
_FORWARD_MARKERS = (
    "ביטוח",
    "לאומי",
    "סניף",
    "שירות",
    "תשלום",
    "תקופה",
    "סכום",
    "מענה",
    "לכבוד",
)

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


def _looks_visually_reversed(text: str) -> bool:
    """Detect Hebrew/Arabic text stored in visual (reversed) order."""
    reversed_hits = sum(1 for marker in _REVERSED_MARKERS if marker in text)
    forward_hits = sum(1 for marker in _FORWARD_MARKERS if marker in text)
    if reversed_hits == 0 and forward_hits == 0:
        rtl_chars = len(_HEBREW_RE.findall(text)) + len(_ARABIC_RE.findall(text))
        return rtl_chars > 40 and "ביטוח" not in text and "לאומי" not in text
    return reversed_hits > forward_hits


def _token_rtl_ratio(token: str) -> float:
    letters = re.findall(r"[A-Za-z\u0590-\u05FF\u0600-\u06FF]", token)
    if not letters:
        return 0.0
    rtl = len(_HEBREW_RE.findall(token)) + len(_ARABIC_RE.findall(token))
    return rtl / len(letters)


def _restore_ltr_runs(text: str) -> str:
    """After reversing RTL text, put numbers/Latin tokens back in reading order."""
    return _LTR_RUN_RE.sub(lambda match: match.group(0)[::-1], text)


def _fix_visual_token(token: str) -> str:
    """Fix one token that was stored with reversed RTL letters."""
    if _token_rtl_ratio(token) < 0.3:
        return token
    return _restore_ltr_runs(token[::-1])


def _fix_visual_line(line: str) -> str:
    """Convert visually ordered RTL OCR/PDF text into logical reading order."""
    if not line.strip():
        return line
    rtl_chars = len(_HEBREW_RE.findall(line)) + len(_ARABIC_RE.findall(line))
    if rtl_chars < 3:
        return line

    words = line.split()
    if not words:
        return line

    fixed_words = [_fix_visual_token(word) for word in words]
    # LTR scanners read RTL lines left→right, so word order is usually reversed.
    if sum(1 for word in fixed_words if _token_rtl_ratio(word) >= 0.3) >= 2:
        fixed_words.reverse()
    return " ".join(fixed_words)


def normalize_extracted_text(text: str) -> str:
    """Make OCR/PDF Hebrew (and Arabic) text readable when stored visually reversed."""
    cleaned = text.replace("\u200f", "").replace("\u200e", "")
    cleaned = cleaned.replace("\ufeff", "")
    cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    if not _looks_visually_reversed(cleaned):
        return cleaned.strip()
    fixed_lines = [_fix_visual_line(line) for line in cleaned.splitlines()]
    normalized = "\n".join(fixed_lines)
    # "סחנין סניף" → "סניף סחנין"
    normalized = re.sub(r"(?m)^(\S+)\s+סניף\s*$", r"סניף \1", normalized)
    # "2 מתוך 1 דף" → "דף 1 מתוך 2"
    normalized = re.sub(
        r"(?m)^(\d+)\s+מתוך\s+(\d+)\s+דף\s*$",
        r"דף \2 מתוך \1",
        normalized,
    )
    # Common glued payment OCR in either order
    normalized = re.sub(
        r"(20\d{2})(\d{3,4})\s*₪\s*(\d{1,2}/\d{1,2}/20\d{2})",
        r"תקופה \1 | סכום \2 ₪ | לתשלום עד \3",
        normalized,
    )
    normalized = re.sub(
        r"₪\s*(\d{1,2}/\d{1,2}/20\d{2})\s+(20\d{2})(\d{3,4})",
        r"תקופה \2 | סכום \3 ₪ | לתשלום עד \1",
        normalized,
    )
    normalized = re.sub(r"[ \t]{2,}", " ", normalized)
    return normalized.strip()

def extract_regular_text(pdf_bytes: bytes) -> str:
    """Extract embedded text from a PDF (PyMuPDF first, pypdf fallback)."""
    try:
        document = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        document = None

    if document is not None:
        try:
            extracted_pages: list[str] = []
            for page in document:
                page_text = (page.get_text("text") or "").strip()
                if page_text:
                    extracted_pages.append(page_text)
            if extracted_pages:
                return "\n\n".join(extracted_pages)
        finally:
            document.close()

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

    extracted_pages = []
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
                config="--psm 6 -c preserve_interword_spaces=1",
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

    final_text = normalize_extracted_text(final_text)
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
