"""Settings come from the environment; the training recipe comes from a committed file."""

from __future__ import annotations

from importlib import resources
from pathlib import Path

import yaml
from pydantic import AliasChoices, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Where things run. Differs between a workstation, CI, and production."""

    model_config = SettingsConfigDict(
        env_prefix="EXAMPLE_MODEL_", env_file=".env", extra="ignore", populate_by_name=True
    )

    gcp_project: str | None = None
    region: str = "us-central1"
    model_name: str = "example-model"
    # Root for model artifacts: a governed GCS prefix, or a temporary directory in tests.
    model_bucket: str = ".models"
    # Root for evaluation fixtures: a team folder in the governed bucket, readable
    # by the production training service account.
    fixture_bucket: str = ".fixtures"
    # MLflow tracking server. Empty turns tracking off, and the gate then fails.
    tracking_uri: str | None = Field(
        default=None,
        validation_alias=AliasChoices("EXAMPLE_MODEL_TRACKING_URI", "MLFLOW_TRACKING_URI"),
    )
    # One experiment per model. Defaults to the model name.
    experiment: str | None = None
    serving_image: str | None = None
    # Monitoring, production only. Tables are <dataset>.<table> in gcp_project.
    predictions_table: str = "model_monitoring.predictions"
    labels_table: str = "model_monitoring.labels"
    metrics_table: str = "model_monitoring.model_metrics"
    # Root for Evidently reports and Model Monitoring output, a governed prefix.
    reports_bucket: str = ".reports"
    alert_emails: list[str] = Field(default_factory=list)
    # How long the prediction lookup service keeps its in-memory copy of the
    # latest batch before re-reading it.
    cache_ttl_seconds: int = 300
    git_commit: str | None = Field(
        default=None, validation_alias=AliasChoices("EXAMPLE_MODEL_GIT_COMMIT", "CI_COMMIT_SHA")
    )


class Reference(BaseModel):
    """The research run production training must reproduce.

    Written by ``example-model reference <run_id>``, never by hand. The fixture is
    the research run's holdout rows with its scores; production scores the same
    rows and must agree.
    """

    run_id: str | None = None
    fixture_uri: str | None = None
    fixture_digest: str | None = None
    metrics: dict[str, float] = Field(default_factory=dict)
    tolerance: float = 0.02
    # Minimum Spearman rank correlation between research and production scores.
    min_agreement: float = 0.95


class Monitoring(BaseModel):
    """How this model is watched in production. Model-specific; environment is in Settings."""

    # How long after a prediction its label is expected. Performance is computed
    # only for predictions at least this old, so unlabeled rows are not counted.
    label_delay_days: int = 30
    # Jensen-Shannon divergence above which Vertex AI Model Monitoring alerts.
    drift_threshold: float = 0.3
    # Performance alert: the metric and the level below which an alert fires.
    alert_metric: str = "roc_auc"
    alert_floor: float = 0.7
    # Vertex AI Model Monitoring schedule, in cron form.
    schedule: str = "0 6 * * *"


class TrainConfig(BaseModel):
    """What to train. Committed, versioned, and shipped inside the package."""

    table: str
    as_of: str
    # The column that identifies the entity. Rows are assigned to train or
    # holdout by hashing it, so the holdout is the same in research and production.
    entity_id: str = "entity_id"
    target: str
    # Columns the model sees. Names not in the table are built by features.build.
    features: list[str]
    params: dict[str, float | int] = Field(default_factory=dict)
    test_size: float = 0.2
    seed: int = 0
    reference: Reference = Field(default_factory=Reference)
    monitoring: Monitoring = Field(default_factory=Monitoring)


def load_config(name_or_path: str) -> TrainConfig:
    """Load a packaged config by name (``train``) or a config file by path."""
    path = Path(name_or_path)
    if path.suffix in {".yaml", ".yml"}:
        text = path.read_text()
    else:
        text = resources.files("example_model.configs").joinpath(f"{name_or_path}.yaml").read_text()
    return TrainConfig.model_validate(yaml.safe_load(text))
