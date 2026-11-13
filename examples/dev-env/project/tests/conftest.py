"""Tests use synthetic data only. Real data never appears in tests or fixtures."""

import numpy as np
import pandas as pd
import pytest

from example_model.config import Settings, TrainConfig


@pytest.fixture
def frame() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    n = 2000
    x = rng.normal(size=(n, 3))
    logits = 1.5 * x[:, 0] - 1.0 * x[:, 1] + 0.2 * x[:, 2]
    label = (rng.random(n) < 1 / (1 + np.exp(-logits))).astype(int)
    frame = pd.DataFrame(
        {"entity_id": np.arange(n), "f1": x[:, 0], "f2": x[:, 1], "f3": x[:, 2], "label": label}
    )
    frame.attrs["source"] = {"table": "synthetic", "as_of": "2026-01-01"}
    return frame


@pytest.fixture
def config() -> TrainConfig:
    return TrainConfig(
        table="synthetic",
        as_of="2026-01-01",
        target="label",
        features=["f1", "f2", "f3", "f3_ratio"],
        params={"C": 1.0, "max_iter": 1000},
    )


@pytest.fixture
def settings(tmp_path, monkeypatch) -> Settings:
    """Local stores: a SQLite MLflow backend and a temporary fixture directory."""
    monkeypatch.delenv("MLFLOW_TRACKING_URI", raising=False)
    return Settings(
        model_bucket=str(tmp_path / "models"),
        fixture_bucket=str(tmp_path / "fixtures"),
        tracking_uri=f"sqlite:///{tmp_path / 'mlruns.db'}",
        git_commit="abc123",
    )
