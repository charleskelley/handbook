---
title: "DR-0003: Experiments are tracked on a team MLflow server, models stay in the Vertex AI registry"
type: decision-record
owner: mle-lead
audience: [all]
status: draft
last_reviewed: 2026-11-11
review_cadence: 365d
tags: [experiments, mlops]
---

# DR-0003: Experiments are tracked on a team MLflow server, models stay in the Vertex AI registry

## Context

[DR-0002](DR-0002-train-models-in-production.md) requires production training
to reproduce a recorded research run. That needs a tracker every research run
goes through, and the tracker has to be cheap to use from a notebook or the gate
will be fed numbers typed by hand. Vertex AI Experiments logs params and metrics
but has no dataset record, no evaluation helpers, needs a TensorBoard instance
for anything over time, and a thin comparison UI; using it well meant writing a
client library that MLflow already is. MLflow has an official recipe for Google
Cloud, autologging for scikit-learn and statsmodels, dataset digests, and a
validation API. It costs one Cloud Run service and a small Cloud SQL instance.

## Decision

Research and production runs are logged to a team MLflow tracking server on
Cloud Run in the dev project, authenticated by Google identity tokens. Models
are not registered in MLflow: the Vertex AI Model Registry remains the catalog
of production models, because model monitoring hangs off it. The research run
production must reproduce is named in the config by run id, with a fixture of
its holdout rows and scores, and the gate checks both metrics and rank
agreement against that fixture. The reference is written only by
`example-model reference`, which refuses runs from a dirty checkout or without
a fixture.

## Alternatives considered

- **Vertex AI Experiments with thin helpers.** No server to run, and it is kept
  as the fallback if the server is refused, with the plan in the skeleton. More
  code to own for a worse tool.
- **A hosted tracker (Weights & Biases, Neptune, Comet).** Artifacts that can
  carry personal data would leave the perimeter, and procurement would take
  longer than the Terraform.
- **MLflow's model registry instead of Vertex AI's.** Would work for the
  catalog, but monitoring and pipelines on Vertex AI expect the Vertex entry.
  Two registries would be worse than either.

## Consequences

- One more service and database to run; MLflow upgrades are a runbook item.
- Every research run worth shipping leaves a fixture in the governed bucket,
  which is also the artifact a reviewer can look at.
- Notebook-defined features cannot reach the reference, which is a habit to
  teach, not a tool to buy.
- If the server is refused, the fallback plan in `examples/dev-env/` keeps the
  fixture, the gate, and the reference command unchanged and swaps only the
  tracker.

## Status

Proposed
