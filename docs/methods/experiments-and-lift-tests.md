---
title: "Experiments and lift tests"
type: method
depth: build
owner: ds-lead
audience: [ds, analyst, product]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [causal, experimentation, marketing]
sources:
  - "Kohavi, Tang, and Xu, Trustworthy Online Controlled Experiments, Cambridge University Press, 2020"
  - "Gerber and Green, Field Experiments: Design, Analysis, and Interpretation, W. W. Norton, 2012"
  - "Lehr, Sixteen S-squared over D-squared, Statistics in Medicine 11(8), 1992"
---

# Experiments and lift tests

How to find out what an action changed by withholding it from a group chosen
at random. It is the only design in which the comparison group can be trusted
without argument, and the standard against which every other estimate of
impact on this site is judged.

## What it is

A randomized experiment assigns units, such as customers, sessions, or
stores, to receive an action or not by a chance mechanism that nothing else
influences. Because chance decided, the two groups are alike on average in
every respect, measured or not, and a difference in their outcomes afterwards
is the effect of the action plus sampling noise. The noise can be quantified.
A **lift test** is the marketing name for the same thing: a campaign is sent
to most of an audience and withheld from a random holdout, and the
difference is the campaign's lift. An **A/B test** is the same thing on a
website or in a product. This page covers the design, the sample size, the
analysis, and how to read a lift number produced by a tool.

## When it is the right choice

- The business controls who gets the action and can withhold it from some.
- Money or effort will be moved on the size of the effect.
- The action will be repeated, so the cost of the test is spread over many
  later decisions.
- Two versions are being compared and neither is known to be better.
- An observational estimate is in dispute and a test would end the dispute.

## When it is not

- **The action cannot be withheld or assigned.** A price set in law, a
  rebrand, a change every customer must get on the same day. See
  [measuring impact without an experiment](measuring-impact-without-an-experiment.md).
- **There are too few units.** Twelve regions cannot be split into two groups
  that chance makes alike. See [matching](matching.md) for designs that pair
  units first, and [synthetic control](synthetic-control.md).
- **Treated units affect untreated ones.** Sellers and buyers in a
  marketplace, staff sharing a rota, customers in one household. Randomize a
  larger unit that contains the spillover, or accept that the estimate is
  biased.
- **The effect is too small to detect at any affordable size.** Work out the
  sample size first. If it exceeds the customer base, the test cannot answer
  the question, and running it anyway produces noise that will be read as a
  finding.
- **The outcome arrives too late.** An effect on retention over two years
  cannot be read in a four-week test. Agree a nearer measure in advance, or
  keep a long-running holdout.

## Assumptions

| Assumption | What it means | How it is checked |
|---|---|---|
| Assignment was random and happened as designed | Nothing but chance decided who was in which group | The group sizes match the designed split. The groups were alike before the test on the outcome and on a few known characteristics |
| No interference | One unit's assignment does not change another unit's outcome | By the choice of unit. Cannot be checked from the result |
| The same measurement in both groups | Outcomes are recorded identically whatever the group | Outcomes come from the business's own records for everyone, not from the tool that delivered the action |
| Nobody was removed after assignment | Every unit assigned is analysed in the group it was assigned to | The analysed counts equal the assigned counts |
| The test is like the rollout | The units, the period, and the action tested are those the decision is about | Judgment. Stated in the write-up |

## Designing a test

A test is designed, and the design is written down, before any unit is
assigned.

### The question

One action, one comparison, one primary outcome, one decision.

- **The primary outcome** is the measure the decision turns on, defined
  exactly: which events, over what window, from which dataset. For a
  marketing action it is total purchases or margin per customer assigned,
  across all channels and products, not responses to the campaign.
- **Guardrail outcomes** are measures the action must not harm: returns,
  unsubscribes, margin, complaints, page speed.
- **The smallest effect that matters** is the size below which the action
  would not be rolled out. It sets the sample size.

### The unit

The unit of randomization is what is assigned: a customer, a household, a
session, a store, a region. Choose the smallest unit that contains the
action's whole effect.

| Unit | Use when | Cost |
|---|---|---|
| Customer | The action is addressed to a person and its effect stays with them | Needs a stable identifier, and misses shared households |
| Session or visit | Customers cannot be recognised | A returning customer can see both versions |
| Store, region, or market | The action cannot be targeted to individuals, such as a broadcast advertisement or a store layout, or individuals affect one another | Few units, so far less precision. See [matching](matching.md) |
| Time period, alternating, known as a switchback test | One system serves everyone, such as a pricing or dispatch rule | Effects carry over between periods |

