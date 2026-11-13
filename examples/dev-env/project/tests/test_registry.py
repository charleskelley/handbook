import json

from example_model import features, registry
from example_model.config import Settings
from example_model.train import train


def test_save_and_load_round_trip(tmp_path, config, frame):
    settings = Settings(_env_file=None, model_bucket=str(tmp_path), git_commit="abc123")
    result = train(config, frame)
    uri = registry.save(settings, result.model, result.metrics, config, "7")

    loaded = registry.load(uri)
    x = features.build(frame, config.features)[config.features]
    assert (loaded.predict_proba(x) == result.model.predict_proba(x)).all()

    metadata = json.loads((tmp_path / "example-model" / "7" / "metadata.json").read_text())
    assert metadata["model_version"] == "7"
    assert metadata["git_commit"] == "abc123"
    assert metadata["metrics"] == result.metrics
    assert metadata["data"] == {"table": "synthetic", "as_of": "2026-01-01"}
