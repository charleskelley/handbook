---
title: "Customer lifetime value"
type: method
depth: build
owner: ds-lead
audience: [ds, mle, analyst, leadership]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [predictive, customers, modeling, valuation]
sources:
  - "Fader and Hardie, Probability Models for Customer-Base Analysis, Journal of Interactive Marketing 23(1), 2009"
  - "Fader, Hardie, and Lee, Counting Your Customers the Easy Way: An Alternative to the Pareto/NBD Model, Marketing Science 24(2), 2005"
  - "Fader and Hardie, Customer-Base Valuation in a Contractual Setting: The Perils of Ignoring Heterogeneity, Marketing Science 29(1), 2010"
---

# Customer lifetime value

An estimate of what a customer will be worth to the business from now on.
This is a problem page: it says what the quantity is, how it differs between
subscription and non-subscription businesses, and which models estimate it.
The first models here need nothing but the transaction history, which makes
lifetime value a good early project for a team whose data is still being
built.

## What it is

Customer lifetime value, CLV, is the present value of the future margin a
customer is expected to generate. Three words in that sentence do the work.
*Future*: it looks forward from today, so what a customer has already spent
is evidence and not the answer. *Margin*: it is profit after the costs of
serving the customer, not revenue. *Expected*: it is an average over what
might happen, and for any one customer the range around it is wide. It is
built from three parts: how long the customer stays active, how much they buy
while they are, and what each purchase is worth. A discount rate turns later
margin into today's money. Which models are used depends on one fact about
the business: whether customers leave observably, by ending a contract, or
silently, by not coming back.

## When it is the right choice

- To set how much the business can afford to spend to acquire a customer,
  by channel or campaign.
- To decide which customers get costlier service, retention effort, or
  offers.
- To compare cohorts: whether customers acquired this year are worth what
  last year's were.
- To weigh a [churn score](churn-and-propensity.md): the risk of losing a
  customer matters in proportion to what they are worth.
- To value the customer base as a whole.

## When it is not

- **A precise figure for one customer.** The estimate for an individual is
  very uncertain. Use it to rank customers and to value groups.
- **Too little history.** A cohort must be observed for long enough to see
  repeat buying or cancellation. For a business in its first year, any
  lifetime value is mostly assumption.
- **A business that has changed.** Models project past behaviour forward. A
  new pricing scheme, product, or market makes the past a poor guide.
- **The effect of an action.** High-value customers are valuable. That does
  not show that spending more on them makes them more so. See
  [directional versus causal](directional-versus-causal.md).
- **Purchases that are rare by nature.** Where most customers buy once in
  many years, there is little repeat behaviour to model.

## The definition, in parts

Settle these before modelling. Two lifetime values built on different
choices cannot be compared.

