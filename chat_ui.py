"""Reusable chat rendering with per-message RTL/LTR detection."""

from __future__ import annotations

import html
import re
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from models import humanize_guided_text


_STRONG_RE = re.compile(
    r"[\u0590-\u05FF\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB1D-\uFDFF\uFE70-\uFEFF]|[A-Za-z]"
)
_RTL_RE = re.compile(
    r"[\u0590-\u05FF\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB1D-\uFDFF\uFE70-\uFEFF]"
)
_HEBREW_RE = re.compile(r"[\u0590-\u05FF\uFB1D-\uFB4F]")
_ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")
_LTR_CORE_RE = re.compile(
    r"(https?://[^\s<]+|"
    r"[\w.+-]+@[\w.-]+\.\w{2,}|"
    r"(?:₪\s*)?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:\s*%|\s*₪)?"
    r"|(?:\+?\d[\d\s().-]{6,}\d)"
    r"|(?:\d{1,2}[./-]\d{1,2}[./-]\d{2,4}))"
)
_LTR_ISLAND_RE = re.compile(
    _LTR_CORE_RE.pattern[:-1] + r"|(?:\b[A-Za-z][A-Za-z0-9._-]{1,}\b))"
)
_YOU_LABEL = {"ar": "أنت", "he": "אתה", "en": "You"}
_PLACEHOLDER_RE = re.compile(r"\ue000(\d+)\ue001")
_ENTITY_RE = re.compile(r"&(?:[a-zA-Z]+|#\d+|#x[0-9A-Fa-f]+);")


def detect_text_direction(text: str) -> str:
    """Return rtl, ltr, or auto from the first strong letter."""
    cleaned = re.sub(r"<[^>]*>", "", text or "")
    cleaned = re.sub(r"https?://\S+", "", cleaned).strip()
    cleaned = re.sub(r"[#*_>`~\-\[\]()]+", "", cleaned)
    match = _STRONG_RE.search(cleaned)
    if not match:
        return "auto"
    return "rtl" if _RTL_RE.search(match.group(0)) else "ltr"


def detect_message_language(text: str) -> str:
    """Best-effort BCP 47 tag for the first strong letter."""
    cleaned = re.sub(r"<[^>]*>", "", text or "")
    match = _STRONG_RE.search(cleaned)
    if not match:
        return "und"
    char = match.group(0)
    if _HEBREW_RE.search(char):
        return "he"
    if _ARABIC_RE.search(char):
        return "ar"
    return "en"


def isolate_ltr_islands(text: str, *, rtl: bool = True) -> str:
    """Wrap numbers, URLs, emails, and similar tokens for safe RTL embedding."""
    if not rtl:
        return text

    holes: list[str] = []

    def hide(match: re.Match[str]) -> str:
        holes.append(match.group(0))
        return "\ue002"

    def _wrap(match: re.Match[str]) -> str:
        token = match.group(0)
        return f'<bdi dir="ltr">{token}</bdi>'

    hidden = _PLACEHOLDER_RE.sub(hide, text)
    hidden = _ENTITY_RE.sub(hide, hidden)
    wrapped = _LTR_ISLAND_RE.sub(_wrap, hidden)
    hole_iter = iter(holes)
    return re.sub("\ue002", lambda _: next(hole_iter), wrapped)


def _stash_html_segments(markup: str) -> tuple[str, list[str]]:
    stored: list[str] = []

    def stash(match: re.Match[str]) -> str:
        stored.append(match.group(0))
        return f"\ue000{len(stored) - 1}\ue001"

    protected = re.sub(
        r"<(pre|code|a|bdi)\b[^>]*>[\s\S]*?</\1>",
        stash,
        markup,
        flags=re.I,
    )
    protected = re.sub(r"<[^>]+>", stash, protected)
    return protected, stored


def _restore_html_segments(markup: str, stored: list[str]) -> str:
    return _PLACEHOLDER_RE.sub(lambda match: stored[int(match.group(1))], markup)


