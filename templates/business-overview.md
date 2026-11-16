---
title: Business
type: business-overview
owner: ds-lead
audience: [all]
status: draft
last_reviewed: YYYY-MM-DD
review_cadence: 180d
tags: []
sources: []
---

# Business

!!! note "Gather first"

    The annual report or regulatory filing (the Business and Risk Factors
    sections), the latest investor or all-hands deck, the product or price
    list, and the organization chart. List each one under `sources` in the
    front matter. Where these are silent, write `*[unverified: needs source]*`
    rather than a plausible value.

*Add: one sentence on what this page is for: the company as a new team member
needs to understand it before reading anything else here.* Why: this is the
entry point of the landscape; every outcome the team works on starts from
something on this page.

## What the company does

*Add: one paragraph a new hire can repeat correctly after one reading: what
the company sells, to whom, and what it is paid for.* Why: the test of the
section is that it survives being repeated to a customer.

## Products and segments

*Add: the products and services, grouped the way finance reports them, with
one line each on what it is and who buys it. Render segment names and revenue
share from `facts/business.yaml`, never typed here.* Why: the segments are the
units the business is judged on, and the KPI tree is built per segment.

## How money is made

*Add: per segment, who pays, for what, when, and on what pricing basis
(subscription, transaction, spread, licence, usage). Note what is paid up
front and what is paid over time.* Why: the revenue mechanism decides which
decisions have a measurable outcome and over what horizon.

## Customers and markets

*Add: who the customers are, how the business segments them, which
geographies and channels matter, and what concentration exists.* Why: the
customer segmentation here is the one the data should carry; mismatches
between the two are a recurring source of misread numbers.

## Operations

*Add: how the product is delivered, and the handful of operational processes
whose performance the business watches. Name the process owners by role.* Why:
the processes are where decisions are made and where drift shows up first.

## Regulation and risk

*Add: the regulators and rules that bind the business, and the risk factors
from the filing that touch data, models, or automated decisions. Link to the
team's governance and model-monitoring pages.* Why: this is the Govern half
of the landscape as the business sees it, and it sets the constraints every
model must respect.

## Seasonality and cycles

*Add: the calendar effects everyone must know before reading a chart: fiscal
year, peak periods, billing cycles, regulatory dates, and anything that makes
one month not comparable to another.* Why: a reader who does not know these
will report seasonality as a finding.

## Organization

*Add: how the business is organized (by product, region, function), who the
senior owners are by role, and where the data science team sits and reports.*
Why: the reporting line decides which outcomes the team is asked about and
who can act on a measured result.

## What this means for the team

*Add: the two or three outcomes the business is judged on, stated in the
business's own words, and where on this page each one comes from. Link each
to its root in the KPI driver tree.* Why: the loop is entered at Outcome, and
this section is where the team names the outcomes it enters at.
