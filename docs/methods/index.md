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
[Sources](../data/sources/index.md), domains as subpages, and the trust and quirks of
each table written where the table is described. Level 1 of the
[feature rule](development/experiment-tracking.md#feature-engineering-where-each-transformation-lives):
joins, filters, and history aggregations live in the feature factory, run
once, and serve every consumer. Development can read production data, so
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
arrive, and reports a person reads. That is the engineering. What must be
watched on every model, who acts, and what the business's risk appetite
requires are policy, and policy lives in [Oversight](../oversight/index.md),
along with the [insights](../oversight/insights/index.md) that record the
events that change how data should be read.
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

The pages are in three groups. A method is filed by what it produces, not by
the technique it uses.

Each method page is at one of two depths, marked beside it below. A **build**
page is the full contract: a reader can carry the method out from it. A
**guide** page is orientation: what the approaches are, how to question a
result someone else produced, and where the canonical reading is. A guide
becomes a build page when the team builds the method.

### Analysis

Methods that end in a finding a person interprets: a description, a
comparison, or an estimate of an effect. Experiments and causal designs
belong here, including those that fit a model on the way to the estimate.

Understanding the business:

- [Customer-base audit](customer-base-audit.md) (build): a descriptive
  framework for reading revenue and profit by customer, through five lenses.
- [RFM analysis](rfm-analysis.md) (build): customers scored and grouped by
  how recently, how often, and how much they bought.
- [Survival analysis](survival-analysis.md) (build): how long until
  something happens, when for many customers it has not happened yet.
- [Decomposing a change](decomposing-a-change.md) (build): splitting the
  movement in a number into rate and mix, components, or price, volume, and
  mix.
- [Funnel analysis](funnel-analysis.md) (guide): where along a path
  customers are lost, for the acquisition, retention, and development
  questions an audit raises.
- [Segmentation](segmentation.md) (guide): dividing customers into groups
  that will be treated differently.

Experiments and causal claims:

- [Directional versus causal](directional-versus-causal.md) (principles):
  what separates "it moved" from "the action moved it", and the grades of
  evidence.
- [Causal diagrams](causal-diagrams.md) (guide): drawing what causes what,
  and deciding what to adjust for.
- [Stating uncertainty](stating-uncertainty.md) (principles): what to
  report beside every estimate.
- [Experiments and lift tests](experiments-and-lift-tests.md) (build):
  designing, sizing, and analysing a randomized test, and reading a lift a
  tool reports.
- [Measuring impact without an experiment](measuring-impact-without-an-experiment.md)
  (guide): choosing a design when randomization is not possible.
- [Difference-in-differences](difference-in-differences.md) (build): a
  change some units got and others did not.
- [Matching](matching.md) (guide): making groups alike, to analyse
  observational data and to design tests on few units.
- [Synthetic control](synthetic-control.md) (guide): a comparison built
  from untreated units, for a change to one market or region.
- [Marketing mix modeling](marketing-mix-modeling.md) (guide): sales
  explained by marketing over time, and how far to trust it.

### Modeling

Methods that end in an artifact built to an objective, which then runs on new
data and is deployed and monitored.

- [Framing and evaluating a prediction](framing-and-evaluating-a-prediction.md)
  (build): stating what is predicted, for what decision, and showing the
  model beats the baseline. Every model page leans on it.
- [Linear and logistic regression](regression.md) (build): the adjustment
  tool for analysis and the baseline for every prediction.
- [Gradient-boosted trees](gradient-boosted-trees.md) (guide): the default
  step up from regression for tabular data.
- [Churn and propensity models](churn-and-propensity.md) (build): scoring
  customers on what they will do next. The recommended first model to take
  end to end.
- [Customer lifetime value](customer-lifetime-value.md) (build): what a
  customer will be worth from now on.
- [Time-series forecasting](time-series-forecasting.md) (build): future
  values of a number recorded over time.
- [Uplift modeling](uplift-modeling.md) (guide): predicting whom an action
  will change.
- [Anomaly detection](anomaly-detection.md) (guide): finding what does not
  fit, on data that is uneven to begin with.
- [Recommenders](recommenders.md) (guide): choosing which few items to show
  each customer.

### Development

- [Development practices](development/index.md): style guides, conventions,
  testing, environments, path to production, experiment tracking, model
  monitoring.

### Where to start

Two threads through these pages take a new team end to end.

The customer thread follows one loop of the landscape above. Describe the
customers with the [customer-base audit](customer-base-audit.md) and
[RFM analysis](rfm-analysis.md). Read
[framing and evaluating a prediction](framing-and-evaluating-a-prediction.md),
then build a [churn model](churn-and-propensity.md) on features that are the
RFM measures as of a date, first as a [regression](regression.md). Test the
action the scores are used for with a
[holdout](experiments-and-lift-tests.md). That closes the loop from Outcome
through Measure with nothing but the transaction history.

The planning thread is
[time-series forecasting](time-series-forecasting.md) for finance and
operations, with [decomposing a change](decomposing-a-change.md) for the
question that follows every forecast miss.

Read [directional versus causal](directional-versus-causal.md) and
[stating uncertainty](stating-uncertainty.md) before presenting anything to
a partner.
