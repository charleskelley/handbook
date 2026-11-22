---
title: Predictions
type: general
owner: mle-lead
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-22
review_cadence: 180d
tags: [predictions, prediction-log, data]
---

# Predictions

What a model writes. Every score a model produces is appended to the
prediction log, and the log is the last stage of the chain: the record of
what was predicted, for whom, by which version, from which features.

## What a prediction row carries

| Carried | What it is |
|---|---|
| Entity | The id of the thing scored |
| Decision time | The moment the prediction is made for |
| Score | The model's output |
| Model version | The version in the model registry that produced the score |
| Features | The feature values the model read |
| When it was written | The time the row was appended |

The column names follow
[time columns](../methods/development/conventions.md#time-columns).

## Practices

- **Every score is logged**, including the scores nothing was done with. A
  log of only the acted-on scores cannot say how the model behaves across
  the population it scores.
- **The log is appended, never overwritten.** A score made again for the
  same entity and time is a new row.
- **Features are logged as they were read.** The log is then the record of
  what the model saw, and the source for drift, for performance, and for
  reports: see
  [Model monitoring](../methods/development/model-monitoring.md).
- **One log, written from one place.** A consumer that needs a score reads
  the scoring job's output. It does not score for itself, so there is one
  place a prediction can come from.

## Three records, kept apart

A prediction, the decision made from it, and the outcome that followed are
three records with one key: the entity and the decision time.

| Record | Says | Where |
|---|---|---|
| Prediction log | What the model said | This page |
| Decision log | What was done with it, under which policy | [Decision log](../oversight/decision-log.md) |
| Label table | What happened afterwards | [Training data](training-data.md#labels) |

A prediction is not a decision. A score becomes an action only through a
policy, and the action is recorded in the decision log. Joined on their key,
the three records are what a model's performance, and the effect of acting
on it, are measured from.

## A prediction is also a source

A score that is read as a feature by another model, or by one of the
business's systems, is a [source](sources/index.md) like any other. It
has a grain, a key, a lag, and an owner, and it gets a source page.

Once a model's scores drive actions, they also shape the outcomes the next
version is trained on. An outcome that an action changed is no longer a
clean label. Keeping a group that is scored and left untouched is how that
is handled: see
[Churn and propensity models](../methods/churn-and-propensity.md).

!!! note "What a model's repository must document"

    A model's predictions are documented in the model's repository, not in
    the handbook, as the
    [data contract](../methods/development/conventions.md#data-contracts) of
    its prediction table. It is checked before the model goes to
    [production](../methods/development/path-to-production.md). Between
    them, the contract and the repository's documentation must say:

    - **The output**: where the scores are written, their key, and how often
      they are written.
    - **The score**: what it means, its range, and which direction is which.
    - **The log**: which features are logged with each score, and how the
      model version is recorded.
    - **The consumers**: who reads the scores, and the decision each one
      uses them for.
    - **The untouched group**: whether one is kept, and how it is drawn.
