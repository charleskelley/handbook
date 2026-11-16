---
title: Oversight
type: general
owner: ds-lead
audience: [all]
status: draft
last_reviewed: 2026-11-15
review_cadence: 180d
---

# Oversight

The Monitor & Govern band of the landscape: what is watched on every model in
production and who acts when it moves, the rules a model must satisfy before
and after it goes live, the record of the decisions models drive so they can
be audited and replayed, and the insights that change how the data should be
read. Oversight in the sense of supervision: the part of the team's work that
keeps a running loop honest.

Oversight says what must be true and who answers for it. How the team makes
it true is engineering and lives in [Methods](../methods/index.md); the
tools it runs on live in [Technology](../technology/index.md). A page here
that starts describing a tool is on the wrong side of that line.

## How the parts relate

Monitoring watches the regions for drift and feeds the operational cost into
Measure. Governance sets the limits monitoring is held to and decides who may
change a running model. The decision log is where the Decision handoff lands
in this band: every recorded decision is auditable and replayable from it.
Insights are what monitoring and the business learn that changes how a number
should be read, written down once with a date.

## Pages

- [Monitoring](monitoring.md): what must be watched on every model, the
  thresholds, who acts, and the register of what is watched today.
- [Governance](governance.md): approvals, model risk, access and privacy, and
  the business's risk appetite applied to models.
- [Decision log](decision-log.md): the contract for recording the decisions
  models drive.
- [Insights](insights/index.md): the index of every insight, generated from
  `facts/insights.yaml`, and the freestanding writeups.