def _inline_markdown(escaped: str) -> str:
    escaped = re.sub(
        r"`([^`]+)`",
        lambda match: f'<code dir="ltr">{match.group(1)}</code>',
        escaped,
    )
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
        lambda match: (
            f'<a href="{match.group(2)}" target="_blank" rel="noopener noreferrer" '
            f'dir="ltr">{match.group(1)}</a>'
        ),
        escaped,
    )
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", escaped)
    return escaped


def markdown_to_chat_html(text: str) -> str:
    """Convert a safe Markdown subset to HTML, then isolate LTR islands."""
    source = (text or "").replace("\r\n", "\n").strip()
    if not source:
        return ""

    parts = re.split(r"(```[\s\S]*?```)", source)
    chunks: list[str] = []
    for part in parts:
        if part.startswith("```") and part.endswith("```"):
            body = part[3:-3]
            if "\n" in body:
                _lang, _, code = body.partition("\n")
            else:
                code = body
            chunks.append(
                f'<pre dir="ltr"><code dir="ltr">{html.escape(code.strip())}</code></pre>'
            )
            continue

        escaped = html.escape(part)
        blocks = escaped.split("\n")
        html_blocks: list[str] = []
        list_items: list[str] = []
        list_type = ""

        def flush_list() -> None:
            nonlocal list_items, list_type
            if not list_items:
                return
            tag = "ol" if list_type == "ol" else "ul"
            html_blocks.append(
                f"<{tag}>" + "".join(f"<li>{item}</li>" for item in list_items) + f"</{tag}>"
            )
            list_items = []
            list_type = ""

        paragraph: list[str] = []

        def flush_paragraph() -> None:
            nonlocal paragraph
            if paragraph:
                html_blocks.append(f"<p>{'<br>'.join(paragraph)}</p>")
                paragraph = []

        for line in blocks:
            stripped = line.strip()
            if not stripped:
                flush_list()
                flush_paragraph()
                continue
            numbered = re.match(r"^(\d+)\.\s+(.*)$", stripped)
            bullet = re.match(r"^[-*•]\s+(.*)$", stripped)
            if numbered:
                flush_paragraph()
                if list_type != "ol":
                    flush_list()
                    list_type = "ol"
                list_items.append(_inline_markdown(numbered.group(2)))
                continue
            if bullet:
                flush_paragraph()
                if list_type != "ul":
                    flush_list()
                    list_type = "ul"
                list_items.append(_inline_markdown(bullet.group(1)))
                continue
            flush_list()
            paragraph.append(_inline_markdown(stripped))

        flush_list()
        flush_paragraph()
        chunks.append("".join(html_blocks))

    markup = "".join(chunks)
    protected, stored = _stash_html_segments(markup)
    if detect_text_direction(source) != "ltr":
        protected = isolate_ltr_islands(protected, rtl=True)
    return _restore_html_segments(protected, stored)


def _citation_html(citations: list[dict[str, Any]] | None, strings: dict[str, Any]) -> str:
    if not citations:
        return ""
    items: list[str] = []
    for item in citations:
        url = html.escape(str(item.get("source_url") or ""), quote=True)
        title = html.escape(str(item.get("title") or item.get("authority") or url))
        authority = html.escape(str(item.get("authority") or ""))
        if not url:
            continue
        items.append(
            f'<li class="fb-chat-cite-item">'
            f'<span class="fb-chat-cite-authority">{authority}</span> '
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" dir="ltr">{title}</a>'
            f"</li>"
        )
    if not items:
        return ""
    label = html.escape(str(strings.get("official_sources", "Sources")))
    return (
        f'<aside class="fb-chat-cites" aria-label="{label}">'
        f'<p class="fb-chat-cites-title">{label}</p><ul>{"".join(items)}</ul></aside>'
    )


def _avatar_svg() -> str:
    return (
        '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">'
        '<path fill="currentColor" d="M12 3 4.5 7v5.5c0 4.4 3.2 8.5 7.5 9.5 4.3-1 7.5-5.1 7.5-9.5V7L12 3zm0 3.1 5.5 2.9v3.5c0 3.2-2.3 6.3-5.5 7.2-3.2-.9-5.5-4-5.5-7.2V9L12 6.1z"/>'
        "</svg>"
    )


