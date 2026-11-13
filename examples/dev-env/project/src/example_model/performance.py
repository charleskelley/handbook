"""Model performance from the prediction log, once labels have arrived.

Drift says the inputs changed; only labels say the model got worse. A scheduled
Cloud Run job joins the prediction log to the labels table for predictions old
enough to have labels, computes metrics per model version and week, appends
them to the metrics table, and publishes them as Cloud Monitoring custom metrics
so an alert policy can watch them.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

from example_model import data
from example_model.config import Settings, TrainConfig

METRIC_PREFIX = "custom.googleapis.com/example_model"


def metrics_by_period(joined: pd.DataFrame, target: str = "label") -> pd.DataFrame:
    """One row per model version and week: roc_auc, average_precision, and n.

    ``joined`` has ``model_version``, ``scored_at``, ``score``, and the label.
    Groups with one class only are skipped: no metric is defined for them.
    """
    rows = []
    week = joined["scored_at"].dt.to_period("W").dt.start_time
    for (version, start), group in joined.groupby(["model_version", week]):
        if group[target].nunique() < 2:
            continue
        rows.append(
            {
                "model_version": version,
                "week_start": start,
                "n": int(len(group)),
                "roc_auc": float(roc_auc_score(group[target], group["score"])),
                "average_precision": float(average_precision_score(group[target], group["score"])),
            }
        )
    return pd.DataFrame(rows)


def labeled_predictions(settings: Settings, config: TrainConfig, days: int) -> pd.DataFrame:
    """Predictions from the last ``days`` that are old enough to have a label, joined to it."""
    delay = config.monitoring.label_delay_days
    sql = f"""
        SELECT p.model_version, p.scored_at, p.score, l.label
        FROM `{settings.gcp_project}.{settings.predictions_table}` p
        JOIN `{settings.gcp_project}.{settings.labels_table}` l
          ON l.{config.entity_id} = p.{config.entity_id} AND l.labeled_at > p.scored_at
        WHERE p.scored_at BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days + delay} DAY)
                              AND TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {delay} DAY)
    """
    return data.query(settings, sql)


def publish(settings: Settings, metrics: pd.DataFrame) -> None:
    """Write the latest week's metrics as Cloud Monitoring custom metrics."""
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    now = int(datetime.now(UTC).timestamp())
    latest = metrics.sort_values("week_start").groupby("model_version").tail(1)
    series = []
    for _, row in latest.iterrows():
        for name in ("roc_auc", "average_precision"):
            ts = monitoring_v3.TimeSeries()
            ts.metric.type = f"{METRIC_PREFIX}/{name}"
            ts.metric.labels["model_version"] = str(row["model_version"])
            ts.resource.type = "global"
            ts.resource.labels["project_id"] = settings.gcp_project or ""
            ts.points = [
                monitoring_v3.Point(
                    {
                        "interval": {"end_time": {"seconds": now}},
                        "value": {"double_value": row[name]},
                    }
                )
            ]
            series.append(ts)
    if series:
        client.create_time_series(name=f"projects/{settings.gcp_project}", time_series=series)


def run(settings: Settings, config: TrainConfig, days: int = 7) -> pd.DataFrame:
    joined = labeled_predictions(settings, config, days)
    metrics = metrics_by_period(joined, config.target)
    if not metrics.empty:
        metrics["computed_at"] = datetime.now(UTC)
        data.append_frame(settings, metrics, f"{settings.gcp_project}.{settings.metrics_table}")
        publish(settings, metrics)
    return metrics
