---
title: Decision log
type: general
owner: ds-lead
audience: [ds, mle, leadership]
status: draft
last_reviewed: 2026-11-15
review_cadence: 180d
sources: []
---

# Decision log

!!! note "Gather first"

    The [decision inventory](../business/decisions.md) rows whose mechanism
    is a rule or a model, the policy that turns each score into an action,
    and wherever those decisions are recorded today, if anywhere. This page
    is a contract, not a system: it says what a record must contain, not how
    it is stored.

The record of the decisions models and rules drive, kept so that every
decision can be audited and replayed. This is where the Decision handoff lands
in the Monitor & Govern band. The glossary separates a
[decision log](../reference/glossary.md) from a decision record: the log holds
business decisions made at run time, the record holds the team's own.

## What a record contains

*Add: the fields every entry carries: the prediction, the policy that turned
it into an action (with its version and owner), the action, the actor, the
time, the basis, and the holdout assignment if there is one. Define each in
one line.* Why: a decision with no record has no outcome to attribute.

## The policy block

*Add: the contract for a policy: the rule, its version, its owner, the holdout
fraction, and its mode (live, shadow, or control). Say who may change a
policy and what record the change leaves.* Why: the policy is the handoff; a
model output without one is a prediction, not a decision.

## Replay

*Add: what it means to replay a decision: given the record, reproduce the
action, and given a changed policy, say what the action would have been. Say
what is retained for how long to make that possible.* Why: replay is how a
counterfactual is built after the fact and how an audit is answered.

## Who reads it and when

*Add: the audiences: Measure for attribution, governance for audit, the
decider for appeal or explanation; and the cadence or trigger for each.* Why:
a log nobody reads is storage.

## What we would need to believe to change this

*Add: the conditions under which the contract should change.* Why: a contract
page rots like any other.
