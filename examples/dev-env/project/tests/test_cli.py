"""The reference command writes a run into the config without touching the rest of it."""

import yaml

from example_model import cli, tracking
from example_model.config import load_config
from example_model.train import train


def test_reference_writes_config(settings, config, frame, tmp_path, monkeypatch):
    monkeypatch.setattr(tracking, "git_state", lambda: ("abc123", False))
    for key, value in settings.model_dump().items():
        if value is not None:
            monkeypatch.setenv(f"EXAMPLE_MODEL_{key.upper()}", str(value))
    with tracking.run(settings, "research-cli") as run:
        result = train(config, frame)
        run.fixture(result.holdout, result.metrics)
        run_id = run.run_id

    path = tmp_path / "train.yaml"
    path.write_text(
        "# a comment that must survive\n"
        + yaml.safe_dump(config.model_dump(exclude={"reference"}))
        + "reference:\n  run_id: null\n"
    )
    cli.main(["reference", run_id, "--write", str(path)])

    text = path.read_text()
    assert text.startswith("# a comment that must survive")
    written = load_config(str(path))
    assert written.reference.run_id == run_id
    assert written.reference.metrics["roc_auc"] == result.metrics["roc_auc"]
    assert written.features == config.features
