"""Admin page for the official knowledge base."""

from __future__ import annotations

import os

import streamlit as st  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv

from knowledge_base.service import KnowledgeBaseService
from ui_components import inject_global_css


load_dotenv()


def _authorized() -> bool:
    expected = os.getenv("KB_ADMIN_PASSWORD", "")
    if not expected:
        st.warning("Set KB_ADMIN_PASSWORD in .env to unlock source management.")
        return False
    st.info("Enter the admin password from your `.env` file (`KB_ADMIN_PASSWORD`).")
    password = st.text_input("Admin password", type="password", key="os_admin_password")
    if not password:
        st.caption("Waiting for password…")
        return False
    if password != expected:
        st.error("Wrong password.")
        return False
    return True


st.set_page_config(page_title="Official Sources", layout="wide")
inject_global_css()
st.title("Official Sources")
st.caption("FormBridge is not affiliated with the Israeli government. Sources are informational only.")

if not _authorized():
    st.stop()

service = KnowledgeBaseService()
st.subheader("Authorities")
rows = service.list_status()
st.dataframe(rows, use_container_width=True)

authority_options = [str(row["authority_key"]) for row in rows if row.get("authority_key")]
selected_key = st.selectbox("Authority", authority_options) if authority_options else None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Update all enabled sources", type="primary"):
        with st.spinner("Updating fixtures / allowlisted sources..."):
            service.update_all()
        st.success("Update finished.")
        st.rerun()
with col2:
    if st.button("Update selected"):
        if selected_key is None:
            st.warning("Select an authority first.")
        else:
            service.update_one(selected_key)
            st.success(f"Updated {selected_key}")
            st.rerun()
with col3:
    if st.button("Rebuild selected index"):
        if selected_key is None:
            st.warning("Select an authority first.")
        else:
            service.rebuild(selected_key)
            st.success(f"Rebuilt {selected_key}")
            st.rerun()

st.subheader("Search knowledge base")
query = st.text_input("Query")
if query:
    hits = service.search(query)
    for hit in hits:
        st.markdown(
            f"**{hit.chunk.metadata.authority}** · {hit.chunk.metadata.source_type} · "
            f"[source]({hit.chunk.metadata.source_url})"
        )
        st.write(hit.chunk.text)

st.subheader("Ingestion history")
history = service.ingestion_history(20)
if not history:
    st.info("No ingestion events yet.")
else:
    st.dataframe(
        [
            {
                "Time": item.get("timestamp", "—"),
                "Event": item.get("event", "—"),
                "Authority": item.get("authority", "—"),
                "Added": item.get("added", "—"),
                "Error": item.get("error") or "",
            }
            for item in history
        ],
        hide_index=True,
        use_container_width=True,
    )
    errors = [item for item in history if item.get("event") == "ingest_error"]
    if errors:
        with st.expander(f"Errors ({len(errors)})", expanded=False):
            for item in errors:
                st.write(
                    f"**{item.get('authority', '—')}** · {item.get('timestamp', '—')}"
                )
                st.error(item.get("error") or "Unknown error")
