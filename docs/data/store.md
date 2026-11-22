---
title: Store
type: general
owner: mle-lead
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-22
review_cadence: 180d
tags: [features, feature-store, data]
---

# Store

The feature store is where a model, a notebook, or a scoring job gets its
features: by name, for a list of entities, as of a time. It serves the
[factory](factory.md)'s tables and computes nothing of its own.

## What it is

Views over the factory's output

:   The store reads the factory's tables from the factory's own output
    location and from nowhere else. A feature in the store is a column of a
    factory table, under the same name.

A contract

:   For each feature: its name, the entity it is keyed by, its type, and its
    version. The contract is what a model depends on, and what a change to a
    feature is checked against.

One way to read

:   A consumer asks for features by name through the store's interface. It
    does not write its own join to the tables underneath.

A read at a point in time

:   Given entities and a time for each, the store returns each feature as it
    stood at that time.

## What the store promises

- **The same value for training and for scoring.** Both read through the
  same interface from the same tables, so a model is scored on features
  built the way its training features were.
- **Nothing from after the time asked.** For each entity, a read returns the
  latest row that was usable at that time. The rule, and the declared lag it
  depends on, are on
  [Conventions](../methods/development/conventions.md#reading-a-table-at-a-point-in-time).
- **A missing feature fails the read.** A feature that was renamed or
  retired stops the consumer with an error. It does not come back empty.
- **Freshness is stated.** Each view says when it was last loaded, so a
  consumer can state the oldest value it will accept.
- **A version says what changed.** Which code produced which features is
  settled by the factory's version and the store's contract,
  not by renaming a feature.

## What the store does not do

- **Define a feature.** Definitions are in the factory. The reasons are on
  [Factory](factory.md#why-it-is-a-stage-of-its-own).
- **Repair the factory's tables.** The store's read at a point in time is
  only as good as the time columns it is given. If a table overwrote its
  history, the store serves the overwritten value.
- **Hold labels.** A label is what happened after the time asked, which is
  exactly what a feature read must not return. See
  [Training data](training-data.md).

## Serving by key

Models are scored in batch, and a batch reads the same views that training
does. Where a decision needs a feature by key at the moment of a request,
the copy that answers it is loaded from the same factory output as
everything else, never from a second computation. Nothing is served this way
until a decision needs it: see
[DR-0004](../team/decisions/DR-0004-serve-from-batch.md).

## Reading from the store

- **A model in production reads through the store** for training, for batch
  scoring, and for serving, and asks for its features by name.
- **A training set is a read at many points in time**: each label's row gets
  the features as they stood at that row's decision time. See
  [Training data](training-data.md#training-sets).
- **A feature is retired in order.** It is marked as deprecated in the
  store, its readers are found and moved, and only then is it removed from
  the factory.

!!! note "What the store's documentation must carry"

    The store is a project with its own documentation. The detail of its
    views and features is kept there, not in the handbook. That
    documentation must say:

    - **For every view**: the factory table it serves, the entity it is
      keyed by, and when it was last loaded.
    - **For every feature**: its name, its type, its version, and whether it
      is deprecated.
    - **For every feature**: which models read it.
    - **For the contract**: its version, and what each version changed.
    - **For a consumer**: how to ask for features by name, and how to read
      them at a point in time.
    - **For serving by key**: which features have a copy that answers by
      key, and how old a value it may return.

*Add: a link to the store's documentation in place of the note above, once
it is published, with its address kept in `facts/apps.yaml`.* Why: the
handbook holds the concept and the project holds the detail, so a reader has
to be able to get from one to the other.
