---
title: "Customer-base audit"
type: general
owner: ds-lead
audience: [all]
status: draft
last_reviewed: 2026-11-18
review_cadence: 180d
tags: [customers, cohorts]
sources: []
---

# Customer-base audit

!!! note "Gather first"

    The transaction dataset the audit ran on and its page under Data, the
    definitions of a customer already in use in the business and where each
    is written down, the period and cohort definitions used, the date the
    data was cut, and the notebook or report the figures came from. List each
    one under `sources` in
    the front matter. Headline figures go in `facts/business.yaml` with an
    as-of date and are shown here with a macro. Where the analysis has not
    been run, leave the prompt in place rather than describing what it would
    probably show.

What the company's customers look like when revenue and profit are read by
customer: how they differ, how they change, and what the base is made of. This
page is the report. The framework behind it, and what each lens is, are on the
[customer-base audit method page](../methods/customer-base-audit.md).

## Scope

*Add: the business line and market covered, the periods covered, the period
length, how a cohort is defined, whether the measure is profit or spend, and
the date the data was cut.* Why: none of the figures below can be read, or
compared with the next audit, without these.

## Who counts as a customer

*Add: the definition of a customer used in this audit: the unit (person,
household, account, or business), the identifier that stands for it, and the
rule for merging identifiers that belong to the same customer.* Why: every
count on this page is a count of this.

*Add: the other definitions of a customer in use in the business, and how
this one differs from each.* Why: a reader will compare these figures with
customer counts they already know, and needs to be told why they differ.

*Add: the share of revenue in the period that is tied to an identified
customer, and what is known about the rest.* Why: the audit describes only
the identified part of the business.

*Add: what is excluded and how it is counted: returns, cancelled orders,
staff and internal accounts, resellers, and customers whose first purchase is
older than the data.* Why: the exclusions change every count on the page.

## How customers differ

*Add: for the latest period, the concentration of profit across customers,
the share who bought once, and what separates the top customers from the
rest: order frequency, order value, or margin (Lens 1).* Why: this is the
size of the gap between "the average customer" and the customers the business
depends on.

## What changed since the last period

*Add: the change in profit split into customers who are new to the period,
customers who did not return, and customers present in both, with the
component that moved among those who stayed (Lens 2).* Why: it says whether
the headline change came from who the customers are or from how they bought.

## How a cohort ages

*Add: for one representative cohort, how its activity and spend develop after
acquisition, the share that never buys again, and how long a second purchase
takes (Lens 3).* Why: this is the shape every retention and customer-value
question starts from.

## Whether newer cohorts are better

*Add: recent cohorts compared with earlier ones at the same age, and what
differs by acquisition season or campaign (Lens 4).* Why: it says whether the
quality of the customers being acquired is rising or falling.

## What the base is made of

*Add: each period's profit and active customers split by cohort, and the
share of the latest period that came from customers acquired in it (Lens 5).*
Why: it shows how far the business depends on acquisition to stand still.

## What this means for the team

*Add: the outcomes these findings point at, and the decisions in the
[decision inventory](decisions.md) they bear on.* Why: the audit earns its
place only by changing what the team works on.

## Open questions

*Add: what the audit could not answer and what would answer it: a missing
identifier, a cost that is not recorded, a pattern that needs a causal
design.* Why: an audit describes; the questions it raises are the work that
follows.