def build_message_html(
    content: str,
    role: str,
    *,
    strings: dict[str, Any],
    citations: list[dict[str, Any]] | None = None,
    show_assistant_name: bool = False,
    ui_language: str = "ar",
) -> str:
    """Build one accessible chat row with its own text direction."""
    text = normalize_chat_response(content, ui_language)
    direction = detect_text_direction(text)
    language = detect_message_language(text)
    body = markdown_to_chat_html(text)
    role_name = "assistant" if role == "assistant" else "user"
    label = (
        html.escape(str(strings.get("chat_agent_name", "FormBridge")))
        if role_name == "assistant"
        else _YOU_LABEL.get(ui_language, "You")
    )
    meta = ""
    avatar = ""
    if role_name == "assistant":
        avatar = f'<div class="fb-chat-avatar" aria-hidden="true">{_avatar_svg()}</div>'
        if show_assistant_name:
            meta = (
                f'<p class="fb-chat-name">{html.escape(str(strings.get("chat_agent_name", "FormBridge")))}'
                f'<span class="fb-chat-name-sub">AI</span></p>'
            )
    cites = _citation_html(citations, strings) if role_name == "assistant" else ""
    return (
        f'<article class="fb-chat-message fb-chat-message--{role_name}" '
        f'aria-label="{label}">'
        f"{avatar}"
        f'<div class="fb-chat-bubble fb-chat-bubble--{role_name}">'
        f"{meta}"
        f'<div class="message-content message-content--{direction}" '
        f'dir="{direction}" lang="{language}">{body}</div>'
        f"{cites}"
        f"</div></article>"
    )


def normalize_chat_response(text: str, language: str = "ar") -> str:
    """Light cleanup so assistant answers render consistently."""
    cleaned = html.unescape((text or "").strip().replace("\r\n", "\n"))
    while "\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n", "\n\n")
    if cleaned.startswith("{") or cleaned.startswith("```"):
        cleaned = humanize_guided_text(cleaned, language)
        cleaned = html.unescape(cleaned)
    return cleaned


def _ui_language_code(selected_language: str) -> str:
    if selected_language == "English":
        return "en"
    if selected_language in {"עברית פשוטה", "עברית"}:
        return "he"
    return "ar"


def render_conversation(
    messages: list[dict[str, Any]],
    selected_language: str,
    *,
    empty_text: str | None = None,
    strings: dict[str, Any] | None = None,
) -> None:
    """Render the full conversation as one continuous thread."""
    strings = strings or {"chat_agent_name": "FormBridge", "official_sources": "Sources"}
    code = _ui_language_code(selected_language)
    if not messages:
        if empty_text:
            st.markdown(
                f'<div class="fb-chat-empty" dir="auto">{html.escape(empty_text)}</div>',
                unsafe_allow_html=True,
            )
        return

    rows: list[str] = []
    named_assistant = False
    for message in messages:
        role = "assistant" if message.get("role") == "assistant" else "user"
        show_name = role == "assistant" and not named_assistant
        if show_name:
            named_assistant = True
        rows.append(
            build_message_html(
                str(message.get("content") or ""),
                role,
                strings=strings,
                citations=message.get("citations"),
                show_assistant_name=show_name,
                ui_language=code,
            )
        )

    st.markdown(
        f'<div class="fb-chat-thread" role="log" aria-live="polite" aria-relevant="additions">'
        f"{''.join(rows)}"
        f"</div>",
        unsafe_allow_html=True,
    )
    components.html(
        """
        <script>
        const doc = window.parent.document;
        const last = doc.querySelector(".fb-chat-message:last-of-type");
        if (last) {
          last.scrollIntoView({ behavior: "smooth", block: "end" });
        }
        </script>
        """,
        height=0,
    )


def render_chat_bubble(
    content: str,
    role: str,
    selected_language: str,
    citations: list[dict[str, Any]] | None = None,
) -> None:
    """Back-compatible single-message renderer used by existing call sites."""
    render_conversation(
        [{"role": role, "content": content, "citations": citations}],
        selected_language,
    )
