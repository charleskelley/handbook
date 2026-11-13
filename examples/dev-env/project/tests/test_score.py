from datetime import UTC, datetime

from example_model import score
from example_model.train import train


def test_log_rows_carry_version_and_time(config, frame):
    result = train(config, frame)
    when = datetime(2026, 1, 2, tzinfo=UTC)
    log = score.log_rows(result.holdout, config, "7", when)
    assert set(log.columns) == {
        config.entity_id,
        *config.features,
        "score",
        "model_version",
        "as_of",
        "scored_at",
    }
    assert (log["model_version"] == "7").all()
    assert (log["scored_at"] == when).all()
