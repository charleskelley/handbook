"""The reproduction gate: production training must reproduce the research run.

Two checks against the research run's fixture: every recorded metric within
tolerance, and the production model's scores rank the same rows the same way.
The second catches a different model with the same headline number.
"""

from __future__ import annotations

from scipy.stats import spearmanr

from example_model import fixture
from example_model.config import Reference, TrainConfig
from example_model.train import TrainResult, evaluate


class ReproductionError(RuntimeError):
    """Production training did not reproduce the research result."""


def check_reproduction(
    result: TrainResult, reference: Reference, config: TrainConfig
) -> dict[str, float]:
    if not reference.run_id or not reference.fixture_uri:
        raise ReproductionError(
            "No research run recorded. Log one, then run `example-model reference <run_id>`."
        )
    holdout, _ = fixture.load(reference.fixture_uri)
    if fixture.digest(holdout) != reference.fixture_digest:
        raise ReproductionError(
            f"Fixture at {reference.fixture_uri} does not match the digest recorded for "
            f"run {reference.run_id}. It was rewritten; log a new run."
        )
    observed = evaluate(result.model, holdout, config)
    for name, expected in reference.metrics.items():
        if abs(observed[name] - expected) > reference.tolerance:
            raise ReproductionError(
                f"{name} {observed[name]:.4f} is outside {expected:.4f} +/- {reference.tolerance}. "
                "Look for leakage, notebook state, or a data difference."
            )
    scores = result.model.predict_proba(holdout[config.features])[:, 1]
    agreement = float(spearmanr(holdout["score"], scores).statistic)
    if agreement < reference.min_agreement:
        raise ReproductionError(
            f"Rank agreement with the research scores is {agreement:.3f}, below "
            f"{reference.min_agreement}. Same metrics, different model: check the features."
        )
    return {**observed, "agreement": agreement}
