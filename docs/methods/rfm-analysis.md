---
title: "RFM analysis"
type: method
depth: build
owner: ds-lead
audience: [ds, analyst, product]
status: draft
last_reviewed: 2026-11-19
review_cadence: 180d
tags: [descriptive, customers, segmentation]
sources:
  - "Fader, Hardie, and Lee, RFM and CLV: Using Iso-Value Curves for Customer Base Analysis, Journal of Marketing Research 42(4), 2005"
  - "Hughes, Strategic Database Marketing, McGraw-Hill"
---

# RFM analysis

A summary of each customer's buying history in three numbers: how recently
they bought, how often, and how much. Customers are scored on each and grouped
by the scores. RFM stands for recency, frequency, and monetary value.

## What it is

A descriptive analysis that reduces a customer's whole transaction history, as
of one date, to three measures, and then sorts customers into groups by them.
It comes from direct marketing, where it was used to choose who to mail: the
customers who bought most recently, most often, and for the most money were
the most likely to respond to the next offer. It fits no model. The scores
are ranks or bands, and the output is a table of groups with a count and a
value for each. It is quick to build, easy to explain to a business partner,
and a baseline any model of response, churn, or customer value has to beat.

## When it is the right choice

- As a first segmentation of customers where there are repeat purchases and
  no contract.
- To choose who to contact when there is no response model yet, or as the
  baseline a response model has to beat.
- To describe how the customer base is distributed between active, lapsing,
  and lost, and to track that over time with fixed bands.
- As a summary a business partner can read without knowing how a model works.

## When it is not

- **Deciding who an action will change.** The customers with the best scores
  are the most likely to buy next, with or without the action. Choosing them
  finds the customers who would have bought anyway. The effect of contacting
  a group is a causal question and needs a comparison group that was not
  contacted.
- **Contractual businesses.** Where customers subscribe, cancellation is
  observed and purchases come on a schedule, so recency and frequency say
  little. Use tenure and survival.
- **Purchases that are rare by nature.** Where most customers buy once in
  several years, frequency has almost no spread and recency is mostly a
  measure of when the customer was acquired.
- **A forecast of value.** The scores rank customers. They do not say how
  much a customer will spend. That is a modelling task.
- **Strong seasonality read at one date.** A customer who buys every December
  looks lapsed in November. Use a window and an as-of date that cover the
  cycle.
- **New customers.** They have a recency and little else. Report them as
  their own group.

## The three measures

All three are computed for each customer over an observation window, as of a
single date. The window and the date are stated on every output.

| Measure | What it is | The choices to make |
|---|---|---|
| Recency | Time since the customer's most recent purchase, at the as-of date | The unit: days, weeks, or periods |
| Frequency | Number of purchases in the window | Whether orders on the same day count once; whether the first purchase counts |
| Monetary value | What the customer spent in the window | Total or average per order; spend or profit; how returns are counted |

Four things are settled before any score is cut:

