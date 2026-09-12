"""Unit tests for Israeli form input validation and privacy masking."""

from privacy import mask_sensitive
from validation import (
    validate_date,
    validate_email,
    validate_israeli_id,
    validate_phone,
    validate_required,
    validate_user_input,
)


def test_israeli_id_valid_and_invalid() -> None:
    # Known valid checksum example often used in docs: 123456782
    assert validate_israeli_id("123456782").ok
    assert not validate_israeli_id("123456789").ok
    assert not validate_israeli_id("123").ok


def test_email_phone_date_required() -> None:
    assert validate_email("user@example.com").ok
    assert not validate_email("not-an-email").ok
    assert validate_phone("052-1234567").ok
    assert validate_phone("+972521234567").ok
    assert not validate_phone("123").ok
    assert validate_date("12/03/2024").ok
    assert validate_date("1.2.24").normalized == "01/02/2024"
    assert not validate_date("32/01/2024").ok
    assert validate_required("hello", "name").ok
    assert not validate_required("  ", "name").ok


def test_validate_user_input_dispatch() -> None:
    assert validate_user_input("israeli_id", "123456782").ok
    assert validate_user_input("email", "a@b.co").ok
    assert not validate_user_input("phone", "xx").ok
    assert not validate_user_input("unsupported", "x").ok


def test_mask_sensitive_redacts_id_email_phone_and_keys() -> None:
    text = "ID 123456782 email a@b.com phone 052-1234567 key GEMINI_API_KEY=abc123"
    masked = mask_sensitive(text)
    assert "123456782" not in masked
    assert "a@b.com" not in masked
    assert "052-1234567" not in masked
    assert "abc123" not in masked
    assert "[REDACTED_ID]" in masked
    assert "[REDACTED_EMAIL]" in masked
    assert "[REDACTED_PHONE]" in masked
    assert "[REDACTED_SECRET]" in masked
