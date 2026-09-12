"""Admin monitoring dashboard (anonymized telemetry + KB/eval status)."""

from __future__ import annotations

import json
import os
from pathlib import Path

import streamlit as st  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv

from knowledge_base.service import KnowledgeBaseService
from telemetry import summarize
from ui_components import inject_global_css, is_admin_unlocked, render_sidebar_nav, unlock_admin


load_dotenv()


def _authorized() -> bool:
    if is_admin_unlocked():
        return True
    expected = os.getenv("KB_ADMIN_PASSWORD", "")
    if not expected:
        st.warning("Set KB_ADMIN_PASSWORD in .env to unlock monitoring.")
        return False
    password = st.text_input("Admin password", type="password", key="monitor_admin_password")
    if st.button("Unlock", key="monitor_admin_unlock"):
        if unlock_admin(password):
            st.rerun()
        st.error("Wrong password.")
    return False


st.set_page_config(page_title="Monitor", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
with st.sidebar:
    render_sidebar_nav()
st.title("FormBridge Monitor")
st.caption(
    "Anonymized product metrics only. Private user questions and IDs are not stored in telemetry."
)

if not _authorized():
    st.stop()

summary = summarize()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Events", summary["total_events"])
c2.metric("Successful", summary["successful"])
c3.metric("Failed", summary["failed"])
avg = summary["avg_latency_ms"]
c4.metric("Avg latency (ms)", avg if avg is not None else "—")

st.subheader("Most requested forms")
if summary["top_forms"]:
    st.dataframe(
        [{"form": form, "count": count} for form, count in summary["top_forms"]],
        use_container_width=True,
    )
else:
    st.caption("No form telemetry yet.")

st.subheader("Top authorities")
if summary["top_authorities"]:
    st.dataframe(
        [{"authority": key, "count": count} for key, count in summary["top_authorities"]],
        use_container_width=True,
    )
else:
    st.caption("No authority telemetry yet.")

st.subheader("Events by type")
if summary["by_type"]:
    st.dataframe(
        [{"event_type": name, "count": count} for name, count in summary["by_type"]],
        use_container_width=True,
    )

st.subheader("Knowledge-source status")
service = KnowledgeBaseService()
st.dataframe(service.list_status(), use_container_width=True)

st.subheader("Latest evaluation report")
reports = sorted(Path("evals/reports").glob("*.json"), reverse=True)
if reports:
    latest = reports[0]
    st.caption(f"Showing `{latest.name}`")
    try:
        payload = json.loads(latest.read_text(encoding="utf-8"))
        cols = st.columns(4)
        cols[0].metric("Overall", round(float(payload.get("overall_score", 0)), 3))
        cols[1].metric("Cases", len(payload.get("cases") or []))
        cols[2].metric(
            "Passed",
            sum(1 for case in payload.get("cases") or [] if case.get("passed")),
        )
        cols[3].metric("Avg latency (ms)", payload.get("avg_latency_ms") or "—")
        with st.expander("Raw report JSON"):
            st.json(payload)
    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Could not read report: {error}")
else:
    st.caption("No eval reports yet. Run `python -m evals.run --offline`.")

st.subheader("User feedback (optional, anonymized)")
st.caption("Feedback is recorded as thumbs up/down counts only — never the question text.")
feedback_path = Path("data/feedback.jsonl")
if feedback_path.exists():
    ups = downs = 0
    for line in feedback_path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("rating") == "up":
            ups += 1
        elif row.get("rating") == "down":
            downs += 1
    f1, f2 = st.columns(2)
    f1.metric("Thumbs up", ups)
    f2.metric("Thumbs down", downs)
else:
    st.caption("No feedback events yet.")
