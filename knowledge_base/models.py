"""Pydantic models for official knowledge-base chunks and status."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class ChunkMetadata(BaseModel):
    document_id: str
    authority: str
    authority_key: str
    source_type: str
    document_type: str = "page"
    form_number: str = ""
    form_name: str = ""
    category: str = ""
    language: str = "he"
    source_url: str
    page_number: int = 1
    title: str = ""
    content_hash: str
    published_at: str | None = None
    last_updated_at: str | None = None
    last_checked_at: str = Field(default_factory=utc_now)

    @field_validator("source_type")
    @classmethod
    def validate_source_type(cls, value: str) -> str:
        if value not in {"official", "secondary"}:
            raise ValueError("source_type must be official or secondary")
        return value

    @field_validator("source_url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("source_url must be https")
        return value


class IndexedChunk(BaseModel):
    chunk_id: str
    text: str
    metadata: ChunkMetadata


class AuthorityStatus(BaseModel):
    authority_key: str
    enabled: bool = True
    source_type: str = "official"
    documents: int = 0
    chunks: int = 0
    last_success: str | None = None
    last_attempt: str | None = None
    last_error: str | None = None
    status: str = "idle"
