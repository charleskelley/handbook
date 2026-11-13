"""The recipe: the same function runs in a notebook, on a workstation, and in the pipeline."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

from example_model import data, features
from example_model.config import TrainConfig


@dataclass
class TrainResult:
    model: Pipeline
    metrics: dict[str, float]
    # The holdout rows with a ``score`` column: what the research run saves as the fixture.
    holdout: pd.DataFrame


def evaluate(model: Pipeline, frame: pd.DataFrame, config: TrainConfig) -> dict[str, float]:
    scores = model.predict_proba(frame[config.features])[:, 1]
    target = frame[config.target]
    return {
        "roc_auc": float(roc_auc_score(target, scores)),
        "average_precision": float(average_precision_score(target, scores)),
    }


def train(config: TrainConfig, frame: pd.DataFrame) -> TrainResult:
    frame = features.build(frame, config.features)
    train_frame, holdout = data.split(frame, config)
    # Fitted transforms live inside the pipeline (level 3 of the feature rule).
    model = make_pipeline(StandardScaler(), LogisticRegression(**config.params))
    model.fit(train_frame[config.features], train_frame[config.target])
    holdout = holdout.copy()
    holdout["score"] = model.predict_proba(holdout[config.features])[:, 1]
    return TrainResult(model=model, metrics=evaluate(model, holdout, config), holdout=holdout)
