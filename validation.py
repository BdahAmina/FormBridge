"""Input validators for Israeli forms assistance."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import datetime


EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
# Israeli mobiles: 05X-XXXXXXX; landlines: 0Y-XXXXXXX (area codes 2-9, not 5 for mobile)
PHONE_RE = re.compile(
    r"^(?:\+972[\-\s]?|0)"
    r"(?:5[0-9]|[2-489])"
    r"[\-\s]?"
    r"\d{7}$"
)
DATE_RE = re.compile(
    r"^(?P<d>\d{1,2})[./\-](?P<m>\d{1,2})[./\-](?P<y>\d{2,4})$"
)


@dataclass
class ValidationResult:
    field: str
    value: str
    ok: bool
    normalized: str = ""
    message: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def validate_israeli_id(value: str) -> ValidationResult:
    """Validate Israeli Teudat Zehut with Luhn-like checksum."""
    digits = re.sub(r"\D", "", value or "")
    if len(digits) != 9 or not digits.isdigit():
        return ValidationResult(
            field="israeli_id",
            value=value,
            ok=False,
            message="Israeli ID must be exactly 9 digits.",
        )
    total = 0
    for index, char in enumerate(digits):
        num = int(char) * ((index % 2) + 1)
        if num > 9:
            num -= 9
        total += num
    ok = total % 10 == 0
    return ValidationResult(
        field="israeli_id",
        value=value,
        ok=ok,
        normalized=digits if ok else "",
        message="Valid Israeli ID." if ok else "Israeli ID checksum failed.",
    )


def validate_email(value: str) -> ValidationResult:
    text = (value or "").strip()
    ok = bool(EMAIL_RE.match(text))
    return ValidationResult(
        field="email",
        value=value,
        ok=ok,
        normalized=text.lower() if ok else "",
        message="Valid email." if ok else "Email format is invalid.",
    )


def validate_phone(value: str) -> ValidationResult:
    text = (value or "").strip()
    compact = re.sub(r"[\s\-()]", "", text)
    # Normalize +9725... -> 05...
    if compact.startswith("+972"):
        compact = "0" + compact[4:]
    display = compact
    ok = bool(PHONE_RE.match(text) or PHONE_RE.match(compact))
    if ok and compact.startswith("0") and len(compact) >= 9:
        display = f"{compact[:3]}-{compact[3:]}" if compact[1] == "5" else f"{compact[:2]}-{compact[2:]}"
    return ValidationResult(
        field="phone",
        value=value,
        ok=ok,
        normalized=display if ok else "",
        message="Valid Israeli phone." if ok else "Phone must look like 05X-XXXXXXX or 0Y-XXXXXXX.",
    )


def validate_date(value: str) -> ValidationResult:
    text = (value or "").strip()
    match = DATE_RE.match(text)
    if not match:
        return ValidationResult(
            field="date",
            value=value,
            ok=False,
            message="Date must be DD/MM/YYYY (or D.M.YYYY).",
        )
    day = int(match.group("d"))
    month = int(match.group("m"))
    year = int(match.group("y"))
    if year < 100:
        year += 2000 if year < 50 else 1900
    try:
        parsed = datetime(year, month, day)
    except ValueError:
        return ValidationResult(
            field="date",
            value=value,
            ok=False,
            message="Date values are out of range.",
        )
    normalized = parsed.strftime("%d/%m/%Y")
    return ValidationResult(
        field="date",
        value=value,
        ok=True,
        normalized=normalized,
        message=f"Valid date ({normalized}).",
    )


def validate_required(value: str, field_name: str = "required") -> ValidationResult:
    text = (value or "").strip()
    ok = bool(text)
    return ValidationResult(
        field=field_name,
        value=value,
        ok=ok,
        normalized=text if ok else "",
        message="Required field is present." if ok else f"Required field '{field_name}' is empty.",
    )


def validate_user_input(field_type: str, value: str, field_name: str = "") -> ValidationResult:
    kind = (field_type or "").strip().lower()
    if kind in {"israeli_id", "id", "teudat_zehut", "תז", "ת.ז."}:
        return validate_israeli_id(value)
    if kind in {"email", "e-mail"}:
        return validate_email(value)
    if kind in {"phone", "mobile", "tel"}:
        return validate_phone(value)
    if kind in {"date", "deadline"}:
        return validate_date(value)
    if kind in {"required", "text"}:
        return validate_required(value, field_name or "required")
    return ValidationResult(
        field=field_name or kind or "unknown",
        value=value,
        ok=False,
        message=f"Unsupported field type '{field_type}'. Use israeli_id|email|phone|date|required.",
    )
