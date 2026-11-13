import numpy as np
import pandas as pd

from example_model import performance
from example_model.train import train


def _joined(config, frame) -> pd.DataFrame:
    holdout = train(config, frame).holdout
    joined = holdout[["score", config.target]].copy()
    joined["model_version"] = np.where(np.arange(len(joined)) % 2 == 0, "7", "8")
    joined["scored_at"] = pd.Timestamp("2026-01-05", tz="UTC") + pd.to_timedelta(
        np.arange(len(joined)) % 14, unit="D"
    )
    return joined


def test_metrics_per_version_and_week(config, frame):
    metrics = performance.metrics_by_period(_joined(config, frame), config.target)
    assert set(metrics["model_version"]) == {"7", "8"}
    assert metrics.groupby("model_version").size().min() >= 2  # at least two weeks each
    assert (metrics["roc_auc"] > 0.7).all()
    assert metrics["n"].sum() == len(_joined(config, frame))


def test_single_class_weeks_are_skipped(config, frame):
    joined = _joined(config, frame)
    joined[config.target] = 1
    assert performance.metrics_by_period(joined, config.target).empty
