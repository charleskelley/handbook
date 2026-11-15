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
  - "https://mlflow.org/docs/latest/ml/tracking/autolog/"
  - "https://mlflow.org/docs/latest/ml/dataset/"
---

# Experiment tracking

How research runs are recorded so that the one you choose can be reproduced in
production. Runs go to the team [MLflow server](../../technology/mlflow.md).
The rule is short: **the run production reproduces must exist, and it must have
left a fixture behind.**

## The loop

A research day on a workstation or in a Workbench notebook:

1. Sync the project, and point its settings at the dev project and the tracking
   server. The experiment name defaults to the model name, so everyone working
   on a model sees the same runs.
2. Load a frame once through the project's data module. The frame remembers
   its table and snapshot date.
3. Fit things, many times. Wrap the fits you would want to come back to in a
   tracked run: record the dataset, the params that reproduce the fit, and the
   metrics you will choose between fits with.
4. Compare runs in the notebook: the tracking module returns every run in the
   experiment as a DataFrame with params, metrics, and tags as columns. Use the
   MLflow UI to show someone else, or to read an artifact.
5. When one wins, record it as the reference (below).

## What a run records on its own

Every tracked run is tagged with the git commit, whether the checkout was
dirty, the package version, the user, and the environment. Recording the
dataset logs the table and snapshot date, the schema, and a content digest.
None of this is typed by hand, because none of it would be.

Autolog is off. MLflow's `autolog()` covers scikit-learn and statsmodels, but it
logs every `fit()` inside a cross-validation and knows nothing about the data
snapshot. Switch it on in a cell for a grid search if you want the parent and
child runs; otherwise log what you chose.

## What to log, by library

Params are what you need to re-run the fit. Metrics are what you use to choose
between fits. Anything else is an artifact.

| Library | Params | Metrics | Artifact |
|---|---|---|---|
| scikit-learn | `model.get_params()`, flattened to `clf__C` style | Your `evaluate()`, or `mlflow.models.evaluate` for the standard set with plots | The fitted pipeline, if you will come back to it |
| statsmodels | Formula or exog names, family, fit method | `aic`, `bic`, `llf`, pseudo R², convergence, plus your decision metric | `summary().as_text()`: the coefficient table is what you reread |
| PyTorch | The hyperparameter dict you already have | Final-epoch metrics | The loss curve as a CSV. Time-series metrics need a TensorBoard instance, which we do not run |
| scipy | Initial guess, bounds, method | Fitted parameters, residual norm, `success`, `nfev` | None |

A grid search is one decision, not fifty runs: log the grid as params, the best
point's metrics, and `cv_results_` as a CSV artifact.

## The fixture and the reference

Metrics alone are a weak gate: two different models can share an AUC. A research
run worth shipping therefore leaves a **fixture**, its holdout rows with its
scores, in the governed bucket. The run that produces it calls the package's
training recipe, not notebook code, and records the holdout and the metrics
the recipe returns.

The holdout is chosen by hashing the entity id with the config's seed, so it is
the same rows in a notebook, on a workstation, and in the production pipeline,
and production never trains on them. The project's reference command, given
the winning run's id, writes the run id, the fixture's location and digest,
and the metrics into the model's config. That is the only way the reference
block is written.

In production, the gate scores the same fixture with the freshly trained model
and checks two things: every recorded metric within tolerance, and rank
agreement with the research scores above the configured minimum.

## Feature engineering: where each transformation lives

Notebooks drift from production at the feature step more than anywhere else, so
the rule is explicit. Prototype freely in a cell; before the reference run,
every transformation is in one of three places:

| Level | What | Where it lives | Why there |
|---|---|---|---|
| 1 | Joins, filters, aggregations over history | The feature factory: SQL in the feature vertical, or the query that loads the frame | Runs once for every consumer |
| 2 | Per-row derived columns | The package's features module, one pure function per feature, applied by name | Ships with the package, is unit tested, and is logged by name |
| 3 | Fitted transforms: scaling, encoding, imputation | Inside the model pipeline (`sklearn.Pipeline`, a patsy formula, a saved preprocessing step for a torch model) | Fitted on train only and shipped inside the artifact |

The enforcement is mechanical. The reference command refuses a run whose
dirty-checkout tag is true or that saved no fixture. A feature defined in a
cell means either the checkout is dirty or the features module cannot find the
feature. Commit the function, log the run again, then record it. An ML
engineer pairs on each person's first one.

## What stays on Vertex AI

MLflow records runs. The [Vertex AI Model Registry](../../technology/vertex-ai.md)
remains the catalog of production models, because model monitoring hangs off
it. Do not register models in MLflow; log them as artifacts if you want them
back, and let the production pipeline register the one that ships.

## See also

- [Path to production](path-to-production.md)
- [MLflow tracking server](../../technology/mlflow.md)
- [DR-0003](../../team/decisions/DR-0003-track-experiments-on-mlflow.md)
