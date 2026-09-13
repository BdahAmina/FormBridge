"""FormBridge — AI assistant for understanding official Hebrew documents."""

from __future__ import annotations


import hashlib
import html
import time
import traceback
from pathlib import Path

import streamlit as st
from dotenv import dotenv_values

from knowledge_base.identify import identify_form
from models import DocumentAnalysis, humanize_guided_text, parse_guided_response
from rag import build_knowledge_base, passages_to_dicts
from pdf_reader import (
    ExtractionResult,
    OCRLanguageMissingError,
    OCRNotAvailableError,
    PDFCorruptedError,
    PDFEmptyError,
    PDFPasswordError,
    PDFProcessingError,
    extract_text_from_pdf,
)
from telemetry import log_event, log_feedback
from chat_ui import render_conversation
from ui_components import (
    LANGUAGE_AR,
    LANGUAGE_EN,
    LANGUAGE_HE,
    current_user_is_admin,
    errors,
    inject_global_css,
    lang_code,
    render_account_sidebar,
    render_analysis_dashboard,
    render_auth_panel,
    render_download_buttons,
    render_empty_state,
    render_field_validator,
    render_footer,
    render_guided_result,
    render_header,
    render_landing,
    next_onboarding_step,
    apply_home_navigation,
    render_language_switcher,
    render_sidebar_nav,
    render_start_windows,
    ui,
)


MAX_UPLOAD_MB = 10


