"""RAG: split an uploaded document into a knowledge base and retrieve relevant passages."""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass


CHUNK_SIZE = 450
CHUNK_OVERLAP = 90
TOP_K = 4
MIN_SCORE = 0.04

_TOKEN_RE = re.compile(r"[\w\u0590-\u05FF\u0600-\u06FF]+", re.UNICODE)

# Cross-language aliases so Arabic questions can retrieve Hebrew passages.
TERM_ALIASES: dict[str, list[str]] = {
    "מועד": ["موعد", "deadline", "תאריך"],
    "אחרון": ["نهائي", "اخير"],
    "תשלום": ["دفع", "لשلم", "סכום", "ادفع"],
    "לשלם": ["ادفع", "دفع", "أسدد"],
    "סכום": ["مبلغ", "كم", "כמה"],
    "מסמך": ["مستند", "وثيقة"],
    "מסמכים": ["مستندات", "وثائق"],
    "תעודת": ["هوية", "هوية"],
    "זהות": ["هوية"],
    "נשלח": ["أرسل", "ارسل", "שלח", "נשלחה"],
    "שלח": ["נשלח", "נשלחה", "أرسل"],
    "נשלחה": ["נשלח", "שלח"],
    "למי": ["לכבוד"],
    "מי": ["עירייה", "עיריית"],
    "לכבוד": ["لمن", "المستلم"],
    "עירייה": ["بلدية"],
    "חוב": ["دين", "مستحق"],
    "موعد": ["מועד", "תאריך"],
    "نهائي": ["אחרון"],
    "دفع": ["תשלום", "לשלם"],
    "مبلغ": ["סכום"],
    "مستند": ["מסמך"],
    "وثائق": ["מסמכים"],
    "هوية": ["זהות", "תעודת"],
    "لمن": ["לכבוד", "נמען"],
    "من": ["מי"],
    "كم": ["כמה", "סכום"],
    "أرسل": ["נשלח"],
}


@dataclass
class RetrievedPassage:
    chunk_id: int
    text: str
    score: float


def tokenize(text: str) -> list[str]:
    """Split Hebrew, Arabic, and English text into lowercase tokens."""
    return [token.lower() for token in _TOKEN_RE.findall(text or "")]


def expand_query_tokens(tokens: list[str]) -> list[str]:
    """Add Hebrew/Arabic aliases so mixed-language questions still retrieve."""
    expanded = list(tokens)
    for token in tokens:
        for alias in TERM_ALIASES.get(token, []):
            expanded.append(alias.lower())
    return expanded


def chunk_document(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split document text into overlapping passages."""
    cleaned = re.sub(r"\n{3,}", "\n\n", (text or "").strip())
    if not cleaned:
        return []

    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", cleaned) if part.strip()]
    pieces: list[str] = []
    for paragraph in paragraphs:
        if len(paragraph) <= chunk_size:
            pieces.append(paragraph)
            continue
        start = 0
        while start < len(paragraph):
            pieces.append(paragraph[start : start + chunk_size].strip())
            start += max(chunk_size - overlap, 1)

    merged: list[str] = []
    buffer = ""
    for piece in pieces:
        if not buffer:
            buffer = piece
        elif len(buffer) + 1 + len(piece) <= chunk_size:
            buffer = f"{buffer}\n{piece}"
        else:
            merged.append(buffer)
            buffer = piece
    if buffer:
        merged.append(buffer)
    return merged


def build_knowledge_base(document_text: str) -> dict:
    """Build a lightweight in-memory knowledge base from one document."""
    chunks = chunk_document(document_text)
    tokenized = [tokenize(chunk) for chunk in chunks]
    document_frequency: dict[str, int] = {}
    for tokens in tokenized:
        for token in set(tokens):
            document_frequency[token] = document_frequency.get(token, 0) + 1

    return {
        "chunks": chunks,
        "tokenized": tokenized,
        "document_frequency": document_frequency,
        "chunk_count": len(chunks),
    }


def _idf(token: str, document_frequency: dict[str, int], chunk_count: int) -> float:
    df = document_frequency.get(token, 0)
    return math.log((chunk_count + 1) / (df + 1)) + 1.0


def _score_chunk(
    query_tokens: list[str],
    chunk_tokens: list[str],
    document_frequency: dict[str, int],
    chunk_count: int,
) -> float:
    if not query_tokens or not chunk_tokens:
        return 0.0

    chunk_tf: dict[str, int] = {}
    for token in chunk_tokens:
        chunk_tf[token] = chunk_tf.get(token, 0) + 1

    score = 0.0
    for token in query_tokens:
        tf = chunk_tf.get(token, 0)
        if tf == 0:
            continue
        score += (1.0 + math.log(tf)) * _idf(token, document_frequency, chunk_count)
        if token.isdigit() or any(char.isdigit() for char in token):
            score += 1.2

    query_set = set(query_tokens)
    chunk_set = set(chunk_tokens)
    overlap = len(query_set & chunk_set)
    if query_set:
        score += 0.35 * (overlap / len(query_set))
    return score


def retrieve_passages(
    knowledge_base: dict | None,
    question: str,
    *,
    top_k: int = TOP_K,
) -> list[RetrievedPassage]:
    """Return the most relevant document passages for a user question."""
    if not knowledge_base or not knowledge_base.get("chunks"):
        return []

    query_tokens = expand_query_tokens(tokenize(question))
    if not query_tokens:
        return []

    scored: list[RetrievedPassage] = []
    chunks: list[str] = knowledge_base["chunks"]
    tokenized: list[list[str]] = knowledge_base["tokenized"]
    document_frequency: dict[str, int] = knowledge_base["document_frequency"]
    chunk_count = int(knowledge_base.get("chunk_count") or len(chunks))

    for index, chunk in enumerate(chunks):
        score = _score_chunk(query_tokens, tokenized[index], document_frequency, chunk_count)
        if score >= MIN_SCORE:
            scored.append(RetrievedPassage(chunk_id=index, text=chunk, score=round(score, 4)))

    scored.sort(key=lambda item: item.score, reverse=True)
    return scored[:top_k]


def format_retrieved_context(passages: list[RetrievedPassage]) -> str:
    """Turn retrieved passages into prompt context."""
    if not passages:
        return "No sufficiently relevant passage was retrieved from the document."

    blocks = []
    for index, passage in enumerate(passages, start=1):
        blocks.append(f"[Passage {index} | score {passage.score}]\n{passage.text}")
    return "\n\n".join(blocks)


def passages_to_dicts(passages: list[RetrievedPassage]) -> list[dict]:
    return [asdict(passage) for passage in passages]
