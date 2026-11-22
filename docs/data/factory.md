---
title: Factory
type: general
owner: mle-lead
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-22
review_cadence: 180d
tags: [features, factory, data]
---

# Factory

The feature factory turns [sources](sources/index.md) into feature
tables. It holds the joins, filters, and aggregations over history that
every model would otherwise write for itself. It sits between the sources
and the [store](store.md), and it is where a feature is defined.

## What it does

A source is shaped for running the business. A model needs the same data
shaped around the thing it predicts for and the moment it predicts at: one
row for an entity at a time, carrying what was known then. The factory does
that reshaping once, for every consumer.

Not every transformation belongs here. The factory holds the work that is
the same for every model: joins, filters, and aggregations over history.
A column derived from one row, and a transform fitted on training data, stay
with the model. The rule is on
[Experiment tracking](../methods/development/experiment-tracking.md#feature-engineering-where-each-transformation-lives).

## Why it is a stage of its own

A feature store can be pointed straight at source tables, and many stores
offer to do the transformation themselves. The team keeps the factory as a
separate stage in front of the store for four reasons.

1. **The store serves whatever it is given.** Whether a value is correct at
   a point in time is settled when the table is built: what a row describes,
   when it was written, and whether history was overwritten. A table that
   writes today's value over a past row leaks the future into training, and
   the store will serve that leak faithfully.
2. **The heavy work runs once.** A join or an aggregation over history is
   the expensive part of a feature. Built in the factory, it is computed one
   time, and training, batch scoring, and serving all read the same result.
   Built in each consumer, it is computed many times and drifts into
   several versions of one feature.
3. **A definition is code the team owns.** It is written in the team's own
   transformation code, where it is reviewed, versioned, and tested on
   synthetic data like any other software. It is not held in a serving
   product's configuration, so the store, or the engine underneath it, can
   be replaced without redefining a feature.
4. **The store's contract stays thin.** With the logic upstream, the store
   has only names, keys, types, and versions to keep. A thin contract is one
   that can be checked, and one that a reader can hold in their head.

The two stages also change for different reasons. The factory changes when a
definition changes. The store changes when a consumer's way of reading
changes. Keeping them apart means one kind of change does not put the other
at risk.

## More than one engine

The factory is a role, not a tool. Most of it is SQL, run in the warehouse.
Some sources cannot be worked there. Data in a data
lake that is too large, too raw, or too far from tabular for SQL is
transformed by a pipeline on a distributed processing engine.

That pipeline is part of the factory, and the factory's contract does not
depend on the engine.

| Whatever the engine | The rule |
|---|---|
| Output | A factory table with the names, the time columns, and a declared key, as on [Conventions](../methods/development/conventions.md#data-modeling-conventions) |
| Code | Reviewed, versioned, and tested on synthetic data, as on [Testing](../methods/development/testing.md) |
| Built table | Tested at every build, starting with duplicates on its key |
| Production run | From an artifact built by CI, never from a notebook: see [Path to production](../methods/development/path-to-production.md) |
| One definition | A feature is computed in one engine. It is never defined in both |

The pipeline does the least it has to. It reduces what SQL cannot handle to
a table at the lowest useful grain and lands it. Roll-ups and windows are
then built in SQL from that table, so that higher grains are still rolled up
from one place.

## What the factory promises

The contract is on
[Conventions](../methods/development/conventions.md#data-modeling-conventions)
and is not repeated here. In short, a factory table has a name that means
one thing everywhere, the three time columns, a declared key, a declared
lag, and a stated rule for restatement. The tests that hold a table to that
contract are on
[Testing](../methods/development/testing.md#tests-on-tables).

The factory's tables are an interface. A removed or renamed column, a
changed key, or a changed meaning is a major version of the project that
builds them: see
[Versions](../methods/development/conventions.md#versions).

## What does not belong in the factory

- **A label.** A label looks forward from the decision time, and a feature
  looks back. See [Training data](training-data.md).
- **A column derived from one row, or a fitted transform.** These ship with
  the model, as above.
- **Anything the store could decide differently.** The factory builds
  values. Which features a model reads, and as of when, is the store's and
  the model's business.

!!! note "What the factory's documentation must carry"

    The factory is a project with its own documentation. The detail of its
    tables is kept there, not in the handbook. Each table's part of it is
    the table's
    [data contract](../methods/development/conventions.md#data-contracts).
    That documentation must say:

    - **For every table**: what one row is, its declared key, its period,
      its declared lag, whether it is rebuilt or appended, and its owner.
    - **For every table**: the sources it reads, and the engine that builds
      it.
    - **For every column**: its one definition, and its unit.
    - **For every change of definition**: the date, recorded at the
      column, and whether history was rebuilt.
    - **For every build**: which tests ran, and whether they passed.
    - **For the project**: its version, what each major version changed,
      and the rules it adds to those on Conventions.

*Add: a link to the factory's documentation in place of the note above, once
it is published, with its address kept in `facts/apps.yaml`.* Why: the
handbook holds the concept and the project holds the detail, so a reader has
to be able to get from one to the other.
