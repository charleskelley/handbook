---
title: "Survival analysis"
type: method
depth: build
owner: ds-lead
audience: [ds, analyst, product]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [descriptive, customers, retention, time-to-event]
sources:
  - "Kaplan and Meier, Nonparametric Estimation from Incomplete Observations, Journal of the American Statistical Association 53(282), 1958"
  - "Singer and Willett, Applied Longitudinal Data Analysis, Oxford University Press, 2003"
  - "Fader and Hardie, How to Project Customer Retention, Journal of Interactive Marketing 21(1), 2007"
---

# Survival analysis

The analysis of how long it takes for something to happen, when for many of
the subjects it has not happened yet. In this business the something is
usually a customer leaving, and the method is how retention is measured
without being fooled by the customers who are still here.

## What it is

A set of methods for time-to-event data: the time from a starting point, such
as a first purchase or the start of a subscription, to an event, such as a
cancellation or a second purchase. What sets it apart is censoring. At the
date the data was taken, some subjects have not had the event, and all that
is known is that their time is at least as long as they have been observed.
Survival analysis uses that partial information correctly, where an average
or a simple proportion cannot. Its basic outputs are the survival curve, the
share of subjects who have not yet had the event at each time since the
start, and the hazard, the rate at which those still at risk have it. This
page covers the descriptive methods. Models that predict the time for one
customer are introduced at the end and belong to
[churn and propensity models](churn-and-propensity.md).

## When it is the right choice

- The question is how long until something happens, or what share has had it
  happen by a given time: retention by tenure, time to second purchase, time
  from sign-up to first order, time from a complaint to a cancellation.
- Subjects started at different dates, so they have been observed for
  different lengths of time.
- Retention is to be compared between cohorts, plans, or channels at the same
  tenure.
- A [customer lifetime value](customer-lifetime-value.md) is being built for a
  subscription business, which needs the survival curve as an input.

## When it is not

- **Everyone has been observed for the whole period of interest.** If every
  subject has at least twelve months of history and the question is twelve
  month retention, a plain proportion is the same answer with less work.
