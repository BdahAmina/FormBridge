"""The Triangle page renders, reacts to presets and inputs, and fits the shared sidebar."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"


def _open_triangle_page(**state: object) -> AppTest:
    at = AppTest.from_file(str(APP), default_timeout=60)
    for key, value in state.items():
        at.session_state[key] = value
    at.run()
    at.switch_page("pages/4_Triangle.py")
    return at.run()


def test_page_solves_the_default_right_triangle() -> None:
    at = _open_triangle_page()
    assert not at.exception
    assert at.title[0].value == "Triangle"
    assert at.subheader[0].value == "Right scalene triangle"
    assert [(metric.label, metric.value) for metric in at.metric] == [
        ("Perimeter", "12"),
        ("Area", "6"),
        ("Inradius", "1"),
        ("Circumradius", "2.5"),
    ]
    assert any("<svg" in block.value for block in at.markdown)


def test_presets_fill_the_sides_and_bad_sides_show_an_error() -> None:
    at = _open_triangle_page()
    next(button for button in at.button if button.label == "Equilateral").click().run()
    assert [field.value for field in at.number_input] == [5.0, 5.0, 5.0]
    assert at.subheader[0].value == "Acute equilateral triangle"

    at.number_input(key="tri_side_c").set_value(20.0).run()
    assert "can't form a triangle" in at.error[0].value
    assert not at.subheader


def test_sidebar_links_to_the_page() -> None:
    at = AppTest.from_file(str(APP), default_timeout=60).run()
    assert any(link.proto.page == "Triangle" for link in at.sidebar.get("page_link"))


def test_sidebar_new_chat_returns_home() -> None:
    at = _open_triangle_page(fb_guest=True, privacy_consent=True, fb_mode_chosen=True)
    at.sidebar.button(key="fb_new_chat_guest").click().run()
    assert not at.exception
    assert "_fb_new_chat" not in at.session_state
    assert at.session_state["fb_mode_chosen"] is False
