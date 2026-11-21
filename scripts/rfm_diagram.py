#!/usr/bin/env python3
"""Generate the recency-by-frequency grid on the RFM analysis method page.

Writes docs/assets/rfm-grid-light.svg and -dark.svg: a five-by-five grid of
recency score against frequency score, with the four corners named. The
drawing is the handbook's own and carries no data.

Run:  uv run python scripts/rfm_diagram.py
"""

from __future__ import annotations

import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "docs" / "assets"
FONT_STACK = "'Avenir Next', Avenir, 'Helvetica Neue', Helvetica, Arial, sans-serif"

# The same colours as the landscape diagram (scripts/dpom_diagram.py).
THEMES = {
    "light": dict(structure="#1c2024", muted="#6b7b86", text="#4b5861", accent="#126128"),
    "dark": dict(structure="#e6eaed", muted="#8a97a1", text="#aab4bc", accent="#5cc47a"),
}

N = 5                    # scores per measure
CELL = 52
GRID = N * CELL
LEFT = 64                # room for the frequency axis
TOP = 12
WIDTH = LEFT + GRID + 16
HEIGHT = TOP + GRID + 58

# Each corner: recency scores, frequency scores, two label lines, fill opacity.
CORNERS = [
    ((4, 5), (4, 5), ("Recent and", "frequent"), 0.30),
    ((4, 5), (1, 2), ("Recent,", "few orders"), 0.16),
    ((1, 2), (4, 5), ("Frequent,", "not recent"), 0.16),
    ((1, 2), (1, 2), ("Few orders,", "not recent"), 0.06),
]


def text(x, y, s, size, weight, fill, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="middle"{extra}>{s}</text>')


def col_x(recency: int) -> float:
    """Left edge of a recency score's column. Score 5, most recent, is on the right."""
    return LEFT + (recency - 1) * CELL


def row_y(frequency: int) -> float:
    """Top edge of a frequency score's row. Score 5, most orders, is at the top."""
    return TOP + (N - frequency) * CELL


def render(theme: dict) -> str:
    out = []
    for recency in range(1, N + 1):
        for frequency in range(1, N + 1):
            # The corners are drawn as one block each, so their cells are skipped.
            if recency != 3 and frequency != 3:
                continue
            out.append(f'<rect x="{col_x(recency) + 1.5:.1f}" y="{row_y(frequency) + 1.5:.1f}" '
                       f'width="{CELL - 3}" height="{CELL - 3}" rx="2" fill="none" '
                       f'stroke="{theme["muted"]}" stroke-width="1" stroke-opacity="0.6"/>')
    for (r_lo, r_hi), (f_lo, f_hi), lines, opacity in CORNERS:
        x, y = col_x(r_lo), row_y(f_hi)
        w, h = (r_hi - r_lo + 1) * CELL, (f_hi - f_lo + 1) * CELL
        out.append(f'<rect x="{x + 1.5:.1f}" y="{y + 1.5:.1f}" width="{w - 3}" height="{h - 3}" '
                   f'rx="3" fill="{theme["accent"]}" fill-opacity="{opacity}" '
                   f'stroke="{theme["accent"]}" stroke-width="1.5"/>')
        cx, cy = x + w / 2, y + h / 2
        out.append(text(cx, cy - 3, lines[0], 13, 600, theme["structure"]))
        out.append(text(cx, cy + 14, lines[1], 13, 600, theme["structure"]))
    for score in range(1, N + 1):
        out.append(text(col_x(score) + CELL / 2, TOP + GRID + 17, score, 12, 500, theme["text"]))
        out.append(text(LEFT - 12, row_y(score) + CELL / 2 + 4, score, 12, 500, theme["text"]))
    out.append(text(LEFT + GRID / 2, TOP + GRID + 37, "recency score →", 13, 500, theme["text"]))
    out.append(text(LEFT + GRID / 2, TOP + GRID + 52, "5 is the most recent", 11, 400,
                    theme["muted"]))
    lx, ly = LEFT - 34, TOP + GRID / 2
    out.append(text(lx, ly, "frequency score →", 13, 500, theme["text"],
                    f' transform="rotate(-90 {lx:.1f} {ly:.1f})"'))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
            f'width="{WIDTH}" height="{HEIGHT}" font-family="{FONT_STACK}">\n'
            + "\n".join(out) + "\n</svg>\n")


def main() -> None:
    for name, theme in THEMES.items():
        path = OUT / f"rfm-grid-{name}.svg"
        path.write_text(render(theme), encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
