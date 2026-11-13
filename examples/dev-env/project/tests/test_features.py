import pytest

from example_model import features


def test_build_adds_registered_features(frame):
    out = features.build(frame, ["f1", "f3_ratio"])
    assert "f3_ratio" in out.columns
    assert "f3_ratio" not in frame.columns  # the input is not modified


def test_build_rejects_unknown_names(frame):
    with pytest.raises(KeyError, match="features.py"):
        features.build(frame, ["nope"])
