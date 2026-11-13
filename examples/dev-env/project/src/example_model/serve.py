"""Prediction lookup on Cloud Run: the latest batch scores, served by entity id.

Serving is batch first. This app does not run the model; it answers from the
output table of the last scoring job, held in memory and re-read when stale.
Real-time scoring, if latency or freshness ever require it, is a separate app
that loads the model the way ``score.py`` does, and a decision record.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Prediction(BaseModel):
    entity_id: str
    score: float
    model_version: str | None = None
    scored_at: str | None = None


class LatestScores:
    """An in-memory copy of the latest batch, refreshed when older than the TTL."""

    def __init__(self, load: Callable[[], pd.DataFrame], ttl_seconds: int) -> None:
        self._load = load
        self._ttl = ttl_seconds
        self._lock = threading.Lock()
        self._frame: pd.DataFrame | None = None
        self._loaded_at = 0.0

    def get(self, entity_id: str) -> dict | None:
        with self._lock:
            if self._frame is None or time.monotonic() - self._loaded_at > self._ttl:
                self._frame = self._load().set_index("entity_id")
                self._frame.index = self._frame.index.astype(str)
                self._loaded_at = time.monotonic()
            if entity_id not in self._frame.index:
                return None
            return self._frame.loc[entity_id].to_dict()


def create_app(lookup: Callable[[str], dict | None]) -> FastAPI:
    app = FastAPI(title="example-model")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/predictions/{entity_id}")
    def prediction(entity_id: str) -> Prediction:
        row = lookup(entity_id)
        if row is None:
            raise HTTPException(status_code=404, detail="no prediction for this entity")
        return Prediction(
            entity_id=entity_id,
            score=float(row["score"]),
            model_version=row.get("model_version"),
            scored_at=str(row["scored_at"]) if row.get("scored_at") is not None else None,
        )

    return app


def production_app() -> FastAPI:
    from example_model import data
    from example_model.config import Settings

    settings = Settings()
    table = f"{settings.gcp_project}.scoring.output"
    sql = f"SELECT CAST(entity_id AS STRING) AS entity_id, score FROM `{table}`"
    cache = LatestScores(lambda: data.query(settings, sql), settings.cache_ttl_seconds)
    return create_app(cache.get)
