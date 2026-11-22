---
title: "Experiment tracking"
type: general
owner: mle-lead
audience: [ds, mle]
status: draft
last_reviewed: 2026-11-11
review_cadence: 180d
tags: [experiments, mlops, research]
sources:
  - "https://mlflow.org/docs/latest/ml/dataset/"
---

# Experiment tracking

How research runs are recorded so that the one you choose can be reproduced in
production. Runs go to the team [MLflow server](../../technology/mlflow.md).
The rule is short: **the run production reproduces must exist, and it must have
left a fixture behind.**

## The loop

A research day on a workstation or in a hosted notebook:

1. Sync the project, and point its settings at dev and the tracking server.
   The experiment name defaults to the model name, so everyone working on a
   model sees the same runs.
2. Load a frame once through the project's data module. The frame remembers
   its table and snapshot date.
3. Set the out-of-time holdout aside (below). Nothing is chosen with it.
4. Fit things, many times, on the in-time data. Wrap the fits you would want
   to come back to in a tracked run: record the dataset, the params that
   reproduce the fit, and the metrics you will choose between fits with.
5. Compare runs in the notebook: the tracking module returns every run in the
   experiment as a table with params, metrics, and tags as columns. Use the
   MLflow UI to show someone else, or to read an artifact.
6. When one wins, score the holdout with it once and record the run as the
   reference (below).

## In time and out of time

The data is split by time before anything is fitted.

| Set | What it is | Used for |
|---|---|---|
| In-time data | The earlier as-of dates | Split into training and test data, with cross-validation, for tuning and for choosing between models |
| Out-of-time holdout | The latest as-of dates | Scored once, by the model that was chosen. Its rows and scores are the fixture |

- **The holdout is always out of time.** It stands in for the future, so it
  comes after everything the model was fitted and chosen on.
- **Every choice is made in time.** Tuning and model selection use the
  in-time split and cross-validation. A holdout that has been used to make
  a choice is no longer a holdout.
- **The rest of the rules are on the framing page**, including which
  training rows are dropped because their outcome window runs into the
  holdout: see
  [Splitting the data](../framing-and-evaluating-a-prediction.md#splitting-the-data).

### In-time folds

Random folds of rows are the commonest cause of an in-time score that is too
good. Where the same entity is scored at many dates, its rows fall on both
sides of a fold with nearly the same features, and the model is tested on
what it has already seen. So the folds are built from the shape of the data.

| The data | In-time folds |
|---|---|
| Enough periods to spare | Blocked by time: fit on earlier as-of dates, validate on later ones, rolling forward |
| Too few periods for that | Grouped by entity, so that no entity is on both sides of a fold |
| One row for each entity, and no outcome windows that overlap | Random folds of rows |

Blocked by time is the default where the history allows it, and grouped by
entity is the least that is accepted where it does not. In both, training
rows whose outcome window runs into a fold's validation rows are dropped, as
they are before the holdout.

### Keeping the holdout honest

- **Record the gap.** The reference run logs the in-time score and the
  out-of-time score side by side. A large gap between them is the sign of
  overfitting, and it is on the run for a reviewer to see.
- **A holdout that fails is not tuned against.** Going back to change the
  model and scoring the same holdout again turns it into validation data.
  Move the holdout forward to newer as-of dates and start again. Where there
  is no newer data, the reference run records how many times the holdout was
  scored.

## What a run records on its own

Every tracked run is tagged with the git commit, whether the checkout was
dirty, the package version, the user, and the environment. Recording the
dataset logs the table and snapshot date, the schema, and a content digest.
None of this is typed by hand, because none of it would be.

## What to log

| Logged as | What it is |
|---|---|
| Params | What you need to run the fit again |
| Metrics | What you use to choose between fits, starting with the main measure in the model's [framing](../framing-and-evaluating-a-prediction.md#measures) |
| Artifact | Anything else worth coming back to |

A grid search is one decision, not fifty runs: log the grid as params, the
best point's metrics, and the full results as an artifact. What this means
for each modeling library, and when automatic logging is worth switching on,
is on the [MLflow page](../../technology/mlflow.md#what-to-log-by-library).

## The fixture and the reference

Metrics alone are a weak gate: two different models can share a metric. A
research run worth shipping therefore leaves a **fixture**, the rows of its
out-of-time holdout with its scores, in the governed bucket. The run that
produces it calls the package's training recipe, not notebook code, and
records the holdout and the metrics the recipe returns.

The holdout is set by as-of dates in the model's config, so it is the same
rows in a notebook, on a workstation, and in the production pipeline, and the
production run that reproduces the reference never trains on them. The
project's reference command, given the winning run's id, writes the run id,
the fixture's location and digest, and the metrics into the model's config.
That is the only way the reference is written.

In production, the gate scores the same fixture with the freshly trained model
and checks two things: every recorded metric within tolerance, and rank
agreement with the research scores above the configured minimum.

## Feature engineering: where each transformation lives

Notebooks drift from production at the feature step more than anywhere else, so
the rule is explicit. Prototype freely in a cell; before the reference run,
every transformation is in one of three places:

| Level | What | Where it lives | Why there |
|---|---|---|---|
| 1 | Joins, filters, aggregations over history | The [feature factory](../../data/factory.md), or the project's data module that loads the frame | Runs once for every consumer |
| 2 | Per-row derived columns | The package's features module, one pure function per feature, applied by name | Ships with the package, is unit tested, and is logged by name |
| 3 | Fitted transforms: scaling, encoding, imputation | Inside the model pipeline, saved with the model | Fitted on training data only and shipped inside the artifact |

The enforcement is mechanical. The reference command refuses a run that was
logged from a dirty checkout or that saved no fixture. A feature defined in a
cell means either the checkout is dirty or the features module cannot find the
feature. Commit the function, log the run again, then record it. An ML
engineer pairs on each person's first one.

## What stays in the model registry

MLflow records runs. The [model registry](../../technology/vertex-ai.md)
remains the catalog of production models, because model monitoring hangs off
it. Do not register models in MLflow; log them as artifacts if you want them
back, and let the production pipeline register the one that ships.

## See also

- [Path to production](path-to-production.md)
- [Framing and evaluating a prediction](../framing-and-evaluating-a-prediction.md)
- [MLflow tracking server](../../technology/mlflow.md)
- [DR-0003](../../team/decisions/DR-0003-track-experiments-on-mlflow.md)
