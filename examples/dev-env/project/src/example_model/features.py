"""Per-row derived features: one pure function per feature, applied by ``build``.

Level 2 of the feature rule. Joins, filters, and history aggregations belong in
the feature factory (SQL); fitted transforms such as scaling belong inside the
model pipeline. A function here takes the frame and returns one column. Prototype
it in a notebook cell with the same signature, then move it here and commit
before logging the run you intend to ship: the reference command refuses runs
from a dirty checkout.
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

FEATURES: dict[str, Callable[[pd.DataFrame], pd.Series]] = {}


def feature(fn: Callable[[pd.DataFrame], pd.Series]) -> Callable[[pd.DataFrame], pd.Series]:
    """Register ``fn`` under its own name."""
    FEATURES[fn.__name__] = fn
    return fn


@feature
def f3_ratio(frame: pd.DataFrame) -> pd.Series:
    return frame["f3"] / (frame["f2"].abs() + 1.0)


def build(frame: pd.DataFrame, names: list[str]) -> pd.DataFrame:
    """Return ``frame`` with every requested feature present, building the missing ones."""
    out = frame.copy()
    for name in names:
        if name in out.columns:
            continue
        if name not in FEATURES:
            raise KeyError(f"{name!r} is not a column and features.py does not define it")
        out[name] = FEATURES[name](out)
    return out
