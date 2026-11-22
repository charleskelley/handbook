---
title: Training data
type: general
owner: ds-lead
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-22
review_cadence: 180d
tags: [labels, training-sets, data]
---

# Training data

What a model learns from: labels, and the training sets that join labels to
features. This is the point in the chain where what was known meets what
happened next.

## Labels

A label is the outcome a model is trained to predict, as defined in the
model's
[framing](../methods/framing-and-evaluating-a-prediction.md#the-framing):
what is predicted, from which data, over what window.

A feature and a label look in opposite directions from the same moment.

| | Looks | Answers |
|---|---|---|
| Feature | Back from the decision time | What was known then? |
| Label | Forward from the decision time | What happened next? |

This is why a label is never a feature table's column and is never read
through the [store](store.md). The store's whole promise is that it
returns nothing from after the time asked.

### What a label table carries

| Carried | What it is |
|---|---|
| Entity | The id of the thing the outcome belongs to |
| Decision time | The moment the outcome is counted from |
| Outcome | The value, under one written definition |
| When it became known | The time at which the outcome could first have been read |

The column names follow
[time columns](../methods/development/conventions.md#time-columns).

### Label practices

- **A label is not known until its window has closed.** A row whose outcome
  window is still open is not a negative. It is absent, and it stays out of
  training and out of performance measurement until the window closes.
- **Record when the outcome became known.** Some outcomes arrive late, and
  some are corrected after they arrive. The time it became known is what
  lets a past training set be rebuilt as it was.
- **One definition, used twice.** The label a model is trained on is the
  label its performance in production is measured against. Both read the
  same label table.
- **A changed definition is a new label.** It takes a new name beside the
  old one, as a changed measure does: see
  [restatement and backfill](../methods/development/conventions.md#restatement-and-backfill).

## Training sets

A training set is a label table joined to features, with each row's features
read as they stood at that row's decision time. The join is the store's read
at a point in time. A training set is never built by joining labels to the
latest value of a feature.

### Training set practices

- **A research run records the data it was fitted on.** See
  [Experiment tracking](../methods/development/experiment-tracking.md).
- **The training set of a full production training run is saved** to cold
  storage where possible. A table that has since been restated will not give
  the same rows again, and the saved set is the only exact record of what
  the model saw.
- **A training set is governed data**, like the tables it came from. It is
  held where governed data is held and does not land on a machine: see
  [Development environments](../methods/development/environments.md#data-never-lands-on-a-machine).
- **Nothing is built on a training set.** It is the record of one read. A
  feature that a second model needs is built in the
  [factory](factory.md), not copied out of the first model's
  training set.

!!! note "What a model's repository must document"

    A model's training data is documented in the model's repository, not in
    the handbook, as
    [data contracts](../methods/development/conventions.md#data-contracts):
    one for the label table and one for the saved training set. They are
    checked before the model goes to
    [production](../methods/development/path-to-production.md). Between
    them, the contracts and the repository's documentation must say:

    - **The label**: its definition, the data it is built from, its outcome
      window, and how the time it became known is set.
    - **The features**: each by name, and the version of the store's
      contract they were read under.
    - **The rows**: the population, and the range of decision times.
    - **The split**: how the rows were divided for evaluation.
    - **The saved set**: where the training set of the production training
      run is held.
