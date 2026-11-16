#!/usr/bin/env python3
"""Generate the landscape diagram on the Methods page.

Writes docs/assets/dpom-landscape-light.svg and dpom-landscape-dark.svg. The
layout is DPOM's landscape (v0.3.0, CC BY 4.0, Charles Kelley) with the
handbook's colours, set in a system sans-serif stack and sized to read at the
site's content width, about 760px on a wide screen.

Run:  uv run --with pillow python scripts/dpom_diagram.py
Pillow is used only to measure text for line wrapping; without it the script
falls back to an average character width.
"""

from __future__ import annotations

import pathlib
import textwrap

OUT = pathlib.Path(__file__).resolve().parent.parent / "docs" / "assets"
FONT_STACK = "'Avenir Next', Avenir, 'Helvetica Neue', Helvetica, Arial, sans-serif"
FONT_FILE = "/System/Library/Fonts/Avenir Next.ttc"
FACE = {400: 7, 500: 5, 600: 2}  # face index in the collection

# `muted` is for lines, arrowheads, and band outlines. `text` is the same grey
# two steps darker (lighter on dark), so small text clears 7:1 contrast on the
# page and on the band tint; at ~15px the muted grey reads as blurred.
THEMES = {
    "light": dict(structure="#1c2024", muted="#6b7b86", text="#4b5861",
                  accent="#126128", accent2="#1b7d36", record="#22a04b"),
    "dark": dict(structure="#e6eaed", muted="#8a97a1", text="#aab4bc",
                 accent="#5cc47a", accent2="#86d99c", record="#4ade80"),
}

# ---- type scale (SVG units; the page scales the whole drawing by ~0.69) ----
T_TITLE = (30, 600)      # region titles
T_DESC = (22, 500)       # region descriptions
LH_DESC = 28
T_SUB = (15, 600)        # START HERE
T_BAND_T = (28, 600)     # band titles
T_BAND_D = (21, 400)     # band descriptions
T_LABEL = (21, 500)      # Drift, Cost, Audit & Replay
LH_LABEL = 26
T_PILL_T = (28, 600)
T_PILL_S = (20, 500)
T_DECISION = (22, 600)

# ---- geometry ----
M = 4                    # margin for stroke clearance
BOX_W, BOX_H = 210, 290
GAP = 40                 # between Data/Prediction and Outcome/Measure
ZONE = 170               # Prediction -> Outcome, holding the diamond
Y_BOX = 150
PILL_W, PILL_H, Y_PILL = 320, 86, 8
Y_LOOP = Y_PILL + PILL_H / 2
DIAMOND = 64             # half-diagonal
ARROW_GAP = 110          # boxes -> Monitor band (room for Drift labels)
BAND_H, BAND_GAP = 76, 12
STROKE = 2.5
PAD = 11                 # text inset inside boxes
DESC_TOP = 92            # description block starts below title and subtitle

X = [M, M + BOX_W + GAP]
X.append(X[1] + BOX_W + ZONE)
X.append(X[2] + BOX_W + GAP)
W = X[3] + BOX_W + M
CY = Y_BOX + BOX_H / 2
CX_DIAMOND = X[1] + BOX_W + ZONE / 2
Y_MON = Y_BOX + BOX_H + ARROW_GAP
Y_INF = Y_MON + BAND_H + BAND_GAP
H = Y_INF + BAND_H + M
X_COST = X[3] + BOX_W / 2  # the Cost line rises into Measure's centre

REGIONS = [
    ("Data", "Business records and signals, transformed into a trusted foundation that grounds decisions", False),
    ("Prediction", "Any method, from rules to large models, that produces decisions the business acts on", False),
    ("Outcome", "The business result the organization has aligned on, driven by recorded decisions", True),
    ("Measure", "The outcome’s impact quantified, financially or as a stated proxy, via counterfactual attribution", False),
]


def measure(size: int, weight: int):
    try:
        from PIL import ImageFont
        font = ImageFont.truetype(FONT_FILE, size, index=FACE[weight])
        return lambda s: font.getlength(s)
    except Exception:  # noqa: BLE001
        return lambda s: 0.53 * size * len(s)


