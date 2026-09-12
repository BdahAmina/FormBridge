"""Facade used by the Streamlit app, CLI, and evals."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from knowledge_base.authorities import AUTHORITIES
from knowledge_base.config import KBConfig
from knowledge_base.identify import FormIdentity, identify_form
from knowledge_base.ingest import ingest_all, ingest_authority, rebuild_authority
from knowledge_base.retrieve import OfficialHit, retrieve_official
from knowledge_base.store import open_store


class KnowledgeBaseService:
    def __init__(self, config: KBConfig | None = None) -> None:
        self.config = config or KBConfig.from_env()
        self.store = open_store(self.config.vector_db_path)

    def search(self, question: str, identity: FormIdentity | None = None) -> list[OfficialHit]:
        return retrieve_official(question, identity=identity, config=self.config, store=self.store)

    def identify(self, text: str, analysis_org: str = "") -> FormIdentity:
        return identify_form(text, analysis_org)

    def list_status(self) -> list[dict]:
        path = Path(self.config.status_path)
        saved = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        stats = self.store.stats()
        rows = []
        for key, authority in AUTHORITIES.items():
            row = saved.get(key, {})
            rows.append(
                {
                    "authority_key": key,
                    "authority": authority.name_he,
                    "source_type": authority.source_type,
                    "enabled": authority.enabled,
                    "chunks": stats["by_authority"].get(key, 0),
                    "documents": 1 if stats["by_authority"].get(key, 0) else 0,
                    "last_success": row.get("last_success"),
                    "last_attempt": row.get("last_attempt"),
                    "status": row.get("status", "idle"),
                    "last_error": row.get("last_error"),
                    "seed_url": authority.seed_urls[0],
                }
            )
        return rows

    def update_one(self, authority_key: str):
        return ingest_authority(authority_key, config=self.config, store=self.store)

    def update_all(self):
        return ingest_all(self.config)

    def rebuild(self, authority_key: str):
        return rebuild_authority(authority_key, self.config)

    def _sources_stale(self) -> bool:
        """True when any enabled authority is older than SOURCE_UPDATE_INTERVAL_HOURS."""
        path = Path(self.config.status_path)
        if not path.exists():
            return True
        try:
            saved = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return True
        interval_hours = max(1, int(self.config.update_interval_hours or 168))
        now = datetime.now(timezone.utc)
        for key, authority in AUTHORITIES.items():
            if not authority.enabled:
                continue
            last_success = (saved.get(key) or {}).get("last_success")
            if not last_success:
                return True
            try:
                stamp = datetime.fromisoformat(str(last_success).replace("Z", "+00:00"))
            except ValueError:
                return True
            if stamp.tzinfo is None:
                stamp = stamp.replace(tzinfo=timezone.utc)
            age_hours = (now - stamp).total_seconds() / 3600
            if age_hours >= interval_hours:
                return True
        return False

    def ensure_seeded(self) -> None:
        """Seed an empty index, or refresh when sources exceed the update interval."""
        if self.store.stats()["chunks"] == 0 or self._sources_stale():
            ingest_all(self.config)

    def ingestion_history(self, limit: int = 50) -> list[dict]:
        path = Path(self.config.log_path)
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").splitlines()[-limit:]
        rows = []
        for line in lines:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return list(reversed(rows))
