---
title: "DR-0003: Experiments are tracked on a team MLflow server, models stay in the model registry"
type: decision-record
owner: mle-lead
audience: [all]
status: draft
last_reviewed: 2026-11-11
review_cadence: 365d
tags: [experiments, mlops]
---

# DR-0003: Experiments are tracked on a team MLflow server, models stay in the model registry

## Context

[DR-0002](DR-0002-train-models-in-production.md) requires production training
to reproduce a recorded research run. That needs a tracker every research run
goes through, and the tracker has to be cheap to use from a notebook or the gate
will be fed numbers typed by hand. The cloud platform's own experiment tracker
logs params and metrics but has no dataset record, no evaluation helpers,
needs a separate service for anything over time, and has a thin comparison
UI; using it well meant writing a client library that MLflow already is.
MLflow has an official recipe for the team's cloud, autologging for the
modeling libraries the team uses, dataset digests, and a validation API. It
costs one small service and one small database.

## Decision

Research and production runs are logged to a team MLflow tracking server,
run as a service in dev and authenticated by the cloud's identity tokens.
Models are not registered in MLflow: the platform's model registry remains
the catalog of production models, because model monitoring hangs off it. The research run
production must reproduce is named in the config by run id, with a fixture of
its holdout rows and scores, and the gate checks both metrics and rank
agreement against that fixture. The reference is written only by the
project's reference command, which refuses runs from a dirty checkout or
without a fixture.

## Alternatives considered

- **The platform's own experiment tracker, with thin helpers.** No server to run, and it is kept
  as the fallback if the server is refused, with the plan in the skeleton. More
  code to own for a worse tool.
- **A hosted tracker from a vendor.** Artifacts that can carry personal data
  would leave the perimeter, and procurement would take longer than writing
  the infrastructure code.
- **MLflow's model registry instead of the platform's.** Would work for the
  catalog, but the platform's monitoring and pipelines expect an entry in
  its own registry. Two registries would be worse than either.

## Consequences

- One more service and database to run; MLflow upgrades are a runbook item.
- Every research run worth shipping leaves a fixture in the governed bucket,
  which is also the artifact a reviewer can look at.
- Notebook-defined features cannot reach the reference, which is a habit to
  teach, not a tool to buy.
- If the server is refused, the fallback is the platform's own tracker. It keeps
  the fixture, the gate, and the reference command unchanged and swaps only
  the tracker.

## Status

Proposed
