---
title: "Model monitoring"
type: general
owner: mle-lead
audience: [ds, mle, leadership]
status: draft
last_reviewed: 2026-11-12
review_cadence: 180d
tags: [monitoring, mlops, production]
sources:
  - "examples/dev-env/project/src/example_model/score.py"
  - "examples/dev-env/project/src/example_model/performance.py"
  - "examples/dev-env/project/src/example_model/monitoring.py"
  - "examples/dev-env/project/src/example_model/report.py"
  - "examples/dev-env/infra/envs/prod/main.tf"
  - "https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview"
---

# Model monitoring

How a model in production is watched, what fires an alert, and what happens
when one fires. Three layers, each answering a different question. The reasons
are in [DR-0005](../../team/decisions/DR-0005-monitor-with-vertex-and-evidently.md).

| Layer | Question | Tool | Cadence |
|---|---|---|---|
| Prediction log | What did we predict, for whom, with which version? | The score job appends every prediction to BigQuery | Every batch |
| Drift | Have the inputs or the scores changed since training? | Vertex AI Model Monitoring, per champion version | Daily |
| Performance | Is the model worse, now that labels are in? | A scheduled job joins predictions to labels; Cloud Monitoring alerts | Weekly |
| Report | Why? | An Evidently report, saved as a static page | Weekly, or on demand |

## The prediction log

Nothing can be monitored that was not recorded. The batch scoring job writes
the output table for consumers and appends the same rows, with the features,
the score, the model version, and the time, to the prediction log. It is
partitioned by `scored_at`, which is the timestamp Model Monitoring windows on.

```python
--8<-- "examples/dev-env/project/src/example_model/score.py"
```

Serving reads from the output table; it does not score, so there is one log and
one place a prediction can come from. See
[Path to production](path-to-production.md#serving).

## Labels

Ground truth arrives days, weeks, or months after a prediction, depending on
the domain. The `labels` table is the contract: entity id, label, and when it
became known. The business process that learns the outcome fills it. Each
model's config says how long to wait, `monitoring.label_delay_days`, and
performance is computed only for predictions at least that old, so a quiet
week is never mistaken for a good one.

## Drift: Vertex AI Model Monitoring

The standard for every production model. When a version is promoted, the same
command creates its monitor: baseline is the training snapshot the version was
trained on, target is the prediction log in daily windows, objectives are input
feature drift and prediction drift, alerts go to the team list. Feature
attribution is not available for models served off Vertex AI, and is not
needed for an alert.

```python
--8<-- "examples/dev-env/project/src/example_model/monitoring.py"
```

A drift alert means the world moved, not that the model is wrong. It is the
prompt to open the report and, if labels agree, to retrain.

## Performance: labeled predictions

A weekly Cloud Run job joins the log to the labels for the last week's eligible
predictions, computes the metrics per model version and week, appends them to
`model_metrics`, and publishes the latest as Cloud Monitoring custom metrics.
An alert policy watches `roc_auc` against the floor in the config.

```python
--8<-- "examples/dev-env/project/src/example_model/performance.py"
```

## Reports: Evidently

A threshold says that something changed; it does not say what. Where a model
needs the deeper look, a weekly job builds an Evidently report comparing recent
predictions, with labels where present, to the reference run's fixture: drift
per feature, score distribution, and classification quality. It is saved as a
static HTML page and a JSON file in the reports bucket, under the model and the
date, and read by a person. Reports are for understanding; they do not alert.

```python
--8<-- "examples/dev-env/project/src/example_model/report.py"
```

## When an alert fires

1. Open the latest report, or run one for the window in question.
2. Decide: data problem upstream, a real shift, or a labelling gap.
3. If retraining is the answer, start the train job. It trains a challenger
   through the same reproduction gate as any release.
4. A person promotes. Promotion creates the new version's monitor.

Triggered retraining is optional: a subscription on the alert policy can submit
the train pipeline so a challenger is waiting when someone looks. It never
promotes. The ladder is on [Path to production](path-to-production.md#the-retraining-ladder).

## What is in the Terraform

The monitoring dataset and its three tables, the reports bucket, the Vertex AI
service agent's access to it, Cloud Scheduler for the two weekly jobs, the
email notification channel, and the performance alert policy. The Cloud Run
jobs themselves are created by the deploy job from the release image.

## See also

- [Experiment tracking](experiment-tracking.md): the fixture the report compares to.
- [Vertex AI](../../technology/vertex-ai.md)
