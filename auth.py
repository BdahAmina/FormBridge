"""Local user accounts with hashed passwords and private conversation history."""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import secrets
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

from privacy import mask_sensitive


ROOT = Path(__file__).resolve().parent / "data" / "accounts"
USERS_PATH = ROOT / "users.json"
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _read_users() -> dict[str, Any]:
    if not USERS_PATH.exists():
        return {}
    try:
        return json.loads(USERS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _write_users(users: dict[str, Any]) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    USERS_PATH.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")


def _hash_password(password: str, salt: str) -> str:
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        210_000,
    )
    return derived.hex()


def _user_dir(user_id: str) -> Path:
    path = ROOT / user_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def validate_credentials(email: str, password: str) -> str:
    if not EMAIL_RE.match(normalize_email(email)):
        return "invalid_email"
    if len(password or "") < 8:
        return "weak_password"
    return ""


def register_user(email: str, password: str, display_name: str = "") -> dict[str, Any]:
    error = validate_credentials(email, password)
    if error:
        raise ValueError(error)
    users = _read_users()
    key = normalize_email(email)
    if key in users:
        raise ValueError("exists")
    salt = secrets.token_hex(16)
    user_id = uuid4().hex
    users[key] = {
        "user_id": user_id,
        "email": key,
        "display_name": (display_name or key.split("@")[0]).strip()[:80],
        "password_salt": salt,
        "password_hash": _hash_password(password, salt),
        "created_at": _now(),
    }
    _write_users(users)
    return public_user(users[key])


def authenticate(email: str, password: str) -> dict[str, Any] | None:
    users = _read_users()
    record = users.get(normalize_email(email))
    if not record:
        return None
    expected = record.get("password_hash", "")
    actual = _hash_password(password or "", record.get("password_salt", ""))
    if not expected or not hmac.compare_digest(expected, actual):
        return None
    return public_user(record)


def change_password(email: str, current_password: str, new_password: str) -> str:
    """Change a password from the signed-in website. Returns an error code or empty."""
    if len(new_password or "") < 8:
        return "weak_password"
    if not authenticate(email, current_password):
        return "invalid"
    users = _read_users()
    key = normalize_email(email)
    record = users.get(key)
    if not record:
        return "invalid"
    salt = secrets.token_hex(16)
    record["password_salt"] = salt
    record["password_hash"] = _hash_password(new_password, salt)
    record.pop("reset_token_hash", None)
    record.pop("reset_expires_at", None)
    users[key] = record
    _write_users(users)
    return ""


def public_user(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "user_id": record["user_id"],
        "email": record["email"],
        "display_name": record.get("display_name") or record["email"].split("@")[0],
    }


def _history_path(user_id: str) -> Path:
    return _user_dir(user_id) / "conversations.json"


def list_conversations(user_id: str) -> list[dict[str, Any]]:
    path = _history_path(user_id)
    if not path.exists():
        return []
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return sorted(rows, key=lambda item: item.get("updated_at") or "", reverse=True)


def save_conversation(user_id: str, conversation: dict[str, Any]) -> dict[str, Any]:
    rows = list_conversations(user_id)
    payload = {
        "id": conversation.get("id") or uuid4().hex,
        "mode": conversation.get("mode") or "guided",
        "title": mask_sensitive(str(conversation.get("title") or "Conversation"))[:80],
        "updated_at": _now(),
        "guided_history": [
            {**item, "content": mask_sensitive(str(item.get("content") or ""))}
            for item in (conversation.get("guided_history") or [])
        ],
        "chat_history": [
            {**item, "content": mask_sensitive(str(item.get("content") or ""))}
            for item in (conversation.get("chat_history") or [])
        ],
    }
    replaced = False
    for index, row in enumerate(rows):
        if row.get("id") == payload["id"]:
            rows[index] = payload
            replaced = True
            break
    if not replaced:
        rows.append(payload)
    _history_path(user_id).write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload


def delete_conversation(user_id: str, conversation_id: str) -> None:
    rows = [row for row in list_conversations(user_id) if row.get("id") != conversation_id]
    _history_path(user_id).write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_conversation(user_id: str, conversation_id: str) -> dict[str, Any] | None:
    for row in list_conversations(user_id):
        if row.get("id") == conversation_id:
            return row
    return None
