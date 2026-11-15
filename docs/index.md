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
business outcomes**

The scientific method and ML/AI theory are the foundation of the team's work,
but only as far as they are applied to a target business outcome. Development
without a target outcome is pure research. Pure research can fuel discovery, but
it is not this team's focus. The team draws on research but starts and ends its
work with the outcome in mind, the Outcome Loop in the landscape below, and
keeps the data and methods it needs to serve that aim.

The landscape is how outcome focus works in practice. Work on an outcome loop
starts by defining a target outcome, so the first question on any request is
what business result it serves and how it will be measured. Work is not
finished at a model. It is finished when a model's decisions are recorded,
acted on, and measured. Measurement helps decide whether to scale, fix, or
retire a loop. The handbook is an overlay on the landscape, so the section a
page sits in tells you which part it serves.

![The DPOM landscape: Data, Prediction, Outcome, and Measure in a row, a Decision diamond between Prediction and Outcome, the Outcome Loop closing across the top with scale, fix, and retire, and Monitor and Govern and Infrastructure as bands beneath](assets/dpom-landscape-light.svg#only-light)
![The DPOM landscape: Data, Prediction, Outcome, and Measure in a row, a Decision diamond between Prediction and Outcome, the Outcome Loop closing across the top with scale, fix, and retire, and Monitor and Govern and Infrastructure as bands beneath](assets/dpom-landscape-dark.svg#only-dark)

*The landscape is [DPOM](https://doi.org/10.5281/zenodo.23814523), version 0.3.0.*

Enter the landscape at Outcome, not at Data on the left edge. Every outcome loop
begins by defining a business result and a way to measure it, and only then
works back through Data and Prediction. The Decision between Prediction and
Outcome is the handoff to the business. Each decision is recorded so it can be
audited and replayed. Measure closes the loop and provides feedback to help
decide whether to scale, sustain, fix, or retire the loop.

The Drift arrows mean every region decays and has to be watched, which is what
Monitor & Govern is for, along with keeping the organization's risk appetite and
operating constraints in view. The Cost arrow means Infrastructure's billed cost
of data, compute, and serving is the other side of Measure, so financial
efficiency is judged alongside impact.

- [Business](business/index.md), the Outcome region: how the company and its
  products make money, the strategies that matter, the KPIs and what they
  mean. The thing to understand first, because the loop is entered here.
- [Data](data/index.md), the Data region: the inputs, and how the business is
  represented in them. Where the data comes from, how the warehouse is
  organized, what each dataset holds and how far to trust it.
- [Methods](methods/index.md), the Prediction and Measure regions and the
  decision handoff between them: how we practise applied ML, what we owe in
  each part of the landscape, the methods we use, and our development
  practices.
- [Technology](technology/index.md), the Infrastructure band: what we work
  with. Platforms, environments, development tools, setup, and access.
- [Team](team/index.md), the Govern half of Monitor & Govern: how to work with
  us, onboarding, and decision records.
- [Insights](insights/index.md), the Monitor half: the events and
  circumstances that change how the data should be read.
- [Glossary](glossary/index.md): business and working terms and acronyms,
  defined once.
- [Apps](apps/index.md): links to the dashboards and companion applications
  that matter.

## How this handbook is maintained

Every page has an owner and a review date in its front matter. Facts that
change live in one place and are rendered into pages, so a number appears once.
The rules are in the repository's `HANDBOOK-SPEC.md`.
