---
title: Apps
type: general
owner: analytics-lead
audience: [all]
status: draft
last_reviewed: 2026-10-24
review_cadence: 90d
---

# Apps

Companion applications: dashboards, Streamlit and Dash apps, and internal
tools. This table is generated from `facts/apps.yaml`; edit that file, not
this page. Registry as of {{ apps.as_of }}.

| App | Kind | Purpose | Owner | Status |
|---|---|---|---|---|
{% for key, app in apps["items"].items() -%}
| [{{ app.name }}]({{ app.url }}) | {{ app.kind }} | {{ app.purpose }} | {{ app.owner }} | {{ app.status }} |
{% endfor %}
