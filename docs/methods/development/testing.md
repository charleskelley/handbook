---
title: Testing
type: general
owner: mle-lead
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-21
review_cadence: 365d
tags: [testing, quality, ci]
---

# Testing

How the team tests code that is shared or runs in production: what a test
asserts, how much of the world it makes real, and what each kind of project
must have.

## What a test is for

A test checks that code does what its users rely on. Two other checks are
often called testing and are not on this page.

| Check | Question | Data | Where |
|---|---|---|---|
| Test | Does the code do what its users rely on? | Synthetic | This page |
| Evaluation | Is the model good enough for the decision? | Real, held out | [Framing and evaluating a prediction](../framing-and-evaluating-a-prediction.md) |
| Monitoring | Does it stay good enough? | Production | [Model monitoring](model-monitoring.md) |

## Behavior at the usage level

A test states a behavior that a user of the code relies on, and exercises it
the way a user would, through the public interface.

- **Given, when, then.** A test sets up a situation, does one thing, and
  checks the result. It is written in plain test code. There is no separate
  specification language.
- **Named for the behavior, in the domain's words.** A reader should learn
  what the code promises from the test names alone.
- **Nothing inside is asserted.** A test does not check private functions,
  the order of calls, or intermediate state, so a change that keeps the
  behavior breaks no test.
- **Only what the project does not own is replaced.** The network, the
  warehouse, and the clock may be stood in for. Everything the project owns
  runs for real, on synthetic data.

An illustration, made up for this page:

> Given an order dated after the decision time, when features are built for
> that time, then they are the same as they would be without the order.

The behavior tests are the project's interface, written so it can be run.
[Conventions](conventions.md#versions) names the interface of each kind of
project for versioning. A change that forces a behavior test to change is the
sign of a major version.

### Coverage

There is no target for lines covered. The rule is that **every public
behavior has a test, and every fixed bug has a test that failed before the
fix.**

## Writing the test first

Writing the test before the code works where the expected result is known
before the code exists: a feature function, library and infrastructure code,
and a bug fix, which starts with the test that reproduces the bug.

It does not fit modeling, where the result is discovered. There the tests
are written when the work is shaped for production, not before.

## Three sizes

Behavior says what a test asserts. Size says how much of the world is real.
The two are separate: a test at the usage level can be any size.

| Size | What is real | Data | Runs |
|---|---|---|---|
| Unit | Nothing outside the process: one behavior, in memory | Synthetic rows written in the test | Every commit, anywhere, including a laptop |
| Integration | A boundary the project owns: a real engine, a file store, the training recipe run small from fit to score | Synthetic | Every commit, in CI |
| End-to-end | The released artifact, through its real entry point, in a real environment | Governed data | At release |

- **A unit is a unit of behavior, not a function.** One behavior may pass
  through several functions, and they are tested together.
- **Use the smallest size that can show the behavior.** End-to-end tests are
  few, because they are slow and a failure says little about where.
- **The reproduction gate is a model's end-to-end test.** See
  [Experiment tracking](experiment-tracking.md).
- **At release, the tests run again against the published artifact**,
  installed in a clean environment. See
  [Path to production](path-to-production.md).

## Tests on tables

A project that builds tables has two kinds of test. A transformation's logic
is tested on fixed input rows, which is a unit test. A built table is tested by
assertions that run on the real table at every build.

**Every table the team builds for others to read declares a primary or
natural key, and has a test for duplicates on that key.** This applies to the
feature factory and to any other shared table alike, whatever engine builds
it. A columnar warehouse does not enforce a
primary or unique key the way a transactional database does, so a declared
key is only a claim until a test checks it.

Tables in the feature factory are also tested for what
[Conventions](conventions.md#data-modeling-conventions) promises of them:

- A roll-up agrees with the lowest grain it was rolled up from.
- The observed lag is within the lag the table declares.

## Testing a model

A model has no single right answer, so a test cannot compare its output with
an expected value. Four kinds of expectation take the place of examples.

| Expectation | What it checks |
|---|---|
| Invariant | What must hold for any input: the range of a score, one row per entity, the same output for the same seed |
| Direction | Changing an input in a known direction does not move the score the wrong way |
| Planted signal | On synthetic data where the outcome depends on one feature, the training recipe finds it |
| Point in time | Changing rows dated after the decision time leaves the features unchanged |

All four run on synthetic data, against the training recipe and the scoring
code. They test the recipe, not a trained model. Whether a trained model is
good enough is evaluation, and whether production training matches research
is the reproduction gate.

Anything random takes a fixed seed, and a numeric result is compared within a
stated tolerance. A test that fails now and then is fixed or removed, never
retried until it passes.

## What each kind of project must have

| Project | Tests required | A merge is blocked when they fail |
|---|---|---|
| Shared library, application infrastructure | Every public behavior, and every fixed bug | Yes |
| Feature factory | The duplicate test on every table, the convention tests, and the logic of each transformation | Yes |
| Any other table the team shares | The duplicate test on the table | Yes |
| Model in production | The training recipe run small from fit to score, invariants, the point-in-time test, and direction and planted signal where they apply | Yes |
| Model before production | None | No. The production contract is the control: see [Conventions](conventions.md#branches-and-review) |
| Notebooks and personal projects | None | No |

## Synthetic data

Test data is made by the project. It is small, written in the test or built
by a helper the project keeps, and it is never sampled from real data: see
[Development environments](environments.md).

It includes the awkward cases on purpose: an entity with little history, an
empty group, a duplicate key, and a row at the last moment of a day.
