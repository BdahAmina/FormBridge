"""Local account and conversation-history tests."""

from auth import (
    authenticate,
    change_password,
    delete_conversation,
    list_conversations,
    register_user,
    save_conversation,
    validate_credentials,
)


def test_register_and_login(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("auth.ROOT", tmp_path)
    monkeypatch.setattr("auth.USERS_PATH", tmp_path / "users.json")
    user = register_user("Ada@example.com", "secret123", "Ada")
    assert user["email"] == "ada@example.com"
    assert authenticate("ada@example.com", "secret123")["user_id"] == user["user_id"]
    assert authenticate("ada@example.com", "wrongpass") is None


def test_rejects_weak_or_duplicate_accounts(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("auth.ROOT", tmp_path)
    monkeypatch.setattr("auth.USERS_PATH", tmp_path / "users.json")
    assert validate_credentials("bad", "secret123") == "invalid_email"
    assert validate_credentials("a@b.co", "short") == "weak_password"
    register_user("user@example.com", "secret123")
    try:
        register_user("user@example.com", "secret123")
        raise AssertionError("duplicate email should fail")
    except ValueError as error:
        assert str(error) == "exists"


def test_password_can_change_from_the_website(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("auth.ROOT", tmp_path)
    monkeypatch.setattr("auth.USERS_PATH", tmp_path / "users.json")
    register_user("reset@example.com", "oldpass12")
    assert change_password("reset@example.com", "wrongpass", "newpass99") == "invalid"
    assert change_password("reset@example.com", "oldpass12", "short") == "weak_password"
    assert change_password("reset@example.com", "oldpass12", "newpass99") == ""
    assert authenticate("reset@example.com", "newpass99")
    assert authenticate("reset@example.com", "oldpass12") is None


def test_conversation_history_masks_sensitive_values(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("auth.ROOT", tmp_path)
    monkeypatch.setattr("auth.USERS_PATH", tmp_path / "users.json")
    user = register_user("hist@example.com", "secret123")
    saved = save_conversation(
        user["user_id"],
        {
            "mode": "guided",
            "title": "ID 123456782 email a@b.com",
            "guided_history": [{"role": "user", "content": "call 052-1234567"}],
        },
    )
    assert "123456782" not in saved["title"]
    assert "052-1234567" not in saved["guided_history"][0]["content"]
    assert list_conversations(user["user_id"])
    delete_conversation(user["user_id"], saved["id"])
    assert list_conversations(user["user_id"]) == []
