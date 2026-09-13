"""Pydantic models for structured document analysis output."""

from __future__ import annotations

import json
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator


NOT_MENTIONED_AR = "غير مذكور في المستند"
NOT_MENTIONED_HE = "לא צוין במסמך"
NOT_MENTIONED_EN = "Not mentioned in the document"


class OfficialLink(BaseModel):
    title: str = ""
    url: str = ""


class GuidedGuidance(BaseModel):
    """Structured result for the guided form/service intake flow."""

    status: Literal["need_clarification", "ready"] = "need_clarification"
    assistant_message: str = ""
    clarifying_questions: list[str] = Field(default_factory=list)
    identified_service: str = ""
    authority: str = ""
    form_number: str = ""
    eligibility_summary: str = ""
    required_documents: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    official_links: list[OfficialLink] = Field(default_factory=list)
    confidence_note: str = ""
    important_fields: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    preview_summary: str = ""
    ready_to_file: bool = False

    @field_validator(
        "clarifying_questions",
        "required_documents",
        "steps",
        "important_fields",
        "missing_fields",
        mode="before",
    )
    @classmethod
    def normalize_string_lists(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            stripped = value.strip()
            return [stripped] if stripped else []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return []

    @field_validator("official_links", mode="before")
    @classmethod
    def normalize_links(cls, value: object) -> list[dict[str, str]]:
        if not value:
            return []
        if isinstance(value, dict):
            value = [value]
        if not isinstance(value, list):
            return []
        links: list[dict[str, str]] = []
        for item in value:
            if isinstance(item, str) and item.startswith("http"):
                links.append({"title": item, "url": item})
            elif isinstance(item, dict):
                url = str(item.get("url") or item.get("link") or "").strip()
                title = str(item.get("title") or item.get("name") or url).strip()
                if url:
                    links.append({"title": title or url, "url": url})
        return links

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value: object) -> str:
        text = str(value or "").strip().lower()
        if text in {"ready", "complete", "done", "answer"}:
            return "ready"
        return "need_clarification"


