import pytest

from example_model import fixture
from example_model.config import Reference
from example_model.gate import ReproductionError, check_reproduction
from example_model.train import train


@pytest.fixture
def reference(settings, config, frame) -> Reference:
    """What a research run leaves behind."""
    result = train(config, frame)
    uri, digest = fixture.save(settings, "run1", result.holdout, result.metrics)
    return Reference(run_id="run1", fixture_uri=uri, fixture_digest=digest, metrics=result.metrics)


def test_passes_when_reproduced(config, frame, reference):
    observed = check_reproduction(train(config, frame), reference, config)
    assert observed["agreement"] > 0.99


def test_fails_when_metrics_differ(config, frame, reference):
    # The strongest feature dropped: the metric moves well beyond the tolerance.
    reference = reference.model_copy(update={"min_agreement": 0.0})
    fewer = config.model_copy(update={"features": ["f3", "f3_ratio"]})
    with pytest.raises(ReproductionError, match="outside"):
        check_reproduction(train(fewer, frame), reference, fewer)


def test_fails_when_ranking_differs(config, frame, reference):
    # Same data, a feature dropped: the headline metric may survive, the ranking will not.
    reference = reference.model_copy(update={"tolerance": 1.0})
    fewer = config.model_copy(update={"features": ["f3", "f3_ratio"]})
    result = train(fewer, frame)
    with pytest.raises(ReproductionError, match="agreement"):
        check_reproduction(result, reference, fewer)


def test_fails_without_research_run(config, frame):
    with pytest.raises(ReproductionError, match="No research run"):
        check_reproduction(train(config, frame), Reference(), config)


def test_fails_when_fixture_was_rewritten(settings, config, frame, reference):
    result = train(config, frame)
    fixture.save(settings, "run1", result.holdout.head(100), result.metrics)
    with pytest.raises(ReproductionError, match="digest"):
        check_reproduction(result, reference, config)
