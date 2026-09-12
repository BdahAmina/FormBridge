"""Privacy helpers: masking sensitive values and consent text."""

from __future__ import annotations

import re


_ID_RE = re.compile(r"\b\d{9}\b")
_PHONE_RE = re.compile(r"(?:\+972[\-\s]?|0)(?:5\d|[2-489])[\-\s]?\d{7}")
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_CARD_RE = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
_API_KEY_RE = re.compile(
    r"(?:GEMINI_API_KEY|GROQ_API_KEY|GOOGLE_API_KEY|sk-|gsk_|AQ\.)[^\s\"']+",
    re.IGNORECASE,
)


def mask_sensitive(text: str) -> str:
    """Mask IDs, phones, emails, card-like numbers, and API keys for logs."""
    if not text:
        return ""
    masked = _API_KEY_RE.sub("[REDACTED_SECRET]", text)
    masked = _EMAIL_RE.sub("[REDACTED_EMAIL]", masked)
    masked = _PHONE_RE.sub("[REDACTED_PHONE]", masked)
    masked = _ID_RE.sub("[REDACTED_ID]", masked)
    masked = _CARD_RE.sub("[REDACTED_NUMBER]", masked)
    return masked


PRIVACY_NOTICE = {
    "ar": (
        "FormBridge مساعد معلوماتي فقط وليس بديلاً عن استشارة رسمية أو قانونية. "
        "لا نخزّن أرقام هوية أو بيانات صحية أو مالية إلا إذا وافقت صراحة. "
        "يمكنك حذف المحادثة في أي وقت."
    ),
    "he": (
        "FormBridge הוא כלי מידע בלבד ואינו מחליף ייעוץ רשמי או משפטי. "
        "איננו שומרים מספרי זהות, מידע רפואי או פיננסי אלא אם אישרתם במפורש. "
        "ניתן למחוק את השיחה בכל עת."
    ),
    "en": (
        "FormBridge is an informational assistant only and not a substitute for "
        "official or legal advice. We do not store ID numbers, health, or financial "
        "details unless you explicitly consent. You can delete the conversation at any time."
    ),
}

CONSENT_LABEL = {
    "ar": "أوافق على معالجة وصفي/مستندي لهذا الجلسة فقط، وأفهم أنه لا يُنصح برفع بيانات حساسة غير ضرورية.",
    "he": "אני מסכים/ה לעיבוד התיאור/המסמך בסשן זה בלבד, ומבין/ה שאין להעלות מידע רגיש מיותר.",
    "en": "I consent to processing my description/document for this session only, and understand not to upload unnecessary sensitive data.",
}
