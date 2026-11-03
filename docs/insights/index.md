---
title: Insights
type: general
owner: ds-lead
audience: [all]
status: draft
last_reviewed: 2026-11-02
review_cadence: 90d
---

# Insights

Events and circumstances that change how the data should be read. An endogenous
insight comes from inside the company, such as a record system change. An
exogenous one comes from outside, such as a market shock. Structural, timeless
properties of a system are quirks and live on its data page.

Small insights live inline on the page they affect. Large ones have a page here.
This index is generated from `facts/insights.yaml`; edit that file, not this page.
Registry as of {{ insights.as_of }}.

{% for key, category in insights.categories.items() %}

## {{ category.name }}

| Insight | Kind | Start | End |
|---|---|---|---|
{% for id, item in category["items"].items() -%}
| [{{ item.title }}](../{{ item.link }}) | {{ item.kind }} | {{ item.start }} | {{ item.end or "" }} |
{% else -%}
| *none yet* | | | |
{% endfor %}
{% endfor %}
