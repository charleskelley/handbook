---
title: Methods
type: general
owner: ds-lead
audience: [all]
status: draft
last_reviewed: 2026-11-13
review_cadence: 180d
tags: [applied-ml, outcome-loop]
sources:
  - "DPOM 0.3.0, Charles Kelley, https://doi.org/10.5281/zenodo.23814523"
---

# Methods

How the team practises applied machine learning: the landscape it works
across, what it owes in each part of it, the methods it uses within them, and
the development practices that carry the work. The analysis methods and model
families live in this section as **method** pages, one per method. This page
is the shape they fit into.

## Applied data science landscape

The [landscape](../index.md#applied-data-science-landscape) is on the home
page: four regions, read left to right, entered at Outcome; two bands beneath
them that every region drifts into and that supply the cost side of Measure;
one loop across the top that ends in scale, sustain, fix, or retire.

Each part below says three things: what the region owes, how the team
practises it, and what that runs on. Where the team has nothing yet, it says
so. An open loop that is written down is the first step to closing it.

## Outcome: start here

**What it owes.** A business result the organization has agreed it wants
moved, named before any data or modelling work starts, with the quantity it
will be measured in.

**How we practise it.** Every model names the KPI it is meant to move, from
the [Business](../business/index.md) section, and the decision the business
has agreed to make with its predictions. A model without a named outcome is
research, and is tracked as such.

**What it runs on.** A KPI page: definition, formula, owner, source of truth.
Nothing technical.

## Data

**What it owes.** A dataset fit for the named decision: the rows the decision
is made about, the signals known at decision time, and nothing from after it.

**How we practise it.** One directory per source system under
[Data](../data/index.md), domains as subpages, and the trust and quirks of
each table written where the table is described. Level 1 of the
[feature rule](development/experiment-tracking.md#feature-engineering-where-each-transformation-lives):
joins, filters, and history aggregations live in SQL in the feature vertical,
run once, and serve every consumer. Development can read production data, so
data never lands on a machine: see
[Development environments](development/environments.md#data-never-lands-on-a-machine).

**What it runs on.** The warehouse and the governed bucket, in the
[Technology](../technology/index.md) section.

## Prediction

**What it owes.** A decision the business acts on, not a model output. The
region ends at a recorded decision.

**How we practise it.** Method pages in this section, one per analysis method
or model family, each saying where it applies, when it is the wrong choice,
and what has been learned using it here. Research runs are tracked with a
fixture ([Experiment tracking](development/experiment-tracking.md)).
Production models are trained in production by released code, through a gate
that reproduces the research run
([Path to production](development/path-to-production.md)). Predictions are
served from batch.

**What it runs on.** [MLflow](../technology/mlflow.md),
[Vertex AI](../technology/vertex-ai.md),
[GitLab CI](../technology/gitlab-ci.md), and
[Artifactory](../technology/artifactory.md). Decided in
[DR-0001](../team/decisions/DR-0001-production-runs-ci-built-artifacts.md),
[DR-0002](../team/decisions/DR-0002-train-models-in-production.md),
[DR-0003](../team/decisions/DR-0003-track-experiments-on-mlflow.md), and
[DR-0004](../team/decisions/DR-0004-serve-from-batch.md).

## The decision handoff

**What it owes.** A written policy that turns a score into an action, and a
record of every decision: what was decided about, the score, the policy and
its version, the action, and when. Without the record nothing downstream can
be attributed, and the loop is open at its narrowest point.

**How we practise it.** Not yet. The intended practice is a decision log: a
table every decision is appended to, written by the same job that scores,
with a policy block in each model's config that names the rule, its version,
its owner, and a holdout fraction that receives no action, so that Measure has
a comparison group from the first day. The log's fields are chosen to match a
full decision ledger's, so moving to one later is a change of writer, not of
record.

**What it runs on.** Nothing yet. The
[prediction log](development/model-monitoring.md#the-prediction-log) records
what was predicted. It does not record what was decided.

## Measure

**What it owes.** Two answers. Whether the outcome is attributable to the
decisions, against a counterfactual, at a stated confidence. And what it cost,
across the whole landscape, to produce it. The net of the two is what a model
is worth. It is quantified in the outcome's own unit first; a proxy for its
money value is a separate, stated step.

**How we practise it.** Not yet. No model has a counterfactual for its
decisions, and no model has a cost figure. The holdout in the decision handoff
above is the first counterfactual. The cost side starts with the billed cost
of data, compute, and serving per model, which Infrastructure can supply, and
the people cost, which it cannot.

**What it runs on.** Nothing yet.

## Monitor & Govern

**What it owes.** The health of the system over time, drift in every region,
risk and audit, and the operational cost that feeds Measure's cost side.
Monitoring is not measurement: a healthy model can be worth nothing.

**How we practise it.** [Model monitoring](development/model-monitoring.md):
a prediction log, drift per champion version, labelled performance once labels
arrive, and reports a person reads. [Insights](../insights/index.md) record
the events that change how data should be read.
[Decision records](../team/decisions/index.md) record the team's own
decisions and why, blamelessly.

**What it runs on.** Vertex AI Model Monitoring, a weekly performance job, and
Evidently reports, decided in
[DR-0005](../team/decisions/DR-0005-monitor-with-vertex-and-evidently.md).

## Infrastructure

**What it owes.** The platform the landscape runs on, and the billed cost of
data, compute, and serving, by model, so Measure can see it.

**How we practise it.** [Development environments](development/environments.md)
and [Path to production](development/path-to-production.md): every
environment the same, every input through Artifactory, production running
only what CI built.

**What it runs on.** The [Technology](../technology/index.md) section, one
page per platform component.

## Scale, sustain, fix, retire

The loop's exit. A measured result has an owner and one of four paths: scale
the system, sustain it unchanged, fix it, or retire it. Sustain is a recorded
verdict, not the absence of one. A drift alert prompts a fix; only Measure can
say scale, sustain, or retire. Promotion stays a person's decision at every rung of
the [retraining ladder](development/path-to-production.md#the-retraining-ladder).
Not yet practised beyond that, because Measure is not yet built.

## Pages

- [Development practices](development/index.md): style guides, conventions,
  environments, path to production, experiment tracking, model monitoring.

*No method pages yet. Start with the methods used on the outcome the team is
most often asked about.*
