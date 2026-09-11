"""Admin page for offline RAG evaluations."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from evals.run import run_offline
from ui_components import inject_global_css


load_dotenv()


def _authorized() -> bool:
    expected = os.getenv("KB_ADMIN_PASSWORD", "")
    if not expected:
        st.warning("Set KB_ADMIN_PASSWORD in .env to unlock evals.")
        return False
    password = st.text_input("Admin password", type="password")
    return password == expected


st.set_page_config(page_title="Evals", layout="wide")
inject_global_css()
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
    st.metric("Overall", f"{report['overall_score']:.2f}")
    st.metric("Status", "PASS" if report["passed"] else "FAIL")
    st.json({k: report[k] for k in report if k != "cases"})
    failed = [case for case in report.get("cases", []) if not case.get("passed")]
    st.subheader("Failed cases")
    st.json(failed or [{"info": "No failed cases"}])
    report_path = Path("evals/reports/latest.md")
    if report_path.exists():
        st.download_button("Download latest report", report_path.read_text(encoding="utf-8"), file_name="eval_report.md")
else:
    st.info("Run offline evals to see scores.")
