---
title: Handbook
type: general
owner: ds-lead
audience: [all]
status: draft
last_reviewed: 2026-10-24
review_cadence: 180d
sources:
  - "DPOM 0.3.0, Charles Kelley, https://doi.org/10.5281/zenodo.23814523"
---

# Data Science Handbook

The Data Science Handbook, or Handbook, provides a common knowledge base,
practical guidance, and discipline for how the Data Science Team (DS Team)
works. It clearly lays out where the team's focus lies and serves as a reference
for best practices and policies that align the team's work to business outcomes
while protecting the organization.

!!! tip "Where to start"

    **Business partners ->** See [How we work](team/how-we-work.md) to discover
    what the DS Team does and how to ask for work.

    **Technical practitioners ->** Read on for an overview of the DS Team's
    operational landscape.

## Applied data science landscape

**The DS Team practices applied data science: work that delivers measurable
business outcomes.**

The scientific method and ML/AI theory are the foundation of the team's work,
but only as far as they are applied to a target business outcome. Development
without a target outcome is pure research. Pure research can fuel discovery, but
it is not this team's focus. The team draws on research but starts and ends its
work with the outcome in mind, the Outcome Loop, and cultivates the data and
methods it needs to serve that aim.

The landscape shows how outcome focus looks in practice. Work on an outcome loop
starts by defining a target outcome, so the first question on any work request is
what business result it serves and how it will be measured. Work is not finished
at a model. It is finished when a model's decisions are recorded, acted on, and
measured, and the measurement decides what runs next.

![The DPOM landscape: Data, Prediction, Outcome, and Measure in a row, a Decision diamond between Prediction and Outcome, the Outcome Loop closing across the top with scale, fix, and retire, and Monitor and Govern and Infrastructure as bands beneath](assets/dpom-landscape-light.svg#only-light)
![The DPOM landscape: Data, Prediction, Outcome, and Measure in a row, a Decision diamond between Prediction and Outcome, the Outcome Loop closing across the top with scale, fix, and retire, and Monitor and Govern and Infrastructure as bands beneath](assets/dpom-landscape-dark.svg#only-dark)

*The landscape is [DPOM](https://doi.org/10.5281/zenodo.23814523), version 0.3.0.*

### Navigating the landscape

Enter the landscape at Outcome, not at Data on the left edge, and work back
through Data and Prediction only once the result and its measure are defined.
The Decision handoff between Prediction and Outcome is a prediction acted on by
the business. Each decision is recorded so it can be audited and replayed.
Measure closes the loop and provides feedback to help decide whether to scale,
sustain, fix, or retire the loop.

Nothing in the landscape is fixed. The business environment shifts, data
changes shape, and a model eventually makes predictions based on a world that no
longer exists. This decay causes Data, Prediction, and Outcome drift. A
deliberate effort to Monitor & Govern keeps the process aligned to the
organization's risk appetite and operating constraints.

Beneath everything is the infrastructure the landscape runs on. Its billed cost
of data, compute, and serving is the Cost arrow into Measure, so financial
efficiency is judged alongside business impact rather than after it.

### Handbook to landscape mapping

The handbook is an overlay on the landscape with each section mapping to one or
more landscape elements.

| Section | Landscape element | What it covers |
|---|---|---|
| [Business](business/index.md) | Outcome, the entry point | How the company makes money, the strategies that matter, the KPIs and what they mean |
| [Data](data/index.md) | Data | Where the data comes from, how the warehouse is organized, what each dataset holds and how far to trust it |
| [Methods](methods/index.md) | Prediction, Measure, and the Decision handoff | How the team practises applied ML, what it owes in each region, the methods it uses |
| [Technology](technology/index.md) | Infrastructure | Platforms, environments, development tools, setup, and access |
| [Oversight](oversight/index.md) | Monitor & Govern | What is watched on every model, the governance rules, the decision log, and the insights that change how data is read |
| [Team](team/index.md) | The team that runs the loop | How to work with the team, onboarding, decision records |
| [Glossary](glossary/index.md) | Reference | Business and working terms, defined once |
| [Apps](apps/index.md) | Reference | Dashboards and companion applications |
