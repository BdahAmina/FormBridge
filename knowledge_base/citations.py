"""Citation objects for grounded answers."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from knowledge_base.models import ChunkMetadata


@dataclass
class Citation:
    title: str
    authority: str
    authority_key: str
    source_type: str
    source_url: str
    page_number: int | None
    last_checked_at: str
    form_number: str = ""
    form_name: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def citation_from_metadata(metadata: ChunkMetadata) -> Citation:
    return Citation(
        title=metadata.title or metadata.form_name or metadata.authority,
        authority=metadata.authority,
        authority_key=metadata.authority_key,
        source_type=metadata.source_type,
        source_url=metadata.source_url,
        page_number=metadata.page_number,
        last_checked_at=metadata.last_checked_at,
        form_number=metadata.form_number,
        form_name=metadata.form_name,
    )


def format_citations(citations: list[Citation], language: str = "he") -> str:
    if not citations:
        return ""
    heading = {
        "ar": "المصادر",
        "en": "Sources",
        "he": "מקורות",
    }.get(language, "מקורות")
    lines = [f"{heading}:"]
    for item in citations:
        badge = "רשמי" if item.source_type == "official" else "משני / כל זכות"
        page = f" · עמוד {item.page_number}" if item.page_number and item.page_number > 1 else ""
        form = f" (טופס {item.form_number})" if item.form_number else ""
        lines.append(f"- {item.authority} — {item.title}{form} [{badge}]")
        lines.append(f"  {item.source_url}{page}")
        lines.append(f"  Last checked: {item.last_checked_at}")
    return "\n".join(lines)
