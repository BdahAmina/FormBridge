"""Triangle geometry and drawing used by the Triangle page."""

import math
import re

import pytest

from triangle import TriangleError, format_number, triangle_from_sides, triangle_svg


def test_right_triangle_3_4_5() -> None:
    tri = triangle_from_sides(3, 5, 4)
    assert tri.description == "Right scalene triangle"
    assert tri.largest_angle_vertex == "B"
    assert tri.angles == pytest.approx((36.8699, 90.0, 53.1301), abs=1e-4)
    assert tri.perimeter == pytest.approx(12)
    assert tri.area == pytest.approx(6)
    assert tri.heights == pytest.approx((4, 2.4, 3))
    assert tri.inradius == pytest.approx(1)
    assert tri.circumradius == pytest.approx(2.5)


def test_equilateral_and_isosceles_types() -> None:
    equilateral = triangle_from_sides(2, 2, 2)
    assert equilateral.description == "Acute equilateral triangle"
    assert equilateral.angles == pytest.approx((60, 60, 60))
    assert equilateral.area == pytest.approx(math.sqrt(3))

    isosceles = triangle_from_sides(5, 5, 8)
    assert isosceles.description == "Obtuse isosceles triangle"
    assert isosceles.area == pytest.approx(12)
    assert isosceles.largest_angle_vertex == "C"


def test_decimal_right_triangle_survives_float_rounding() -> None:
    assert triangle_from_sides(0.3, 0.5, 0.4).angle_type == "right"


@pytest.mark.parametrize("sides", [(4, 5, 8), (7, 8, 9), (0.001, 1, 1), (1, 1, 1.999)])
def test_angles_sum_to_180_and_vertices_match_sides(sides: tuple[float, float, float]) -> None:
    tri = triangle_from_sides(*sides)
    assert sum(tri.angles) == pytest.approx(180)
    (ax, ay), (bx, by), (cx, cy) = tri.vertices()
    assert (ax, ay, by) == (0, 0, 0)
    assert cy > 0
    assert math.dist((bx, by), (cx, cy)) == pytest.approx(tri.a)
    assert math.dist((cx, cy), (ax, ay)) == pytest.approx(tri.b)
    assert math.dist((ax, ay), (bx, by)) == pytest.approx(tri.c)


@pytest.mark.parametrize(
    "sides",
    [(1, 2, 3), (0.1, 0.2, 0.3), (1, 2, 10), (0, 1, 1), (-1, 2, 2), (math.nan, 1, 1), (math.inf, 1, 1)],
)
def test_rejects_sides_that_cannot_form_a_triangle(sides: tuple[float, float, float]) -> None:
    with pytest.raises(TriangleError):
        triangle_from_sides(*sides)


def test_error_explains_the_triangle_inequality() -> None:
    with pytest.raises(TriangleError, match=r"add up to 3 \(1 \+ 2\).*longest side \(10\)"):
        triangle_from_sides(1, 2, 10)


def test_format_number_trims_trailing_zeros() -> None:
    assert format_number(6.0) == "6"
    assert format_number(2.5) == "2.5"
    assert format_number(36.86989) == "36.87"
    assert format_number(1234.5) == "1,234.5"


def test_svg_labels_vertices_and_sides() -> None:
    svg = triangle_svg(triangle_from_sides(3, 5, 4))
    assert svg.startswith("<svg") and svg.endswith("</svg>")
    for label in (">A<", ">B<", ">C<", ">a = 3<", ">b = 5<", ">c = 4<"):
        assert label in svg
    assert 'aria-label="Right scalene triangle with sides a = 3, b = 5, c = 4"' in svg


def test_svg_marks_only_right_angles() -> None:
    assert "<polyline" in triangle_svg(triangle_from_sides(3, 5, 4))
    assert "<polyline" not in triangle_svg(triangle_from_sides(5, 5, 5))


@pytest.mark.parametrize("sides", [(3, 5, 4), (1, 1, 1.999), (10, 10, 0.5), (1_000_000, 1_000_000, 1)])
def test_svg_scales_any_shape_into_the_canvas(sides: tuple[float, float, float]) -> None:
    svg = triangle_svg(triangle_from_sides(*sides), width=480, height=360)
    points = re.search(r'<polygon points="([^"]+)"', svg)
    assert points is not None
    for pair in points.group(1).split():
        x, y = (float(value) for value in pair.split(","))
        assert 0 <= x <= 480
        assert 0 <= y <= 360
