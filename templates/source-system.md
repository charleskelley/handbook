---
title: <Source system name>
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

## What it emits

Events or tables, with grain and keys.

## How it lands

Pipeline, cadence {{ data.source_systems['example-source'].cadence }}, latency, as of {{ data.as_of }}.

## Owner and contact

Owner: {{ data.source_systems['example-source'].owner }}.

## Known quirks

Timezones, late arrivals, soft deletes, re-statements.