def _guard_streamlit_closed_event_loop() -> None:
    """Drop ScriptRunner events after Streamlit has already closed its loop."""
    try:
        from streamlit.runtime.app_session import AppSession
    except Exception:
        return
    if getattr(AppSession, "_formbridge_closed_loop_guard", False):
        return

    original = AppSession._on_scriptrunner_event

    def _safe_on_scriptrunner_event(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        loop = getattr(self, "_event_loop", None)
        if loop is None or loop.is_closed():
            return
        try:
            return original(self, *args, **kwargs)
        except RuntimeError as error:
            if "Event loop is closed" in str(error):
                return
            raise

    AppSession._on_scriptrunner_event = _safe_on_scriptrunner_event
    setattr(AppSession, "_formbridge_closed_loop_guard", True)


_guard_streamlit_closed_event_loop()


def _init_session_state() -> None:
    defaults = {
        "document_text": None,
        "analysis": None,
        "analysis_language": None,
        "uploaded_file_id": None,
        "chat_history": [],
        "user_style_notes": [],
        "knowledge_base": None,
        "last_rag_passages": [],
        "form_identity": None,
        "last_error": None,
        "extraction_meta": None,
        "app_mode": "guided",
        "guided_history": [],
        "guided_result": None,
        "guided_pending": None,
        "guided_tools_used": [],
        "last_guided_citations": [],
        "privacy_consent": False,
        "fb_mode_chosen": False,
        "fb_user": None,
        "fb_guest": False,
        "conversation_id": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _file_identity(uploaded_file) -> str:
    content = uploaded_file.getvalue()
    digest = hashlib.sha256(content).hexdigest()
    return f"{uploaded_file.name}:{len(content)}:{digest}"


def _reset_workspace() -> None:
    st.session_state.guided_history = []
    st.session_state.guided_result = None
    st.session_state.guided_tools_used = []
    st.session_state.last_guided_citations = []
    st.session_state.conversation_id = None
    st.session_state.pop("guided_pending", None)
    _reset_analysis_state()


def _persist_current_conversation() -> None:
    user = st.session_state.get("fb_user")
    if not user:
        return
    history = st.session_state.guided_history or st.session_state.chat_history
    title = next(
        (item.get("content") for item in history if item.get("role") == "user"),
        "",
    )
    if not title:
        return
    from auth import save_conversation

    saved = save_conversation(
        user["user_id"],
        {
            "id": st.session_state.get("conversation_id"),
            "mode": st.session_state.get("app_mode") or "guided",
            "title": title,
            "guided_history": st.session_state.guided_history,
            "chat_history": st.session_state.chat_history,
        },
    )
    st.session_state.conversation_id = saved["id"]


def _apply_account_actions() -> None:
    if st.session_state.pop("_fb_new_chat", None):
        _reset_workspace()
    conversation_id = st.session_state.pop("_fb_load_chat", None)
    user = st.session_state.get("fb_user")
    if conversation_id and user:
        from auth import load_conversation

        row = load_conversation(user["user_id"], conversation_id)
        if row:
            st.session_state.conversation_id = row["id"]
            st.session_state.guided_history = row.get("guided_history") or []
            st.session_state.chat_history = row.get("chat_history") or []
            st.session_state.app_mode = row.get("mode") or "guided"
            st.session_state.fb_mode_chosen = True


def _reset_analysis_state() -> None:
    st.session_state.document_text = None
    st.session_state.analysis = None
    st.session_state.analysis_language = None
    st.session_state.chat_history = []
    st.session_state.user_style_notes = []
    st.session_state.knowledge_base = None
    st.session_state.last_rag_passages = []
    st.session_state.form_identity = None
    st.session_state.extraction_meta = None
    st.session_state.last_error = None
    st.session_state.pop("debug_error", None)


def _active_provider() -> str:
    values = dotenv_values(Path(__file__).resolve().parent / ".env")
    choice = (values.get("LLM_PROVIDER") or "auto").strip().lower() or "auto"
    groq_key = (values.get("GROQ_API_KEY") or "").strip()
    gemini_key = (
        values.get("GEMINI_API_KEY") or values.get("GOOGLE_API_KEY") or ""
    ).strip()
    placeholders = {"your_api_key_here", "YOUR_API_KEY"}
    if choice == "groq":
        return "groq"
    if choice in {"gemini", "google"}:
        return "gemini"
    if gemini_key and gemini_key not in placeholders:
        return "gemini"
    if groq_key and groq_key not in placeholders:
        return "groq"
    return choice


def _map_exception_to_message(error: Exception, selected_language: str) -> str:
    err = errors(selected_language)
    text = f"{error}".lower()
    provider = _active_provider()
    using_groq = provider == "groq" or "groq" in text
    if any(
        token in text
        for token in (
            "tool_use_failed",
            "failed to parse tool call",
            "failed_generation",
            "invalid tool call",
        )
    ):
        return err.get("api_groq_tools", err["generic"])
    if any(
        token in text
        for token in (
            "429",
            "resource_exhausted",
            "quota exceeded",
            "exceeded your current quota",
            "rate-limit",
            "rate_limit",
        )
    ):
        if using_groq:
            return err.get("api_groq_quota", err["api_quota"])
        return err["api_quota"]
    if any(
        token in text
        for token in (
            "404",
            "not_found",
            "no longer available",
            "is not found",
            "model_not_found",
            "does not exist or you do not have access",
        )
    ):
        if using_groq:
            return err.get("api_groq_model_missing", err["api_model_missing"])
        return err["api_model_missing"]
    if any(
        token in text
        for token in (
            "403",
            "permission_denied",
            "denied access",
            "permission denied",
        )
    ):
        if using_groq:
            return err.get("api_groq_denied", err["api_denied"])
        return err["api_denied"]
    if any(
        token in text
        for token in ("timed out", "timeout", "connection", "unreachable", "urlopen")
    ):
        return err.get("source_unreachable", err["generic"])
    mapping = {
        PDFEmptyError: err["empty_pdf"],
        PDFPasswordError: err["password_pdf"],
        PDFCorruptedError: err["corrupted_pdf"],
        OCRNotAvailableError: err["ocr_missing"],
        OCRLanguageMissingError: err["ocr_lang_missing"],
    }
    for exc_type, message in mapping.items():
        if isinstance(error, exc_type):
            return message
    if isinstance(error, ValueError):
        if using_groq or "groq_api_key" in text:
            return err.get("api_groq_key_missing", err["api_key_missing"])
        return err["api_key_missing"]
    if isinstance(error, PDFProcessingError):
        return err["generic"]
    return err["generic"]


def _run_analysis(uploaded_file, selected_language: str) -> None:
    strings = ui(selected_language)
    err = errors(selected_language)

    if uploaded_file is None:
        st.session_state.last_error = err["no_file"]
        return

    if uploaded_file.size > MAX_UPLOAD_MB * 1024 * 1024:
        st.session_state.last_error = err["file_too_large"]
        return

    started = time.perf_counter()
    try:
        with st.spinner(strings["processing"]):
            extraction: ExtractionResult = extract_text_from_pdf(uploaded_file)
            ocr_warning = extraction.ocr_warning
            if extraction.truncated:
                note = strings["truncated_note"]
                ocr_warning = f"{ocr_warning} {note}" if ocr_warning else note

            from agent import analyze_document

            analysis = analyze_document(
                extraction.text,
                selected_language,
                ocr_warning=ocr_warning.strip() if ocr_warning else None,
            )

            st.session_state.document_text = extraction.text
            st.session_state.analysis = analysis
            st.session_state.analysis_language = selected_language
            st.session_state.knowledge_base = build_knowledge_base(extraction.text)
            st.session_state.last_rag_passages = []
            identity = identify_form(extraction.text, analysis.issuing_organization)
            st.session_state.form_identity = identity.to_dict()
            st.session_state.extraction_meta = {
                "used_ocr": extraction.used_ocr,
                "truncated": extraction.truncated,
                "rag_chunks": st.session_state.knowledge_base["chunk_count"],
            }
            st.session_state.chat_history = []
            st.session_state.last_error = None
            st.session_state.pop("debug_error", None)
            log_event(
                event_type="analyze_document",
                success=True,
                latency_ms=int((time.perf_counter() - started) * 1000),
                form_number=identity.form_number or "",
                authority_key=identity.authority_key or "",
                language=lang_code(selected_language),
            )

    except Exception as error:
        st.session_state.last_error = _map_exception_to_message(error, selected_language)
        st.session_state.debug_error = traceback.format_exc()
        log_event(
            event_type="analyze_document",
            success=False,
            latency_ms=int((time.perf_counter() - started) * 1000),
            language=lang_code(selected_language),
            error_class=type(error).__name__,
        )


def _render_chat_section(selected_language: str) -> None:
    strings = ui(selected_language)
    analysis: DocumentAnalysis | None = st.session_state.analysis
    if analysis is None or st.session_state.document_text is None:
        return

    if st.session_state.analysis_language != selected_language:
        return

    code = lang_code(selected_language)

    st.markdown("---")
    st.markdown(
        f'<div class="fb-chat-panel fb-chat-{code}">'
        f'<div class="fb-section-title">{strings["chat_title"]}</div>',
        unsafe_allow_html=True,
    )
    st.caption(strings["chat_hint"])

    st.markdown(
        f'<div class="fb-chat-suggestions">'
        f'<div class="fb-chat-suggestions-title">{strings["chat_suggestions_title"]}</div>',
        unsafe_allow_html=True,
    )
    suggestion_cols = st.columns(2)
    for index, question in enumerate(strings["example_questions"]):
        if suggestion_cols[index % 2].button(
            question,
            key=f"example_q_{index}",
            use_container_width=True,
        ):
            st.session_state.pending_chat_question = question
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    pending_question = st.session_state.pop("pending_chat_question", None)
    if pending_question:
        st.session_state.chat_history.append({"role": "user", "content": pending_question})

    render_conversation(
        st.session_state.chat_history,
        selected_language,
        empty_text=strings["chat_empty"],
        strings=strings,
    )

    user_input = st.chat_input(strings["chat_placeholder"])
    if user_input:
        st.session_state.pending_chat_question = user_input
        st.rerun()

    if pending_question:
        question = pending_question
        started = time.perf_counter()
        with st.spinner(strings["chat_processing"]):
            try:
                from agent import ask_document_question, infer_user_style

                st.session_state.user_style_notes = infer_user_style(
                    question,
                    st.session_state.chat_history[:-1],
                    st.session_state.user_style_notes,
                )
                result = ask_document_question(
                    document_text=st.session_state.document_text,
                    initial_analysis=analysis,
                    question=question,
                    selected_language=selected_language,
                    conversation_history=st.session_state.chat_history[:-1],
                    user_style_notes=st.session_state.user_style_notes,
                    knowledge_base=st.session_state.knowledge_base,
                )
                answer = result.text
                citations = [item.to_dict() for item in result.official_citations]
                st.session_state.last_rag_passages = passages_to_dicts(result.document_passages)
                if result.identity:
                    st.session_state.form_identity = result.identity.to_dict()
                if "search_official_sources" in (result.tools_used or []):
                    st.caption(strings.get("chat_tools_used", "Official search tool used"))
                identity = st.session_state.get("form_identity") or {}
                log_event(
                    event_type="chat",
                    success=True,
                    latency_ms=int((time.perf_counter() - started) * 1000),
                    form_number=str(identity.get("form_number") or ""),
                    authority_key=str(identity.get("authority_key") or ""),
                    language=code,
                    tools_used=result.tools_used or [],
                )
            except Exception as error:
                answer = _map_exception_to_message(error, selected_language)
                citations = []
                st.session_state.debug_error = traceback.format_exc()
                log_event(
                    event_type="chat",
                    success=False,
                    latency_ms=int((time.perf_counter() - started) * 1000),
                    language=code,
                    error_class=type(error).__name__,
                )

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer, "citations": citations}
        )
        _persist_current_conversation()
        st.rerun()

    if st.session_state.chat_history:
        if st.button(strings["clear_chat"], key="clear_chat_btn", type="tertiary"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def _render_guided_section(selected_language: str) -> None:
    strings = ui(selected_language)
    code = lang_code(selected_language)
    st.markdown(
        f"""
        <div class="fb-panel">
            <div class="fb-section-title">{html.escape(strings["guided_title"])}</div>
            <span class="fb-bridge-line" style="margin: 0.55rem 0 0.85rem auto;"></span>
        """,
        unsafe_allow_html=True,
    )

    suggestions = strings.get("guided_example_questions") or []
    if suggestions and not st.session_state.guided_history:
        st.markdown(f"**{strings.get('guided_suggestions_title', 'Suggested questions')}**")
        cols = st.columns(min(3, len(suggestions)))
        for index, question in enumerate(suggestions):
            if cols[index % len(cols)].button(
                question,
                key=f"guided_suggestion_{index}",
                use_container_width=True,
            ):
                st.session_state.guided_pending = question
                st.rerun()

    history = st.session_state.guided_history
    rewritten: list[dict] = []
    history_changed = False
    for message in history:
        content = message.get("content") or ""
        if message.get("role") == "assistant" and content.lstrip().startswith(("{", "```")):
            language = lang_code(selected_language)
            parsed = parse_guided_response(content, language)
            content = humanize_guided_text(content, language)
            history_changed = True
            if st.session_state.guided_result is None and (
                parsed.identified_service or parsed.steps or parsed.official_links
            ):
                st.session_state.guided_result = parsed
        rewritten.append({**message, "content": content})
    if history_changed:
        st.session_state.guided_history = rewritten
        history = rewritten

    pending = st.session_state.pop("guided_pending", None)
    if pending:
        history.append({"role": "user", "content": pending})
        st.session_state.guided_history = history

    render_conversation(
        history,
        selected_language,
        empty_text=strings.get("guided_empty"),
        strings=strings,
    )

    user_input = st.chat_input(strings["guided_placeholder"], key="guided_chat_input_v2")
    if user_input:
        st.session_state.guided_pending = user_input
        st.rerun()

    if pending:
        question = pending
        started = time.perf_counter()
        with st.spinner(strings["chat_processing"]):
            try:
                from agent import run_guided_intake

                guidance, citations, tools_used = run_guided_intake(
                    user_message=question,
                    selected_language=selected_language,
                    conversation_history=st.session_state.guided_history[:-1],
                    previous_guidance=st.session_state.get("guided_result"),
                )
                st.session_state.guided_result = guidance
                st.session_state.guided_tools_used = tools_used
                st.session_state.guided_history.append(
                    {
                        "role": "assistant",
                        "content": humanize_guided_text(
                            guidance.assistant_message, code
                        ),
                    }
                )
                st.session_state.last_guided_citations = [
                    item.to_dict() for item in citations
                ]
                log_event(
                    event_type="guided",
                    success=True,
                    latency_ms=int((time.perf_counter() - started) * 1000),
                    form_number=guidance.form_number or "",
                    authority_key="",
                    language=code,
                    tools_used=tools_used or [],
                )
            except Exception as error:
                answer = _map_exception_to_message(error, selected_language)
                st.session_state.guided_history.append(
                    {"role": "assistant", "content": answer}
                )
                st.session_state.guided_result = None
                st.session_state.last_guided_citations = []
                st.session_state.debug_error = traceback.format_exc()
                log_event(
                    event_type="guided",
                    success=False,
                    latency_ms=int((time.perf_counter() - started) * 1000),
                    language=code,
                    error_class=type(error).__name__,
                )
        _persist_current_conversation()
        st.rerun()

    if st.session_state.get("debug_error") and st.session_state.guided_result is None:
        with st.expander("Technical details (development)"):
            st.code(st.session_state.debug_error)

    if st.session_state.guided_result is not None:
        render_guided_result(
            st.session_state.guided_result,
            selected_language,
            citations=st.session_state.get("last_guided_citations") or [],
        )
        render_field_validator(selected_language)
        fb1, fb2 = st.columns(2)
        if fb1.button("👍", key="fb_up"):
            log_feedback(
                "up",
                language=code,
                form_number=getattr(st.session_state.guided_result, "form_number", "") or "",
            )
            st.caption("Thanks.")
        if fb2.button("👎", key="fb_down"):
            log_feedback(
                "down",
                language=code,
                form_number=getattr(st.session_state.guided_result, "form_number", "") or "",
            )
            st.caption("Thanks.")

    if st.session_state.guided_history:
        if st.button(strings["guided_clear"], key="guided_clear_btn"):
            st.session_state.guided_history = []
            st.session_state.guided_result = None
            st.session_state.guided_tools_used = []
            st.session_state.pop("last_guided_citations", None)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="FormBridge",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    _init_session_state()
    apply_home_navigation()

    if "language_selector" not in st.session_state:
        st.session_state.language_selector = LANGUAGE_AR

    # Sync ?lang= only on first load so the radio remains the source of truth afterward.
    if "fb_language_bootstrapped" not in st.session_state:
        qp_lang = st.query_params.get("lang")
        if isinstance(qp_lang, (list, tuple)):
            qp_lang = qp_lang[0] if qp_lang else None
        lang_from_code = {"ar": LANGUAGE_AR, "he": LANGUAGE_HE, "en": LANGUAGE_EN}
        if qp_lang in lang_from_code:
            st.session_state.language_selector = lang_from_code[qp_lang]
            st.session_state.fb_language_query = qp_lang
        st.session_state.fb_language_bootstrapped = True

    selected_language = st.session_state.language_selector
    inject_global_css(selected_language)

    selected_language = render_language_switcher(selected_language)
    inject_global_css(selected_language)
    strings = ui(selected_language)

    mode_label = st.session_state.get("app_mode", "guided")
    if mode_label == "guided":
        if st.session_state.guided_result is not None and getattr(
            st.session_state.guided_result, "status", ""
        ) == "ready":
            header_status = "done"
        elif st.session_state.guided_history:
            header_status = "ready"
        else:
            header_status = "idle"
    else:
        header_status = (
            "done"
            if st.session_state.analysis
            else ("ready" if st.session_state.uploaded_file_id else "idle")
        )
    signed_in = bool(st.session_state.get("fb_user") or st.session_state.get("fb_guest"))
    if current_user_is_admin():
        st.session_state.fb_admin_unlocked = True
        st.switch_page("pages/1_Official_Sources.py")
        return

    onboard_done = (not signed_in) or next_onboarding_step(
        bool(st.session_state.get("privacy_consent")),
        bool(st.session_state.get("fb_mode_chosen")),
    ) == "done"
    if signed_in and onboard_done:
        render_header(selected_language, header_status, mode=mode_label)

    with st.sidebar:
        render_sidebar_nav()
        render_account_sidebar(selected_language)

    _apply_account_actions()

    if not st.session_state.get("fb_user") and not st.session_state.get("fb_guest"):
        render_landing(selected_language)
        render_auth_panel(selected_language)
        render_footer(selected_language)
        return

    flash = st.session_state.pop("fb_flash", None)
    if flash:
        st.success(flash)

    if not render_start_windows(selected_language):
        render_footer(selected_language)
        return

    mode_label = st.session_state.get("app_mode") or "guided"

    if mode_label == "guided":
        _render_guided_section(selected_language)
        render_footer(selected_language)
        return

    st.markdown(
        f'<div class="fb-panel"><div class="fb-section-title">{strings["workspace_title"]}</div>'
        f'<div class="fb-section-title" style="font-size:0.92rem;color:var(--fb-text-muted);font-weight:600;">'
        f'{strings["upload_title"]}</div>',
        unsafe_allow_html=True,
    )
    st.caption(strings["upload_help"])

    uploaded_file = st.file_uploader(
        "PDF document",
        type=["pdf"],
        label_visibility="collapsed",
        key="pdf_uploader",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None:
        current_file_id = _file_identity(uploaded_file)
        if st.session_state.uploaded_file_id != current_file_id:
            st.session_state.uploaded_file_id = current_file_id
            _reset_analysis_state()
        st.success(f"{strings['file_selected']}: {uploaded_file.name}")
    elif st.session_state.uploaded_file_id is not None:
        st.session_state.uploaded_file_id = None
        _reset_analysis_state()

    action_col1, action_col2, action_col3 = st.columns([2, 1, 1])
    with action_col1:
        analyze_clicked = st.button(
            strings["analyze_button"],
            type="primary",
            use_container_width=True,
            disabled=uploaded_file is None,
        )
    with action_col2:
        reanalyze = st.button(
            strings["analyze_again"],
            use_container_width=True,
            disabled=uploaded_file is None,
        )
    with action_col3:
        clear_doc = st.button(strings["clear_document"], use_container_width=True)

    if clear_doc:
        st.session_state.uploaded_file_id = None
        _reset_analysis_state()
        st.rerun()

    if analyze_clicked or reanalyze:
        _run_analysis(uploaded_file, selected_language)

    if st.session_state.last_error:
        st.error(st.session_state.last_error)
        if st.session_state.get("debug_error"):
            with st.expander("Technical details (development)"):
                st.code(st.session_state.debug_error)

    analysis: DocumentAnalysis | None = st.session_state.analysis
    language_matches = (
        analysis is not None and st.session_state.analysis_language == selected_language
    )

    if analysis and not language_matches:
        st.warning(strings["language_mismatch"])

    if language_matches and analysis is not None:
        render_analysis_dashboard(analysis, selected_language)
        render_download_buttons(analysis, selected_language)

        with st.expander(strings["original_text"]):
            doc_text = st.session_state.document_text or ""
            st.markdown(
                """
                <style>
                .fb-original-text {
                  direction: auto;
                  text-align: start;
                  unicode-bidi: plaintext;
                  white-space: pre-wrap;
                  font-family: "Noto Sans Hebrew", "Noto Sans Arabic", "Segoe UI", sans-serif !important;
                  line-height: 1.85;
                  background: var(--fb-surface-soft);
                  border: 1px solid var(--fb-border);
                  border-radius: 12px;
                  padding: 1rem 1.1rem;
                  color: var(--fb-text);
                  font-size: 1.02rem;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="fb-original-text" dir="auto">{html.escape(doc_text)}</div>',
                unsafe_allow_html=True,
            )

        identity = st.session_state.get("form_identity") or {}
        if identity:
            with st.expander(strings.get("form_identity", "Form identity")):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**{strings.get('issuing_org', 'Authority')}**")
                    st.write(identity.get("authority") or "—")
                    st.markdown(f"**{strings.get('form_label', 'Form')}**")
                    form_no = identity.get("form_number") or ""
                    form_name = identity.get("form_name") or ""
                    if form_no and form_name:
                        st.write(f"{form_no} — {form_name}")
                    elif form_no:
                        st.write(form_no)
                    elif form_name:
                        st.write(form_name)
                    else:
                        st.write("—")
                with c2:
                    st.markdown(f"**{strings.get('document_type', 'Category')}**")
                    st.write(identity.get("category") or "—")
                    st.markdown(f"**{strings.get('confidence', 'Confidence')}**")
                    conf = identity.get("confidence")
                    conf_label = f"{float(conf):.0%}" if isinstance(conf, (int, float)) else "—"
                    if identity.get("uncertain"):
                        conf_label = f"{conf_label} (uncertain)"
                    st.write(conf_label)

        kb = st.session_state.get("knowledge_base") or {}
        chunk_count = kb.get("chunk_count", 0)
        with st.expander(f"{strings['rag_title']} · {chunk_count} {strings['rag_chunks']}"):
            passages = st.session_state.get("last_rag_passages") or []
            if not passages:
                st.caption(strings["rag_empty"])
            else:
                for item in passages:
                    st.markdown(
                        f"**#{item.get('chunk_id', 0) + 1}** · score `{item.get('score', 0)}`"
                    )
                    st.write(item.get("text", ""))

        _render_chat_section(selected_language)
    elif analysis is None and uploaded_file is None:
        render_empty_state(selected_language)

    render_footer(selected_language)


if __name__ == "__main__":
    main()
