---
title: Glossary
type: general
owner: analytics-lead
audience: [all]
status: draft
last_reviewed: 2026-10-24
review_cadence: 180d
---

# Glossary

Terms the team and its partners use, defined once. Alphabetical. Where a page
explains the term in depth, the definition links to it.

Artifact
:   A versioned, immutable build output stored in Artifactory: a package, a
    container image, or a model version. Production runs only artifacts built
    by CI. See [Path to production](../methods/development/path-to-production.md).

Champion, challenger
:   Aliases in the model registry. The champion is the version production
    scores with; a challenger is a registered version waiting for a person to
    promote it. See [Path to production](../methods/development/path-to-production.md).

Counterfactual
:   What would have happened without the decision or treatment. The comparison
    every measured outcome needs.

Data contract
:   A file, kept beside the code that builds a data object, that says what
    the object is, what each column means, and what a reader can rely on.
    Written by whoever builds the data, and checked against the object. See
    [Conventions](../methods/development/conventions.md#data-contracts).

Decision log
:   The record of each decision a model's prediction was turned into: the
    entity, the score, the policy and its version, the action, and when. The
    handoff between Prediction and Outcome, and the thing Measure attributes
    against. Not a decision record. See
    [Methods](../methods/index.md#the-decision-handoff).

Decision record
:   A short, numbered, append-only document recording a team decision and its
    reasoning. Not a decision log. See
    [Decision records](../team/decisions/index.md).

Drift
:   A change in the distribution of a model's inputs or scores relative to the
    data it was trained on. A signal that the world moved, not that the model
    is wrong. See [Model monitoring](../methods/development/model-monitoring.md).

Fixture
:   A research run's holdout rows with the scores its model gave them, saved in
    the governed bucket under the run id. Production training scores the same
    rows and must agree. See
    [Experiment tracking](../methods/development/experiment-tracking.md).

Insight
:   An endogenous or exogenous event or circumstance that changes how data is
    interpreted. Interpretation differs before and after its date. See
    [Insights](../oversight/insights/index.md).

Outcome loop
:   The path across Data, Prediction, Outcome, and Measure: a decision the
    business agreed to make, a prediction turned into a decision by a policy,
    the decision recorded, the outcome attributed against a counterfactual,
    and the result deciding what runs next: scale, sustain, fix, or retire. See
    [Methods](../methods/index.md).

Policy
:   The written rule that turns a score into an action, with a version and an
    owner. See [Methods](../methods/index.md#the-decision-handoff).

KPI
:   Key performance indicator. A business metric with a definition, a formula,
    an owner, and a source of truth. One page per KPI under Business.

Prediction log
:   The BigQuery table every batch prediction is appended to, with its features,
    score, model version, and time. The source for drift, performance, and
    reports. See [Model monitoring](../methods/development/model-monitoring.md).

Promotion
:   Copying a tested artifact, byte for byte, from a dev repository to a
    release repository. See [Artifactory](../technology/artifactory.md).

Quirk
:   A structural, timeless property of a system or table that affects how its
    data is used, such as a field that defaults to one value.

Reference run
:   The research run, named by id in a model's config, that production
    training must reproduce before the model can be registered. Written only by
    the project's reference command. See
    [Experiment tracking](../methods/development/experiment-tracking.md).

Repository: local, remote, virtual
:   In Artifactory, a local repository holds what we publish, a remote caches a
    public source, and a virtual combines several behind one address. See
    [Artifactory](../technology/artifactory.md).

Run (experiment)
:   One fit on one data snapshot, recorded in the experiment tracker with its
    params, metrics, dataset, and the commit it ran from.

Source of truth
:   The one report, table, or system whose value for a fact is canonical when
    sources disagree. A system of record says which system is authoritative for
    a kind of data. A source of truth says which value to use.

Source system
:   Any system in the chain that data comes from, whether it first records the
    data or holds a copy that analysts pull from.

System of record
:   The system that is authoritative for a kind of data, which may differ from
    the one analysts pull it from. A relationship, not a kind of system.
