"""Analysis dashboard should behave the same in Arabic, Hebrew, and English."""

from models import NOT_MENTIONED_AR, NOT_MENTIONED_EN, NOT_MENTIONED_HE
from ui_components import (
    LANGUAGE_AR,
    LANGUAGE_EN,
    LANGUAGE_HE,
    _is_missing,
    _missing_label,
    ui,
)


def test_missing_labels_match_each_analysis_language() -> None:
    assert _missing_label("ar") == NOT_MENTIONED_AR
    assert _missing_label("he") == NOT_MENTIONED_HE
    assert _missing_label("en") == NOT_MENTIONED_EN


def test_missing_filter_accepts_all_language_placeholders() -> None:
    for phrase in (NOT_MENTIONED_AR, NOT_MENTIONED_HE, NOT_MENTIONED_EN, "n/a"):
        assert _is_missing(phrase, NOT_MENTIONED_EN)


def test_analysis_copy_exists_in_every_language() -> None:
    for language in (LANGUAGE_AR, LANGUAGE_HE, LANGUAGE_EN):
        strings = ui(language)
        assert strings["overview"]
        assert strings["form_label"]
        assert strings["analysis_title"]
        assert strings["analyze_button"]
