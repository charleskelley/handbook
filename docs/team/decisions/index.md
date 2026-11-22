---
title: Decision records
type: general
owner: ds-lead
audience: [all]
status: draft
last_reviewed: 2026-10-24
review_cadence: 180d
---

# Decision records

One file per decision, numbered, append-only once accepted. A record says what
was decided, what else was considered, and what follows from it, so the reason
survives the people who made it.

To add one, copy `templates/decision-record.md` to
`docs/team/decisions/DR-NNNN-short-slug.md`, using the next number, and add it
to the list below and to the navigation.

## Records

| Number | Title | Status | Date |
|---|---|---|---|
| [DR-0001](DR-0001-production-runs-ci-built-artifacts.md) | Production runs only CI-built artifacts from the artifact registry | Proposed | 2026-11-11 |
| [DR-0002](DR-0002-train-models-in-production.md) | Production models are trained in production | Proposed | 2026-11-11 |
| [DR-0003](DR-0003-track-experiments-on-mlflow.md) | Experiments are tracked on a team MLflow server, models stay in the model registry | Proposed | 2026-11-11 |
| [DR-0004](DR-0004-serve-from-batch.md) | Predictions are served from batch; real-time scoring only when required | Proposed | 2026-11-12 |
| [DR-0005](DR-0005-monitor-with-vertex-and-evidently.md) | A managed monitor alerts, Evidently explains, people promote | Proposed | 2026-11-12 |
