"""Identify the issuing authority and form from uploaded text."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from knowledge_base.authorities import AUTHORITIES, Authority


@dataclass
class FormIdentity:
    authority_key: str | None
    authority: str | None
    form_number: str
    form_name: str
    category: str
    language: str
    confidence: float
    uncertain: bool

    def to_dict(self) -> dict:
        return asdict(self)


# Prefer explicit "טופס NNNN" / "form NNNN".
_EXPLICIT_FORM_RE = re.compile(r"(?:טופס|form)\s*#?\s*(\d{3,5})\b", re.IGNORECASE)
# Generic number candidates (used only when not a phone/service code).
_NUMBER_RE = re.compile(r"\b(\d{3,5})\b")
_PHONE_CONTEXT_RE = re.compile(
    r"(?:\*|טל(?:פון)?|פקס|מוקד|קו\s*חמה|call\s*center|fax|tel|"
    r"04-|08-|02-|03-|09-)\s*(\d{3,5})\b",
    re.IGNORECASE,
)
_CURRENCY_NUMBER_RE = re.compile(r"(?:₪\s*(\d{3,5})|(\d{3,5})\s*₪)")
_POSTAL_CONTEXT_RE = re.compile(r"(?:ת\"ד|ת\.ד\.|מיקוד|zip|p\.?\s*o\.?\s*box)\s*[:\-]?\s*(\d{3,7})", re.I)
# BTL short codes / payment codes that are not form IDs.
_SERVICE_CODES = {"6050", "28900", "10013", "05450"}


def _detect_language(text: str) -> str:
    hebrew = len(re.findall(r"[\u0590-\u05FF]", text))
    arabic = len(re.findall(r"[\u0600-\u06FF]", text))
    if arabic > hebrew and arabic > 8:
        return "ar"
    if hebrew > 8:
        return "he"
    return "en"


def _domain_mentioned(domain: str, haystack: str) -> bool:
    pattern = rf"(?<![a-z0-9-]){re.escape(domain.lower())}(?![a-z0-9-])"
    return re.search(pattern, haystack) is not None


def _extract_form_number(text: str) -> str:
    explicit = _EXPLICIT_FORM_RE.search(text)
    if explicit:
        return explicit.group(1)

    phone_numbers = {match.group(1) for match in _PHONE_CONTEXT_RE.finditer(text)}
    phone_numbers.update(re.findall(r"\*\s*(\d{3,5})\b", text))
    currency_numbers = set()
    for match in _CURRENCY_NUMBER_RE.finditer(text):
        currency_numbers.update(group for group in match.groups() if group)
    postal_numbers = {match.group(1) for match in _POSTAL_CONTEXT_RE.finditer(text)}

    for match in _NUMBER_RE.finditer(text):
        number = match.group(1)
        if (
            number in _SERVICE_CODES
            or number in phone_numbers
            or number in currency_numbers
            or number in postal_numbers
        ):
            continue
        # Skip years and bare payment-looking values.
        if number.startswith("20") and len(number) == 4:
            continue
        if number.startswith("0") and len(number) == 5:
            # Likely a postal code, not a government form id.
            continue
        start = match.start()
        window = text[max(0, start - 12) : match.end() + 12]
        if "₪" in window or "דמי" in window or "סכום" in window or 'ת"ד' in window:
            continue
        return number
    return ""


def identify_form(text: str, analysis_org: str = "") -> FormIdentity:
    haystack = f"{text}\n{analysis_org}".lower()
    scores: dict[str, float] = {key: 0.0 for key in AUTHORITIES}
    form_number = _extract_form_number(text)

    for key, authority in AUTHORITIES.items():
        for hint in authority.form_hints:
            if hint.lower() in haystack:
                scores[key] += 2.0 if hint.isdigit() else 1.0
        if form_number and form_number in authority.form_hints:
            scores[key] += 3.0
        for domain in authority.allowed_domains:
            if _domain_mentioned(domain, haystack):
                scores[key] += 2.5
        if authority.name_he and authority.name_he in text:
            scores[key] += 2.0

    # Prefer the more specific official site when both could match.
    if "btl.gov.il" in haystack:
        scores["btl"] = scores.get("btl", 0) + 3.0
    if "דמי ביטוח" in text or "ביטוח לאומי" in text:
        scores["btl"] = scores.get("btl", 0) + 2.0

    best_key = max(scores, key=lambda item: scores[item])
    best_score = scores[best_key]
    confidence = min(1.0, best_score / 5.0)
    uncertain = confidence < 0.45
    authority: Authority | None = AUTHORITIES.get(best_key) if best_score else None
    form_name = ""
    category = ""
    if authority and not uncertain:
        form_name = {
            "1500": "תביעה לדמי אבטלה",
            "101": "כרטיס עובד",
        }.get(form_number, "")
        if form_number and form_number in (authority.form_hints if authority else ()):
            category = authority.categories[0] if authority.categories else ""
        elif "דמי ביטוח" in text:
            category = "דמי ביטוח"
        else:
            category = ""
    return FormIdentity(
        authority_key=None if uncertain else (authority.key if authority else None),
        authority=None if uncertain else (authority.name_he if authority else None),
        form_number=form_number,
        form_name=form_name,
        category=category,
        language=_detect_language(text),
        confidence=round(confidence, 2),
        uncertain=uncertain,
    )