The analysis is done at the unit that was randomized. A test randomized by
store has as many observations as it has stores, however many customers
shopped.

### The groups

- **Treatment** gets the action. **Control** gets what would have happened
  otherwise, which is usually business as usual and not nothing.
- **A holdout** is a control group for a campaign: customers who qualified
  and were not sent it.
- Both groups are drawn from the same population by the same rule at the
  same time. A control group taken from customers who did not qualify, did
  not open, or were not reached is not a control group.
- The control does not need to be half. Precision is governed by the smaller
  group, so a small holdout costs sample size, and the cost is known in
  advance.

### Assignment

Assignment is by a random number or by a hash of the unit's identifier with
a value unique to the test, so that the same customer is not always in the
control group of every test. It is fixed before anyone is exposed, recorded
for every unit with its time, and never changed. Do not assign by anything
that could relate to the outcome: alphabetical order, region, sign-up date,
or whoever the sales team had time to call.

### Sample size and duration

The number of units needed in each group, for a test that will detect a
difference of *d* four times in five at the usual 5% threshold, is close to

16 × variance of the outcome ÷ *d* squared

For a conversion rate *p*, the variance is *p* × (1 − *p*).

| Baseline rate | Difference to detect | Units in each group |
|---|---|---|
| 2% | 0.2 points | 78,400 |
| 5% | 0.5 points | 30,400 |
| 5% | 0.25 points | 121,600 |
| 20% | 2 points | 6,400 |
| 20% | 1 point | 25,600 |

Halving the difference to detect quadruples the sample. Outcomes measured in
money vary far more than yes-or-no outcomes and need more. With groups of
unequal size, it is the harmonic mean of the two sizes that must reach the
number in the table: 2 ÷ (1 ÷ the first size + 1 ÷ the second). The smaller
group dominates.

The weeks needed are the units needed ÷ the eligible units that arrive each
week. Run for whole weeks, for at least one usual gap between purchases, and
for the length decided in advance. A test of a novelty needs long enough for the
novelty to wear off.

## Analysing a test

- **Compare everyone assigned, as assigned.** Every unit assigned to
  treatment is counted in treatment, whether or not it opened the email, saw
  the page, or redeemed the offer. This is the intent-to-treat comparison,
  and it is the only one randomization protects. Comparing customers who
  opened with the control group compares a self-selected group with a random
  one.
- **Report the difference and its interval,** in the units of the decision.
  For an outcome that is an amount, such as margin per customer, the
  standard error of the difference is the square root of (the variance in
  treatment ÷ its units + the variance in control ÷ its units). See
  [stating uncertainty](stating-uncertainty.md).
- **The effect on those actually reached** is a separate question. Where the
  action cannot affect a customer it did not reach, it is the difference
  above ÷ the share of the treatment group that was reached. It is never the
  reached customers compared with the control.

| Quantity | Definition |
|---|---|
| Difference | Outcome per unit in treatment − outcome per unit in control |
| Lift | Difference ÷ outcome per unit in control |
| Incremental total | Difference × number of units treated |
| Net value | Incremental margin − the cost of the action, including discounts given to those who would have bought anyway |

- **Use the pre-period to sharpen the estimate.** Adjusting each unit's
  outcome for its own outcome before the test removes variation that has
  nothing to do with the test, and can cut the sample needed substantially.
  It does not bias a randomized comparison. The usual method is called
  CUPED: regress the outcome on the pre-period measure across all units,
  subtract from each unit's outcome that slope × the unit's pre-period
  measure less its overall mean, and compare the adjusted outcomes. A
  regression of the outcome on the group and the pre-period measure gives
  the same answer.
- **Treat segments as exploration.** The test was sized for the whole
  population. A difference between segments is a hypothesis for the next
  test.

### Kinds of lift test

| Kind | The control | Suits | Watch for |
|---|---|---|---|
| A/B test | Users shown the current version | Changes to a site, an app, a message | Returning users, and stopping early |
| Campaign holdout | Qualified customers not sent the campaign | Email, direct mail, app messages, offers | The holdout being removed from other campaigns too |
| Universal holdout | A fixed random group that gets no marketing of a given kind for a quarter or a year | The combined effect of all campaigns, which do not add up one by one | Keeping it truly untouched, and rotating it |
| Geographic test | Regions where the activity is withheld or reduced | Media that cannot be targeted to a person | Few units. Pair or match the regions first |
| Placebo or ghost-ad test | Users who would have been shown the advertisement and were shown something neutral, or flagged without being shown anything | Paid digital advertising, where only some of the treatment group is ever reached | Needs the advertising platform's cooperation |

