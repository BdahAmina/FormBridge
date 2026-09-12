"""Admin page for offline RAG evaluations."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from evals.run import run_offline
from ui_components import inject_global_css, is_admin_unlocked, render_sidebar_nav, unlock_admin


load_dotenv()


def _authorized() -> bool:
    if is_admin_unlocked():
        return True
    expected = os.getenv("KB_ADMIN_PASSWORD", "")
    if not expected:
        st.warning("Set KB_ADMIN_PASSWORD in .env to unlock evals.")
        return False
    password = st.text_input("Admin password", type="password", key="evals_admin_password")
    if st.button("Unlock", key="evals_admin_unlock"):
        if unlock_admin(password):
            st.rerun()
        st.error("Wrong password.")
    return False


def _render_report(report: dict) -> None:
    status = "PASS" if report.get("passed") else "FAIL"
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Overall", f"{report.get('overall_score', 0):.3f}")
    c2.metric("Retrieval", f"{report.get('retrieval_score', 0):.3f}")
    c3.metric("Citation", f"{report.get('citation_score', 0):.3f}")
    c4.metric("Critical failures", report.get("critical_failures", 0))
    c5.metric("Status", status)

    st.caption(
        f"Run {report.get('timestamp', '—')} · "
        f"Dataset {report.get('dataset_version', '—')} · "
        f"Prompt {report.get('prompt_version', '—')} · "
        f"Rubric {report.get('rubric_version', '—')}"
    )

    if "baseline_overall" in report:
        st.info(
            f"Baseline overall: {report['baseline_overall']} · "
            f"Regression: {report.get('regression', 0)}"
        )

    gates = report.get("gates") or {}
    if gates:
        with st.expander("Pass gates", expanded=False):
            g1, g2, g3 = st.columns(3)
            g1.write(f"**Min overall:** {gates.get('min_overall', '—')}")
            g2.write(f"**Min retrieval:** {gates.get('min_retrieval_recall', '—')}")
            g3.write(f"**Min citation:** {gates.get('min_citation', '—')}")
            g4, g5 = st.columns(2)
            g4.write(f"**Max unsupported:** {gates.get('max_unsupported', '—')}")
            g5.write(f"**Max critical:** {gates.get('max_critical', '—')}")

    cases = report.get("cases") or []
    failed = [case for case in cases if not case.get("passed")]
    passed_count = len(cases) - len(failed)
    st.write(f"**Cases:** {passed_count} passed · {len(failed)} failed · {len(cases)} total")

    st.subheader("Failed cases")
    if not failed:
        st.success("No failed cases.")
    else:
        for case in failed:
            title = (
                f"{case.get('id', 'case')} · {case.get('category', '—')} · "
                f"score {case.get('overall', 0):.3f}"
            )
            with st.expander(title, expanded=False):
                m1, m2, m3 = st.columns(3)
                m1.write(f"**Language:** {case.get('language', '—')}")
                m2.write(f"**Authority:** {case.get('authority') or '—'}")
                m3.write(f"**Critical:** {'yes' if case.get('critical') else 'no'}")

                s1, s2, s3, s4, s5, s6 = st.columns(6)
                s1.metric("Retrieval", f"{case.get('retrieval', 0):.2f}")
                s2.metric("Groundedness", f"{case.get('groundedness', 0):.2f}")
                s3.metric("Citation", f"{case.get('citation', 0):.2f}")
                s4.metric("Answer", f"{case.get('answer_quality', 0):.2f}")
                s5.metric("Multilingual", f"{case.get('multilingual', 0):.2f}")
                s6.metric("Safety", f"{case.get('safety', 0):.2f}")

                if case.get("answer"):
                    st.markdown("**Answer**")
                    st.write(case["answer"])
                retrieved = case.get("retrieved") or []
                if retrieved:
                    st.markdown("**Retrieved sources**")
                    for url in retrieved:
                        st.write(f"- {url}")
                metrics = case.get("metrics") or {}
                if metrics:
                    with st.expander("Metric details"):
                        for key, value in metrics.items():
                            st.write(f"**{key}:** {value}")

    if cases:
        with st.expander("All cases", expanded=False):
            st.dataframe(
                [
                    {
                        "id": case.get("id"),
                        "category": case.get("category"),
                        "language": case.get("language"),
                        "score": case.get("overall"),
                        "passed": case.get("passed"),
                        "critical": case.get("critical"),
                    }
                    for case in cases
                ],
                hide_index=True,
                use_container_width=True,
            )

    report_path = Path("evals/reports/latest.md")
    if report_path.exists():
        st.download_button(
            "Download latest report",
            report_path.read_text(encoding="utf-8"),
            file_name="eval_report.md",
        )


st.set_page_config(page_title="Evals", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
with st.sidebar:
    render_sidebar_nav()
st.title("Evals")
st.caption("Offline evaluations use fixtures only. They never crawl live government sites.")

if not _authorized():
    st.stop()

if st.button("Run offline evals", type="primary"):
    with st.spinner("Running offline evaluation suite..."):
        report = run_offline()
    st.session_state["latest_eval_report"] = report

report = st.session_state.get("latest_eval_report")
if report:
    _render_report(report)
else:
    st.info("Run offline evals to see scores.")
