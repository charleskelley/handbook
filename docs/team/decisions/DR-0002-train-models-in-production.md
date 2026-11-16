---
title: "DR-0002: Production models are trained in production"
type: decision-record
owner: mle-lead
audience: [all]
status: draft
last_reviewed: 2026-11-11
review_cadence: 365d
tags: [models, mlops]
---

# DR-0002: Production models are trained in production

## Context

A model can reach production in two ways: the model trained during research is
reviewed and uploaded, or the research code is released and a production
pipeline trains the model again. The first is quicker for one model. The second
is the starting point for scheduled and triggered retraining, which every model
needs eventually. Junior data scientists find the second harder to accept,
because it means running training twice.

## Decision

Production models are trained by a production pipeline running released code
and a committed config. A model trained in research is never promoted. The first
production run must reproduce the research result, recorded in the experiment
tracker and in the config, within a stated tolerance
([DR-0003](DR-0003-track-experiments-on-mlflow.md) names the tracker).

## Alternatives considered

- **Promote research models after review.** Faster at first, but nothing proves
  the model can be rebuilt, and retraining later means building the pipeline
  anyway.
- **Promote research models only for expensive training runs.** Rejected: the
  answer to cost is to research on samples and make the production run the only
  full-scale run.

## Consequences

- Every model has a pipeline from its first release. The project template and an
  ML engineer pairing on each person's first pipeline make that cheap.
- The reproduction gate catches leakage, notebook state, and data differences
  before a stakeholder does.
- Retraining moves from manual to scheduled to triggered without rework. The
  triggered step needs model monitoring, which is not in place yet.

## Status

Proposed
