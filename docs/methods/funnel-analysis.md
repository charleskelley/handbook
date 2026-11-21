---
title: "Funnel analysis"
type: method
depth: guide
owner: ds-lead
audience: [ds, analyst, product]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [descriptive, customers, conversion]
sources:
  - "Fader and Toms, The Customer Centricity Playbook, Wharton School Press, 2018"
  - "Blattberg, Kim, and Neslin, Database Marketing: Analyzing and Managing Customers, Springer, 2008"
---

# Funnel analysis

A count of how many customers get from each step of a path to the next, and
how long it takes them. It is where to look once a
[customer-base audit](customer-base-audit.md) has said that acquisition,
retention, or development is the problem and the next question is where along
the way customers are lost.

## What it is

A descriptive analysis of an ordered path: a set of steps a customer is
meant to pass through, such as visit, sign up, first purchase, second
purchase. For each step it reports how many units reached it, the share of
those at the step before who went on, and how long that took. The steepest
drop, or the slowest step, is where attention goes next. The arithmetic is
counting. The difficulty is all in the definitions: what a step is, who is
counted, over what time, and whether the people at one step are the same
people who were at the step before.

## When it is the right choice

- The audit has pointed at a stage of the customer's life and the question is
  where within it customers stop: before a first purchase, between the first
  and the second, or before they widen what they buy.
- A process has ordered steps that are each recorded: a checkout, an
  application, an onboarding sequence, a renewal.
- Two groups are to be compared step by step: channels, devices, cohorts,
  plans.
- A team is choosing which step to work on and needs the size of the loss at
  each.

## When it is not

- **There is no order.** Customers who reach the same end by many routes do
  not form a funnel. Forcing them into one loses those who took another
  route. Describe the routes first, by counting the most common sequences of
  events customers actually followed.
- **The steps are not recorded.** A step with no reliable event is a guess.
  Say so, or leave it out.
- **The question is whether a change to a step worked.** A funnel before and
  after a change is a before-and-after comparison, with everything that
  implies. Use an [experiment](experiments-and-lift-tests.md).
- **The loss is not at a step.** Customers who complete every step and then
  drift away are a retention question. See
  [survival analysis](survival-analysis.md).

## The parts of a funnel

| Part | Definition | The choices to make |
|---|---|---|
| Unit | What is counted | Customer, account, visitor, session, or order. A session funnel and a customer funnel of the same data give different rates |
| Entry | What puts a unit at the top | A first visit, a sign-up, a first purchase |
| Step | An event the unit must have to be counted there | Which event, and whether it must come after the step before |
| Step conversion | Units reaching a step ÷ units at the step before | |
| Overall conversion | Units reaching the last step ÷ units at the entry | The product of the step conversions, when every step is measured on the same units |
| Drop-off | 1 − step conversion | |
| Time to convert | Time from one step to the next, for those who took it | Its distribution, not only its average |
| Window | How long a unit is given to take a step, counted from the step before | Fixed for everyone, and stated for each step |

## From the audit to a funnel

The audit says what is happening to the customer base. It does not say where
along the customer's path the cause sits. The three levers a business has on
its customers are usually named acquisition, retention, and development, and
each has a funnel.

| The audit shows | Lever | The funnel to build | What to look for |
|---|---|---|---|
| Fewer customers acquired each period, or the cost of each rising | Acquisition | From first contact to first purchase: visit, sign-up or registration, first basket, first order. By channel | The step with the largest loss, and whether it is the same in every channel |
| Newer cohorts worth less at the same age | Acquisition | The same, split by channel and by the offer that brought the customer | Whether the channels that grew are the ones whose customers are worth least |
| A large share of each cohort never buys twice | Retention | From first purchase to second, with the steps between: delivery, first use, a return, a contact with service, the first reminder | What the customers who came back did between the two purchases that the others did not |
| Newer cohorts less active at the same age than older ones were | Retention | The repeat-purchase ladder: first, second, third, fourth purchase, each within a stated time | Whether the loss is at the second purchase or later |
| Value concentrated in a few customers and spend per customer flat | Development | From one category to two, from occasional purchases to a subscription, from the basic tier to a higher one | How many customers are eligible for the next step at all, and how many of those take it |

The last column describes, it does not explain. A difference between
customers who went on and customers who did not is a place to look and a
hypothesis to test, not a finding about cause.

## Common approaches

The rows are not all alternatives to one another. A funnel makes three
separate choices: who is counted, a snapshot or a cohort; the order rule,
strict or open; and the time rule, a window or a time-to-event analysis.

