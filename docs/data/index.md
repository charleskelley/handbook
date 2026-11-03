---
title: Data
type: general
owner: platform-owner
audience: [ds, mle, de, analyst]
status: draft
last_reviewed: 2026-10-25
review_cadence: 180d
---

# Data

Where the team's data comes from, how the warehouse is organized, and what each
dataset holds and how far it can be trusted. Business meaning of the data lives
here; the systems that store and move it live under Technology.

Page types here: **source-system** (one per system in the chain, including what
it is the system of record for), **data-domain** (one per business domain within
a system, with its model, tables, and join keys), **dataset** (a table that
outgrew its domain page, or a large table that spans domains).

## How this section is organized

A system with many tables gets a directory named for what people call it. Its
index page is the overview and the map of everything below it. Subpages are
business domains, or single large tables. A smaller system is one page here.

Tables start on their domain page. Structural, timeless behaviour goes in a
page's Quirks section. Events that change how data is read are
[insights](../insights/index.md).

## Pages

*No pages yet. Start with the system analysts pull from most, then its domain
for the core product, then the systems that feed it.*
