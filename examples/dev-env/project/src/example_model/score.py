"""Batch scoring as a Cloud Run job: read a table, score it, write a table, log it.

The output table is the latest scores and is replaced each run. The prediction
log is appended, partitioned by ``scored_at``, and is what monitoring reads.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pandas as pd

from example_model import data, features, registry
from example_model.config import Settings, TrainConfig


def log_rows(
    frame: pd.DataFrame, config: TrainConfig, model_version: str, scored_at: datetime
) -> pd.DataFrame:
    """The rows written to the prediction log: id, features, score, version, time."""
    log = frame[[config.entity_id, *config.features, "score"]].copy()
    log[config.entity_id] = log[config.entity_id].astype(str)  # the log keys on a string
    log["model_version"] = model_version
    log["as_of"] = config.as_of
    log["scored_at"] = scored_at
    return log


def score(settings: Settings, config: TrainConfig, input_table: str, output_table: str) -> int:
    uri = registry.resolve(settings)
    model = registry.load(uri)
    frame = features.build(data.load_frame(settings, input_table, config.as_of), config.features)
    frame["score"] = model.predict_proba(frame[config.features])[:, 1]
    data.write_frame(settings, frame, output_table)
    data.append_frame(
        settings,
        log_rows(frame, config, uri.rstrip("/").rsplit("/", 1)[-1], datetime.now(UTC)),
        f"{settings.gcp_project}.{settings.predictions_table}",
    )
    return len(frame)
