"""Triangle geometry for the Triangle page: solve from three sides and draw it as SVG."""

from __future__ import annotations

import html
import math
from dataclasses import dataclass


REL_TOL = 1e-9
VERTEX_NAMES = ("A", "B", "C")
SIDE_NAMES = ("a", "b", "c")


class TriangleError(ValueError):
    """Raised when three lengths cannot form a triangle."""


def format_number(value: float, digits: int = 2) -> str:
    text = f"{value:,.{digits}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _close(x: float, y: float) -> bool:
    return math.isclose(x, y, rel_tol=REL_TOL)


def _angle(opposite: float, side1: float, side2: float) -> float:
    cosine = (side1**2 + side2**2 - opposite**2) / (2 * side1 * side2)
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


def _area(a: float, b: float, c: float) -> float:
    # Kahan's form of Heron's formula stays accurate for needle-like triangles.
    x, y, z = sorted((a, b, c), reverse=True)
    product = (x + (y + z)) * (z - (x - y)) * (z + (x - y)) * (x + (y - z))
    return 0.25 * math.sqrt(max(product, 0.0))


@dataclass(frozen=True)
class Triangle:
    """Triangle ABC where each side is named after the vertex it faces: a = BC, b = CA, c = AB."""

    a: float
    b: float
    c: float
    angle_a: float
    angle_b: float
    angle_c: float
    area: float

    @property
    def sides(self) -> tuple[float, float, float]:
        return (self.a, self.b, self.c)

    @property
    def angles(self) -> tuple[float, float, float]:
        return (self.angle_a, self.angle_b, self.angle_c)

    @property
    def perimeter(self) -> float:
        return self.a + self.b + self.c

    @property
    def heights(self) -> tuple[float, float, float]:
        """Height onto each side, in the order a, b, c."""
        return (2 * self.area / self.a, 2 * self.area / self.b, 2 * self.area / self.c)

    @property
    def inradius(self) -> float:
        return 2 * self.area / self.perimeter

    @property
    def circumradius(self) -> float:
        return self.a * self.b * self.c / (4 * self.area)

    @property
    def side_type(self) -> str:
        equal_pairs = sum(
            (_close(self.a, self.b), _close(self.b, self.c), _close(self.c, self.a))
        )
        if equal_pairs == 3:
            return "equilateral"
        if equal_pairs >= 1:
            return "isosceles"
        return "scalene"

    @property
    def angle_type(self) -> str:
        shortest, middle, longest = sorted(self.sides)
        legs = shortest**2 + middle**2
        if _close(legs, longest**2):
            return "right"
        return "obtuse" if legs < longest**2 else "acute"

    @property
    def largest_angle_vertex(self) -> str:
        return VERTEX_NAMES[self.sides.index(max(self.sides))]

    @property
    def description(self) -> str:
        return f"{self.angle_type.capitalize()} {self.side_type} triangle"

    def vertices(self) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
        """A at the origin, B on the positive x-axis, C above the x-axis."""
        cx = (self.b**2 + self.c**2 - self.a**2) / (2 * self.c)
        cy = 2 * self.area / self.c
        return ((0.0, 0.0), (self.c, 0.0), (cx, cy))


def triangle_from_sides(a: float, b: float, c: float) -> Triangle:
    """Solve a triangle from its three side lengths (SSS)."""
    sides = (float(a), float(b), float(c))
    if any(not math.isfinite(side) or side <= 0 for side in sides):
        raise TriangleError("Every side must be a number greater than 0.")
    shortest, middle, longest = sorted(sides)
    if shortest + middle < longest or _close(shortest + middle, longest):
        raise TriangleError(
            "These sides can't form a triangle: the two shorter sides add up to "
            f"{format_number(shortest + middle)} ({format_number(shortest)} + "
            f"{format_number(middle)}), but together they must be longer than the "
            f"longest side ({format_number(longest)})."
        )
    a, b, c = sides
    return Triangle(
        a=a,
        b=b,
        c=c,
        angle_a=_angle(a, b, c),
        angle_b=_angle(b, c, a),
        angle_c=_angle(c, a, b),
        area=_area(a, b, c),
    )


