"""The evaluation fixture: a research run's holdout rows with its scores.

Saved to the governed bucket under the run id, and logged to the run with its
digest. Production scores the same rows; the gate compares. The fixture is a
concrete thing to point at when asking "what did research get, on what data".
"""

from __future__ import annotations

import hashlib
import io
import json

import fsspec
import pandas as pd

from example_model.config import Settings


def uri_for(settings: Settings, run_id: str) -> str:
    return f"{settings.fixture_bucket.rstrip('/')}/{settings.model_name}/{run_id}"


def digest(frame: pd.DataFrame) -> str:
    """A content hash that is the same wherever the frame is read."""
    buf = io.BytesIO()
    frame.sort_index(axis=1).to_parquet(buf, index=False)
    return hashlib.sha256(buf.getvalue()).hexdigest()


def save(
    settings: Settings, run_id: str, holdout: pd.DataFrame, metrics: dict[str, float]
) -> tuple[str, str]:
    """Write the fixture. Returns its URI and digest."""
    uri = uri_for(settings, run_id)
    with fsspec.open(f"{uri}/holdout.parquet", "wb") as f:
        holdout.to_parquet(f, index=False)
    with fsspec.open(f"{uri}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    return uri, digest(holdout)


def load(uri: str) -> tuple[pd.DataFrame, dict[str, float]]:
    with fsspec.open(f"{uri.rstrip('/')}/holdout.parquet", "rb") as f:
        holdout = pd.read_parquet(f)
    with fsspec.open(f"{uri.rstrip('/')}/metrics.json") as f:
        metrics = json.load(f)
    return holdout, metrics
