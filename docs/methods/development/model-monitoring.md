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
  - "https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview"
---

# Model monitoring

How a model in production is watched: how each monitor is built, what fires an
alert, and what happens when one fires. What must be watched on every model,
how a threshold is set, and who acts are policy, on
[Monitoring](../../oversight/monitoring.md) under Oversight. The reasons for
the design are in
[DR-0005](../../team/decisions/DR-0005-monitor-with-vertex-and-evidently.md).

There are four layers, each answering a different question.

| Layer | Question | How | Cadence |
|---|---|---|---|
| Prediction log | What did we predict, for whom, with which version? | The scoring job appends every prediction | Every batch |
| Drift | Have the inputs or the scores changed since training? | The platform's model monitoring service, per champion version | Daily |
| Performance | Is the model worse, now that labels are in? | A scheduled job joins predictions to labels and raises an alert | Weekly |
| Report | Why? | An Evidently report, saved as a static page | Weekly, or on demand |

## The prediction log

Nothing can be monitored that was not recorded. The batch scoring job writes
the output table for consumers and appends the same rows to the prediction
log. What a row carries, and the rules for the log, are on
[Predictions](../../data/predictions.md). The log is partitioned by the time
each row was written, which is the time the drift monitor windows on.

Serving reads from the output table; it does not score, so there is one log and
one place a prediction can come from. See
[Path to production](path-to-production.md#serving).

## Labels

Performance needs outcomes, and an outcome arrives days, weeks, or months
after its prediction. The label table and its rules are on
[Training data](../../data/training-data.md#labels). Each model's config
states its label delay, and performance is computed only for predictions at
least that old, so a quiet week is never mistaken for a good one.

## Drift

The standard for every production model. When a version is promoted, the same
command creates its monitor in the
[platform's model monitoring service](../../technology/vertex-ai.md).

| Part of the monitor | What it is |
|---|---|
| Baseline | The training snapshot the version was trained on |
| Target | The prediction log, in daily windows |
| Watched | Drift in the input features, and drift in the scores |
| Alert | To the team list |

A drift alert means the world moved, not that the model is wrong. It is the
prompt to open the report and, if labels agree, to retrain.

## Performance

A weekly job joins the prediction log to the label table for the predictions
old enough to have labels, computes the model's measures for each version and
week, and appends them to a metrics table.

- **One measure alerts.** It is the main measure in the model's
  [framing](../framing-and-evaluating-a-prediction.md#measures): for a model
  whose top scores are acted on, precision or lift at the decision's
  capacity. An alert fires when it falls below the floor in the model's
  config. The other measures are stored, and are read in the report.
- **It is computed on units that were left alone.** Once a score drives an
  action, the outcome of a unit that was acted on is no longer a clean
  label. Where a model's scores are acted on, performance is computed on the
  group that was scored and left untouched: see
  [Living with the model](../churn-and-propensity.md#living-with-the-model).
- **It does not say whether the action worked.** That is a different
  question with a different method: see
  [Experiments and lift tests](../experiments-and-lift-tests.md).

## Reports

A threshold says that something changed; it does not say what. Where a model
needs the deeper look, a weekly job builds an Evidently report comparing recent
predictions, with labels where present, to the reference run's fixture: drift
for each feature, the distribution of scores, and the quality of the
classification. It is saved as a static page and a data file in the reports
bucket, under the model and the date, and read by a person. Reports are for
understanding; they do not alert.

## When an alert fires

1. Open the latest report, or run one for the window in question.
2. Decide: data problem upstream, a real shift, or a labelling gap.
3. If retraining is the answer, start the training job. It trains a challenger
   through the same reproduction gate as any release.
4. A person promotes. Promotion creates the new version's monitor.

Triggered retraining is optional: a subscription on the alert can submit the
training pipeline so a challenger is waiting when someone looks. It never
promotes. The ladder is on [Path to production](path-to-production.md#the-retraining-ladder).

## What the infrastructure provides

The infrastructure repository defines the monitoring dataset and its tables,
the reports bucket, the monitoring service's access to it, the schedules for
the two weekly jobs, the notification channel, and the performance alert. The
jobs themselves are created at deploy, from the release container.

## See also

- [Monitoring](../../oversight/monitoring.md): what must be watched, the
  thresholds, and who acts.
- [Predictions](../../data/predictions.md) and
  [Training data](../../data/training-data.md): the log and the labels.
- [Experiment tracking](experiment-tracking.md): the fixture the report compares to.
