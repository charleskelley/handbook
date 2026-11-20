#!/usr/bin/env python3
"""Generate the five-lens diagram on the customer-base audit method page.

Writes docs/assets/customer-base-audit-lenses-light.svg and -dark.svg. Each
panel is the same cohort-by-period grid with the slice one lens looks at
filled in. The framework is from Fader, Hardie, and Ross, The Customer-Base
Audit (2022); the drawing is the handbook's own.

Run:  uv run python scripts/customer_base_audit_diagram.py
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

N = 5                    # cohorts and periods shown
CELL = 22
PANEL_W = 152
GRID = N * CELL
GRID_X = (PANEL_W - GRID) / 2
GRID_Y = 52
HEIGHT = GRID_Y + GRID + 26

# Each lens: title, subtitle, and a test for whether cell (cohort, period) is in its slice.
LENSES = [
    ("Lens 1", "one period", lambda c, p: p == N - 1),
    ("Lens 2", "two periods", lambda c, p: p >= N - 2),
    ("Lens 3", "one cohort", lambda c, p: c == 0),
    ("Lens 4", "two cohorts", lambda c, p: c <= 1),
    ("Lens 5", "the whole base", lambda c, p: True),
]


def text(x, y, s, size, weight, fill, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="middle"{extra}>{s}</text>')


def panel(index: int, theme: dict) -> list[str]:
    title, subtitle, in_slice = LENSES[index]
    x0 = index * PANEL_W
    centre = x0 + PANEL_W / 2
    out = [
        text(centre, 18, title, 15, 600, theme["structure"]),
        text(centre, 37, subtitle, 13, 500, theme["text"]),
    ]
    # A cohort exists from the period it was acquired in, so the grid is a staircase.
    for cohort in range(N):
        for period in range(cohort, N):
            x = x0 + GRID_X + period * CELL
            y = GRID_Y + cohort * CELL
            if in_slice(cohort, period):
                fill, stroke = theme["accent"], theme["accent"]
            else:
                fill, stroke = "none", theme["muted"]
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL - 3}" height="{CELL - 3}" '
                       f'rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1.25"/>')
    if index == 0:
        out.append(text(centre, GRID_Y + GRID + 14, "period →", 12, 500, theme["text"]))
        lx, ly = x0 + GRID_X - 9, GRID_Y + GRID / 2
        out.append(text(lx, ly, "← cohort", 12, 500, theme["text"],
                        f' transform="rotate(-90 {lx:.1f} {ly:.1f})"'))
    return out


def render(theme: dict) -> str:
    width = PANEL_W * len(LENSES)
    body = [line for i in range(len(LENSES)) for line in panel(i, theme)]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {HEIGHT}" '
            f'width="{width}" height="{HEIGHT}" font-family="{FONT_STACK}">\n'
            + "\n".join(body) + "\n</svg>\n")


def main() -> None:
    for name, theme in THEMES.items():
        path = OUT / f"customer-base-audit-lenses-{name}.svg"
        path.write_text(render(theme), encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
