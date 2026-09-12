"""Anonymized product telemetry for the admin monitor (no private question text)."""

from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

from knowledge_base.models import utc_now
from privacy import mask_sensitive


DEFAULT_PATH = Path("data/telemetry.jsonl")


def _path() -> Path:
    return Path(os.getenv("TELEMETRY_PATH", str(DEFAULT_PATH)))


def log_event(
    *,
    event_type: str,
    success: bool,
    latency_ms: int | None = None,
    form_number: str = "",
    authority_key: str = "",
    language: str = "",
    tools_used: list[str] | None = None,
    error_class: str = "",
) -> None:
    """Append an anonymized event. Never stores raw user questions or IDs."""
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "timestamp": utc_now(),
        "event_type": event_type,
        "success": bool(success),
        "latency_ms": latency_ms,
        "form_number": form_number or "",
        "authority_key": authority_key or "",
        "language": language or "",
        "tools_used": tools_used or [],
        "error_class": mask_sensitive(error_class or "")[:120],
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def read_events(limit: int = 2000) -> list[dict[str, Any]]:
    path = _path()
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows[-limit:]


def summarize(limit: int = 2000) -> dict[str, Any]:
    events = read_events(limit)
    total = len(events)
    successes = sum(1 for item in events if item.get("success"))
    failures = total - successes
    latencies = [int(item["latency_ms"]) for item in events if isinstance(item.get("latency_ms"), int)]
    forms = Counter(item.get("form_number") or "unknown" for item in events if item.get("form_number"))
    authorities = Counter(
        item.get("authority_key") or "unknown" for item in events if item.get("authority_key")
    )
    return {
        "total_events": total,
        "successful": successes,
        "failed": failures,
        "avg_latency_ms": round(sum(latencies) / len(latencies), 1) if latencies else None,
        "top_forms": forms.most_common(8),
        "top_authorities": authorities.most_common(8),
        "by_type": Counter(item.get("event_type") or "unknown" for item in events).most_common(),
    }


def log_feedback(rating: str, *, language: str = "", form_number: str = "") -> None:
    """Store anonymized thumbs feedback only (never question text)."""
    path = Path(os.getenv("FEEDBACK_PATH", "data/feedback.jsonl"))
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": utc_now(),
        "rating": "up" if rating == "up" else "down",
        "language": language or "",
        "form_number": form_number or "",
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
