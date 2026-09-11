"""Environment-driven knowledge-base settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

ROOT = Path(__file__).resolve().parent.parent


def _bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class KBConfig:
    enabled: bool = True
    vector_db_path: str = str(ROOT / "data" / "chroma")
    status_path: str = str(ROOT / "data" / "kb_status.json")
    log_path: str = str(ROOT / "data" / "ingestion_log.jsonl")
    fixtures_path: str = str(ROOT / "knowledge_base" / "fixtures")
    top_k: int = 6
    min_score: float = 0.18
    chunk_size: int = 700
    chunk_overlap: int = 120
    request_delay: float = 1.0
    max_retries: int = 3
    update_interval_hours: int = 168
    ingest_mode: str = "fixtures"
    admin_password: str = ""
    embedding_backend: str = "local"

    @classmethod
    def from_env(cls) -> "KBConfig":
        return cls(
            enabled=_bool("KNOWLEDGE_BASE_ENABLED", True),
            vector_db_path=os.getenv("VECTOR_DB_PATH", str(ROOT / "data" / "chroma")),
            status_path=os.getenv("KB_STATUS_PATH", str(ROOT / "data" / "kb_status.json")),
            log_path=os.getenv("KB_LOG_PATH", str(ROOT / "data" / "ingestion_log.jsonl")),
            fixtures_path=os.getenv(
                "KB_FIXTURES_PATH",
                str(ROOT / "knowledge_base" / "fixtures"),
            ),
            top_k=_int("RAG_TOP_K", 6),
            min_score=_float("RAG_MIN_RELEVANCE_SCORE", 0.18),
            chunk_size=_int("RAG_CHUNK_SIZE", 700),
            chunk_overlap=_int("RAG_CHUNK_OVERLAP", 120),
            request_delay=_float("INGESTION_REQUEST_DELAY_SECONDS", 1),
            max_retries=_int("INGESTION_MAX_RETRIES", 3),
            update_interval_hours=_int("SOURCE_UPDATE_INTERVAL_HOURS", 168),
            ingest_mode=os.getenv("KB_INGEST_MODE", "fixtures").strip().lower(),
            admin_password=os.getenv("KB_ADMIN_PASSWORD", ""),
            embedding_backend=os.getenv("KB_EMBEDDING_BACKEND", "local").strip().lower(),
        )


PROMPT_VERSION = "official-rag-v1"
CHUNKING_VERSION = "chunk-700-120-v1"
DATASET_VERSION = "formbridge_eval_v1"
RUBRIC_VERSION = "eval-rubric-v1"
