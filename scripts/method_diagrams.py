#!/usr/bin/env python3
"""Generate the small figures on the method pages.

Writes a light and a dark SVG for each figure into docs/assets/:

  survival-curve       a Kaplan-Meier curve for the worked example on the
                       survival analysis page
  did                  difference-in-differences: two groups, before and after
  synthetic-control    a treated series and its synthetic comparison
  rolling-origin       the splits of a rolling-origin backtest
  prediction-timeline  observation window, as-of date, outcome window

The drawings are the handbook's own. Any figures in them are the made-up
figures of the worked example on the page that shows them.

Run:  uv run python scripts/method_diagrams.py
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


def text(x, y, s, fill, size=12, weight=400, anchor="middle", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{s}</text>')


def line(x1, y1, x2, y2, stroke, width=1.0, dash="", opacity=1.0):
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
            f'stroke-width="{width}" stroke-opacity="{opacity}"{dashed}/>')


def path(points, stroke, width=2.0, dash=""):
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(points))
    return (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" '
            f'stroke-linejoin="round" stroke-linecap="round"{dashed}/>')


def rect(x, y, w, h, stroke, fill="none", fill_opacity=1.0, width=1.5):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="{fill}" '
            f'fill-opacity="{fill_opacity}" stroke="{stroke}" stroke-width="{width}"/>')


def svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" font-family="{FONT_STACK}">\n'
            + "\n".join(body) + "\n</svg>\n")


class Plot:
    """A plot area that maps data coordinates to pixels."""

    def __init__(self, left, top, width, height, x_range, y_range):
        self.left, self.top, self.width, self.height = left, top, width, height
        self.x_range, self.y_range = x_range, y_range

    def x(self, value):
        lo, hi = self.x_range
        return self.left + (value - lo) / (hi - lo) * self.width

    def y(self, value):
        lo, hi = self.y_range
        return self.top + self.height - (value - lo) / (hi - lo) * self.height

    def xy(self, points):
        return [(self.x(a), self.y(b)) for a, b in points]

    def axes(self, theme):
        bottom = self.top + self.height
        return [line(self.left, bottom, self.left + self.width, bottom, theme["muted"]),
                line(self.left, self.top, self.left, bottom, theme["muted"])]


def survival_curve(theme):
    """Ten subscribers: events at months 1, 2, 2, 5; censored at 3, 4, 6, 6, 6, 6."""
    plot = Plot(64, 16, 420, 200, (0, 6), (0, 1))
    out = plot.axes(theme)
    for level in (0.25, 0.5, 0.75, 1.0):
        out.append(line(plot.left, plot.y(level), plot.left + plot.width, plot.y(level),
                        theme["muted"], 0.6, "2 4", 0.7))
    for level in (0, 0.25, 0.5, 0.75, 1.0):
        out.append(text(plot.left - 8, plot.y(level) + 4, f"{level:.0%}", theme["text"], anchor="end"))
    for month in range(7):
        out.append(text(plot.x(month), plot.top + plot.height + 18, month, theme["text"]))
    steps = [(0, 1), (1, 1), (1, 0.9), (2, 0.9), (2, 0.7), (5, 0.7), (5, 0.56), (6, 0.56)]
    out.append(path(plot.xy(steps), theme["accent"], 2.5))
    for month, level in ((3, 0.7), (4, 0.7), (6, 0.56)):
        out.append(line(plot.x(month), plot.y(level) - 7, plot.x(month), plot.y(level) + 7,
                        theme["structure"], 1.5))
    for month, level, label in ((1.5, 0.9, "90%"), (3.5, 0.7, "70%"), (5.5, 0.56, "56%")):
        out.append(text(plot.x(month), plot.y(level) - 12, label, theme["structure"], 12, 600))
    out.append(text(plot.left + plot.width / 2, plot.top + plot.height + 40,
                    "months since the subscription started", theme["text"], 13, 500))
    out.append(text(plot.x(3.5), plot.y(0.7) + 24, "tick: a customer censored", theme["muted"], 11))
    lx, ly = 16, plot.top + plot.height / 2
    out.append(text(lx, ly, "still subscribed", theme["text"], 13, 500,
                    extra=f' transform="rotate(-90 {lx:.1f} {ly:.1f})"'))
    return svg(504, 266, out)


def did(theme):
    """Treated 100 to 120, comparison 80 to 90: an effect of 10."""
    plot = Plot(56, 20, 300, 200, (0, 1), (70, 125))
    bottom = plot.top + plot.height
    out = plot.axes(theme)
    out.append(line(plot.x(0.5), plot.top, plot.x(0.5), bottom, theme["muted"], 1, "4 4"))
    out.append(text(plot.x(0.5), plot.top - 6, "the change", theme["muted"], 11))
    out.append(text(plot.x(0), bottom + 18, "before", theme["text"], 13, 500))
    out.append(text(plot.x(1), bottom + 18, "after", theme["text"], 13, 500))
    for value in (80, 90, 100, 110, 120):
        out.append(text(plot.left - 8, plot.y(value) + 4, value, theme["text"], anchor="end"))
    out.append(path(plot.xy([(0, 80), (1, 90)]), theme["muted"], 2.5))
    out.append(path(plot.xy([(0, 100), (1, 110)]), theme["accent"], 2, "6 5"))
    out.append(path(plot.xy([(0, 100), (1, 120)]), theme["accent"], 2.5))
    right = plot.x(1)
    out.append(text(right + 30, plot.y(120) + 4, "treated", theme["structure"], 12, 600, "start"))
    out.append(text(right + 30, plot.y(110) + 4, "treated, had it moved", theme["text"], 12, 400, "start"))
    out.append(text(right + 30, plot.y(110) + 19, "as the comparison did", theme["text"], 12, 400, "start"))
    out.append(text(right + 30, plot.y(90) + 4, "comparison", theme["structure"], 12, 600, "start"))
    out.append(line(right + 12, plot.y(120), right + 12, plot.y(110), theme["structure"], 1.5))
    out.append(line(right + 8, plot.y(120), right + 16, plot.y(120), theme["structure"], 1.5))
    out.append(line(right + 8, plot.y(110), right + 16, plot.y(110), theme["structure"], 1.5))
    out.append(text(right + 30, plot.y(115) + 4, "effect: 10", theme["accent"], 12, 600, "start"))
    return svg(540, 250, out)


def synthetic_control(theme):
    """A treated series and a weighted mix of untreated ones. Schematic, no data."""
    treated = [50, 53, 51, 55, 54, 58, 57, 60, 59, 63, 62, 65, 70, 74, 75, 79, 80, 83, 85, 88]
    synthetic = [51, 52, 52, 54, 55, 57, 58, 59, 60, 62, 63, 65, 66, 68, 68, 71, 71, 73, 74, 76]
    start = 11  # index of the last period before the change
    plot = Plot(40, 20, 430, 190, (0, len(treated) - 1), (45, 92))
    bottom = plot.top + plot.height
    out = plot.axes(theme)
    gap = [(i, treated[i]) for i in range(start, len(treated))]
    gap += [(i, synthetic[i]) for i in range(len(treated) - 1, start - 1, -1)]
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(plot.xy(gap)))
    out.append(f'<path d="{d} Z" fill="{theme["accent"]}" fill-opacity="0.18" stroke="none"/>')
    out.append(line(plot.x(start), plot.top, plot.x(start), bottom, theme["muted"], 1, "4 4"))
    out.append(text(plot.x(start), plot.top - 6, "the change", theme["muted"], 11))
    out.append(path(plot.xy(list(enumerate(synthetic))), theme["muted"], 2, "6 5"))
    out.append(path(plot.xy(list(enumerate(treated))), theme["accent"], 2.5))
    out.append(text(plot.x(start / 2), bottom + 18, "before: the weights are fitted here",
                    theme["text"], 12))
    out.append(text(plot.x((start + len(treated) - 1) / 2), bottom + 18, "after: the gap is the estimate",
                    theme["text"], 12))
    out.append(text(plot.x(19) + 8, plot.y(88) + 4, "treated", theme["structure"], 12, 600, "start"))
    out.append(text(plot.x(19) + 8, plot.y(76) + 4, "synthetic", theme["structure"], 12, 600, "start"))
    return svg(550, 246, out)


def rolling_origin(theme):
    """Four forecast origins, each scored on the periods after it."""
    left, top, unit, bar, step = 96, 34, 26, 20, 34
    periods, horizon, first_origin = 15, 3, 6
    out = [text(left + first_origin * unit / 2, top - 12, "history used to fit", theme["text"], 12),
           text(left + (first_origin + 1.5) * unit, top - 12, "scored", theme["text"], 12)]
    for row in range(4):
        y, origin = top + row * step, first_origin + row * 2
        out.append(text(left - 10, y + bar / 2 + 4, f"origin {row + 1}", theme["text"], 12, 500, "end"))
        out.append(rect(left, y, origin * unit - 2, bar, theme["accent"], theme["accent"], 0.28))
        out.append(rect(left + origin * unit, y, horizon * unit - 2, bar, theme["structure"]))
    axis = top + 4 * step + 4
    out.append(line(left, axis, left + periods * unit, axis, theme["muted"]))
    out.append(text(left + periods * unit / 2, axis + 18, "time →", theme["text"], 12, 500))
    return svg(left + periods * unit + 20, axis + 30, out)


def prediction_timeline(theme):
    """What a prediction may see and what it is scored on."""
    left, top, bar = 20, 40, 34
    observation, gap, outcome = 260, 40, 170
    as_of = left + observation
    out = [rect(left, top, observation - 2, bar, theme["accent"], theme["accent"], 0.28),
           text(left + observation / 2, top + bar / 2 + 4, "observation window: features",
                theme["structure"], 12, 600),
           rect(as_of + gap, top, outcome, bar, theme["structure"]),
           text(as_of + gap + outcome / 2, top + bar / 2 + 4, "outcome window: label",
                theme["structure"], 12, 600),
           line(as_of, top - 16, as_of, top + bar + 16, theme["structure"], 2),
           text(as_of, top - 22, "as-of date: the prediction is made", theme["structure"], 12, 600),
           text(as_of + gap / 2, top + bar + 14, "gap", theme["muted"], 11),
           line(left, top + bar + 34, as_of + gap + outcome, top + bar + 34, theme["muted"]),
           text(left + (observation + gap + outcome) / 2, top + bar + 52, "time →", theme["text"], 12, 500)]
    return svg(left + observation + gap + outcome + 20, top + bar + 62, out)


FIGURES = {
    "survival-curve": survival_curve,
    "did": did,
    "synthetic-control": synthetic_control,
    "rolling-origin": rolling_origin,
    "prediction-timeline": prediction_timeline,
}


def main() -> None:
    for name, render in FIGURES.items():
        for theme_name, theme in THEMES.items():
            target = OUT / f"{name}-{theme_name}.svg"
            target.write_text(render(theme), encoding="utf-8")
            print(f"wrote {target}")


if __name__ == "__main__":
    main()
