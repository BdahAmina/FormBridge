"""Local hashed embeddings so retrieval works without a paid model."""

from __future__ import annotations

import hashlib
import math

from knowledge_base.text import tokenize


EMBED_DIM = 256


def embed_text(text: str) -> list[float]:
    """Deterministic hashed TF-IDF-style embedding."""
    tokens = tokenize(text)
    vector = [0.0] * EMBED_DIM
    if not tokens:
        return vector
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    for token, count in counts.items():
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:2], "little") % EMBED_DIM
        sign = 1.0 if digest[2] % 2 == 0 else -1.0
        vector[index] += sign * (1.0 + math.log(count))
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))
