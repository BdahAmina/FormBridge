"""Triangle explorer: enter three side lengths to see the shape, its angles, and its area."""

from __future__ import annotations

import streamlit as st  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv

from triangle import (
    SIDE_NAMES,
    VERTEX_NAMES,
    TriangleError,
    format_number,
    triangle_from_sides,
    triangle_svg,
)
from ui_components import (
    LANGUAGE_EN,
    inject_global_css,
    render_account_sidebar,
    render_sidebar_nav,
)


load_dotenv()

PRESETS: dict[str, tuple[float, float, float]] = {
    "Right (3-4-5)": (3.0, 5.0, 4.0),
    "Equilateral": (5.0, 5.0, 5.0),
    "Isosceles": (6.0, 6.0, 4.0),
    "Obtuse": (4.0, 5.0, 8.0),
}
SIDE_KEYS = ("tri_side_a", "tri_side_b", "tri_side_c")
SIDE_LABELS = ("Side a (B to C)", "Side b (C to A)", "Side c (A to B)")


def _apply_preset(sides: tuple[float, float, float]) -> None:
    for key, value in zip(SIDE_KEYS, sides):
        st.session_state[key] = value


st.set_page_config(
    page_title="Triangle",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css(LANGUAGE_EN)
with st.sidebar:
    render_sidebar_nav()
    render_account_sidebar(st.session_state.get("language_selector") or LANGUAGE_EN)
# "New chat" and "Recent chats" in the sidebar are applied by the main app page.
if st.session_state.get("_fb_new_chat") or st.session_state.get("_fb_load_chat"):
    st.switch_page("app.py")

st.markdown(
    """
    <style>
        .fb-triangle-figure {
            background: var(--fb-surface, #FFFFFF);
            border: 1px solid var(--fb-line, #E6E0D6);
            border-radius: var(--fb-radius, 22px);
            padding: 1.25rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<p class="fb-eyebrow">Geometry</p>', unsafe_allow_html=True)
st.title("Triangle")
st.caption("Enter three side lengths to draw the triangle and see its angles, area, and type.")

for key, value in zip(SIDE_KEYS, PRESETS["Right (3-4-5)"]):
    st.session_state.setdefault(key, value)

for column, (label, sides) in zip(st.columns(len(PRESETS)), PRESETS.items()):
    column.button(label, on_click=_apply_preset, args=(sides,), width="stretch")

for column, key, label in zip(st.columns(3), SIDE_KEYS, SIDE_LABELS):
    column.number_input(
        label,
        min_value=0.0,
        max_value=1_000_000.0,
        step=0.5,
        format="%.2f",
        key=key,
    )

try:
    tri = triangle_from_sides(*(st.session_state[key] for key in SIDE_KEYS))
except TriangleError as error:
    st.error(str(error))
    st.stop()

st.subheader(tri.description)
figure_col, facts_col = st.columns([3, 2], gap="large")
with figure_col:
    st.markdown(
        f'<div class="fb-triangle-figure">{triangle_svg(tri)}</div>',
        unsafe_allow_html=True,
    )
with facts_col:
    m1, m2 = st.columns(2)
    m1.metric("Perimeter", format_number(tri.perimeter))
    m2.metric("Area", format_number(tri.area))
    m3, m4 = st.columns(2)
    m3.metric(
        "Inradius",
        format_number(tri.inradius),
        help="Radius of the largest circle that fits inside the triangle.",
    )
    m4.metric(
        "Circumradius",
        format_number(tri.circumradius),
        help="Radius of the circle that passes through all three corners.",
    )
    st.dataframe(
        [
            {
                "Vertex": vertex,
                "Angle": f"{format_number(angle)}°",
                "Opposite side": f"{side_name} = {format_number(side)}",
                "Height from vertex": format_number(height),
            }
            for vertex, angle, side_name, side, height in zip(
                VERTEX_NAMES, tri.angles, SIDE_NAMES, tri.sides, tri.heights
            )
        ],
        hide_index=True,
        width="stretch",
    )
    if tri.angle_type == "right":
        shortest, middle, longest = sorted(tri.sides)
        st.caption(
            f"Pythagoras checks out: {format_number(shortest)}² + "
            f"{format_number(middle)}² = {format_number(longest)}²."
        )
