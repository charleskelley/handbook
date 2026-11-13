"""Evidently reports: the deeper, model-specific look that an alert threshold is not.

A scheduled Cloud Run job compares recent predictions, with labels where they
have arrived, against the reference run's fixture, and saves a static HTML and
JSON report to the governed bucket. Reports are read, not watched: Vertex AI
Model Monitoring alerts, Evidently explains.
"""

from __future__ import annotations

from datetime import UTC, datetime

import fsspec
import pandas as pd

from example_model import data, fixture
from example_model.config import Settings, TrainConfig


def build(reference: pd.DataFrame, current: pd.DataFrame, config: TrainConfig):
    """Data drift always; classification quality when the current frame has labels."""
    from evidently import BinaryClassification, DataDefinition, Dataset, Report
    from evidently.presets import ClassificationPreset, DataDriftPreset

    has_labels = config.target in current.columns and current[config.target].notna().any()
    for frame in (reference, current):
        frame["predicted"] = (frame["score"] >= 0.5).astype(int)
    definition = DataDefinition(
        numerical_columns=[*config.features, "score"],
        categorical_columns=[config.target, "predicted"] if has_labels else ["predicted"],
        classification=[
            BinaryClassification(
                target=config.target, prediction_labels="predicted", prediction_probas="score"
            )
        ]
        if has_labels
        else [],
    )
    presets = [DataDriftPreset(columns=[*config.features, "score"])]
    if has_labels:
        presets.append(ClassificationPreset())
    report = Report(presets)
    return report.run(
        Dataset.from_pandas(current, data_definition=definition),
        Dataset.from_pandas(reference, data_definition=definition),
    )


def recent_predictions(settings: Settings, config: TrainConfig, days: int) -> pd.DataFrame:
    sql = f"""
        SELECT p.*, l.label
        FROM `{settings.gcp_project}.{settings.predictions_table}` p
        LEFT JOIN `{settings.gcp_project}.{settings.labels_table}` l
          ON l.{config.entity_id} = p.{config.entity_id} AND l.labeled_at > p.scored_at
        WHERE p.scored_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
    """
    return data.query(settings, sql)


def run(settings: Settings, config: TrainConfig, days: int = 7) -> str:
    """Build the report and save it. Returns the folder it was written to."""
    reference, _ = fixture.load(config.reference.fixture_uri)
    current = recent_predictions(settings, config, days)
    result = build(reference, current, config)
    folder = (
        f"{settings.reports_bucket.rstrip('/')}/{settings.model_name}/{datetime.now(UTC):%Y-%m-%d}"
    )
    with fsspec.open(f"{folder}/report.html", "w") as f:
        f.write(result.get_html_str(as_iframe=False))
    with fsspec.open(f"{folder}/report.json", "w") as f:
        f.write(result.json())
    return folder