def _greedy(words: list[str], width: float, length) -> list[str]:
    lines, line = [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if line and length(trial) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def wrap(text: str, width: float, size: int, weight: int) -> list[str]:
    """Wrap to the fewest lines that fit, then even the line lengths out.

    Greedy wrapping leaves a short last line and stray single words. Keeping
    the same line count while narrowing the width until it would need one
    more line gives balanced lines, which read faster when centred.
    """
    length = measure(size, weight)
    words = text.split()
    best = _greedy(words, width, length)
    n = len(best)
    lo, hi = max(length(w) for w in words), width
    while hi - lo > 1:
        mid = (lo + hi) / 2
        cand = _greedy(words, mid, length)
        if len(cand) == n:
            best, hi = cand, mid
        else:
            lo = mid
    return best


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;")


def text(x, y, s, size, weight, fill, anchor="middle", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def lines(x, y, items, size, weight, fill, lh, anchor="middle"):
    spans = "".join(
        f'<tspan x="{x:.1f}" dy="{0 if i == 0 else lh}">{esc(s)}</tspan>'
        for i, s in enumerate(items))
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{spans}</text>')


def rrect(x, y, w, h, r, stroke, sw, fill="none", fo=1):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" fill-opacity="{fo}" stroke="{stroke}" stroke-width="{sw}"/>')


def path(d, stroke, sw=STROKE, marker=None, fill="none", fo=1):
    m = f' marker-end="url(#{marker})"' if marker else ""
    return (f'<path d="{d}" fill="{fill}" fill-opacity="{fo}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{m}/>')


def build(theme: str) -> str:
    c = THEMES[theme]
    out = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
      f'width="{W:.0f}" height="{H:.0f}" font-family="{FONT_STACK}" role="img" '
      f'aria-labelledby="t">')
    a('<title id="t">The DPOM landscape: Data, Prediction, Outcome, and Measure, '
      'the decision handoff, the outcome loop, and the Monitor and Govern and '
      'Infrastructure bands</title>')
    a('<defs>')
    for mid, col in (("arrow-muted", c["muted"]), ("arrow-accent", c["accent"])):
        a(f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="12" '
          f'markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
          f'<path d="M 0 0 L 10 5 L 0 10 Z" fill="{col}"/></marker>')
    a('</defs>')

    # Bands
    mon_right = X[2] + BOX_W
    a(rrect(M, Y_MON, mon_right - M, BAND_H, 10, c["muted"], 1.5, c["muted"], 0.1))
    a(rrect(M, Y_INF, W - 2 * M, BAND_H, 10, c["muted"], 1.5, c["muted"], 0.1))
    bx = (M + mon_right) / 2
    a(text(bx, Y_MON + 33, "Monitor & Govern", *T_BAND_T, c["structure"]))
    a(text(bx, Y_MON + 61, "health, drift, risk, audit, and the operational cost", *T_BAND_D, c["text"]))
    a(text(W / 2, Y_INF + 33, "Infrastructure", *T_BAND_T, c["structure"]))
    a(text(W / 2, Y_INF + 61, "platform the landscape runs on; the billed cost of data, compute, and serving", *T_BAND_D, c["text"]))

    # Cost: both bands feed one arrow rising into Measure
    y_mid_mon = Y_MON + BAND_H / 2
    a(path(f"M {X_COST:.1f} {Y_INF:.1f} L {X_COST:.1f} {y_mid_mon:.1f}", c["muted"]))
    a(path(f"M {mon_right:.1f} {y_mid_mon:.1f} L {X_COST:.1f} {y_mid_mon:.1f} "
           f"L {X_COST:.1f} {Y_BOX + BOX_H + 6:.1f}", c["muted"], marker="arrow-muted"))
    a(text(X_COST + 14, (Y_BOX + BOX_H + y_mid_mon) / 2 + 7, "Cost", *T_LABEL, c["text"], anchor="start"))

    # Regions
    for i, (title, desc, entry) in enumerate(REGIONS):
        x = X[i]
        cx = x + BOX_W / 2
        sw = STROKE * 2 if entry else STROKE
        a(rrect(x, Y_BOX, BOX_W, BOX_H, 16, c["accent"], sw))
        a(text(cx, Y_BOX + 46, title, *T_TITLE, c["structure"]))
        if entry:
            a(text(cx, Y_BOX + 72, "START HERE", *T_SUB, c["accent2"], extra=' letter-spacing="1.5"'))
        body = wrap(desc, BOX_W - 2 * PAD, *T_DESC)
        avail = BOX_H - DESC_TOP - PAD
        block = (len(body) - 1) * LH_DESC + T_DESC[0]
        y0 = Y_BOX + DESC_TOP + (avail - block) / 2 + T_DESC[0] * 0.78
        a(lines(cx, y0, body, *T_DESC, c["text"], LH_DESC))
        # Drift arrows for Data, Prediction, Outcome
        if i < 3:
            a(path(f"M {cx:.1f} {Y_BOX + BOX_H + 2:.1f} L {cx:.1f} {Y_MON - 3:.1f}", c["muted"], marker="arrow-muted"))
            a(text(cx + 14, (Y_BOX + BOX_H + Y_MON) / 2 + 7, "Drift", *T_LABEL, c["text"], anchor="start"))

    # Flow arrows between regions
    y = CY
    a(path(f"M {X[0] + BOX_W + 2:.1f} {y:.1f} L {X[1] - 3:.1f} {y:.1f}", c["accent"], marker="arrow-accent"))
    a(path(f"M {X[1] + BOX_W + 2:.1f} {y:.1f} L {CX_DIAMOND - DIAMOND - 3:.1f} {y:.1f}", c["accent"], marker="arrow-accent"))
    a(path(f"M {CX_DIAMOND + DIAMOND + 2:.1f} {y:.1f} L {X[2] - 3:.1f} {y:.1f}", c["accent"], marker="arrow-accent"))
    a(path(f"M {X[2] + BOX_W + 2:.1f} {y:.1f} L {X[3] - 3:.1f} {y:.1f}", c["accent"], marker="arrow-accent"))

    # Decision diamond and its Audit & Replay arrow
    d = DIAMOND
    a(path(f"M {CX_DIAMOND:.1f} {CY - d:.1f} L {CX_DIAMOND + d:.1f} {CY:.1f} "
           f"L {CX_DIAMOND:.1f} {CY + d:.1f} L {CX_DIAMOND - d:.1f} {CY:.1f} Z",
           c["record"], sw=3, fill=c["record"], fo=0.1))
    a(text(CX_DIAMOND, CY + 8, "Decision", *T_DECISION, c["record"]))
    a(path(f"M {CX_DIAMOND:.1f} {CY + d + 2:.1f} L {CX_DIAMOND:.1f} {Y_MON - 3:.1f}", c["muted"], marker="arrow-muted"))
    a(lines(CX_DIAMOND + 14, (Y_BOX + BOX_H + Y_MON) / 2 - 5, ["Audit &", "Replay"], *T_LABEL, c["text"], LH_LABEL, anchor="start"))

    # Outcome loop: pill, and the line from Measure around to Prediction and Data
    px = W / 2 - PILL_W / 2
    a(rrect(px, Y_PILL, PILL_W, PILL_H, 16, c["accent"], STROKE, c["accent"], 0.06))
    a(text(W / 2, Y_PILL + 38, "Outcome Loop", *T_PILL_T, c["structure"]))
    a(text(W / 2, Y_PILL + 67, "scale • sustain • fix • retire", *T_PILL_S, c["accent2"]))
    x_meas = X[3] + BOX_W / 2
    a(path(f"M {x_meas:.1f} {Y_BOX - 2:.1f} L {x_meas:.1f} {Y_LOOP:.1f} L {px + PILL_W + 3:.1f} {Y_LOOP:.1f}",
           c["accent"], marker="arrow-accent"))
    x_pred = X[1] + BOX_W / 2
    x_data = X[0] + BOX_W / 2
    a(path(f"M {px - 2:.1f} {Y_LOOP:.1f} L {x_data:.1f} {Y_LOOP:.1f} L {x_data:.1f} {Y_BOX - 3:.1f}",
           c["accent"], marker="arrow-accent"))
    a(path(f"M {x_pred:.1f} {Y_LOOP:.1f} L {x_pred:.1f} {Y_BOX - 3:.1f}", c["accent"], marker="arrow-accent"))

    a('</svg>')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for theme in THEMES:
        p = OUT / f"dpom-landscape-{theme}.svg"
        p.write_text(build(theme))
        print(f"wrote {p.relative_to(OUT.parent.parent)}  ({W:.0f}x{H:.0f})")