class DocumentAnalysis(BaseModel):
    """Structured analysis returned by the AI agent."""

    document_type: str = ""
    issuing_organization: str = ""
    recipient: str = ""
    summary: str = ""
    why_sent: str = ""
    urgency_level: Literal["low", "medium", "high"] = "medium"
    important_dates: list[str] = Field(default_factory=list)
    deadlines: list[str] = Field(default_factory=list)
    amounts_and_payments: list[str] = Field(default_factory=list)
    required_documents: list[str] = Field(default_factory=list)
    missing_or_unclear: list[str] = Field(default_factory=list)
    actions_required: list[str] = Field(default_factory=list)
    action_plan: list[str] = Field(default_factory=list)
    suggested_formal_reply_hebrew: str = ""
    confidence_score: int = Field(default=50, ge=0, le=100)
    ocr_warning: str | None = None

    @field_validator("urgency_level", mode="before")
    @classmethod
    def normalize_urgency(cls, value: object) -> str:
        if not isinstance(value, str):
            return "medium"
        normalized = value.strip().lower()
        if normalized in {"low", "medium", "high"}:
            return normalized
        if normalized in {"נמוכה", "منخفض", "منخفضة"}:
            return "low"
        if normalized in {"גבוהה", "عالية", "عالي", "high"}:
            return "high"
        return "medium"

    @field_validator("confidence_score", mode="before")
    @classmethod
    def normalize_confidence(cls, value: object) -> int:
        try:
            score = int(float(value))
        except (TypeError, ValueError):
            return 50
        return max(0, min(100, score))

    @field_validator(
        "important_dates",
        "deadlines",
        "amounts_and_payments",
        "required_documents",
        "missing_or_unclear",
        "actions_required",
        "action_plan",
        mode="before",
    )
    @classmethod
    def normalize_list_fields(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped or stripped.lower() in {
                "none",
                "n/a",
                NOT_MENTIONED_AR,
                NOT_MENTIONED_HE,
                NOT_MENTIONED_EN,
            }:
                return []
            return [stripped]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return []


def _extract_json_block(raw_text: str) -> str:
    """Extract JSON from a raw LLM response."""
    text = raw_text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence_match:
        return fence_match.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def _looks_like_json(text: str) -> bool:
    stripped = (text or "").strip()
    return stripped.startswith("{") and ("\"status\"" in stripped or "'status'" in stripped)


def _repair_json_text(text: str) -> str:
    repaired = _extract_json_block(text)
    repaired = repaired.replace("“", '"').replace("”", '"').replace("„", '"')
    repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
    return repaired


def _load_json_object(raw_text: str) -> dict:
    """Parse the first JSON object, including slightly malformed LLM output."""
    if isinstance(raw_text, dict):
        return raw_text
    text = str(raw_text or "").strip()
    candidates = [_repair_json_text(text), text]
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            start = candidate.find("{")
            if start == -1:
                continue
            try:
                payload, _ = json.JSONDecoder().raw_decode(candidate[start:])
            except json.JSONDecodeError:
                continue
        if isinstance(payload, str) and _looks_like_json(payload):
            payload = json.loads(_repair_json_text(payload))
        if isinstance(payload, dict):
            return payload
    raise json.JSONDecodeError("Could not parse guided JSON", text, 0)


def _message_from_broken_json(raw_text: str, fallback: str) -> str:
    match = re.search(
        r'"assistant_message"\s*:\s*"((?:\\.|[^"\\])*)"',
        raw_text or "",
    )
    if match:
        try:
            return json.loads(f'"{match.group(1)}"')
        except json.JSONDecodeError:
            return match.group(1)
    if _looks_like_json(raw_text):
        return fallback
    return (raw_text or "").strip() or fallback


def parse_analysis_response(
    raw_text: str,
    *,
    ocr_warning: str | None = None,
    language: str = "ar",
) -> DocumentAnalysis:
    """Parse AI output into DocumentAnalysis with safe fallback."""
    not_mentioned = {
        "ar": NOT_MENTIONED_AR,
        "he": NOT_MENTIONED_HE,
        "en": NOT_MENTIONED_EN,
    }.get(language, NOT_MENTIONED_AR)

    try:
        payload = json.loads(_extract_json_block(raw_text))
        if ocr_warning:
            payload["ocr_warning"] = ocr_warning
        return DocumentAnalysis.model_validate(payload)
    except (json.JSONDecodeError, ValueError):
        pass

    return DocumentAnalysis(
        document_type=not_mentioned,
        issuing_organization=not_mentioned,
        recipient=not_mentioned,
        summary=raw_text.strip() or not_mentioned,
        why_sent=not_mentioned,
        urgency_level="medium",
        important_dates=[],
        deadlines=[],
        amounts_and_payments=[],
        required_documents=[],
        missing_or_unclear=[not_mentioned],
        actions_required=[],
        action_plan=[],
        suggested_formal_reply_hebrew="",
        confidence_score=30,
        ocr_warning=ocr_warning,
    )


def parse_guided_response(raw_text: str, language: str = "ar") -> GuidedGuidance:
    """Parse guided-intake agent output into GuidedGuidance."""
    fallback_message = {
        "ar": "أحتاج بعض التفاصيل الإضافية لأحدد الاستمارة أو الخدمة المناسبة.",
        "he": "אני צריך/ה עוד כמה פרטים כדי לזהות את הטופס או השירות המתאים.",
        "en": "I need a few more details to identify the right form or service.",
    }.get(language, "I need a few more details.")

    try:
        payload = _load_json_object(raw_text)
        guidance = GuidedGuidance.model_validate(payload)
        if _looks_like_json(guidance.assistant_message):
            nested = _load_json_object(guidance.assistant_message)
            guidance = GuidedGuidance.model_validate(nested)
        if not guidance.assistant_message or _looks_like_json(guidance.assistant_message):
            guidance.assistant_message = fallback_message
        return guidance
    except (json.JSONDecodeError, ValueError):
        pass

    return GuidedGuidance(
        status="need_clarification",
        assistant_message=_message_from_broken_json(raw_text, fallback_message),
        clarifying_questions=[],
    )


def humanize_guided_text(text: str, language: str = "ar") -> str:
    """Never show raw guided JSON in the chat UI."""
    cleaned = (text or "").strip()
    if not cleaned:
        return ""
    if not (cleaned.startswith("{") or cleaned.startswith("```")):
        return cleaned
    guidance = parse_guided_response(cleaned, language=language)
    message = (guidance.assistant_message or "").strip()
    if message and not _looks_like_json(message):
        return message
    if guidance.identified_service:
        return guidance.identified_service
    return {
        "ar": "تم تحديد الخدمة. راجعي التفاصيل في البطاقات أدناه.",
        "he": "השירות זוהה. ראו את הפרטים בכרטיסים למטה.",
        "en": "The service was identified. See the cards below.",
    }.get(language, "See the details below.")
