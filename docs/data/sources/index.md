---
title: Sources
type: general
owner: platform-owner
audience: [ds, mle, de, analyst]
status: draft
last_reviewed: 2026-11-22
review_cadence: 180d
tags: [sources, data]
---

# Sources

The raw material. A source is any system in the chain that data comes from:
the systems that run the business, and the warehouse or data lake where
their records land. This page says what the team needs to know about a
source before building on it, and how to read from one.

The team reads sources and mostly does not own them. See
[where the team's promises start](../index.md#where-the-teams-promises-start).

## What a source is

Two relationships describe every source, and they are often held by
different systems.

System of record

:   The system that is authoritative for a kind of data. When two systems
    disagree, this one is right.

Where it is read

:   The copy the factory and analysts actually pull from. This is usually
    the warehouse or the data lake, not the system that first wrote the
    record.

The copy is a source too, with a page of its own. Both terms are in the
[glossary](../../reference/glossary.md).

A source is shaped for running the business, not for analysis. It holds what
the business needs now, in the structure its application needs. It will
overwrite a value where an analyst would want the history, and it changes
when the business's needs change.

## What to know before building on a source

| Question | Why it matters downstream |
|---|---|
| What business process writes it? | The meaning of a column is what the process meant by it |
| What is it the system of record for? | It says which system wins when two disagree |
| What is one row, and what is its key? | A key is a claim until a test checks it |
| When does a record arrive, and how late can one be? | It sets the lag a factory table declares |
| Does it keep history? | It decides whether a feature can be rebuilt for a past date |
| Can a record change after it is written? | Corrections, restatements, and deletes decide whether a rebuild gives the same answer twice |
| In what time zone does its day close? | It decides which day a date-level row describes |
| Who owns it, and how is a change announced? | A source's change arrives as someone else's release |

A source page answers each of these. Where the answer is not known, the page
says so.

## Whether a source keeps history

How a source records time decides more about what can be built on it than
anything else on its page.

| The source keeps | A feature can be rebuilt for a past date |
|---|---|
| Events, appended and never changed | Yes, for as far back as the events go |
| State, with the period each value was valid | Yes, if the validity periods can be trusted |
| Current state only | No |

A source that keeps only current state has no past. Its history begins on
the day someone starts keeping snapshots of it, and a feature built on it is
correct at a point in time only from that day. The snapshot has to start
before the first model needs it, because it cannot be made afterwards.

## How to read from a source

- **Land it as it is.** The copy the factory reads is the source's own
  records, unchanged. Cleaning, renaming, and reshaping happen in the
  [factory](../factory.md), where they are versioned and tested.
- **Say which copy is read, and what it is a copy of.** A page that names
  only the warehouse table hides the system that decides what the data
  means.
- **Keep when a record arrived apart from when it happened.** The time a row
  describes and the time it landed are different columns. The gap between
  them is the lag that the factory's tables declare: see
  [time columns](../../methods/development/conventions.md#time-columns).
- **Snapshot a source that keeps only current state**, on a schedule and
  from the earliest day possible.
- **Check what the factory relies on at the point of entry**: the key, the
  arrival time, and the volume. A source that breaks one of them should stop
  the build, not flow through it.
- **Know the owner before depending on the source.** Agree how a change to
  its structure or its meaning will be announced, and write the contact on
  the source's page.

## Quirks and insights

A source's behavior is recorded in one of two places.

- **A quirk** is structural and timeless: a time zone, a field that defaults
  to one value, a record that is marked deleted and kept. It goes in the
  Quirks section of the source's page.
- **An insight** is an event with a date that changes how the data is read
  before and after it: a migration, a changed definition, an outage. It is
  recorded as an [insight](../../oversight/insights/index.md).

## Pages

Each system gets a page of type `source-system`. A system with many tables
gets a directory here, named for what people call it. Its index page is the
overview and the map of everything below it, and its subpages are business
domains or single large tables. A smaller system is one page.

*No pages yet. Start with the system the factory reads from most, then the
systems that feed it.*
