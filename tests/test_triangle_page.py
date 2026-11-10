"""The Triangle page is a blank #FEEFEF page that fits the shared sidebar."""

from pathlib import Path

from streamlit.testing.v1 import AppTest
from streamlit.testing.v1.element_tree import Block


APP = Path(__file__).resolve().parents[1] / "app.py"


def _open_triangle_page(**state: object) -> AppTest:
    at = AppTest.from_file(str(APP), default_timeout=60)
    for key, value in state.items():
        at.session_state[key] = value
    at.run()
    at.switch_page("pages/4_Triangle.py")
    return at.run()


def test_page_is_blank_with_a_feefef_background() -> None:
    at = _open_triangle_page()
    assert not at.exception
    elements = [node for node in at.main if not isinstance(node, Block)]
    assert all(
        node.type == "markdown" and node.value.strip().startswith("<style>")
        for node in elements
    )
    assert elements[-1].value == "<style>.stApp { background: #FEEFEF !important; }</style>"


def test_sidebar_links_to_the_page() -> None:
    at = AppTest.from_file(str(APP), default_timeout=60).run()
    assert any(link.proto.page == "Triangle" for link in at.sidebar.get("page_link"))


def test_sidebar_new_chat_returns_home() -> None:
    at = _open_triangle_page(fb_guest=True, privacy_consent=True, fb_mode_chosen=True)
    at.sidebar.button(key="fb_new_chat_guest").click().run()
    assert not at.exception
    assert "_fb_new_chat" not in at.session_state
    assert at.session_state["fb_mode_chosen"] is False