- **The customer.** RFM depends on a customer identifier as much as any
  customer analysis does. A customer split across two identifiers is two
  customers with low frequency. The questions to settle are on the
  [customer-base audit](customer-base-audit.md#defining-the-customer) page.
- **The window.** All of history, or a trailing window such as the last two
  years. With a trailing window, a customer with no purchase in it is not in
  the analysis, so the window decides who can be called lapsed.
- **Monetary value as total or as average.** Total spend rises with
  frequency by construction, so the two scores largely repeat each other.
  Average spend per order is closer to a third, separate piece of
  information. Say which is used.
- **The customer's age.** A customer acquired last month cannot have a high
  frequency. Either carry time since first purchase beside the three
  measures, or run the analysis within a cohort.

### Table contract

The analysis is one table, built from the order summary described on the
[customer-base audit](customer-base-audit.md#table-contracts) page: one row
per order, with the customer, the date, the spend, and the profit.

RFM table

:   One row per customer with at least one order in the window. Columns:
    customer identifier, as-of date, start of the window, date of the first
    order, date of the last order, recency, frequency, monetary value, the
    three scores, and the cell. Only orders dated from the start of the
    window to the as-of date are used. The date of the first order is the
    exception: it is the customer's earliest order in all of history, so that
    a long-standing customer is not taken for a new one.

| Column | Definition |
|---|---|
| Recency | As-of date less the date of the last order in the window |
| Frequency | Number of orders in the window |
| Monetary value, as total | Spend summed over the orders in the window |
| Monetary value, as average | Total spend ÷ frequency |
| Time since first purchase | As-of date less the date of the first order |
| Cell | The recency, frequency, and monetary scores, in that order |

## Scoring

Each measure is turned into a score, by convention from 1 to 5 with 5 the
best: the most recent, the most frequent, the highest value. Recency is
therefore scored in reverse, the shortest time since purchase scoring 5. The
three scores together name a cell, written as three digits, so 545 is a
customer in the top fifth on recency and value and the next fifth down on
frequency. Five scores on three measures give 125 cells.

There are two ways to cut the scores, and they do not give the same answer.

- **Quantiles.** Rank customers on a measure and cut them into five groups of
  equal size. A score is then a rank against the other customers in that run.
  A customer's score can change from one run to the next with no change in
  their behaviour, because the others moved.
- **Fixed bands.** Set the cut points by hand, for example one purchase, two,
  three to five, and so on. A score then means the same thing in every run,
  which is what tracking over time needs. The bands need a reason and a
  review when the business changes.

Frequency usually forces the choice. Where most customers have bought once,
the lowest three or four quintiles of frequency would all hold the same
value, and the cuts fall arbitrarily among identical customers. Use fixed
bands for frequency in that case.

With quantiles there is a second choice. Scored independently, each measure
is ranked across all customers, and because the measures are related the
cells are of very unequal size, some of them empty. Scored in sequence,
customers are cut by recency, then by frequency within each recency group,
then by value within each of those, which gives cells of equal size but makes
a frequency score mean something different in each recency group.

The three digits are a label, not a number. Adding them, or weighting and
adding them, gives one score that is easy to rank by and hides which measure
produced it. Keep the cells, and group cells that will be treated alike.

## Reading the grid

Recency and frequency carry most of the picture, so the usual first view is
the two of them as a grid, with the number of customers and the value in each
cell.

![A five-by-five grid of recency score against frequency score, with the four corners named. Top right, recent and frequent. Bottom right, recent with few orders. Top left, frequent but not recent. Bottom left, few orders and not recent.](../assets/rfm-grid-light.svg#only-light)
![A five-by-five grid of recency score against frequency score, with the four corners named. Top right, recent and frequent. Bottom right, recent with few orders. Top left, frequent but not recent. Bottom left, few orders and not recent.](../assets/rfm-grid-dark.svg#only-dark)

*Recency score across, frequency score up. Monetary value is read within each
cell.*

| Corner | Who is usually in it | What to ask |
|---|---|---|
| Recent and frequent | The established, active customers | How much of total value sits here, and how few customers it is |
| Recent, few orders | New customers and occasional buyers | Which of the two; split by time since first purchase |
| Frequent, not recent | Customers who used to buy regularly and have stopped | Whether they have lapsed or are between purchases |
| Few orders, not recent | One-time buyers from long ago | How large this group is as a share of all customers ever acquired |

Many tools give these groups names, such as champions or at risk. The names
are a convention of the tool, not a standard, and the cut points behind them
differ from one tool to the next. Where names are used here, define them by
their cells.

Three points about reading it:

- **Recency usually matters most.** Of the three, recency is the strongest
  single sign that a customer is still active, frequency the next, and
  monetary value the weakest. That is the order of the letters.
- **High frequency with poor recency is a warning, not a credit.** Take two
  customers whose last purchase was equally long ago. The one who used to buy
  often has gone much longer than their usual gap between purchases, and is
  more likely to have stopped for good than the one who always bought rarely.
  More past purchases do not always mean more future value. Fader, Hardie,
  and Lee (2005) show this with a model of buying and lapsing.
- **A cell describes, it does not predict.** The score says where a customer
  has been. Which cells are worth acting on is found by measuring what the
  customers in each cell did next.

## Movement between cells

One run is a snapshot. Run again on a later date with the same fixed bands,
and each customer has a cell at both dates. The table of movement between
them shows how many customers in each group stayed, improved, or fell back,
and where the recent and frequent group is filled from. This needs fixed
bands: with quantiles the groups are the same size at every run by
construction, and movement between them is partly an effect of the ranking.

## From scores to models

The three measures are also the inputs to models of customer value. The
models of buying and lapsing used for businesses without contracts need only
each customer's number of repeat purchases, the time of the last one, and the
length of time the customer has been observed, with average spend per
purchase handled separately. Two differences from the scores matter when
moving between them. Those models count repeat purchases, so the first
purchase is left out of frequency. And they measure recency from the
customer's first purchase forward to the last one, not back from the as-of
date. An RFM table built for scoring is not their input without those changes.
The models are on the [customer lifetime value](customer-lifetime-value.md)
page.

As model features, the measures are computed as of the date the decision is
made and from nothing after it.

## Building the outputs

The sections above say what the scores mean. This section is the contract
for building them: the choices to start from, what each output is built from,
its rows and columns, and the form it is shown in.

### Defaults

Start from these where nothing about the business decides otherwise. They
are a starting point, not a standard. The choices the team has settled on are
under [Where it applies to our data](#where-it-applies-to-our-data), and
those take precedence.

| Choice | Default | Why |
|---|---|---|
| As-of date | The last complete day in the data | A day still filling up makes its customers look less recent than they are |
| Window | A trailing window of whole years, long enough to hold the usual gap between purchases several times over | Whole years give every season the same weight |
| Unit of recency | Days | Coarser units can be made from days, and not the reverse |
| Frequency | Orders, with orders on the same day counted once and the first purchase counted | An order sent in two parts is one decision to buy |
| Monetary value | Average spend per order, with returns taken off | It adds something frequency does not already say |
| Spend or profit | Spend, unless a cost is held for every item | A margin built on partial costs ranks customers by what is missing |
| Number of scores | Five on each measure | The convention, and enough to separate the corners of the grid |
| How scores are cut | Fixed bands on all three measures | The analysis is nearly always run again, and only fixed bands can be compared between runs |
| Where the bands come from | The quintiles of the first run, rounded to values a person can say, then held | The bands start out balanced and stay put |
| Combined score | None | The cells are kept, and grouped by name where they are treated alike |
| New customers | A group of their own, set by time since first purchase | They have a recency and little else |

Where quantiles are used, customers are ranked across all customers on each
measure, not in sequence, and customers with the same value get the same
score. The groups are then unequal in size, which is reported and not
corrected.

A band is written with both its ends and says which end it includes, so that
a customer on a boundary has one score.

### Outputs

All are built from the RFM table.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| Distribution of a measure | Bands of the measure, before any score is cut | Customers, share of customers | Histogram, with the cut points marked |
| Bands | Each score of a measure | Lower and upper end, customers, share of customers | Table, one for each measure |
| Recency by frequency grid | Frequency score, 5 at the top | Recency score, 5 at the right | Grid, with customers, share of customers, value, and share of value in each cell |
| Cells | Each cell with at least one customer | Customers, value, average monetary value | Table, sorted by value |
| Named groups | Each group | The cells in it, customers, value, share of each | Table |
| Movement | Group at the first date, and a row for not yet a customer | Group at the second date, and a column for no order in the window | Table of counts, with each row also as shares |
| What happened next | Each cell or group | Customers, share who bought in the following period, spend per customer in it | Table |

Value in a cell is the customers' total spend in the window, whichever form
of monetary value is scored. The average monetary value of a cell is the
cell's spend ÷ the cell's orders, not the average of its customers'
averages.

Look at the distribution of each measure before cutting anything. It shows
whether frequency has enough spread for quantiles and where natural bands
fall.

What happened next needs an as-of date earlier than the end of the data, so
that there is a following period to look at. It is the output that shows
whether the cells separate customers who went on to buy from those who did
not, and it is the test of any change to the bands.

## Checks

Run these before reading any output. A failure is a fault in the table, not a
finding.

- The number of rows equals the number of distinct customers with an order in
  the window in the order summary.
- Frequency adds up to the number of orders in the window, and total spend to
  the spend in the window, under the same rule for orders on the same day.
- No order after the as-of date is used. Recency is never below zero and
  never longer than the window.
- The date of the first order is never after the date of the last.
- Every customer has one score on each measure. The bands of each measure
  cover every value with no gap and no overlap.
- The scores run the right way: average recency falls as the recency score
  rises, and average frequency and monetary value rise with their scores.
- The cells of the grid add up to all customers and to all value.
- Each named group is a set of cells, and no cell is in two groups.
- In the movement table, the rows add up to the customers at the first date
  and the columns to the customers at the second.

## Pitfalls

- **Data from after the as-of date.** Returns, merged identifiers, and
  corrections arrive later and change the history. A table built today for a
  past date differs from the one built on that date. For describing the
  past, say which was done. For model features and for what happened next,
  nothing from after the as-of date may be used.
- **Ties under quantiles.** Where many customers share a value, a cut falls
  among them and customers who are the same get different scores. Give equal
  values equal scores, or use fixed bands.
- **Recency is limited by the window.** With a trailing window no customer is
  less recent than the window is long. Customers who last bought before it
  are missing, not scored 1, so the lowest recency score is not all lapsed
  customers.
- **Customers with one order.** Their recency is their time since first
  purchase, so for them the recency score is a measure of when they were
  acquired. Where they are most of the base, the grid is mostly a picture of
  acquisition.
- **Orders split or repeated.** One purchase sent as two orders, or a
  cancelled order placed again, raises frequency with no change in
  behaviour. Settle this in the order summary, not in the scores.
- **Returns.** A customer whose orders were all returned has an order count
  and no spend. Decide whether they are in the table, and what a monetary
  value of zero or less scores.
- **One very large order.** It does not disturb a customer's band, but it
  can dominate the value of a cell. Give the number of customers beside
  every value.
- **Bands left alone too long.** Fixed bands set for one mix of customers
  drift out of balance as the business changes. Changing them is a break in
  every series, and is recorded as one.

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data. Six customers, a trailing window of two years, and monetary
value as average spend per order. Times are in days before the as-of date.

| Customer | First order | Last order | Orders | Total spend |
|---|---|---|---|---|
| A | 700 | 10 | 12 | 1,440 |
| B | 20 | 20 | 1 | 60 |
| C | 720 | 400 | 8 | 1,600 |
| D | 400 | 400 | 1 | 30 |
| E | 500 | 100 | 3 | 135 |
| F | 300 | 45 | 2 | 180 |

The fixed bands, each including both its ends:

| Score | Recency, days | Frequency, orders | Monetary value, per order |
|---|---|---|---|
| 5 | 0 to 30 | 11 or more | 200 or more |
| 4 | 31 to 90 | 6 to 10 | 100 to 199 |
| 3 | 91 to 180 | 3 to 5 | 50 to 99 |
| 2 | 181 to 365 | 2 | 25 to 49 |
| 1 | 366 or more | 1 | Under 25 |

The RFM table:

| Customer | Recency | Frequency | Monetary value | R | F | M | Cell |
|---|---|---|---|---|---|---|---|
| A | 10 | 12 | 120 | 5 | 5 | 4 | 554 |
| B | 20 | 1 | 60 | 5 | 1 | 3 | 513 |
| C | 400 | 8 | 200 | 1 | 4 | 5 | 145 |
| D | 400 | 1 | 30 | 1 | 1 | 2 | 112 |
| E | 100 | 3 | 45 | 3 | 3 | 2 | 332 |
| F | 45 | 2 | 90 | 4 | 2 | 3 | 423 |

Frequency adds up to 27 orders and total spend to 3,445, which are the
figures to check against the order summary.

Three things to read from it:

- **B is recent with one order, and is new.** B's first order and last order
  are the same one, 20 days ago. Time since first purchase is what separates
  B from an occasional buyer of long standing.
- **C and D have the same recency and are not alike.** Both last bought 400
  days ago. C made 8 orders in the 320 days before that, about one every 46
  days, and has now been silent for many times that gap. D bought once, and
  400 days says little about a customer with no usual gap. C has very
  probably stopped. For D there is not enough to say.
- **Total spend would rank C first and average spend does too, for different
  reasons.** C has the highest total because of 8 orders and the highest
  average because each order was large. A has the next highest total, 1,440,
  almost all of it from frequency: scored on total spend, A's monetary score
  would repeat A's frequency score.

## Where it applies to our data

*Add: the transaction datasets RFM can be computed from, linked to their
pages under Data, with the customer identifier each one carries.* Why: the
scores are only as good as the identifier that ties a customer's purchases
together.

*Add: the observation window, the as-of date convention, and the definition
chosen for each of the three measures, including whether monetary value is
total or average and spend or profit.* Why: two RFM tables built with
different definitions cannot be compared.

*Add: the bands or quantiles used for each score, and the groups of cells the
business has agreed names for.* Why: a named group means nothing without the
cells behind it.

*Add: the decisions the groups are used for, from the
[decision inventory](../business/decisions.md).* Why: a segmentation nobody
acts on is a report.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Fader, Peter S., Bruce G. S. Hardie, and Ka Lok Lee. "RFM and CLV: Using
Iso-Value Curves for Customer Base Analysis." *Journal of Marketing Research*
42, no. 4 (2005): 415–430. The link from the three measures to a model of
customer value, and the result that higher frequency does not always mean
higher value at a given recency.

Hughes, Arthur M. *Strategic Database Marketing.* Probus Publishing and
McGraw-Hill. First published in 1994, with later editions in 2000, 2005, and
2012. The scoring of each measure in fifths, from 1 to 5, and the use of the
cells for selecting customers to contact.
