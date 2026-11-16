---
title: "DR-0005: Vertex AI Model Monitoring alerts, Evidently explains, people promote"
type: decision-record
owner: mle-lead
audience: [all]
status: draft
last_reviewed: 2026-11-12
review_cadence: 365d
tags: [monitoring, mlops]
---

# DR-0005: Vertex AI Model Monitoring alerts, Evidently explains, people promote

## Context

[DR-0002](DR-0002-train-models-in-production.md) ends with a retraining ladder
whose top rung needs a trigger, and nothing was watching production models.
Labels arrive days to months after a prediction, by domain, so a drift signal
is the only early warning, and a performance signal needs a label delay built
into it. Vertex AI Model Monitoring works on models in the registry even when
served elsewhere, takes BigQuery as its source, and alerts; it does not explain.
Evidently produces the per-feature, per-metric view a person needs to decide.

## Decision

Three layers, all standard for every production model: the score job appends
every prediction to a BigQuery prediction log; Vertex AI Model Monitoring
watches feature and prediction drift against the training snapshot, daily, per
champion version, created at promotion; a weekly job computes performance from
labeled predictions, after the model's label delay, and alerts through Cloud
Monitoring. Where a model needs the deeper look, a weekly Evidently report is
saved as a static page in the reports bucket. Triggered retraining is optional
per model and only ever produces a challenger. Promotion is manual.

## Alternatives considered

- **A package-owned drift job instead of Vertex AI Model Monitoring.** Less
  Vertex-specific code, but a drift engine to maintain and no managed
  alerting. Kept as the fallback if Model Monitoring proves unfit.
- **Evidently as the alerting layer.** Its tests can fail a job, but then the
  report is both the signal and the explanation, and the signal has no
  notification channel of its own. Reports are read, not watched.
- **Auto-promotion after a passing gate.** Not yet. The gate proves the
  recipe reproduces; it does not prove the challenger is better in production.

## Consequences

- Every production model has a prediction log, a monitor, a weekly metric,
  and a report location from its first promotion.
- The labels table is a contract with the business process that learns the
  outcome; a model without labels has drift monitoring only, which is stated.
- Promotion stays a person's decision at every rung of the ladder.

## Status

Proposed
