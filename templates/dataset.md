---
title: <Dataset name>
type: dataset
owner: role-or-person
audience: [ds, mle, de, analyst]
status: draft
last_reviewed: YYYY-MM-DD
review_cadence: 90d
tags: []
sources: []
---

# <Dataset name>

## What it holds

One paragraph. Grain: {{ data.datasets.example.grain }}. Primary key: {{ data.datasets.example.primary_key | join(', ') }}.
Location: `{{ data.datasets.example.location }}`.

## Where it comes from

Source system and pipeline, linked.

## Freshness and retention

Freshness {{ data.datasets.example.freshness }}, latency {{ data.datasets.example.latency }}, retention {{ data.datasets.example.retention }}, as of {{ data.as_of }}.

## Columns that matter

| Column | Business meaning | Watch out for |
|---|---|---|
| | | |

## Quality checks

What is tested and what is not.

## Known issues

## Used by

Links to KPI, feature, and model pages.

## Access

