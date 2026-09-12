"""Pydantic models for structured document analysis output."""

from __future__ import annotations

import json
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator


NOT_MENTIONED_AR = "غير مذكور في المستند"
NOT_MENTIONED_HE = "לא צוין במסמך"
NOT_MENTIONED_EN = "Not mentioned in the document"


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