## Reading a result you did not produce

Marketing tools report lift as a built-in number. When that number is large
and the business's own figures have not moved, one or more of the following
is the reason. Work down the list.

**Is it a comparison with a random group at all?**

- Ask how the comparison group was formed. Customers who did not open, did
  not click, were not reachable, or were suppressed by a rule are not a
  control group. Neither is last year, or a "similar audience" chosen by the
  tool.
- Ask whether the split was made before sending, and whether both groups
  qualified under the same rule.
- Ask whether anyone was removed afterwards: bounced addresses, opt-outs,
  customers who did not see the message. Removal from one group only breaks
  the comparison.

**Is it measuring the outcome the business counts?**

- A tool often counts responses it can see: clicks, redemptions of the
  campaign's code, purchases within its own channel. The business counts all
  purchases. A campaign that moves a purchase from the shop to the app, or
  from full price to the offer, shows a response and no gain. Measure total
  margin per customer assigned, in both groups, from the business's records.
- "Attributed" orders are orders by people who were sent the campaign. Most
  of them would have ordered anyway. Attribution is not lift.
- Check the window. An offer can pull a purchase forward from next month
  into this one. Lift measured over the offer's week is then followed by an
  equal fall that nobody measured. Extend the window past the customer's
  usual gap between purchases.
- Check what was given away. The discount went to every buyer in the treated
  group, including the ones who would have bought without it. Net value is
  the margin on the extra purchases less the discount on all of them.

**Is the number as sure as it looks?**

- Ask for the interval. A holdout of a few thousand gives a wide one, and a
  lift of 10% can be consistent with zero.
- Ask how many campaigns were measured. The best of twenty was partly lucky,
  and the average across all twenty is the better guide.
- Ask whether the reported figure is a percentage on a small base. A lift of
  40% in redemptions of one product among a few thousand customers is a
  small number of orders.

**Could a real lift be invisible in the business total?**

- Multiply it out: the lift × the share of the business's sales that come
  from the customers the campaign reached. A true 10% lift among customers
  who make a twentieth of the sales moves the business total by half a
  percent, which is inside its normal variation from month to month. Real and invisible is the usual
  case, and is not a reason to disbelieve the test.
- Lifts from separate campaigns do not add. Two campaigns that each reach
  the same customer can each be credited with the same purchase. Only a
  universal holdout measures the total.
- The control group is rarely untouched. If it received the business's other
  marketing, the test measured this campaign's addition to that, which is the
  right question but a smaller number than the campaign's effect in
  isolation.

**Does it last?**

- A short test of an offer measures the response to the offer, not what
  repeated offers do to what customers will pay. That needs a long-running
  holdout.

When the tool's method cannot be established, the remedy is a holdout the
team sets up itself: a random group withheld before the send, outcomes from
the business's own records. It is the worked example below.

## Building the outputs

Design record

:   Written before assignment and not changed after. Fields: the decision,
    the action and the control condition, the unit, the eligible population,
    the split, the primary outcome with its exact definition and window, the
    guardrails, the smallest effect that matters, the sample size and how it
    was calculated, the start and end dates, and what will be done for each
    possible result.

Assignment table

:   One row per unit per test. Columns: unit identifier, test identifier,
    group, time of assignment. Written at assignment and never updated.

Outcome table

:   One row per unit assigned. Columns: unit identifier, group, the outcome
    in the test window, the same measure in a window before the test, and
    the guardrail measures. Built from the business's own records. Includes
    every assigned unit, with zero for units with no activity.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| Sample size | Scenario | Baseline, smallest effect, units needed in each group, weeks needed | Table, in the design record |
| Assignment check | Group | Units designed, units assigned, the measure before the test | Table |
| Result | Outcome, primary first and then guardrails | Control, treatment, difference, interval, lift, incremental total | Table |
| Value | Line | Incremental margin, cost of the action, net, each with its interval | Table |
| Outcome over time | Day or week | The cumulative difference and its interval | Line. For reading stability, not for deciding when to stop |