| Approach | What it needs | What it rests on | Main weakness |
|---|---|---|---|
| Snapshot funnel: count the units at each step in a period | An event count per step | That the units at each step in the period are comparable | The people at step three this month are mostly not this month's entrants. Rates can exceed 100% and move with volume at the top |
| Cohort funnel: follow the units that entered in a period through the steps | Events tied to a unit identifier, over time | A unit identifier that persists across steps | Recent cohorts have not had time to finish. Needs a window |
| Strict funnel: each step must follow the one before | Ordered, timestamped events | That the order is the real path | Undercounts units who skipped a step or did steps out of order |
| Open funnel: a unit counts at a step whenever it has the event | Event flags | That order does not matter to the question | A later step can have more units than an earlier one |
| Windowed funnel: each step must be taken within a set time of the one before | Timestamps, a chosen window | That the window covers most of those who will ever convert | A short window reads slow converters as lost |
| Time-to-convert analysis: the distribution of time between steps | Timestamps, and the date the data was taken | The methods on the [survival analysis](survival-analysis.md) page | More work, and harder to show on one chart |

The default here is a cohort funnel with a stated window, with a strict
order where the process has one. A snapshot funnel is acceptable only for a
process that completes within one visit, where the units at the bottom
really are those who were at the top.

### Time, windows, and customers who have not finished

A customer who entered last week has had a week to convert. Counting them as
lost makes every recent cohort look worse than older ones. Two ways to handle
it: give every unit the same window and leave out units that have not yet had
the windows of every step, added together, or treat the time to each step as time-to-event data with
censoring, which uses everyone. The second is the same problem as time to
second purchase on the customer-base audit page.

## Reading a result you did not produce

Questions to ask of a funnel chart from a tool, a vendor, or another team.

- **Are the people at each step the same people?** Ask whether it is a cohort
  funnel or a count of events in a period. If the second, the step rates are
  ratios of unrelated counts.
- **What is counted?** Sessions, visitors, customers, or orders. A customer
  who visits five times before buying is one conversion out of one customer
  and one out of five sessions.
- **How is a customer recognised across steps?** Early steps are often
  anonymous and later ones signed in. If the two are not joined, the top of
  the funnel is inflated with repeat visitors counted as new.
- **What is the window, and have the recent entrants had it?** A fall in the
  last few periods is often only customers who have not finished.
- **Did a step's definition or its tracking change?** A new page, a new tag,
  or a consent banner can move a step's count with no change in behaviour.
  Check the dataset's page for a recorded insight.
- **What is at the top?** Overall conversion falls when the top is widened
  with visitors who were never likely to buy. More traffic with lower
  conversion can be more orders. Read the number who reach the bottom beside
  the rate.
- **Is the comparison of groups a comparison of mix?** A funnel that worsened
  overall may have improved in every channel while the channels' shares
  shifted. See
  [decomposing a change](decomposing-a-change.md#a-rate-rate-and-mix).
- **Is a difference between those who went on and those who did not being
  read as a cause?** Customers who used a feature before buying may have been
  the keener customers to begin with. That is a claim to test.
- **Does fixing the worst step pay?** A step that loses the most units may
  lose the ones who would never have bought. Removing friction at one step
  often moves the loss to the next. Only the count reaching the end, measured
  with a control group, settles it.

## Where it applies to our data

*Add: the paths the team reports as funnels, each with its unit, entry,
steps, order rule, and window.* Why: two funnels of the same path with
different definitions cannot be compared.

*Add: the event datasets each step is read from, linked to their pages under
Data, with how a customer is recognised across anonymous and signed-in
steps.* Why: the join between the two is where most funnels go wrong.

*Add: which of acquisition, retention, and development the latest
[customer-base audit report](../business/customer-base-audit.md) pointed at,
and the funnel built in answer.* Why: a funnel is built to answer a question
the audit raised.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Further reading

Fader, Peter, and Sarah Toms. *The Customer Centricity Playbook: Implement a
Winning Strategy Driven by Customer Lifetime Value.* Wharton School Press,
2018. Organised around acquisition, retention, and development as the three
levers. Read it for what each lever is for before measuring any of them.

Blattberg, Robert C., Byung-Do Kim, and Scott A. Neslin. *Database Marketing:
Analyzing and Managing Customers.* Springer, 2008. The reference for the
analysis behind each lever, from acquiring customers to managing them
afterwards.

Croll, Alistair, and Benjamin Yoskovitz. *Lean Analytics: Use Data to Build a
Better Startup Faster.* O'Reilly, 2013. A practitioner's account of which
funnel steps matter in which kind of business. Useful for vocabulary a
product or marketing partner will use.

Hoban, Paul R., and Randolph E. Bucklin. "Effects of Internet Display
Advertising in the Purchase Funnel: Model-Based Insights from a Randomized
Field Experiment." *Journal of Marketing Research* 52, no. 3 (2015):
375–393. An example of measuring an effect at each stage of a funnel with an
experiment, and of the effect differing by stage.

Singer, Judith D., and John B. Willett. *Applied Longitudinal Data Analysis:
Modeling Change and Event Occurrence.* Oxford University Press, 2003. For
time to convert, handled as time-to-event data.
