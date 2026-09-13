"""Direction detection, mixed-script wrapping, and chat HTML rendering."""

from chat_ui import (
    build_message_html,
    detect_message_language,
    detect_text_direction,
    isolate_ltr_islands,
    markdown_to_chat_html,
    normalize_chat_response,
)


STRINGS = {"chat_agent_name": "FormBridge", "official_sources": "Sources"}


def test_detects_arabic_hebrew_and_english_direction() -> None:
    assert detect_text_direction("كيف أطلب دمي أبطالة؟") == "rtl"
    assert detect_message_language("كيف أطلب دمي أبطالة؟") == "ar"
    assert detect_text_direction("איך מגישים בקשה לדמי אבטלה?") == "rtl"
    assert detect_message_language("איך מגישים בקשה לדמי אבטלה?") == "he"
    assert detect_text_direction("How do I apply for unemployment?") == "ltr"
    assert detect_message_language("How do I apply for unemployment?") == "en"


def test_ignores_numbers_punctuation_and_markdown_when_detecting() -> None:
    assert detect_text_direction("60% من الراتب السابق") == "rtl"
    assert detect_text_direction("**70%** מהשכר") == "rtl"
    assert detect_text_direction("4,000 ILS per month") == "ltr"
    assert detect_text_direction("12345 !!!") == "auto"


def test_arabic_mixed_numbers_and_prices_stay_ltr_islands() -> None:
    text = "يمكن الحصول على مبلغ بين 60% و 70%، حتى حوالي 4,000 شيكل."
    html = isolate_ltr_islands(text)
    assert '<bdi dir="ltr">60%</bdi>' in html
    assert '<bdi dir="ltr">70%</bdi>' in html
    assert '<bdi dir="ltr">4,000</bdi>' in html
    assert detect_text_direction(text) == "rtl"


def test_hebrew_urls_and_english_terms_are_isolated() -> None:
    text = "בדקו את האתר הרשמי https://www.gov.il/he/service ואת טופס PDF."
    html = isolate_ltr_islands(text)
    assert '<bdi dir="ltr">https://www.gov.il/he/service</bdi>' in html
    assert '<bdi dir="ltr">PDF</bdi>' in html
    assert detect_text_direction(text) == "rtl"


def test_markdown_keeps_lists_links_and_ltr_code() -> None:
    rendered = markdown_to_chat_html(
        "خطوات:\n\n"
        "1. افتح الموقع\n"
        "2. عبّئ التفاصيل\n\n"
        "- رابط: [Gov](https://www.gov.il)\n\n"
        "```\nprint('form')\n```"
    )
    assert "<ol>" in rendered and "<li>" in rendered
    assert "<ul>" in rendered
    assert 'dir="ltr">Gov</a>' in rendered
    assert '<pre dir="ltr"><code dir="ltr">' in rendered
    assert "print(&#x27;form&#x27;)" in rendered or "print('form')" in rendered


def test_conversation_order_and_per_message_direction() -> None:
    user_ar = build_message_html(
        "كيف أطلب دمي أبطالة؟",
        "user",
        strings=STRINGS,
        ui_language="ar",
    )
    assistant_ar = build_message_html(
        "نعم، يمكن الحصول على مبلغ بين 60% و 70%.",
        "assistant",
        strings=STRINGS,
        show_assistant_name=True,
        ui_language="ar",
    )
    user_en = build_message_html(
        "What documents do I need?",
        "user",
        strings=STRINGS,
        ui_language="en",
    )
    assert 'fb-chat-message--user' in user_ar
    assert 'fb-chat-message--assistant' in assistant_ar
    assert 'message-content--rtl' in user_ar
    assert 'dir="rtl"' in user_ar
    assert 'lang="ar"' in user_ar
    assert 'message-content--ltr' in user_en
    assert 'dir="ltr"' in user_en
    assert "FormBridge" in assistant_ar
    assert "fb-chat-name" in assistant_ar
    second_assistant = build_message_html(
        "איך ממשיכים?",
        "assistant",
        strings=STRINGS,
        show_assistant_name=False,
        ui_language="he",
    )
    assert "fb-chat-name" not in second_assistant
    assert 'lang="he"' in second_assistant


def test_long_answer_preserves_paragraphs_and_does_not_escape_structure() -> None:
    text = (
        "هذه فقرة أولى.\n\n"
        "وهذه فقرة ثانية مع قائمة:\n"
        "- بند واحد\n"
        "- بند اثنان\n\n"
        "Use `dir=auto` only as fallback."
    )
    rendered = markdown_to_chat_html(text)
    assert rendered.count("<p>") >= 2
    assert "<ul>" in rendered
    assert '<code dir="ltr">' in rendered


def test_english_messages_do_not_wrap_every_latin_word() -> None:
    rendered = markdown_to_chat_html("How do I apply for unemployment benefits?")
    assert "<bdi" not in rendered
    assert "unemployment benefits" in rendered


def test_arabic_quotes_are_not_broken_into_quot_entities() -> None:
    text = 'يمكنك تغيير عنوانك عبر خدمة "שינוי כתובת" على موقع رשות האוכלוסין.'
    rendered = markdown_to_chat_html(text)
    assert '<bdi dir="ltr">quot</bdi>' not in rendered
    assert "&quot;" in rendered
    assert "שינוי כתובת" in rendered


def test_normalize_unescapes_quoted_html_entities() -> None:
    cleaned = normalize_chat_response(
        "خدمة &quot;שינוי כתובת&quot; على الموقع",
        "ar",
    )
    assert "&quot;" not in cleaned
    assert '"שינוי כתובת"' in cleaned


def test_document_followup_omits_payments_unless_asked() -> None:
    from agent import _compact_analysis_for_question
    from models import DocumentAnalysis

    analysis = DocumentAnalysis(
        summary="رسالة من التأمين الوطني",
        actions_required=["تقديم اعتراض خلال 30 يوماً"],
        amounts_and_payments=["يجب دفع 400 شيكل"],
    )
    compact = _compact_analysis_for_question(analysis, "ماذا يجب أن أفعل؟")
    assert "400" not in compact
    assert "تقديم اعتراض" in compact
    asked = _compact_analysis_for_question(analysis, "كم يجب أن أدفع؟")
    assert "400" in asked


def test_guided_details_skip_empty_and_placeholder_cards() -> None:
    from models import GuidedGuidance
    from ui_components import _guidance_has_sidebar_details, _visible_guided_value

    assert _visible_guided_value("—") == ""
    assert _visible_guided_value("שינוי כתובת") == "שינוי כתובת"
    empty = GuidedGuidance(status="ready", assistant_message="hello")
    assert not _guidance_has_sidebar_details(empty)
    filled = GuidedGuidance(
        status="ready",
        assistant_message="hello",
        identified_service="שינוי כתובת",
        authority="רשות האוכלוסין",
    )
    assert _guidance_has_sidebar_details(filled)


def test_normalize_chat_response_humanizes_json_blobs() -> None:
    cleaned = normalize_chat_response('{"assistant_message": "Hello"}', "en")
    assert "{" not in cleaned
    assert "Hello" in cleaned
