"""Hybrid official-source retrieval with authority-priority reranking."""

from __future__ import annotations

from dataclasses import dataclass

from knowledge_base.authorities import source_priority
from knowledge_base.citations import Citation, citation_from_metadata
from knowledge_base.config import KBConfig
from knowledge_base.identify import FormIdentity
from knowledge_base.models import IndexedChunk
from knowledge_base.store import FileVectorStore, open_store
from knowledge_base.text import sanitize_evidence, tokenize


@dataclass
class OfficialHit:
    chunk: IndexedChunk
    score: float
    citation: Citation


def _keyword_bonus(question: str, chunk: IndexedChunk) -> float:
    bonus = 0.0
    q = question.lower()
    meta = chunk.metadata
    if meta.form_number and meta.form_number in question:
        bonus += 0.45
    question_tokens = set(tokenize(question))
    chunk_tokens = set(tokenize(chunk.text + " " + meta.title + " " + meta.form_name))
    if question_tokens and chunk_tokens:
        bonus += 0.25 * (len(question_tokens & chunk_tokens) / len(question_tokens))
    if meta.authority and meta.authority in question:
        bonus += 0.1
    if "כל זכות" in q and meta.authority_key != "kolzchut":
        bonus += 0.0
    return bonus


def _priority_bonus(authority_key: str) -> float:
    priority = source_priority(authority_key)
    return {1: 0.12, 2: 0.08, 3: 0.04, 4: -0.08}.get(priority, 0.0)


def retrieve_official(
    question: str,
    identity: FormIdentity | None = None,
    config: KBConfig | None = None,
    store: FileVectorStore | None = None,
) -> list[OfficialHit]:
    config = config or KBConfig.from_env()
    if not config.enabled:
        return []
    store = store or open_store(config.vector_db_path)
    filters = {}
    if identity and identity.authority_key and not identity.uncertain:
        filters["authority_key"] = identity.authority_key
    hits = store.query(question, top_k=max(config.top_k * 2, 8), filters=filters or None)
    if identity and identity.authority_key and not hits:
        hits = store.query(question, top_k=max(config.top_k * 2, 8))

    ranked: list[OfficialHit] = []
    for chunk, semantic in hits:
        text = sanitize_evidence(chunk.text)
        if not text:
            continue
        chunk.text = text
        score = semantic + _keyword_bonus(question, chunk) + _priority_bonus(chunk.metadata.authority_key)
        if identity and identity.form_number and chunk.metadata.form_number == identity.form_number:
            score += 0.2
        ranked.append(OfficialHit(chunk=chunk, score=score, citation=citation_from_metadata(chunk.metadata)))
    ranked.sort(key=lambda item: item.score, reverse=True)

    # Official sources must outrank Kol Zchut when both are relevant.
    official = [item for item in ranked if item.chunk.metadata.source_type == "official"]
    secondary = [item for item in ranked if item.chunk.metadata.source_type == "secondary"]
    merged = official + secondary
    filtered = [item for item in merged if item.score >= config.min_score]
    return filtered[: config.top_k]
