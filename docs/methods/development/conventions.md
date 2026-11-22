---
title: Conventions
type: general
owner: mle-lead
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-02
review_cadence: 365d
tags: [conventions, repositories, data-modeling, features]
---

# Conventions

The contracts the team's projects and tables keep, so that a person or a
pipeline can rely on them without asking. There are three parts: how a
repository is run, how a table is named and shaped, and how a data object is
documented for the people who read it. How code is written is on
[Style guides](style-guide.md). The [Data](../../data/index.md) pages
link here.

This page holds the rules that every project and every table share. A rule
that applies to one project, such as the feature factory, is in that
project's own documentation.

## Repository conventions

### Where a project lives

A project starts in a personal space, where its owner works however the work
needs. Standalone scripts, with or without their own declared dependencies,
are fine there, as notebooks are. It moves to the team group **when a
repeated deliverable comes out of it**, whether the deliverable is internal
to the team or goes to a business partner.

The conventions below apply from that move. Before it, only the rules that
cannot be put right afterwards apply: how data is handled, and that no
machine holds the only copy of the work. Both are on
[Development environments](environments.md).

### What a team project contains

- A Python project is a package: its logic is importable and tested.
  Runnable scripts are thin entry points that call the package.
- A lockfile, so that every machine and CI resolve the same environment.
- A committed example of its settings, with no secrets in it.
- Tests that run on synthetic data.
- A statement of the decision or deliverable it serves, and who owns it.
- A [data contract](#data-contracts) for every data object it produces for
  others to read.

### Branches and review

Development is trunk-based: short branches off the main branch, merged
often.

| What | Rule |
|---|---|
| Applies to | Major infrastructure, shared libraries, the feature factory, the feature store, and models in production |
| A merge needs | The checks to pass, and one reviewer |
| A merge also needs the owner or the data science lead | When it changes a table that other projects read, or breaks a library's interface |

A model that has not reached production is not held to this. How its project
is branched and organised is the data scientist's choice. The control is the
production contract: to ship, the work has to fit the package, pass the
checks, and reproduce its research run. See
[Path to production](path-to-production.md) and
[Experiment tracking](experiment-tracking.md).

### Versions

Every project uses semantic versioning. A major version means the project's
interface broke, so each kind of project states what its interface is.

| Kind of project | Its interface | A major version is |
|---|---|---|
| Shared library | Its public functions | A change that breaks a caller |
| Data project, such as the feature factory | The tables its consumers read | A removed or renamed column, a changed key, or a changed meaning |
| Model project | The output its consumers read | A change a consumer has to act on |

A trained model's version is the model registry's, not the project's. Each
trained model records the project version that trained it.

## Data modeling conventions

These apply to every table the team builds for others to read, whatever
builds it: SQL run in the warehouse, or a pipeline on a distributed
processing engine. A project may add rules of its own in its own
documentation. It may not relax these.

### Names

- **A name means one thing everywhere.** A dimension or a measure has the
  exact same name in every table it appears in, and one definition, kept in
  the documentation of the project that builds it.
- **A measure is named `<measure>_<unit>_<window or aggregation>`.** The last
  part is optional. For example, `order_total_usd`, and `order_total_usd_90d`
  for the same measure over a trailing window. These two names are
  illustrations, not columns that exist.
- **A window trails and ends at the row's `data_as_of_utc`.**
- **A dimension that plays two roles** in one table, such as a billing and a
  shipping country, is the one exception to the first rule: each takes its
  role as a prefix.

*Add: the allowed unit suffixes, the allowed window and aggregation suffixes,
and their order when a name carries both. Why: without fixed lists the
pattern drifts into several spellings of one thing.*

*Add: when a measure is zero and when it is null, including for an entity
with less history than the window. Why: a model reads the two differently.*

### Time columns

Every table carries the same time columns, in UTC.

`data_as_of_utc`

:   The data's effective time: the moment the row's values describe.
    Date-level data carries its date with the last moment of that day, so a
    row for a day is never read by a decision made earlier the same day.
    That last moment is defined once, in code, and never typed by hand.

`modified_as_of_utc`

:   When the row was written, and so when the feature was available.

`source_modified_as_of_utc`

:   When the source last changed the record. Carried only where the gap
    between the source and the feature pipeline is large.

A decision's own time, on a prediction table or a label table, takes a
descriptive name ending in `_as_of_utc` or `_at_utc`. A label table also
carries when the outcome became known.

*Add: which day a date-level row describes when the source closes its day in
local time. Why: a local business day does not end at the last moment of the
UTC date.*

### Entity tables

The top-level tables are one full table of an entity and its dimensions at
each entity grain. The primary key is always the entity id and
`data_as_of_utc`, usually with one row per day, week, or month.

Every entity table declares:

| Declared | Values |
|---|---|
| Key | The entity id and `data_as_of_utc` |
| Rows | Periodic, and the period |
| Lag | How long after `data_as_of_utc` a row is usable |
| Load | Rebuilt or appended |
| Owner | Who decides that a restatement is major |

### Measures and roll-ups

A measure that can be aggregated starts in the table at the lowest grain,
which carries the id of every higher entity grain. Every higher grain is
rolled up from that table and from nowhere else, which is what guarantees
that two grains agree.

Rolling up is only safe for a measure that adds:

- **A ratio** is carried as its numerator and its denominator, and divided
  after the roll-up.
- **A distinct count** is computed from the lowest grain each time, never
  from another roll-up.
- **A balance** adds across entities at one moment, and never across time.

### Reading a table at a point in time

A decision made at a given time reads, for each entity, the latest row whose
`data_as_of_utc` plus the table's declared lag is at or before that time.
The lag is checked against what is observed: the gap between
`modified_as_of_utc` and `data_as_of_utc` when a row is first loaded.

A declared lag is the rule until a model is served in real time.

### Restatement and backfill

| Table | Default |
|---|---|
| Small enough that a rebuild is cheap | Rebuilt: history is overwritten with the best current knowledge |
| Extremely large | Appended: new periods are added and history is left alone |

- **A major restatement gets a backfill.** The table's owner decides what is
  major. The test is whether a model that reads the table would see a changed
  value.
- **On an appended table, a backfill replaces one column**, not the table. It
  is done when an upstream restatement matters enough, or when a critical
  feature is redefined.
- **A change of meaning rebuilds history or takes a new name.** If history
  cannot be recomputed, the new definition gets a new name beside the old
  one.
- **A column backfill is recorded at the column**: the changed definition and
  its date go in the column's documentation and in the version of the feature
  store's contract. `modified_as_of_utc` is per row and cannot show it.
- **An appended table records its seams.** Where a definition changed and
  history was not rebuilt, the date is recorded at the column, in the
  table's own documentation. It is also recorded as an
  [insight](../../oversight/insights/index.md) only when it changes how a
  number is read beyond that table.

Which code version produced which features is settled by the project's
version and the feature store's contract, not by renaming. The training set
for a full production training run is saved to cold storage where possible,
and is governed data like the tables it came from.

### Beyond periodic batch

The wide periodic table is the default while features are built in batch.
When a group of attributes changes faster than the period, or comes from a
source with its own cadence or lag, it moves to a narrow table of its own
with a row written only when something changes. The key and the read rule
stay the same. Such a table also declares how old a row may be and still be
used, because a missing row means "unchanged" there and "missing" in a
periodic table.

Nothing is built this way until a decision needs it. See
[DR-0004](../../team/decisions/DR-0004-serve-from-batch.md).

## Data contracts

Whoever creates data that others use is responsible for its contract. A data
contract is a file that says what a data object is, what each column means,
and what a reader can rely on. It is the object's documentation, and it is
checked against the object, so it cannot drift the way a page can.

### Which objects have one

Every data object that is read outside the project that builds it: a table
in the feature factory, a label table, a saved training set, and a model's
prediction table. An object that only its own project reads does not need
one.

### Where it lives and how it is written

- **In the repository that builds the object**, beside the code, and changed
  in the same merge as the code.
- **In the [{{ platform.contracts.standard_name }}]({{ platform.contracts.standard_url }})**,
  version {{ platform.contracts.standard_version }}. The format is the
  standard's, and the standard's own documentation says how each part is
  written.
- **By the person who builds the object.** Writing the contract is part of
  building the data, not a task for afterwards or for someone else.

### What a contract states

| Stated | What it is |
|---|---|
| What the object is | A description, and what one row is |
| Every column | Its description, its type, and whether it can be empty |
| The key | The columns that identify a row |
| Where a column comes from | The objects it was built from, and the transformation in plain words |
| Quality rules | What must hold of the data for it to be used |
| Service levels | How often it is updated, how late a row can be, and how long it is kept |
| Sensitive columns | The classification of each |
| The owner | Who answers for the object, and how to reach them |

What [Data modeling conventions](#data-modeling-conventions) asks a table to
declare, such as its key, its period, and its lag, is declared in its
contract.

### How it is checked

The checks are run by
[{{ platform.contracts.tool_name }}]({{ platform.contracts.tool_url }}).

| When | Check |
|---|---|
| Every commit | The contract is valid against the standard |
| Every merge | The contract is compared with the last released one, and a change that breaks a reader is reported |
| Every build, and before a release | The built object is tested against its contract: its columns, its types, its key, and its quality rules |

- **A change that breaks a contract is a major version** of the project
  that builds the object: see [Versions](#versions).
- **Nothing goes to production without one.** A data object that others
  read has a contract that passes its test before the project that builds
  it is released: see [Path to production](path-to-production.md).

### Where it is read

A project's contracts are built into a catalog, generated from the files by
the same tool. Other tools read the same files, so a description is written
once and not copied into each place that needs it.
