"""Local account and conversation-history tests."""

from ui_components import next_onboarding_step
from auth import (
    authenticate,
    change_email,
    change_password,
    delete_conversation,
    get_public_user,
    list_conversations,
    register_user,
    save_conversation,
    update_display_name,
    uses_assistant_workspace,
    validate_credentials,
)


def test_register_and_login(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("auth.ROOT", tmp_path)
    monkeypatch.setattr("auth.USERS_PATH", tmp_path / "users.json")
    monkeypatch.setenv("ADMIN_EMAILS", "admin@example.com")
    user = register_user("Ada@example.com", "secret123", "Ada")
    assert user["email"] == "ada@example.com"
    assert user["is_admin"] is False
    assert authenticate("ada@example.com", "secret123")["user_id"] == user["user_id"]
    assert authenticate("ada@example.com", "wrongpass") is None
    admin = register_user("admin@example.com", "secret123", "Admin")
    assert admin["is_admin"] is True
    assert authenticate("admin@example.com", "secret123")["is_admin"] is True
    assert uses_assistant_workspace(user) is True
    assert uses_assistant_workspace(admin) is False
    assert uses_assistant_workspace(None) is True


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


def test_profile_name_and_email_can_change(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("auth.ROOT", tmp_path)
    monkeypatch.setattr("auth.USERS_PATH", tmp_path / "users.json")
    register_user("name@example.com", "secret123", "Old")
    register_user("taken@example.com", "secret123", "Taken")
    assert update_display_name("name@example.com", "  ") == "invalid_name"
    assert update_display_name("name@example.com", "Nour") == ""
    assert get_public_user("name@example.com")["display_name"] == "Nour"
    assert change_email("name@example.com", "bad", "secret123") == "invalid_email"
    assert change_email("name@example.com", "taken@example.com", "secret123") == "exists"
    assert change_email("name@example.com", "new@example.com", "wrongpass") == "invalid"
    assert change_email("name@example.com", "new@example.com", "secret123") == ""
    assert get_public_user("name@example.com") is None
    assert get_public_user("new@example.com")["display_name"] == "Nour"
    assert authenticate("new@example.com", "secret123")


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


def test_start_flow_is_agree_then_choose_mode() -> None:
    assert next_onboarding_step(False, False) == "consent"
    assert next_onboarding_step(True, False) == "mode"
    assert next_onboarding_step(True, True) == "done"
