"""Triangle page: a blank page with a #FEEFEF background."""

from __future__ import annotations

import streamlit as st  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv

from ui_components import (
    LANGUAGE_EN,
    inject_global_css,
    render_account_sidebar,
    render_sidebar_nav,
)


load_dotenv()

st.set_page_config(
    page_title="Triangle",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css(LANGUAGE_EN)
# Must come after inject_global_css so it wins over the shared .stApp background.
st.markdown(
    "<style>.stApp { background: #FEEFEF !important; }</style>",
    unsafe_allow_html=True,
)
with st.sidebar:
    render_sidebar_nav()
    render_account_sidebar(st.session_state.get("language_selector") or LANGUAGE_EN)
# "New chat" and "Recent chats" in the sidebar are applied by the main app page.
if st.session_state.get("_fb_new_chat") or st.session_state.get("_fb_load_chat"):
    st.switch_page("app.py")