- **The event cannot be dated.** Where customers buy without a contract, they
  do not announce that they have left. An event has to be defined first: see
  [businesses without contracts](#businesses-without-contracts).
- **The question is why.** A difference between two curves says that two
  groups differ. It does not say the plan, the channel, or the campaign
  caused the difference. See
  [directional versus causal](directional-versus-causal.md).
- **Very few events.** A curve built on a handful of events is mostly noise,
  and its right-hand end always is.

## Setting up the clock

Four things are settled before anything is computed, and stated on every
output.

| Choice | What it is | Typical options |
|---|---|---|
| Origin | The moment a subject's clock starts | First purchase, start of subscription, sign-up, end of a trial |
| Event | What ends the clock | Cancellation, second purchase, first order, a defined lapse |
| Time scale | The unit and what it measures | Days or billing periods since the origin. Tenure, not calendar date |
| End of observation | The last date on which an event could have been seen | The date the data was taken, less any delay in recording |

The time scale is tenure. Two customers who joined in different years are
compared at the same number of months since each joined. Calendar time enters
only as the reason some customers have been observed for longer than others.

## Censoring and truncation

A subject who has not had the event by the end of observation is **censored**:
their time to the event is unknown, but known to be longer than the time
observed. Censoring is information, not missing data. A customer who has
stayed 30 months so far says a great deal about retention at 12 months.

Three other cases come up in customer data:

- **Left truncation.** The data begins on some date, and customers who
  started before it are in the data only if they were still there on that
  date. Those who started early and left early are missing, so the ones seen
  are survivors. Either leave out customers who started before the data, or
  use a method that lets a subject enter the risk set late, at the tenure
  they had reached when the data began.
- **Other reasons for leaving observation.** A customer may stop being
  observable for a reason that is not the event, such as a move out of the
  market served. They are censored at that date.
- **Informative censoring.** The method assumes that a censored subject is,
  from then on, like the subjects still observed at the same tenure. That
  fails if subjects are removed from observation for a reason tied to the
  event, for example accounts closed for non-payment and treated as censored
  when the event is voluntary cancellation.

## The survival curve and the hazard

| Quantity | Definition |
|---|---|
| At risk at time *t* | Subjects who have neither had the event nor been censored before *t* |
| Hazard at *t* | Events at *t* ÷ at risk at *t*: the chance of the event at *t* for a subject who has reached *t* |
| Survival at *t* | The share of subjects who have not had the event by *t* |
| Median survival time | The first time at which survival is 50% or lower. Not defined if the curve never falls that far |
| Retention rate in a period | Survival at the end of the period ÷ survival at its start, which is 1 less the hazard |

The hazard is the more revealing of the two. Survival always falls, so every
curve looks like a decline. The hazard shows when subjects are most likely to
leave: commonly high at the start, at the end of a trial or a first term, and
at each renewal, and lower for those who have stayed long.

### The Kaplan-Meier estimate

The standard estimate of the survival curve. Order the event times. At each
one, survival is multiplied by the share of those at risk who did not have
the event:

survival after an event time = survival before it × (1 − events ÷ at risk)

A censored subject counts in the at-risk number for every event time up to
the time they were censored, and then drops out of it. That is how their
partial information is used. The curve is a staircase that steps down at each
event time and is flat between.

![A step curve of the share still subscribed against months since the subscription started. It starts at 100%, steps down to 90% at month 1, to 70% at month 2, and to 56% at month 5. Ticks at months 3, 4, and 6 mark customers censored.](../assets/survival-curve-light.svg#only-light)
![A step curve of the share still subscribed against months since the subscription started. It starts at 100%, steps down to 90% at month 1, to 70% at month 2, and to 56% at month 5. Ticks at months 3, 4, and 6 mark customers censored.](../assets/survival-curve-dark.svg#only-dark)

*The curve for the [worked example](#worked-examples) below.*

Where time comes in periods, such as monthly billing, the same calculation
done period by period is called a life table: for each period, the number
entering it, the events, the number censored, the hazard, and survival to the
end of it.

An interval around the curve is usually computed with Greenwood's formula,
which every statistics package offers. It gives the variance of survival at a
time as survival squared × the sum, over the event times up to then, of
events ÷ (at risk × (at risk − events)). The interval widens to the right as
the number at risk falls.

### Comparing groups

Draw one curve per group on the same axes, with the number at risk under the
plot at a few tenures. Read the difference in survival at fixed tenures, such
as 3, 12, and 24 months, and the difference in the hazards, which shows when
the groups part. The log-rank test is the standard test of whether two curves
differ by more than chance: at each event time it compares the events seen in
each group with the number expected if the groups shared one hazard. With
large customer counts it finds even small differences significant, so the
size of the difference matters more than the test: see [stating uncertainty](stating-uncertainty.md).

### More than one way to leave

A subscriber can cancel, or be closed for non-payment, or move away. These
are competing risks: one of them happening removes the chance of the others.
Treating the other ways of leaving as censoring answers a hypothetical
question, what cancellation would look like if nobody could leave any other
way. The share of customers who have left by each route, by tenure, is the
cumulative incidence of each, and the routes add up to all who have left.
To compute it, take each period in turn: the share leaving by a route in the
period is survival from all routes at the start of the period × that route's
events ÷ the number at risk. Add those shares up over the periods. Report it
when the routes call for different actions.

## Businesses without contracts

Where customers subscribe, the event is observed: there is a cancellation
date. Where they buy when they choose, nobody leaves on a date. A customer
who has not bought for a year may be gone or may be between purchases. Three
ways to work with that:

- **Analyse an event that is observed.** Time from first purchase to second,
  and from each purchase to the next, are true time-to-event data with true
  censoring. The [customer-base audit](customer-base-audit.md) uses them.
- **Define a lapse.** Call a customer lapsed after a stated time with no
  purchase, chosen from the distribution of gaps between purchases so that
  few customers who go that long come back: the
  [churn page](churn-and-propensity.md#worked-examples) shows the table to
  choose it from. Set the end of observation earlier than the end of the data
  by the stated time. A customer with no purchase for the stated time after
  their last purchase before that date has the event, dated at that last
  purchase. Every other customer is censored at that date.
- **Model it.** The models on the
  [customer lifetime value](customer-lifetime-value.md) page treat leaving as
  unobserved and estimate the chance that each customer is still active.

## From curves to models

The curve describes a group. Three kinds of model extend it, and each is a
subject of its own.

- **Discrete-time hazard models.** Lay the data out with one row per subject
  and period at risk, and model the event in each row with
  [logistic regression](regression.md). It is the simplest way to bring in
  customer characteristics and values that change over time, and it suits
  data that comes in billing periods.
- **Cox regression.** Models how characteristics multiply the hazard,
  without assuming a shape for the hazard over time. The standard tool for
  continuous time.
- **Parametric and projection models.** Assume a shape for the curve so that
  it can be extended beyond the data. Fader and Hardie's shifted beta
  geometric model projects a cohort's retention from a few periods of
  observation, and explains why a cohort's retention rate rises with tenure:
  the customers most likely to leave do so first.

## Building the outputs

Everything is built from one table.

Subject table

:   One row per subject. Columns: subject identifier, origin date, end date,
    event flag, and any grouping columns such as cohort, plan, or channel.
    The end date is the event date if the event was seen and the end of
    observation otherwise. The duration is the end date less the origin
    date, in the stated unit. Grouping columns hold values as of the origin,
    never values that were set later.

For a life table or a discrete-time model the subject table is expanded.

Subject-period table

:   One row per subject and period at risk, from the first period after the
    origin to the period of the event or of censoring. Columns: subject
    identifier, period number since the origin, and an event flag that is 1
    only in the row where the event happened. Period 1 is the first period
    after the origin. A subject censored part-way through a period has no row
    for that period.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| Life table | Period since the origin | At risk, events, censored, hazard, survival, interval | Table |
| Survival curve | Event times | Survival, interval | Step line, one per group, with the number at risk beneath |
| Hazard by tenure | Period since the origin | Hazard | Bars or a line |
| Survival at fixed tenures | Group or cohort | Survival at each chosen tenure, with the number at risk there | Table |
| Median time | Group or cohort | Median, or a note that it has not been reached | Table |
| Cumulative incidence | Period since the origin | Share that has left by each route | Stacked lines |

Defaults, where nothing about the business decides otherwise:

| Choice | Default | Why |
|---|---|---|
| Origin | The first billed period or first purchase, not sign-up | A trial that never converts is an acquisition question |
| Unit | The billing period for subscriptions, days otherwise | The event can only happen where the business lets it |
| Left-truncated customers | Left out, and counted in a note | Late entry is easy to get wrong |
| Where the curve stops | The last tenure with a stated minimum number at risk | The tail is noise |
| Comparison | Survival at fixed tenures, with intervals | A whole curve invites reading its tail |

## Checks

Run these before reading any output. A failure is a fault in the tables, not a
finding.

- No duration is negative, and none is longer than the span of the data.
- Events plus censored subjects equal the number of subjects.
- Every censored subject's end date is the end of observation, or a stated
  earlier date with a stated reason.
- Survival starts at 100% and never rises. The number at risk never rises,
  unless late entry is in use.
- Every hazard in a life table, which is a share per period, is between 0 and
  1.
- The number at risk in a period equals the number at risk in the period
  before, less its events and its censored.
- The routes in a cumulative incidence table add up to 100% less the survival
  from all routes together.
- For a group with no censoring before some tenure, survival at that tenure
  equals the plain proportion.

## Pitfalls

- **Leaving out the customers who are still here.** Averaging the lifetime of
  customers who have left describes only the ones who left early. The figure
  grows every time the data is extended.
- **Counting censored customers as kept, or leaving them out.** Both turn
  "not yet" into an answer. The worked example shows the two wrong numbers
  on either side of the right one. Counting them as lost is worse still.
- **Groups defined by what happened later.** "Customers who used the app
  live longer" compares customers who survived long enough to use the app
  with everyone else. This is immortal time bias. A group must be defined by
  what was known at the origin, or the characteristic must be handled as one
  that changes over time.
- **Reading the tail.** The last steps of a curve rest on a few subjects.
  One event there moves the curve a long way.
- **Mixing cohorts with different clocks.** A change in price or product
  affects all tenures at one calendar date. In tenure time it is smeared
  across the curve. Draw curves by cohort to see it.
- **A changed definition of the event.** A new cancellation flow or billing
  system can move the recorded date of the event with no change in behaviour.
  Record it as an insight on the dataset's page.
- **Customers who come back.** A customer who cancels and rejoins is either
  one subject with a gap or two subjects. Decide which, and say so.
- **A retention rate for the whole base.** It is an average over customers of
  different tenures and rises as the base ages. Read retention by tenure.

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data. Ten customers subscribed, and the data was taken at
different tenures for each. Four cancelled, at months 1, 2, 2, and 5. Six had
not cancelled when last observed: one at month 3, one at month 4, and four at
month 6.

| Month | At risk | Cancelled | Censored | Hazard | Survival |
|---|---|---|---|---|---|
| 1 | 10 | 1 | 0 | 1 ÷ 10 = 10% | 100% × 90% = 90% |
| 2 | 9 | 2 | 0 | 2 ÷ 9 = 22% | 90% × 78% = 70% |
| 3 | 7 | 0 | 1 | 0% | 70% |
| 4 | 6 | 0 | 1 | 0% | 70% |
| 5 | 5 | 1 | 0 | 1 ÷ 5 = 20% | 70% × 80% = 56% |
| 6 | 4 | 0 | 4 | 0% | 56% |

Retention to month 6 is 56%. Two shortcuts give other answers:

- Counting the six censored customers as kept gives 6 ÷ 10 = 60%. It treats
  the customers last seen at months 3 and 4 as though they were known to
  reach month 6.
- Dropping those two, because their outcome at month 6 is unknown, gives 4 ÷
  8 = 50%. It throws away the months they did stay.

The estimate keeps both customers in the at-risk number for as long as they
were observed, and so falls between. The median time to cancel has not been
reached, because the curve has not fallen to 50%.

## Where it applies to our data

*Add: the events the team analyses this way, with the origin, the event, the
unit, and the end of observation chosen for each.* Why: two retention curves
with different clocks cannot be compared.

*Add: the datasets that hold each origin and event date, linked to their
pages under Data, with how late an event can be recorded after it happens.*
Why: the end of observation has to be set earlier than the date the data was
taken by at least that delay.

*Add: for a business without contracts, the definition of a lapse and the
evidence for the time chosen.* Why: every figure downstream depends on it.

*Add: the date the data begins and how customers who started before it are
handled.* Why: left truncation is invisible in the output.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Kaplan, E. L., and Paul Meier. "Nonparametric Estimation from Incomplete
Observations." *Journal of the American Statistical Association* 53, no. 282
(1958): 457–481. The estimate of the survival curve used on this page.

Singer, Judith D., and John B. Willett. *Applied Longitudinal Data Analysis:
Modeling Change and Event Occurrence.* Oxford University Press, 2003. The
second half is the clearest introduction to discrete-time survival analysis,
the life table, and the subject-period layout. Start here.

Klein, John P., and Melvin L. Moeschberger. *Survival Analysis: Techniques
for Censored and Truncated Data.* Springer. The reference for censoring, left
truncation, and competing risks.

Cox, D. R. "Regression Models and Life-Tables." *Journal of the Royal
Statistical Society, Series B* 34, no. 2 (1972): 187–202. The proportional
hazards model.

Fine, Jason P., and Robert J. Gray. "A Proportional Hazards Model for the
Subdistribution of a Competing Risk." *Journal of the American Statistical
Association* 94, no. 446 (1999): 496–509. Models for cumulative incidence
when there is more than one way to leave.

Fader, Peter S., and Bruce G. S. Hardie. "How to Project Customer Retention."
*Journal of Interactive Marketing* 21, no. 1 (2007): 76–90. Why retention
rates rise with tenure, and a simple model for projecting a cohort's curve.
