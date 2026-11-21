---
title: "Churn and propensity models"
type: method
depth: build
owner: ds-lead
audience: [ds, mle, analyst]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [predictive, customers, retention, modeling]
sources:
  - "Neslin, Gupta, Kamakura, Lu, and Mason, Defection Detection, Journal of Marketing Research 43(2), 2006"
  - "Ascarza, Retention Futility: Targeting High-Risk Customers Might Be Ineffective, Journal of Marketing Research 55(1), 2018"
---

# Churn and propensity models

Models that score each customer on how likely they are to do something in a
coming period: leave, buy, respond, upgrade. This is a problem page, not a
technique page. It says how the problem is set up, and uses the techniques
on other pages to solve it. It is also the recommended first model for a new
team to take end to end, because its inputs can be built from the transaction
history alone.

## What it is

A propensity model predicts, for each customer as of a date, the probability
of a defined event in a defined window after that date. A **churn model** is
the case where the event is the customer leaving. The same structure serves
propensity to buy a category, to respond to a campaign, to upgrade, or to
pay late. The output is a score per customer, used to rank customers so that
a limited action, a call, an offer, a place in a programme, goes to those
for whom it is most worthwhile. The modelling is ordinary supervised
classification. What makes the problem hard is around the model: saying what
"left" means, building a training set that respects time, and the fact that
the customers most likely to leave are not necessarily the ones an action can
keep.

## When it is the right choice

- The business takes an action on a limited number of customers and must
  choose which.
- The event can be defined from data and has happened often enough in the
  past to learn from: hundreds of events at the least, preferably
  thousands.
- History exists for long enough to build features before a date and observe
  outcomes after it.
- A [customer-base audit](customer-base-audit.md) and
  [RFM analysis](rfm-analysis.md) have been done, so the base rates are
  known and there is a rule to beat.

## When it is not

- **There is no action.** A churn score nobody can act on changes nothing.
  Start from the decision: see
  [framing and evaluating a prediction](framing-and-evaluating-a-prediction.md).
- **The question is how many will leave,** not who. That is a forecast or a
  [survival analysis](survival-analysis.md) of the cohort.
