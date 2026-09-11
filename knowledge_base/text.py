"""Hebrew-aware cleaning and chunking."""

from __future__ import annotations

import hashlib
import re


NAV_NOISE = (
    "cookie",
    "cookies",
    "javascript",
    "skip to",
    "דילוג לתוכן",
    "כל הזכויות שמורות",
    "accessibility",
    "נגישות",
)

_TOKEN_RE = re.compile(r"[\w\u0590-\u05FF\u0600-\u06FF]+", re.UNICODE)


def stable_id(*parts: str) -> str:
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def content_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def tokenize(text: str) -> list[str]:
    tokens = [token.lower() for token in _TOKEN_RE.findall(text or "")]
    expanded = list(tokens)
    for token in tokens:
        if token.startswith("ה") and len(token) > 3:
            expanded.append(token[1:])
    return expanded


def clean_text(text: str) -> str:
    lines = []
    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(noise in lowered for noise in NAV_NOISE):
            continue
        if len(line) < 3:
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def strip_html(html: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html or "")
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)<nav.*?>.*?</nav>", " ", text)
    text = re.sub(r"(?is)<footer.*?>.*?</footer>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    return clean_text(text)


def sanitize_evidence(text: str) -> str:
    """Drop instruction-like lines so retrieved text cannot act as a prompt."""
    kept = []
    for line in (text or "").splitlines():
        lowered = line.strip().lower()
        if lowered.startswith(("ignore previous", "system prompt", "reveal api", "override")):
            continue
        if "ignore all instructions" in lowered:
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> list[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", cleaned) if part.strip()]
    pieces: list[str] = []
    for paragraph in paragraphs:
        if len(paragraph) <= chunk_size:
            pieces.append(paragraph)
            continue
        start = 0
        while start < len(paragraph):
            pieces.append(paragraph[start : start + chunk_size].strip())
            start += max(chunk_size - overlap, 1)
    merged: list[str] = []
    buffer = ""
    for piece in pieces:
        if not buffer:
            buffer = piece
        elif len(buffer) + 1 + len(piece) <= chunk_size:
            buffer = f"{buffer}\n{piece}"
        else:
            merged.append(buffer)
            buffer = piece
    if buffer:
        merged.append(buffer)
    return merged
