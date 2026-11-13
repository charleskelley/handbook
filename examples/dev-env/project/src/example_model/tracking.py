"""Experiment tracking on MLflow, with the tags that make a run reproducible.

``run()`` is the one call research and production share. It starts an MLflow run
tagged with the git commit, whether the checkout was dirty, the package version,
the user, and the environment, and logs the dataset a frame came from. Autolog
is off: log what you chose, not every fit inside a cross-validation.
"""

from __future__ import annotations

import getpass
import os
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

import pandas as pd

from example_model import fixture
from example_model.config import Settings


def git_state() -> tuple[str | None, bool]:
    """The HEAD commit and whether the working tree has uncommitted changes."""
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None, True
    return head, bool(status.strip())


def standard_tags(settings: Settings) -> dict[str, str]:
    from example_model.registry import package_version

    commit, dirty = git_state()
    return {
        "git_commit": settings.git_commit or commit or "unknown",
        "git_dirty": str(dirty).lower(),
        "package_version": package_version(),
        "user": os.environ.get("CI_JOB_ID", "") and "ci" or getpass.getuser(),
        "environment": os.environ.get("EXAMPLE_MODEL_ENVIRONMENT", "research"),
    }


@dataclass
class Run:
    settings: Settings
    run_id: str

    def params(self, **params: object) -> None:
        import mlflow

        mlflow.log_params({k: str(v) for k, v in params.items()})

    def metrics(self, **metrics: float) -> None:
        import mlflow

        mlflow.log_metrics(metrics)

    def dataset(self, frame: pd.DataFrame, context: str = "training") -> None:
        """Log where a frame came from. Frames from ``data.load_frame`` carry it."""
        import mlflow

        source = frame.attrs.get("source", {})
        name = f"{source.get('table', 'frame')}@{source.get('as_of', '')}"
        mlflow.log_input(mlflow.data.from_pandas(frame, source=name, name=name), context=context)
        if source:
            self.params(table=source["table"], as_of=source["as_of"])

    def fixture(self, holdout: pd.DataFrame, metrics: dict[str, float]) -> str:
        """Save the holdout with its scores as this run's fixture and record it."""
        uri, digest = fixture.save(self.settings, self.run_id, holdout, metrics)
        self.params(fixture_uri=uri, fixture_digest=digest)
        self.metrics(**metrics)
        return uri


@contextmanager
def run(settings: Settings, name: str, **tags: str) -> Iterator[Run]:
    """Start a tracked run. Research: ``with tracking.run(settings, "research-...") as r:``."""
    import mlflow

    if not settings.tracking_uri:
        raise RuntimeError("Set EXAMPLE_MODEL_TRACKING_URI (or MLFLOW_TRACKING_URI) first.")
    mlflow.set_tracking_uri(settings.tracking_uri)
    mlflow.set_experiment(settings.experiment or settings.model_name)
    with mlflow.start_run(run_name=name, tags={**standard_tags(settings), **tags}) as active:
        yield Run(settings, active.info.run_id)


def runs(settings: Settings) -> pd.DataFrame:
    """Every run in the experiment, one row each: params, metrics, and tags as columns."""
    import mlflow

    mlflow.set_tracking_uri(settings.tracking_uri)
    return mlflow.search_runs(experiment_names=[settings.experiment or settings.model_name])


def reference_from_run(settings: Settings, run_id: str) -> dict[str, object]:
    """Read a research run and return the ``reference`` block for the config.

    Refuses runs logged from a dirty checkout or without a fixture: the gate needs
    code that exists in git and rows that exist in the bucket.
    """
    import mlflow

    mlflow.set_tracking_uri(settings.tracking_uri)
    data = mlflow.get_run(run_id).data
    if data.tags.get("git_dirty") != "false":
        raise ValueError(
            f"Run {run_id} was logged from a dirty checkout. Commit the feature code and log again."
        )
    if "fixture_uri" not in data.params:
        raise ValueError(f"Run {run_id} saved no fixture. Call run.fixture(...) in the notebook.")
    return {
        "run_id": run_id,
        "fixture_uri": data.params["fixture_uri"],
        "fixture_digest": data.params["fixture_digest"],
        "metrics": {k: float(v) for k, v in data.metrics.items()},
    }
