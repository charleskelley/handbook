from example_model.train import train


def test_train_learns_signal(config, frame):
    result = train(config, frame)
    assert result.metrics["roc_auc"] > 0.75


def test_train_is_deterministic(config, frame):
    assert train(config, frame).metrics == train(config, frame).metrics


def test_holdout_carries_scores_and_ids(config, frame):
    holdout = train(config, frame).holdout
    assert {"entity_id", "score", config.target, *config.features} <= set(holdout.columns)