Defaults, where nothing about the business decides otherwise:

| Choice | Default | Why |
|---|---|---|
| Unit | Customer | The smallest unit that holds the effect of most actions |
| Primary outcome | Margin per customer assigned, over all channels | It is what the business keeps |
| Window | The action's duration plus one usual gap between purchases | To catch purchases pulled forward |
| Threshold and power | 5%, two-sided, and 80% | The convention. Change it only in the design record |
| Analysis | Intent to treat, with adjustment for the pre-period measure | Protected by randomization, and more precise |
| Stopping | At the planned end | Stopping on a good day inflates false findings |

## Checks

Run these before reading the result. A failure means the test is not a valid
comparison, whatever it shows.

- **The split is as designed.** Compare the assigned counts with the designed
  ratio by a chi-squared test. A mismatch means units were lost or added on
  one side, and the result cannot be trusted until the cause is found.
- **The groups were alike beforehand.** The primary outcome measured over a
  window before the test differs between the groups by no more than chance.
- **Every assigned unit is in the outcome table, once,** in the group it was
  assigned to.
- **No unit was assigned after it was exposed,** and none appears in both
  groups.
- **The outcome is defined as in the design record,** and is read from the
  same source for both groups.
- **The control group did not get the action.** Check delivery logs.
- **The guardrails are reported** whatever they show.

## Pitfalls

- **Peeking.** Checking the result daily and stopping when it first crosses
  the threshold produces a significant result far more often than 5% of the
  time when there is no effect. Fix the length, or use a method designed for
  continuous monitoring, known as sequential testing.
- **Comparing responders.** "Customers who opened the email bought twice as
  often as the holdout." They opened it because they were interested.
- **A control group built afterwards.** Any group not set aside by chance
  before the action is a comparison of unlike customers.
- **A mismatch in the split, ignored.** It is the most reliable sign that
  something in the pipeline treated the groups differently.