def _unit(dx: float, dy: float) -> tuple[float, float]:
    length = math.hypot(dx, dy) or 1.0
    return (dx / length, dy / length)


def triangle_svg(
    tri: Triangle,
    *,
    width: int = 480,
    height: int = 360,
    padding: int = 56,
) -> str:
    """Draw the triangle to scale, with vertex names, side lengths, and a right-angle mark."""
    points = tri.vertices()
    min_x = min(x for x, _ in points)
    span_x = max(x for x, _ in points) - min_x
    span_y = max(y for _, y in points)
    scale = min((width - 2 * padding) / span_x, (height - 2 * padding) / span_y)
    offset_x = (width - span_x * scale) / 2
    offset_y = (height - span_y * scale) / 2
    screen = [
        (offset_x + (x - min_x) * scale, height - offset_y - y * scale) for x, y in points
    ]
    centroid_x = sum(x for x, _ in screen) / 3
    centroid_y = sum(y for _, y in screen) / 3

    def fmt(value: float) -> str:
        return f"{value:.1f}"

    summary = html.escape(_summary(tri))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" overflow="visible" role="img" aria-label="{summary}">',
        f"<title>{summary}</title>",
        '<polygon points="'
        + " ".join(f"{fmt(x)},{fmt(y)}" for x, y in screen)
        + '" fill="#E7F4F1" stroke="#2F7A72" stroke-width="3" stroke-linejoin="round"/>',
    ]

    if tri.angle_type == "right":
        corner = VERTEX_NAMES.index(tri.largest_angle_vertex)
        vx, vy = screen[corner]
        neighbours = [screen[i] for i in range(3) if i != corner]
        reach = min(math.hypot(px - vx, py - vy) for px, py in neighbours)
        size = min(16.0, reach * 0.25)
        (ux1, uy1), (ux2, uy2) = (_unit(px - vx, py - vy) for px, py in neighbours)
        mark = (
            (vx + ux1 * size, vy + uy1 * size),
            (vx + (ux1 + ux2) * size, vy + (uy1 + uy2) * size),
            (vx + ux2 * size, vy + uy2 * size),
        )
        parts.append(
            '<polyline points="'
            + " ".join(f"{fmt(x)},{fmt(y)}" for x, y in mark)
            + '" fill="none" stroke="#2F7A72" stroke-width="2"/>'
        )

    for index, name in enumerate(VERTEX_NAMES):
        vx, vy = screen[index]
        ux, uy = _unit(vx - centroid_x, vy - centroid_y)
        parts.append(f'<circle cx="{fmt(vx)}" cy="{fmt(vy)}" r="4.5" fill="#2F7A72"/>')
        parts.append(
            f'<text x="{fmt(vx + ux * 20)}" y="{fmt(vy + uy * 20)}" text-anchor="middle" '
            f'dominant-baseline="central" font-size="18" font-weight="700" '
            f'fill="#24302E">{name}</text>'
        )

    for index, name in enumerate(SIDE_NAMES):
        (px, py), (qx, qy) = (screen[i] for i in range(3) if i != index)
        mx, my = (px + qx) / 2, (py + qy) / 2
        nx, ny = _unit(-(qy - py), qx - px)
        if nx * (mx - centroid_x) + ny * (my - centroid_y) < 0:
            nx, ny = -nx, -ny
        label = f"{name} = {format_number(tri.sides[index])}"
        # Push the label's estimated text box fully off the side, whatever the side's slope.
        half_width, half_height = len(label) * 14 * 0.3, 7
        offset = 6 + abs(nx) * half_width + abs(ny) * half_height
        parts.append(
            f'<text x="{fmt(mx + nx * offset)}" y="{fmt(my + ny * offset)}" text-anchor="middle" '
            f'dominant-baseline="central" font-size="14" font-weight="600" '
            f'fill="#4A5A57">{html.escape(label)}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)


def _summary(tri: Triangle) -> str:
    sides = ", ".join(
        f"{name} = {format_number(side)}" for name, side in zip(SIDE_NAMES, tri.sides)
    )
    return f"{tri.description} with sides {sides}"
