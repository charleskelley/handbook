---
title: Monitoring
type: general
owner: mle-lead
audience: [ds, mle, leadership]
status: draft
last_reviewed: 2026-11-15
review_cadence: 90d
sources: []
---

# Monitoring

!!! note "Gather first"

    The list of models in production, the alerts and reports that exist for
    each today, the on-call or ownership arrangement, and the risk appetite
    statement from [Regulation and risk](../business/index.md#regulation-and-risk).
    Thresholds and cadences that can change go in `facts/platform.yaml` or a
    monitoring entry in facts, not on this page.

Policy and register. The policy says what must be watched on every model in
production, at what thresholds, and who acts. The register says what is
watched today. How a monitor is built is
[model monitoring](../methods/development/model-monitoring.md) under
Methods.

## What every model must have watched

*Add: the minimum set, one line each: input drift per region of the
landscape, prediction drift per champion version, labelled performance once
labels arrive, the prediction log's completeness, and the cost of running
it. Say which are required before a model goes live and which may follow.*
Why: a model with no monitor is a loop that cannot report drift, and this
list is the gate.

## Thresholds and who acts

*Add: for each watched quantity, how a threshold is set (fixed, relative to
the reference run, or statistical), who is notified, within what time, and
what they are expected to do: fix, retrain, roll back, or escalate. Render
any number from facts.* Why: an alert nobody is obliged to act on is a
report, not monitoring.

## Operational cost

*Add: how the cost of running each model is captured and passed to Measure,
and at what cadence.* Why: this band supplies the cost side of Measure, and
the Cost arrow has to come from somewhere.

## Register

*Add: one row per model in production: model, owner, what is watched,
threshold basis, where the alert goes, last reviewed. Keep it on this page
until it has more rows than fit, then split it out.* Why: the register is
the answer to "is this model monitored", and the answer must be on one page.

| Model | Owner | Watched | Threshold basis | Alert goes to | Last reviewed |
|---|---|---|---|---|---|
| | | | | | |

## What we would need to believe to change this

*Add: the conditions under which the minimum set or the thresholds should
change: a new class of model, a regulatory change, an incident.* Why: a policy
page rots like any other.
