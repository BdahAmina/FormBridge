"""Allowlist ingestion from local fixtures or public HTTPS pages."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from knowledge_base.authorities import AUTHORITIES, Authority, is_allowed_url
from knowledge_base.config import KBConfig
from knowledge_base.models import AuthorityStatus, ChunkMetadata, IndexedChunk, utc_now
from knowledge_base.store import FileVectorStore, open_store
from knowledge_base.text import chunk_text, content_hash, sanitize_evidence, stable_id, strip_html


LOGGER = logging.getLogger("formbridge.kb")


def _log(config: KBConfig, event: dict) -> None:
    path = Path(config.log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    event["timestamp"] = utc_now()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def _load_status(config: KBConfig) -> dict[str, dict]:
    path = Path(config.status_path)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _save_status(config: KBConfig, status: dict[str, dict]) -> None:
    path = Path(config.status_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_fixture(config: KBConfig, authority: Authority) -> tuple[str, str]:
    fixture = Path(config.fixtures_path) / authority.fixture_file
    if not fixture.exists():
        raise FileNotFoundError(f"Missing fixture for {authority.key}: {fixture}")
    html = fixture.read_text(encoding="utf-8")
    return strip_html(html), authority.seed_urls[0]


def _fetch_live(url: str, delay: float, retries: int) -> str:
    if not is_allowed_url(url):
        raise PermissionError(f"URL is not in the allowlist: {url}")
    import urllib.request

    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            time.sleep(delay)
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "FormBridgeKnowledgeBot/1.0 (educational)"},
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace")
        except Exception as error:  # noqa: BLE001
            last_error = error
            LOGGER.warning("Fetch failed %s attempt %s: %s", url, attempt + 1, error)
    raise RuntimeError(f"Could not fetch {url}: {last_error}")


def ingest_authority(
    authority_key: str,
    config: KBConfig | None = None,
    store: FileVectorStore | None = None,
) -> AuthorityStatus:
    config = config or KBConfig.from_env()
    authority = AUTHORITIES[authority_key]
    store = store or open_store(config.vector_db_path)
    status_map = _load_status(config)
    attempt = utc_now()
    try:
        if config.ingest_mode == "live":
            html = _fetch_live(authority.seed_urls[0], config.request_delay, config.max_retries)
            text = sanitize_evidence(strip_html(html))
            source_url = authority.seed_urls[0]
        else:
            raw, source_url = _read_fixture(config, authority)
            text = sanitize_evidence(raw)

        form_number = ""
        form_name = ""
        if "1500" in text:
            form_number = "1500"
            form_name = "תביעה לדמי אבטלה"
        if "101" in text and authority.key == "tax":
            form_number = "101"
            form_name = "כרטיס עובד"

        pieces = chunk_text(text, config.chunk_size, config.chunk_overlap)
        known = store.known_hashes()
        chunks: list[IndexedChunk] = []
        document_id = stable_id(authority.key, source_url)
        for index, piece in enumerate(pieces, start=1):
            digest = content_hash(piece)
            metadata = ChunkMetadata(
                document_id=document_id,
                authority=authority.name_he,
                authority_key=authority.key,
                source_type=authority.source_type,
                document_type="form" if form_number else "page",
                form_number=form_number,
                form_name=form_name,
                category=authority.categories[0] if authority.categories else "",
                language="he",
                source_url=source_url,
                page_number=index,
                title=authority.name_he,
                content_hash=digest,
                last_checked_at=attempt,
            )
            if digest in known:
                continue
            chunks.append(
                IndexedChunk(
                    chunk_id=stable_id(document_id, digest, str(index)),
                    text=piece,
                    metadata=metadata,
                )
            )
        added = store.upsert(chunks)
        stats = store.stats()
        record = AuthorityStatus(
            authority_key=authority.key,
            enabled=authority.enabled,
            source_type=authority.source_type,
            documents=1,
            chunks=stats["by_authority"].get(authority.key, 0),
            last_success=attempt,
            last_attempt=attempt,
            last_error=None,
            status="ok",
        )
        status_map[authority.key] = record.model_dump()
        _save_status(config, status_map)
        _log(config, {"event": "ingest_ok", "authority": authority.key, "added": added})
        return record
    except Exception as error:  # noqa: BLE001
        record = AuthorityStatus(
            authority_key=authority.key,
            enabled=authority.enabled,
            source_type=authority.source_type,
            last_attempt=attempt,
            last_error=str(error),
            status="error",
        )
        current = status_map.get(authority.key, {})
        current.update(record.model_dump())
        status_map[authority.key] = current
        _save_status(config, status_map)
        _log(config, {"event": "ingest_error", "authority": authority.key, "error": str(error)})
        raise


def ingest_all(config: KBConfig | None = None) -> list[AuthorityStatus]:
    config = config or KBConfig.from_env()
    store = open_store(config.vector_db_path)
    results = []
    for key in AUTHORITIES:
        try:
            results.append(ingest_authority(key, config=config, store=store))
        except Exception as error:  # noqa: BLE001
            LOGGER.error("Ingest failed for %s: %s", key, error)
    return results


def rebuild_authority(authority_key: str, config: KBConfig | None = None) -> AuthorityStatus:
    config = config or KBConfig.from_env()
    store = open_store(config.vector_db_path)
    store.delete_authority(authority_key)
    return ingest_authority(authority_key, config=config, store=store)