- **The question is who can be persuaded.** Risk of leaving and
  responsiveness to an offer are different things. See
  [from a score to an action](#from-a-score-to-an-action) and
  [uplift modeling](uplift-modeling.md).
- **Too few events.** With a few dozen, use a rule and review the accounts
  by hand.
- **The event is forced.** Customers whose contract was ended by the
  business, or who moved out of the area served, are not predicted by
  behaviour and should not be in the outcome.

## Defining the outcome

The definition is a business decision recorded in writing. The model
predicts whatever is defined, including its mistakes.

**Where customers subscribe.** The event is observed, but there are still
choices:

- The date: the request to cancel, the end of the paid term, or the last
  day of service. The first is the earliest the business knows. The model
  should predict far enough ahead of it for an action to be possible.
- Voluntary and involuntary. A customer who cancels and one whose payment
  failed leave for different reasons and call for different actions. Model
  them separately or model only the one the action addresses.
- Downgrades, pauses, and switches between plans. Decide whether each
  counts.

**Where customers buy when they choose.** Nobody announces leaving, so the
event has to be constructed in two steps. First define a lapse: a stated
number of days without a purchase. Choose the number from the data: for
customers who reached each length of time since their last order, find the
share who went on to order again within a year. The threshold is the length
at which that share becomes small enough to call the customer gone. Then
define what the model predicts: for a customer who has not lapsed on the
as-of date, no purchase in that same number of days after it. A customer
with the outcome has, by the end of the window, lapsed under the
definition. It is a trade. A long threshold is rarely
wrong and declares the loss too late to act. A short one acts early and
labels as lost many customers who were only between purchases. The
[worked example](#worked-examples) shows the table. An alternative with no
threshold is the probability of being active from the models on the
[customer lifetime value](customer-lifetime-value.md) page.

**For propensity to buy or respond.** The event is a purchase of the
category, or a response, in the window. One caution for response models: a
model trained on customers who were sent past campaigns learns who responds
among those the business chose to contact. Applied to everyone, it is being
used outside its data.

## The snapshot design

The training set is a stack of snapshots.

1. Choose a series of past as-of dates, commonly the first of each month.
2. For each date, list the customers in the population on that date: those
   active within a stated period and eligible for the action.
3. For each such customer, build features from history up to the date and
   no later.
4. For each, record the outcome in the window after the date.

Each customer appears once for every as-of date on which they were in the
population. The timeline, and the rule that features come only from before
the as-of date, are on the
[framing page](framing-and-evaluating-a-prediction.md#the-framing).

Split by as-of date: the earliest dates to train, later ones to validate,
the latest with complete outcome windows to test. Drop the training dates
whose outcome windows run into the validation period, and likewise between
validation and test, as the
[framing page](framing-and-evaluating-a-prediction.md#splitting-the-data)
sets out. Because the same customer
recurs across snapshots, rows are not independent, and intervals on any
measure are computed by resampling customers, not rows.

## A first feature set

A useful model can be built from the order history and the customer table,
before any feature store exists. Every feature is computed as of the as-of
date from data dated before it.

| Family | Examples | Why |
|---|---|---|
| Recency | Days since last order, since last visit, since last contact | The strongest single sign of activity |
| Frequency | Orders in the last 3, 6, and 12 months | Habit |
| Value | Spend and average order value over the same windows | Size of the relationship |
| Tenure | Months since first order | New customers leave at a different rate |
| Trend | Orders in the last 3 months ÷ orders in the 3 months before. Recency ÷ the customer's own average gap between orders | A fall against the customer's own habit says more than a low level |
| Breadth | Number of categories and channels used | Wider relationships last |
| Friction | Returns, complaints, late deliveries, failed payments | Reasons to go |
| Price | Share of orders made on discount | Sensitivity to offers |
| Contract | Plan, term, time to renewal, payment method | For subscriptions, renewal dates concentrate the risk |

Where a ratio's denominator is zero, as for a customer with no orders in the
earlier window or only one order ever, use the difference in place of the
ratio, or a flag for the case.

The first three rows are the [RFM](rfm-analysis.md) measures. An RFM table
computed as of a date is a ready-made feature set and a baseline in one.
These transformations belong in SQL in the data layer, built once and
shared: see the
[feature rule](development/experiment-tracking.md#feature-engineering-where-each-transformation-lives).

## The ladder of models

Climb only as far as the decision needs. Each rung is the baseline for the
next.

| Rung | What it is | When to stop here |
|---|---|---|
| A rule | Flag customers past a recency threshold, or in certain RFM cells, and use the cell's past event rate as the score | When it meets the need, or events are too few for more |
| [Logistic regression](regression.md) | On the feature families above, with logarithms and a few bands | Often. Explainable, stable, calibrated, quick to deploy |
| [Gradient-boosted trees](gradient-boosted-trees.md) | On the same features and more | When it beats the regression at the capacity that matters by enough to change the decision |
| A discrete-time hazard model | For subscriptions: one row per customer per period at risk. See [survival analysis](survival-analysis.md#from-curves-to-models) | When the timing matters, or the horizon varies |

Evaluate each as the
[framing page](framing-and-evaluating-a-prediction.md#measures) sets out:
lift and precision at the number of customers that can be acted on, on later
as-of dates, against the rung below.

## From a score to an action

A risk score ranks customers by how likely they are to leave. The action
should go to customers for whom it changes the outcome and is worth its
cost. These are different orderings.

Customers divide four ways by what the action would do:

| Group | Without the action | With the action | Acting on them |
|---|---|---|---|
| Persuadable | Leave | Stay | Is the whole gain |
| Lost | Leave | Leave | Wastes the cost |
| Safe | Stay | Stay | Wastes the cost, and any discount given |
| Disturbed | Stay | Leave | Does harm. A reminder that prompts a cancellation |

In the uplift literature the four are called persuadables, lost causes, sure
things, and sleeping dogs.

A churn model puts the persuadable and the lost together at the top, and the
very highest scores are often the lost: customers who have in effect already
gone. Published field experiments have found retention offers aimed at the
highest-risk customers to be ineffective, and in cases harmful. So:

- **Test the action, not only the model.** Score customers, then act on a
  random half of the high scorers and hold the other half out. The
  difference in outcomes is the effect of the action, by score band. See
  [experiments and lift tests](experiments-and-lift-tests.md).
- **Look below the top.** The best band to act on is often the upper middle
  of the risk scores, where customers are wavering.
- **Weigh risk by value.** A moderate risk of losing a valuable customer can
  matter more than a high risk of losing a marginal one. Combine the score
  with [customer lifetime value](customer-lifetime-value.md).
- **Move to uplift when the tests exist.** Once there is data from
  randomized actions, a model can predict the effect of the action directly:
  see [uplift modeling](uplift-modeling.md).

## Living with the model

- **Keep an untouched group.** Once high scorers are treated, their outcomes
  reflect the treatment. A model retrained on that data learns that the
  customers it flagged did not leave. At every scoring run, leave a random
  share of the customers selected for the action untouched, drawn afresh
  each time. This is the test of the action above, made permanent at a
  smaller size. It measures the action and supplies outcomes to retrain
  on.
- **Watch the inputs and the outcome rate.** A change in how orders are
  recorded, or in the population being scored, degrades the model without
  any error being raised. See
  [model monitoring](development/model-monitoring.md).
- **Labels arrive late.** The outcome for today's scores is known only after
  the outcome window. Performance in use is always measured with that
  delay.
- **Retrain on a schedule and on a signal,** and compare each new model with
  the old on the same later data. The route to production is on the
  [path to production](development/path-to-production.md) page.

## Building the outputs

Outcome definition

:   The event, the window, the population, what is excluded, and for a
    constructed lapse, the threshold and the table that justified it. Dated
    and agreed with the owner of the decision.

Snapshot table

:   One row per customer and as-of date. Columns: customer identifier, as-of
    date, each feature, the outcome, the end of the outcome window, and the
    split. Features hold values as known on the as-of date. Rows whose
    outcome window is not complete carry no outcome and are used only for
    scoring.

Scored list

:   One row per customer per scoring run. Columns: customer identifier,
    as-of date, score, rank or band, model version, whether the customer was
    selected for the action, and whether they were then left untouched.

Action log

:   One row per customer per action taken. Columns: customer identifier,
    date, action, and the scoring run that led to it. Without it, later
    outcomes cannot be interpreted.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| Threshold table, for a constructed lapse | Days since last order | Customers who reached that gap at least a year before the end of the data, share of them who ordered again within the year after | Table and curve |
| Evaluation | As on the [framing page](framing-and-evaluating-a-prediction.md#building-the-outputs) | | With the rule and the regression as baseline rows |
| Outcome rate over time | As-of date | Population, events, rate | Line. For reading stability |
| Score bands | Band of score | Customers, event rate, average value | Table |
| Action test | Band of score | Treated and held-out customers, outcome rate in each, difference, interval | Table |

Defaults, where nothing about the business decides otherwise:

| Choice | Default | Why |
|---|---|---|
| As-of dates | Monthly | Matches how often lists are acted on |
| Population | Customers who have not lapsed on the as-of date, past their first 30 days | The newly acquired and the long gone are different problems |
| Outcome window | The lapse threshold, for a constructed lapse. For a subscription, long enough for an action to take effect | A long window delays every label |
| Observation window | 24 months | Covers two seasonal cycles |
| First model | Logistic regression on the feature families above | The baseline for everything after |
| Untouched group | Half of those selected, for the first test of an action. A tenth to a fifth of those selected afterwards, drawn afresh each run | To measure the action and to retrain on |

## Checks

All the checks on the
[framing page](framing-and-evaluating-a-prediction.md#checks) apply. In
addition:

- The event rate by as-of date is steady, or its movements are explained.
- No feature is a restatement of the outcome. Fields that often are:
  account status, a cancellation reason, a closure date, a count of win-back
  contacts, the date of a final bill.
- Activity features for customers who later left do not fall to zero only
  because the customer had already cancelled before the as-of date. If they
  do, the population includes customers who have already left.
- The most recent as-of dates have complete outcome windows before they are
  used for testing.
- The model's highest scorers are still reachable: check how many have had
  any activity in the last month.
- The untouched group is random, and was in fact left untouched.

## Pitfalls

- **Features from the current customer table.** A status field updated at
  cancellation predicts cancellation perfectly. Build from history as it
  stood.
- **Predicting the past.** A model whose top scorers stopped buying months
  ago has learned the lapse definition. Narrow the population to customers
  who are still active.
- **Aiming at the highest risk.** See
  [from a score to an action](#from-a-score-to-an-action).
- **Counting saved customers without a comparison.** "Of 1,000 called, 800
  stayed" says nothing. Most would have stayed. Only the held-out group
  shows how many.
- **Voluntary and involuntary leaving mixed.** The model learns failed
  payments, and the retention call does nothing for them.
- **A definition that drifts.** A new cancellation flow or a change of
  billing system moves the event. Record it as an insight on the dataset.
- **Retraining on treated customers.** See
  [living with the model](#living-with-the-model).
- **Discounts that teach customers to threaten to leave.** A retention offer
  that becomes known changes who cancels. The effect shows only over a long
  period.

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data.

**Choosing a lapse threshold.** For customers who reached each length of
time since their last order, the share who ordered again within the
following year:

| Days since last order | Share who ordered again |
|---|---|
| 30 | 70% |
| 60 | 52% |
| 90 | 35% |
| 120 | 22% |
| 180 | 12% |
| 365 | 4% |

Calling a customer lapsed at 180 days is wrong about one in eight of them,
and declares the loss six months late. At 90 days it is wrong about one in
three. The business settles on 120 days, wrong about one in five. The model
is then asked: among customers who ordered in the last 120 days, who will
place no order in the next 120?

**A snapshot.** Four customers on one as-of date:

| Customer | Days since last order | Orders, last 12 months | Orders, last 3 months | Orders, the 3 months before | Tenure, months | Ordered in the next 120 days | Outcome |
|---|---|---|---|---|---|---|---|
| A | 12 | 9 | 3 | 2 | 30 | Yes | 0 |
| B | 75 | 6 | 1 | 3 | 18 | No | 1 |
| C | 40 | 2 | 1 | 1 | 5 | Yes | 0 |
| D | 88 | 1 | 1 | 0 | 3 | No | 1 |

B is the case trend features exist for: six orders in a year, but one in the
last three months against three in the three before. Frequency alone makes B
look like a good customer.

**A leak.** Suppose the customer table has a status column, and a nightly
job sets it to "inactive" after 120 days without an order. Joined from a
later copy of the table, such as the one at the end of the outcome window,
it reads "inactive" for B and D and "active" for A and C, and the model
scores perfectly. On the as-of date all four were "active". The
feature has to be read as it stood on the as-of date, where it is the same
for everyone and useless, which is the right answer.

**From the score to the decision.** The arithmetic of whom to act on, and
its dependence on the effect of the action, is worked through on the
[framing page](framing-and-evaluating-a-prediction.md#worked-examples).

## Where it applies to our data

*Add: the definition of leaving in use, for each line of business, with the
threshold table for any constructed lapse.* Why: the model predicts the
definition, and so does every report that quotes a churn rate.

*Add: the retention and marketing actions that use a score, their capacity
and cost, and who owns each, from the [decision
inventory](../business/decisions.md).* Why: the capacity sets the depth at
which the model is evaluated.

*Add: the datasets the features are built from, linked to their pages under
Data, and which of them keep history.* Why: features must be built as of a
past date.

*Add: whether an untouched group exists, its size, and where the action log
is kept.* Why: without them the action cannot be measured and the model
cannot be honestly retrained.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Neslin, Scott A., Sunil Gupta, Wagner Kamakura, Junxiang Lu, and Charlotte H.
Mason. "Defection Detection: Measuring and Understanding the Predictive
Accuracy of Customer Churn Models." *Journal of Marketing Research* 43, no. 2
(2006): 204–211. A tournament of churn models on one dataset: how much the
method matters, and what separates good entries from poor ones.

Ascarza, Eva. "Retention Futility: Targeting High-Risk Customers Might Be
Ineffective." *Journal of Marketing Research* 55, no. 1 (2018): 80–98. Field
experiments showing that the customers most at risk are not the ones who
respond to retention offers. The reason for the section on scores and
actions.

Ascarza, Eva, Scott A. Neslin, Oded Netzer, and others. "In Pursuit of
Enhanced Customer Retention Management: Review, Key Issues, and Future
Directions." *Customer Needs and Solutions* 5, no. 1–2 (2018): 65–81. A review of the whole problem: whom to
target, with what, when, and how to measure it.

Lemmens, Aurélie, and Sunil Gupta. "Managing Churn to Maximize Profits."
*Marketing Science* 39, no. 5 (2020): 956–973. Choosing whom to target by
expected profit and not by risk.

Verbeke, Wouter, Karel Dejaeger, David Martens, Joon Hur, and Bart Baesens.
"New Insights into Churn Prediction in the Telecommunication Sector: A
Profit Driven Data Mining Approach." *European Journal of Operational
Research* 218, no. 1 (2012): 211–229. Evaluating churn models by profit at
the depth of list that will be acted on.

Blattberg, Robert C., Byung-Do Kim, and Scott A. Neslin. *Database Marketing:
Analyzing and Managing Customers.* Springer, 2008. The reference text for
the surrounding practice.
