---
title: "MLflow tracking server"
type: platform
owner: mle-lead
audience: [ds, mle]
status: draft
last_reviewed: 2026-11-11
review_cadence: 180d
tags: [mlflow, experiments]
sources:
  - "https://mlflow.org/docs/latest/self-hosting/deploy-to-cloud/gcp/"
---

# MLflow tracking server

## What it is for

Recording research runs and the production runs that reproduce them: params,
metrics, tags, datasets, and artifacts. How to use it from code is on
[Experiment tracking](../methods/development/experiment-tracking.md). It is
not the model registry; that is [Vertex AI](vertex-ai.md).

## Architecture

```mermaid
flowchart LR
    W[Workstation, Workbench, laptop] -- identity token --> S[Cloud Run: mlflow server]
    T[Production training pipeline] -- identity token --> S
    S --> D[(Cloud SQL Postgres)]
    S -- serves artifacts --> B[(Artifact bucket)]
    CI[GitLab CI] -- builds image --> A[Artifactory] --> M[Artifact Registry mirror] --> S
```

MLflow's own GCP recipe: the server on Cloud Run, the backend store in Cloud
SQL, artifacts in a bucket the server proxies so clients need no bucket access.
The service requires IAM authentication. The project's MLflow plugin attaches a
Google identity token to every request: a service account's token for the
service URL, or a person's token from `gcloud`. It lives in the dev project; the
production training service account is granted access so its runs land beside
the research runs. The service, the database, the bucket, and the access
grants are one module in the infrastructure repository; the server image is
built by CI from a pinned MLflow version.

## How we use it

- The tracking URI setting is `{{ platform.dev.mlflow_url }}` in every
  project's `.env`, and a CI variable carries the same address.
- One experiment per model, named after the model.
- The UI at the same address, for comparing runs and reading artifacts.
- Fixtures do not go here: they go to the governed bucket, and the run records
  where.

## Limits and quotas

- Cloud Run scales to zero. The database is the only always-on cost, on the
  smallest tier until it is slow.
- Database and artifact storage limits: *[unverified: needs source]*.

## Owner and support path

Owner: {{ platform.components.mlflow.owner }}. Support:
{{ platform.components.mlflow.support_channel }}.

## Runbooks

- **Upgrade.** Bump the MLflow version in the server image's CI
  configuration, let CI build, then change the image tag in the dev
  infrastructure. The server runs schema migrations at start; take a Cloud SQL
  backup first.
- **403 from a workstation.** You are not in the team group, or the token is
  stale: `gcloud auth login` again. The plugin caches a token for 45 minutes.
- **The UI is slow to open.** Cold start after scaling to zero. Wait, do not
  raise the minimum instances unless it happens all day.

## Known issues

- Runs logged from a dirty checkout cannot become the reference, by design.
  People find this out the first time they try.
