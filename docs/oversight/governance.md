---
title: Governance
type: general
owner: ds-lead
audience: [ds, mle, leadership]
status: draft
last_reviewed: 2026-11-15
review_cadence: 180d
sources: []
---

# Governance

!!! note "Gather first"

    The company's model risk, data access, and privacy policies if they
    exist; the regulators and rules named under
    [Regulation and risk](../business/index.md#regulation-and-risk); and the
    current approval path for a model going live. Do not write a rule the
    company has not adopted; mark the gap with `*[unverified: needs source]*`.

The rules a model must satisfy before and after it goes live, and who decides.
Governance is the limit monitoring is held to and the authority that changes a
running model. Decisions the team makes about its own practice are
[decision records](../team/decisions/index.md), not governance.

## Risk appetite applied

*Add: what the business's stated risk appetite and operating constraints mean
for models: the decisions a model may make alone, the ones that need a person,
and the ones a model may not make.* Why: the Business section states the
appetite; this section is where it binds.

## Approval to go live

*Add: who approves a model for production, what they see (the reproduction
gate, the monitoring plan, the decision log entry), and what they sign. Link
to [path to production](../methods/development/path-to-production.md) for
the engineering gate.* Why: promotion is a person's decision at every rung,
and the person needs a stated basis.

## Changing a running model

*Add: who may retrain, roll back, or retire a model, and what record each
change leaves.* Why: a change nobody can trace is a drift nobody can explain.

## Access and privacy

*Add: the rules on who may see which data and predictions, how personal data
is handled in training and logging, and the retention of the prediction log.
Link to [secrets](../technology/secrets.md) and the Data pages for the
mechanics.* Why: the prediction log is personal data in most businesses.

## Model risk

*Add: how models are tiered by the harm a wrong decision does, and what each
tier requires: review depth, monitoring, a holdout. If the company has no
tiering, say so and propose the smallest one.* Why: the same rules for a
marketing ranker and a credit decision is the wrong amount of rigour for
both.

## What we would need to believe to change this

*Add: the conditions under which these rules should change.* Why: a policy
page rots like any other.
