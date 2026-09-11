"""Vector-store abstraction with a local file backend and optional ChromaDB."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

from knowledge_base.embeddings import cosine, embed_text
from knowledge_base.models import ChunkMetadata, IndexedChunk


class VectorStore(Protocol):
    def upsert(self, chunks: list[IndexedChunk]) -> int: ...
    def query(
        self,
        text: str,
        top_k: int = 6,
        filters: dict[str, Any] | None = None,
    ) -> list[tuple[IndexedChunk, float]]: ...
    def delete_authority(self, authority_key: str) -> int: ...
    def stats(self) -> dict[str, Any]: ...
    def known_hashes(self) -> set[str]: ...


class FileVectorStore:
    """Persistent JSON vector store. Works offline without extra services."""

    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._rows: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            self._rows = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self._rows = []

    def _save(self) -> None:
        self.path.write_text(
            json.dumps(self._rows, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def upsert(self, chunks: list[IndexedChunk]) -> int:
        existing = {row["chunk_id"]: index for index, row in enumerate(self._rows)}
        added = 0
        for chunk in chunks:
            payload = {
                "chunk_id": chunk.chunk_id,
                "text": chunk.text,
                "embedding": embed_text(chunk.text),
                "metadata": chunk.metadata.model_dump(),
            }
            if chunk.chunk_id in existing:
                self._rows[existing[chunk.chunk_id]] = payload
            else:
                self._rows.append(payload)
                added += 1
        self._save()
        return added

    def query(
        self,
        text: str,
        top_k: int = 6,
        filters: dict[str, Any] | None = None,
    ) -> list[tuple[IndexedChunk, float]]:
        query_vec = embed_text(text)
        scored: list[tuple[IndexedChunk, float]] = []
        for row in self._rows:
            metadata = row["metadata"]
            if filters:
                skip = False
                for key, value in filters.items():
                    if value and metadata.get(key) != value:
                        skip = True
                        break
                if skip:
                    continue
            score = cosine(query_vec, row["embedding"])
            chunk = IndexedChunk(
                chunk_id=row["chunk_id"],
                text=row["text"],
                metadata=ChunkMetadata.model_validate(metadata),
            )
            scored.append((chunk, score))
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def delete_authority(self, authority_key: str) -> int:
        before = len(self._rows)
        self._rows = [
            row for row in self._rows if row["metadata"].get("authority_key") != authority_key
        ]
        self._save()
        return before - len(self._rows)

    def stats(self) -> dict[str, Any]:
        by_authority: dict[str, int] = {}
        documents: set[str] = set()
        for row in self._rows:
            key = row["metadata"].get("authority_key", "unknown")
            by_authority[key] = by_authority.get(key, 0) + 1
            documents.add(row["metadata"].get("document_id", ""))
        return {
            "chunks": len(self._rows),
            "documents": len(documents),
            "by_authority": by_authority,
        }

    def known_hashes(self) -> set[str]:
        return {row["metadata"].get("content_hash", "") for row in self._rows}


def open_store(vector_db_path: str) -> FileVectorStore:
    store_file = Path(vector_db_path) / "kb_vectors.json"
    return FileVectorStore(str(store_file))
