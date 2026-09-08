"""FormBridge — AI assistant for understanding official Hebrew documents."""

from __future__ import annotations

import hashlib
import traceback

import streamlit as st

from agent import analyze_document, ask_document_question, infer_user_style
from models import DocumentAnalysis
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
from ui_components import (
    LANGUAGE_AR,
    LANGUAGE_HE,
    errors,
    inject_global_css,
    lang_code,
    render_analysis_dashboard,
    render_chat_bubble,
    render_download_buttons,
    render_empty_state,
    render_footer,
    render_header,
    ui,
)


MAX_UPLOAD_MB = 10


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
        "last_error": None,
        "extraction_meta": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _file_identity(uploaded_file) -> str:
    content = uploaded_file.getvalue()
    digest = hashlib.sha256(content).hexdigest()
    return f"{uploaded_file.name}:{len(content)}:{digest}"


def _reset_analysis_state() -> None:
    st.session_state.document_text = None
    st.session_state.analysis = None
    st.session_state.analysis_language = None
    st.session_state.chat_history = []
    st.session_state.user_style_notes = []
    st.session_state.knowledge_base = None
    st.session_state.last_rag_passages = []
    st.session_state.extraction_meta = None
    st.session_state.last_error = None
    st.session_state.pop("debug_error", None)


def _map_exception_to_message(error: Exception, selected_language: str) -> str:
    err = errors(selected_language)
    mapping = {
        PDFEmptyError: err["empty_pdf"],
        PDFPasswordError: err["password_pdf"],
        PDFCorruptedError: err["corrupted_pdf"],
        OCRNotAvailableError: err["ocr_missing"],
        OCRLanguageMissingError: err["ocr_lang_missing"],
        ValueError: err["api_key_missing"],
    }
    for exc_type, message in mapping.items():
        if isinstance(error, exc_type):
            return message
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

    try:
        with st.spinner(strings["processing"]):
            extraction: ExtractionResult = extract_text_from_pdf(uploaded_file)
            ocr_warning = extraction.ocr_warning
            if extraction.truncated:
                note = strings["truncated_note"]
                ocr_warning = f"{ocr_warning} {note}" if ocr_warning else note

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
            st.session_state.extraction_meta = {
                "used_ocr": extraction.used_ocr,
                "truncated": extraction.truncated,
                "rag_chunks": st.session_state.knowledge_base["chunk_count"],
            }
            st.session_state.chat_history = []
            st.session_state.last_error = None
            st.session_state.pop("debug_error", None)

    except Exception as error:
        st.session_state.last_error = _map_exception_to_message(error, selected_language)
        st.session_state.debug_error = traceback.format_exc()


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

    chat_history = st.session_state.chat_history
    if not chat_history:
        st.markdown(
            f'<div class="fb-chat-empty">{strings["chat_empty"]}</div>',
            unsafe_allow_html=True,
        )

    for message in chat_history:
        render_chat_bubble(message["content"], message["role"], selected_language)

    pending_question = st.session_state.pop("pending_chat_question", None)
    user_input = st.chat_input(strings["chat_placeholder"])
    question = pending_question or user_input

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        render_chat_bubble(question, "user", selected_language)

        with st.spinner(strings["chat_processing"]):
            try:
                st.session_state.user_style_notes = infer_user_style(
                    question,
                    st.session_state.chat_history[:-1],
                    st.session_state.user_style_notes,
                )
                answer, passages = ask_document_question(
                    document_text=st.session_state.document_text,
                    initial_analysis=analysis,
                    question=question,
                    selected_language=selected_language,
                    conversation_history=st.session_state.chat_history[:-1],
                    user_style_notes=st.session_state.user_style_notes,
                    knowledge_base=st.session_state.knowledge_base,
                )
                st.session_state.last_rag_passages = passages_to_dicts(passages)
            except Exception as error:
                answer = _map_exception_to_message(error, selected_language)
                st.session_state.debug_error = traceback.format_exc()

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        render_chat_bubble(answer, "assistant", selected_language)

    if st.session_state.chat_history:
        _, toolbar_right = st.columns([4, 1])
        with toolbar_right:
            if st.button(strings["clear_chat"], key="clear_chat_btn", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="FormBridge",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    _init_session_state()
    inject_global_css()

    if "language_selector" not in st.session_state:
        st.session_state.language_selector = LANGUAGE_AR

    selected_language = st.session_state.language_selector
    header_status = (
        "done"
        if st.session_state.analysis
        else ("ready" if st.session_state.uploaded_file_id else "idle")
    )
    render_header(selected_language, header_status)
    strings = ui(selected_language)

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

    st.markdown(
        f'<div class="fb-section-title">{strings["language_title"]}</div>',
        unsafe_allow_html=True,
    )

    selected_language = st.selectbox(
        "Output language",
        [LANGUAGE_AR, LANGUAGE_HE],
        label_visibility="collapsed",
        key="language_selector",
    )
    strings = ui(selected_language)

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
            st.text_area(
                "Extracted document text",
                value=st.session_state.document_text or "",
                height=260,
                label_visibility="collapsed",
            )

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