- **Many outcomes, one of them significant.** See
  [stating uncertainty](stating-uncertainty.md#many-comparisons).
- **The novelty of a change.** A new design draws attention at first.
  Compare the effect in the first week with later weeks.
- **The same customers in every control group.** A holdout chosen by a fixed
  rule, such as identifiers ending in zero, never receives anything and
  drifts away from the rest. Use a new random draw for each test.
- **A test too small, read anyway.** An underpowered test that comes out
  significant has overstated the effect. One that does not has shown
  nothing.
- **Rolling out and expecting the tested lift.** Winners regress. Expect
  less.
- **Units that affect each other.** A promotion that makes treated customers
  buy stock the control customers then cannot get makes the control look
  worse and the lift look larger.

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data. An offer of 8 off is emailed to 90,000 customers. A random
10,000 who qualified are held out. Over the offer's two weeks and the four
weeks after, the business's own order records give:

| Group | Customers | Bought | Rate |
|---|---|---|---|
| Sent the offer | 90,000 | 4,950 | 5.5% |
| Held out | 10,000 | 500 | 5.0% |

**The difference.** 5.5% − 5.0% = 0.5 points. The standard error is the
square root of (0.055 × 0.945 ÷ 90,000 + 0.050 × 0.950 ÷ 10,000), which is
0.23 points. The interval is 0.5 plus or minus 0.45: from about 0.05 to 0.95
points.

**The lift.** 0.5 ÷ 5.0 = 10%, with an interval from about 1% to 19% taking
the control rate as given, and about 1% to 20% once the noise in the control
rate is allowed for.

**The incremental total.** 0.5% of 90,000 is 450 extra buyers, with an
interval from about 40 to 860.

**What the tool reports.** The campaign tool credits the email with 4,950
orders, every buyer who was sent it. Of those, 4,500 would have bought
anyway.

**The value.** With an average order of 80 and a margin of 30%, each order
is worth 24.

| Line | Working | Amount |
|---|---|---|
| Incremental margin | 450 × 24 | 10,800 |
| Cost of the offer | 4,950 × 8 | 39,600 |
| Net | | −28,800 |

The campaign had a real lift of 10% and lost money, because the discount was
given to eleven buyers for every one it added. At the top of the interval,
860 extra buyers, the incremental margin is 20,640 and the net is −18,960.
At the bottom, 40 extra buyers, the net is −38,640. The campaign loses
across the whole interval.

**Why the business total did not move.** If the business takes 200,000
orders in the same six weeks, 450 is 0.2% of them. A real lift of 10% in this
campaign cannot be seen in the total.

**Whether the test was large enough.** A holdout of 10,000 against 90,000
gives a standard error of 0.23 points, so the smallest difference this design
would detect four times in five is about 2.8 × 0.23 = 0.65 points. The 2.8
is 1.96 + 0.84, the multiples of the standard error that give a 5% threshold
and four chances in five, and the 16 in the sample size rule is twice its
square. The
difference observed was smaller than that and came out just clear of zero.
The honest reading is a lift somewhere between slight and 19%, not a lift of
10%. To measure 0.5 points reliably the harmonic mean of the two groups
would have to reach 30,400, from the table above. Here it is 18,000. Holding
out 20,000 of the 100,000 would have given 32,000.

## Where it applies to our data

*Add: the actions the business takes on customers that can be randomized,
and for each, who controls the assignment.* Why: an experiment needs someone
able to withhold the action.

*Add: where assignments are recorded, and the dataset the primary outcome is
read from, linked to its page under Data.* Why: a test whose assignment was
not recorded cannot be analysed.

*Add: the baseline rate and variance of the outcomes tested most often, from
`facts/kpis.yaml`.* Why: the sample size calculation needs them, and they
should not be typed into a page.

*Add: the marketing tools in use that report lift, and what is known of how
each forms its comparison group.* Why: this is the first question asked of
every number they produce.

*Add: whether a universal holdout exists, its size, and when it rotates.*
Why: it is the only measure of the combined effect of all campaigns.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Kohavi, Ron, Diane Tang, and Ya Xu. *Trustworthy Online Controlled
Experiments: A Practical Guide to A/B Testing.* Cambridge University Press,
2020. The practitioner's reference: metrics, sample ratio mismatch, peeking,
novelty effects, and the organisation around testing. Start here.

Gerber, Alan S., and Donald P. Green. *Field Experiments: Design, Analysis,
and Interpretation.* W. W. Norton, 2012. The textbook treatment of
experiments on people outside a website: clustering, non-compliance,
attrition, and interference.

Lehr, Robert. "Sixteen S-squared over D-squared: A Relation for Crude Sample
Size Estimates." *Statistics in Medicine* 11, no. 8 (1992): 1099–1102. The
rule of thumb used above.

Deng, Alex, Ya Xu, Ron Kohavi, and Toby Walker. "Improving the Sensitivity of
Online Controlled Experiments by Utilizing Pre-Experiment Data." In
*Proceedings of the Sixth ACM International Conference on Web Search and Data
Mining*, 123–132. ACM, 2013. The pre-period adjustment known as CUPED.

Johari, Ramesh, Pete Koomen, Leonid Pekelis, and David Walsh. "Peeking at A/B
Tests: Why It Matters, and What to Do about It." In *Proceedings of the 23rd
ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*,
1517–1525. ACM, 2017.

Fabijan, Aleksander, Jayant Gupchup, Somit Gupta, Jeff Omhover, Wen Qin,
Lukas Vermeer, and Pavel Dmitriev. "Diagnosing Sample Ratio Mismatch in
Online Controlled Experiments: A Taxonomy and Rules of Thumb for
Practitioners." In *Proceedings of the 25th ACM SIGKDD International
Conference on Knowledge Discovery and Data Mining*, 2156–2164. ACM, 2019.
What to do when the split is not as designed.

Johnson, Garrett A., Randall A. Lewis, and Elmar I. Nubbemeyer. "Ghost Ads:
Improving the Economics of Measuring Online Ad Effectiveness." *Journal of
Marketing Research* 54, no. 6 (2017): 867–884. The placebo design for paid
advertising.

Vaver, Jon, and Jim Koehler. "Measuring Ad Effectiveness Using Geo
Experiments." Google, 2011. The geographic design.

Gordon, Brett R., Florian Zettelmeyer, Neha Bhargava, and Dan Chapsky. "A
Comparison of Approaches to Advertising Measurement: Evidence from Big Field
Experiments at Facebook." *Marketing Science* 38, no. 2 (2019): 193–225. How
far observational estimates of advertising lift fall from experimental ones.

Lewis, Randall A., and Justin M. Rao. "The Unfavorable Economics of Measuring
the Returns to Advertising." *The Quarterly Journal of Economics* 130, no. 4
(2015): 1941–1973. Why even very large advertising tests give wide
intervals.
