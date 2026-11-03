---
title: "<Dataset name>"
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

Pulled from {{ data.datasets.example.source_system }}. System of record: {{ data.datasets.example.system_of_record }}. Pipeline, linked.

## Freshness and retention

Freshness {{ data.datasets.example.freshness }}, latency {{ data.datasets.example.latency }}, retention {{ data.datasets.example.retention }}, as of {{ data.as_of }}.

## Columns that matter

| Column | Business meaning | Watch out for |
|---|---|---|
| | | |

## Quality checks

What is tested and what is not.

## Known issues

Current defects.

## Used by

Links to KPI and method pages.

## Access

Optional. Link to the how-to.

## Quirks

Optional. Structural and timeless.

## Insights

Optional. Events that change how the data is read. Format in spec section 6.

