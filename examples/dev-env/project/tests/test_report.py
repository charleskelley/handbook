import json

import numpy as np

from example_model import report
from example_model.train import train


def test_report_has_drift_and_quality_when_labels_present(config, frame):
    holdout = train(config, frame).holdout
    reference = holdout.copy()
    current = holdout.copy()
    current["f1"] = current["f1"] + 2.0  # an obvious shift
    result = report.build(reference, current, config)
    payload = json.loads(result.json())
    assert "metrics" in payload
    assert result.get_html_str(as_iframe=False)


def test_report_without_labels_is_drift_only(config, frame):
    holdout = train(config, frame).holdout
    current = holdout.drop(columns=[config.target]).copy()
    current[config.target] = np.nan
    result = report.build(holdout.copy(), current, config)
    assert result.get_html_str(as_iframe=False)
