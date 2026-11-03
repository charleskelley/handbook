---
title: "<Source system name>"
type: source-system
owner: role-or-person
audience: [ds, mle, de]
status: draft
last_reviewed: YYYY-MM-DD
review_cadence: 180d
tags: []
sources: []
---

# <Source system name>

## What it is

The business process this system runs.

## System of record for

The kinds of data this system is authoritative for, and where analysts actually
pull each one if elsewhere.

## What it emits

Events or tables, with grain and keys.

## How it lands

Pipeline, cadence {{ data.source_systems['example-source'].cadence }}, latency, as of {{ data.as_of }}.

## Owner and contact

Owner: {{ data.source_systems['example-source'].owner }}.

## What's here

Keep this section only on a system directory's `index.md`. The map of domains,
single tables, and carveouts.

- [Domain](domain.md): one line on what it covers.

## Quirks

Optional. Structural and timeless: timezones, late arrivals, soft deletes,
re-statements, fields that default to one value.

## Insights

Optional. Events that change how the data is read. Format in spec section 6.

