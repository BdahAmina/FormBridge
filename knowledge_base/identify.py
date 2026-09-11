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


_FORM_NUMBER_RE = re.compile(r"\b(?:טופס|form)?\s*(\d{3,5})\b", re.IGNORECASE)


def _detect_language(text: str) -> str:
    hebrew = len(re.findall(r"[\u0590-\u05FF]", text))
    arabic = len(re.findall(r"[\u0600-\u06FF]", text))
    if arabic > hebrew and arabic > 8:
        return "ar"
    if hebrew > 8:
        return "he"
    return "en"


def identify_form(text: str, analysis_org: str = "") -> FormIdentity:
    haystack = f"{text}\n{analysis_org}".lower()
    scores: dict[str, float] = {key: 0.0 for key in AUTHORITIES}
    form_number = ""
    match = _FORM_NUMBER_RE.search(text)
    if match:
        form_number = match.group(1)

    for key, authority in AUTHORITIES.items():
        for hint in authority.form_hints:
            if hint.lower() in haystack:
                scores[key] += 2.0 if hint.isdigit() else 1.0
        if form_number and form_number in authority.form_hints:
            scores[key] += 3.0

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
        category = authority.categories[0] if authority.categories else ""
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
