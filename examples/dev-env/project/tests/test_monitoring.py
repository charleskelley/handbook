from example_model import monitoring


def test_schema_covers_features_prediction_and_label(config):
    schema = monitoring.schema(config)
    assert [f.name for f in schema.feature_fields] == config.features
    assert [f.name for f in schema.prediction_fields] == ["score"]
    assert [f.name for f in schema.ground_truth_fields] == [config.target]


def test_baseline_query_pins_the_snapshot(config):
    assert "as_of_date = DATE '2026-01-01'" in monitoring.baseline_query(config)
