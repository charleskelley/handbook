from example_model.config import Settings, load_config


def test_packaged_config_loads():
    config = load_config("train")
    assert config.features
    assert config.reference.run_id is None


def test_settings_read_environment(monkeypatch):
    monkeypatch.setenv("EXAMPLE_MODEL_REGION", "europe-west4")
    monkeypatch.setenv("CI_COMMIT_SHA", "abc123")
    settings = Settings(_env_file=None)
    assert settings.region == "europe-west4"
    assert settings.git_commit == "abc123"
