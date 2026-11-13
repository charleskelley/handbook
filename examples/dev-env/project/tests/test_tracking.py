import pytest

from example_model import tracking
from example_model.train import train


def test_run_tags_and_fixture(settings, config, frame, monkeypatch):
    monkeypatch.setattr(tracking, "git_state", lambda: ("abc123", False))
    with tracking.run(settings, "research-test") as run:
        run.dataset(frame)
        result = train(config, frame)
        run.params(**config.params)
        run.fixture(result.holdout, result.metrics)
        run_id = run.run_id

    runs = tracking.runs(settings)
    assert runs["tags.git_dirty"].tolist() == ["false"]
    assert runs["params.table"].tolist() == ["synthetic"]
    ref = tracking.reference_from_run(settings, run_id)
    assert ref["run_id"] == run_id
    assert ref["metrics"]["roc_auc"] == pytest.approx(result.metrics["roc_auc"])
    assert ref["fixture_uri"].endswith(run_id)


def test_reference_refuses_dirty_runs(settings, config, frame, monkeypatch):
    monkeypatch.setattr(tracking, "git_state", lambda: ("abc123", True))
    with tracking.run(settings, "research-dirty") as run:
        run.fixture(train(config, frame).holdout, {"roc_auc": 0.5})
        run_id = run.run_id
    with pytest.raises(ValueError, match="dirty"):
        tracking.reference_from_run(settings, run_id)


def test_reference_refuses_runs_without_fixture(settings, config, frame, monkeypatch):
    monkeypatch.setattr(tracking, "git_state", lambda: ("abc123", False))
    with tracking.run(settings, "research-nofixture") as run:
        run.metrics(roc_auc=0.5)
        run_id = run.run_id
    with pytest.raises(ValueError, match="fixture"):
        tracking.reference_from_run(settings, run_id)


def test_run_requires_tracking_uri(settings):
    settings = settings.model_copy(update={"tracking_uri": None})
    with pytest.raises(RuntimeError, match="TRACKING_URI"):
        with tracking.run(settings, "x"):
            pass
