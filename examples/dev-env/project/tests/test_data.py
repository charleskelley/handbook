from example_model import data


def test_split_is_deterministic_and_disjoint(config, frame):
    train_a, holdout_a = data.split(frame, config)
    train_b, holdout_b = data.split(frame, config)
    assert holdout_a["entity_id"].tolist() == holdout_b["entity_id"].tolist()
    assert not set(train_a["entity_id"]) & set(holdout_a["entity_id"])
    assert len(train_a) + len(holdout_a) == len(frame)
    assert abs(len(holdout_a) / len(frame) - config.test_size) < 0.03


def test_split_does_not_depend_on_row_order(config, frame):
    _, holdout = data.split(frame, config)
    _, shuffled = data.split(frame.sample(frac=1, random_state=1), config)
    assert set(holdout["entity_id"]) == set(shuffled["entity_id"])