| Choice | Options | Default |
|---|---|---|
| What is counted | Revenue, or margin after cost of goods, delivery, service, and returns | Margin |
| From when | From now, for an existing customer, called residual value. Or from acquisition, for a new one | State which. They differ by everything already received |
| Acquisition cost | Included, giving a net figure, or kept separate | Separate, and compared with it |
| Horizon | A fixed number of years, or without limit | A fixed horizon of 3 to 5 years, stated. Beyond that the estimate is mostly the model's assumption |
| Discount rate | The rate at which later money is worth less | Finance's rate for the business. Not chosen by the team |
| The customer | As defined for the [customer-base audit](customer-base-audit.md#defining-the-customer) | The same |

## Two settings

| | Customers subscribe | Customers buy when they choose |
|---|---|---|
| Leaving | Observed, on a date | Never observed. A customer who has gone quiet may return |
| Purchases | On a schedule, at a known price | At any time, for any amount |
| What is modelled | How long until cancellation | How often they buy while active, and when they silently stop |
| Starting point | The [survival curve](survival-analysis.md) | The [RFM](rfm-analysis.md) summary of each customer |
| Main risk | Assuming one retention rate for everyone | Treating a quiet customer as certainly gone, or certainly still there |

Many businesses have both: a subscription with purchases on top. Model the
two parts separately.

## Where customers subscribe

Lifetime value is the sum, over future periods, of the margin in the period
× the probability the customer is still subscribed × the discount factor for
that period. The middle term is the survival curve. The discount factor for
a period is 1 ÷ (1 + the discount rate per period) to the power of the
number of periods ahead. An annual rate is converted to the unit of time in
use.

**The textbook formula and its flaw.** If every customer had the same
retention rate *r* in every period, a margin *m* per period, and a discount
rate *d*, the sum would be

*m* × *r* ÷ (1 + *d* − *r*)

counting from the first renewal. It is quoted everywhere and is wrong in a
known direction. Customers do not share a retention rate. Those most likely
to leave do so first, so the customers who remain have a higher average
rate, and a cohort's observed retention rate rises with tenure. Applying one
average rate to everyone understates the value of the customers who stay,
and so understates the whole. The [worked example](#worked-examples) shows
the size of the error.

**What to do.** Estimate the survival curve by cohort, from the data. Where
it has to be extended beyond the periods observed, use a model that allows
customers to differ. The shifted beta geometric model of Fader and Hardie
does this with two parameters, which describe how the chance of cancelling
varies across customers. They are fitted to a cohort's first few renewal
periods by maximum likelihood, and the formulas are in their 2007 paper in
the sources. For a customer who has already stayed some time, use survival from
their current tenure onward, which is higher than a new customer's.

Add expected changes in margin, from upgrades, downgrades, and price, as a
separate assumption and say what it is.

## Where customers buy when they choose

The standard models are probability models of a simple story, known
informally as buy-till-you-die models.

- While a customer is active, they buy at random at their own steady rate.
- At some point they become inactive for good, and nobody is told.
- Customers differ in their buying rate and in how soon they become
  inactive.

From that story and the transaction history, the model works out for each
customer the probability that they are still active and the number of
purchases to expect in any future period. The two best known are the
Pareto/NBD model and the BG/NBD model, which make slightly different
assumptions about when a customer becomes inactive and give similar answers.
The BG/NBD is much the easier to fit. It has four parameters: two describe
how buying rates vary across customers, and two how the chance of becoming
inactive varies. They are estimated by maximum likelihood from the customer
summary table below. The likelihood, and the formulas for the probability of
being active and for expected purchases, are in Fader, Hardie, and Lee's
2005 paper in *Marketing Science*, in the sources.

**Inputs.** Three numbers per customer, as of a date:

| Input | Definition |
|---|---|
| Frequency | The number of repeat purchases: purchases after the first |
| Recency | The time from the customer's first purchase to their last |
| Age | The time from the customer's first purchase to the as-of date |

These are not the recency and frequency of an RFM score. The differences are
set out on the [RFM page](rfm-analysis.md#from-scores-to-models). A purchase
is a day with at least one order, so days on which a customer bought more
than once count once. Time is measured in weeks, with fractions. A customer
who ordered on days 0, 30, and 100, seen on day 200, has a frequency of 2, a
recency of 100 days, and an age of 200 days.

**What the model sees that a rule does not.** A customer who bought often
and then stopped is more likely to have gone than one who always bought
rarely and has been quiet for the same time. The long silence is out of
character for the first and normal for the second. So expected future
purchases do not always rise with past frequency.

**Spend.** A second model, the gamma-gamma model, estimates each customer's
average spend per purchase from their own average and the average across all
customers, pulling customers with few purchases toward the overall figure.
It assumes that how much a customer spends per purchase is unrelated to how
often they buy. Check that in the data. It has three parameters, set out in
the same authors' paper on RFM and CLV in the sources. It needs positive
amounts, so where the margin on an order can be zero or negative, model
spend and convert to margin with a margin rate. A customer with no repeat
purchase has no average of their own and is given the average across
customers.

**Putting it together.** Expected purchases in each future period × expected
margin per purchase × the discount factor, summed over the horizon.

### The machine-learning alternative

A supervised model can predict a customer's margin over the next 12 months
directly from features, exactly as on the
[churn and propensity](churn-and-propensity.md) page but with an amount as
the outcome. It can use anything known about the customer, where the
probability models use only purchase timing and amounts. Against that, it
needs a long history to build training examples, predicts only as far ahead
as its outcome window, and has to cope with an outcome that is zero for many
customers and very large for a few.

Start with the probability models. They need little data, give a figure for
any horizon, and are a strong baseline. Add a supervised model when there
are features that should matter, such as acquisition channel or first
product, and enough history to test whether they do.

## Checking a model before using it

A lifetime value cannot be checked against the truth, which lies years
ahead. It can be checked against the recent past.

1. Split the history at a date. Everything before it is the calibration
   period, everything after the holdout period.
2. Fit the model on the calibration period only.
3. Predict each customer's purchases, and margin, in the holdout period.
4. Compare with what happened: in total, period by period, and by group.

Three comparisons matter:

- **Total purchases over time,** predicted against actual, cumulatively.
  Shows whether the model tracks the base as a whole.
- **Purchases in the holdout period by frequency in the calibration
  period.** Shows whether the model separates heavy from light buyers
  correctly.
- **By cohort.** A model fitted to all customers may fit none of the cohorts
  well if they differ.

Compare with a naive baseline: each customer repeats their last year. Once
the model has passed, refit it on the whole history and predict forward from
today.

## Using it

- **Use groups.** Averages over a cohort, a channel, or a segment are far
  more reliable than any individual's figure.
- **Compare with acquisition cost by channel.** The ratio of lifetime value
  to the cost of acquiring the customer, by channel and cohort, is the use
  most businesses come for. It needs value from acquisition. For a cohort
  already observed, that is the margin received so far, including the first
  purchase, plus the residual value of its customers from now. For customers
  yet to be acquired, use the figure for the most recent cohorts from the
  same channel. Be sure both sides are margin and both cover the same
  customers.
- **Give the range.** Report lifetime value under a higher and a lower
  retention assumption and discount rate. If the decision changes within
  the range, say so.
- **The mean hides the shape.** Value is concentrated. A few customers
  carry most of it, as the [customer-base audit](customer-base-audit.md)
  shows for the past. Report the distribution.
- **Do not confuse value with responsiveness.** Whether to spend more on
  high-value customers depends on what the spending changes, which is a
  question for an [experiment](experiments-and-lift-tests.md).

## Building the outputs

Customer summary table, for a business without contracts

:   One row per customer, as of the end of the calibration period. Columns:
    customer identifier, date of first purchase, frequency, recency, age,
    and the average value of the repeat purchases. Built from the order
    summary on the
    [customer-base audit](customer-base-audit.md#table-contracts) page.
    Recency and age are in the same unit of time, and recency is never
    larger than age.

Cohort renewal table, for subscriptions

:   One row per cohort and period since the start. Columns: cohort, period,
    customers subscribed at the start of the period, customers who renewed.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| Parameters | Model | The fitted parameters, the calibration period, the number of customers | Table |
| Tracking | Period | Actual and predicted purchases, per period and cumulative | Two lines, with the split between calibration and holdout marked |
| Conditional expectations | Frequency in the calibration period | Customers, actual and predicted purchases per customer in the holdout period | Two lines |
| Customer predictions | Customer | Probability of being active, expected purchases and margin over the horizon, lifetime value | Table. For ranking and for building groups |
| Value by group | Cohort, channel, segment | Customers, average lifetime value, its range under the alternative assumptions, total | Table |
| Distribution | Band of lifetime value | Customers, share of total value | Histogram and decile table |
| Projected survival, for subscriptions | Period since the start | Observed and projected share subscribed, by cohort | Lines |

Defaults, where nothing about the business decides otherwise:

| Choice | Default | Why |
|---|---|---|
| First model without contracts | BG/NBD for purchases, gamma-gamma for spend | Little data needed, and a baseline for anything later |
| First model with contracts | Survival by cohort from the data, extended by the shifted beta geometric model | Allows customers to differ |
| Unit of time | Weeks | Fine enough for most purchase rates |
| Holdout period | The most recent year | A full seasonal cycle |
| Fitting | By cohort, or by acquisition channel, where they differ | One set of parameters hides real differences |
| Horizon | 3 years, with 5 as an alternative | Further out is assumption |

## Checks

- Every customer's recency is no larger than their age, and a customer with
  no repeat purchase has a frequency and a recency of zero.
- The first purchase is not counted in frequency.
- Total predicted purchases over the calibration period equal the actual
  total, closely.
- In the holdout period, predicted total purchases are within a stated
  tolerance of actual, and the model does better than the naive baseline.
- Predicted purchases by calibration-period frequency follow the actual
  line across its range, not only in the middle.
- Average spend per purchase is not strongly related to frequency. If it
  is, the gamma-gamma model's assumption fails.
- The total of the customers' lifetime values is a believable multiple of
  last year's total margin. A base valued at thirty years of current margin
  is an error.
- For subscriptions, the projected survival curve passes through the
  observed points, and its retention rate rises with tenure.

## Pitfalls

- **Revenue in place of margin.** Customers who buy on discount, return
  often, or cost a lot to serve can have high revenue and low value.
- **One retention rate for everyone.** See above.
- **Past value in place of future value.** A customer who spent a great
  deal and has gone quiet may be worth little now.
- **A period that will not recur.** A promotion, a shortage, or a one-off
  surge in the calibration period is projected forward as normal. Note such
  periods as insights.
- **Cohorts of different quality fitted together.** If recent cohorts are
  weaker, a model fitted to all customers overvalues the new ones.
- **A few very large customers.** Business accounts mixed in with consumers
  dominate the spend model. Model them separately.
- **Reading the probability of being active as certain.** A customer at 40%
  is neither gone nor safe.
- **A horizon without limit and a low discount rate.** Most of the value
  then comes from years the model knows nothing about.
- **Comparing with an acquisition cost that covers different customers,** or
  that leaves out discounts given at acquisition.

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data.

**The simple formula.** A subscription yields a margin of 100 a year. The
retention rate is 80% and the discount rate 10%. Counting from the first
renewal:

100 × 0.80 ÷ (1 + 0.10 − 0.80) = 267

**Two kinds of customer.** Now suppose that 80% is an average over two
groups of equal size: loyal customers who renew at 95%, and others who renew
at 65%.

| Group | Share | Retention | Lifetime value |
|---|---|---|---|
| Loyal | 50% | 95% | 100 × 0.95 ÷ 0.15 = 633 |
| Others | 50% | 65% | 100 × 0.65 ÷ 0.45 = 144 |
| Average | | 80% | 389 |

The true average is 389. The formula with the average rate gave 267, which
is 31% too low. Nothing about the business differs between the two
calculations except whether customers are allowed to differ.

**What the cohort looks like.** Follow 1,000 such customers:

| Year | Loyal remaining | Others remaining | Total | Retention in the year |
|---|---|---|---|---|
| Start | 500 | 500 | 1,000 | |
| 1 | 475 | 325 | 800 | 80% |
| 2 | 451 | 211 | 662 | 83% |
| 3 | 429 | 137 | 566 | 85% |

The retention rate rises each year though no customer's own rate changed.
The cohort is losing its less loyal members. A rising retention rate is
therefore not, on its own, evidence that the business is getting better at
keeping customers, and a single rate taken from the first year badly
undervalues those who are still there in year three.

## Where it applies to our data

*Add: the definition of lifetime value in use: margin or revenue, the
horizon, the discount rate and who set it, and whether it is from
acquisition or from now.* Why: figures quoted around the business cannot be
compared without it.

*Add: which lines of business are contractual and which are not, and the
model used for each.* Why: the wrong kind of model gives a confident wrong
answer.

*Add: the datasets that give margin by order, linked to their pages under
Data, and what costs they include.* Why: lifetime value in revenue
overstates, and by different amounts for different customers.

*Add: the acquisition cost by channel, where it is recorded, and what it
includes.* Why: the comparison with lifetime value is the main use.

*Add: periods in the history that should not be projected forward, from the
insights log.* Why: the models treat all history as typical.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Fader, Peter S., and Bruce G. S. Hardie. "Probability Models for
Customer-Base Analysis." *Journal of Interactive Marketing* 23, no. 1 (2009):
61–69. An overview of the whole family of models, organised by whether
customers have contracts and whether purchases come at any time or at fixed
times. Start here.

Schmittlein, David C., Donald G. Morrison, and Richard Colombo. "Counting
Your Customers: Who Are They and What Will They Do Next?" *Management
Science* 33, no. 1 (1987): 1–24. The Pareto/NBD model, the original.

Fader, Peter S., Bruce G. S. Hardie, and Ka Lok Lee. "'Counting Your
Customers' the Easy Way: An Alternative to the Pareto/NBD Model." *Marketing
Science* 24, no. 2 (2005): 275–284. The BG/NBD model.

Fader, Peter S., Bruce G. S. Hardie, and Ka Lok Lee. "RFM and CLV: Using
Iso-Value Curves for Customer Base Analysis." *Journal of Marketing Research*
42, no. 4 (2005): 415–430. The spend model, and how recency and frequency
together determine value.

Fader, Peter S., and Bruce G. S. Hardie. "How to Project Customer Retention."
*Journal of Interactive Marketing* 21, no. 1 (2007): 76–90. The shifted beta
geometric model for subscriptions.

Fader, Peter S., and Bruce G. S. Hardie. "Customer-Base Valuation in a
Contractual Setting: The Perils of Ignoring Heterogeneity." *Marketing
Science* 29, no. 1 (2010): 85–93. Why a single retention rate undervalues the
base. The basis of the worked example's point.

Gupta, Sunil, Donald R. Lehmann, and Jennifer Ames Stuart. "Valuing
Customers." *Journal of Marketing Research* 41, no. 1 (2004): 7–18. Customer
value as the basis for valuing a firm, using the simple formula.

Berger, Paul D., and Nada I. Nasr. "Customer Lifetime Value: Marketing Models
and Applications." *Journal of Interactive Marketing* 12, no. 1 (1998):
17–30. The early, formula-based treatments.

McCarthy, Daniel M., and Peter S. Fader. "Customer-Based Corporate Valuation
for Publicly Traded Noncontractual Firms." *Journal of Marketing Research*
55, no. 5 (2018): 617–635. Valuing a whole business from its customer
behaviour.
