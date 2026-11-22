---
title: "DR-0004: Predictions are served from batch; real-time scoring only when required"
type: decision-record
owner: mle-lead
audience: [all]
status: draft
last_reviewed: 2026-11-12
review_cadence: 365d
tags: [serving, mlops]
---

# DR-0004: Predictions are served from batch; real-time scoring only when required

## Context

An online scoring service is the default shape of "ML in production" in most
tutorials, and the most expensive to run well: a model process to keep warm,
feature parity between training and the request path, request logging for
monitoring, and latency to defend. Most of the team's use cases consume
predictions in a batch or on a page, and the feature data they need is
computed in the warehouse on a schedule anyway.

## Decision

Models score in batch, or microbatch, in scheduled jobs, writing an output
table and appending every prediction to the prediction log. Where a system
needs a prediction by key, it reads the output table or the lookup service, a
small web service that holds the latest batch in memory and answers by
entity id. No model runs per request. Real-time scoring, a cache store, or
the platform's managed endpoints are added for a model only when freshness
or latency require it, with a decision record that says which and why.

## Alternatives considered

- **A real-time scoring service for every model.** The earlier skeleton did
  this. Rejected as the default: it doubles the feature path and the logging
  path for a latency most consumers do not need.
- **The platform's managed endpoints.** Fine when real-time is required and the model is in
  the registry already; not needed for lookup.

## Consequences

- One prediction log, written by one job, is the source for monitoring.
- The lookup service is stateless apart from a cache, and scales to zero.
- A model that does need real-time scoring is a visible exception with its own
  record, not a silent default.

## Status

Proposed
