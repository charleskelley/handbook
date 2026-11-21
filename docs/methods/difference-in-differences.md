---
title: "Difference-in-differences"
type: method
depth: build
owner: ds-lead
audience: [ds, analyst, product]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [causal, quasi-experiment, observational]
sources:
  - "Angrist and Pischke, Mostly Harmless Econometrics, Princeton University Press, 2009"
  - "Roth, Sant'Anna, Bilinski, and Poe, What's trending in difference-in-differences?, Journal of Econometrics 235(2), 2023"
---

# Difference-in-differences

A way to estimate the effect of a change that some units got and others did
not, when nobody randomized which. It compares how much the treated units
moved with how much the untreated ones moved over the same time. It is the
first tool to reach for when an experiment was not possible, and many pricing
and operational changes are measured this way.

## What it is

A before-and-after comparison, corrected by a comparison group. A simple
before-and-after comparison credits the change with everything that happened
over the period: the season, the trend, the economy. A simple comparison of
treated with untreated units credits it with every way the two groups already
differed. Difference-in-differences takes the change over time in the treated
group and subtracts the change over time in an untreated group. Fixed
differences between the groups cancel, because each group is compared with
itself. Movements common to both cancel, because they appear in both changes.
What is left is the effect, provided one assumption holds: that without the
change, the two groups would have moved by the same amount.

## When it is the right choice

- A change was made in some stores, regions, products, or customer groups
  and not in others, on a known date.
- The outcome is recorded for both groups for several periods before the
  change and after it.
- The untreated group was not affected by the change.
- The groups can be shown to have moved together before the change.

## When it is not

- **The treated units were chosen because of how they were trending.** A
  remedy applied to the stores in steepest decline, or an investment placed
  in the fastest-growing regions, breaks the assumption by design.
- **Nothing was left untreated.** A change made everywhere on one day has no
  comparison group. What remains is a before-and-after comparison: see
  [the weaker relatives](#the-weaker-relatives).
- **Only one or a handful of units were treated.** One region against the
  rest is better handled by [synthetic control](synthetic-control.md), which
  builds a comparison from many untreated units.
- **The untreated units felt the change.** Customers who shop in both a
  treated and an untreated store, or a competitor's reaction that reaches
  every region.
- **Something else happened to one group at the same time.** The estimate
  cannot separate two things that coincide.

## Assumptions

| Assumption | What it means | How it is checked |
|---|---|---|
| Parallel trends | Without the change, the treated group's outcome would have moved by the same amount as the comparison group's | Cannot be tested for the period after. Supported by showing the groups moved together for many periods before, and by placebo tests |
| No anticipation | The treated units did not change their behaviour before the date | The periods just before the change show no gap opening |
| No spillover | The comparison group's outcome is what it would have been had the change never been made anywhere | By the choice of comparison group. Knowledge of the business |
| Nothing else coincides | No other event affected one group and not the other at the same time | A list of what else happened, gathered from the people who run the units and from the insights log |
| The groups stay the same | The units in each group are the same before and after | Fix membership at the start. Check for units entering or leaving |

Parallel trends is an assumption about something that did not happen. No
test proves it. The evidence for it is always indirect, and the write-up
says so.

## The estimate

![Two lines from before to after a change. The comparison group rises from 80 to 90. The treated group rises from 100 to 120. A dashed line shows the treated group rising by 10, as the comparison group did, to 110. The gap between 120 and 110 is marked as the effect, 10.](../assets/did-light.svg#only-light)
![Two lines from before to after a change. The comparison group rises from 80 to 90. The treated group rises from 100 to 120. A dashed line shows the treated group rising by 10, as the comparison group did, to 110. The gap between 120 and 110 is marked as the effect, 10.](../assets/did-dark.svg#only-dark)

*The dashed line is the assumption: where the treated group would have been.*

With two groups and two periods the estimate is four averages:

effect = (treated after − treated before) − (comparison after − comparison before)

The same number comes from a regression of the outcome on three terms: a
flag for the treated group, a flag for the period after, and the two
multiplied together. The coefficient on the product is the estimate. The
regression form is used in practice because it extends to many periods and
many units, allows other variables to be added, and gives a standard error.
With many units and periods, the group flag is replaced by a separate
intercept for each unit and the period flag by one for each period. This is
called a two-way fixed effects regression.

### Standard errors

Outcomes for the same unit in successive periods are related, so the rows
are not independent. Standard errors are clustered by unit, which makes the
unit the thing that counts. This has a hard consequence: the precision of the
estimate depends on the number of units, not the number of rows. A study of
6 treated regions and 10 comparison regions has 16 observations in the sense
that matters, however many weeks or customers lie underneath, and with so
few the usual standard errors are themselves unreliable. With few units, use
a method made for the case, such as a permutation test that reassigns the
change among the units, or the wild cluster bootstrap, and present the
result as indicative. Clustering is explained on the
[regression page](regression.md#standard-errors).

### Many periods: the event study

With several periods either side of the change, estimate the gap between the
groups separately for each period, measured against the gap in the last
period before the change. Plot those estimates against time relative to the
change, with their intervals.

- **Before the change,** the estimates should lie near zero with no drift.
  This is the visible support for parallel trends.
- **After the change,** the estimates trace the effect over time: whether it
  appears at once, builds, or fades.

A flat pre-period is supportive, not conclusive. With few periods or noisy
data, a real difference in trend may not show, and choosing to proceed only
when the pre-period looks flat biases the result in its own right.

### Choosing the comparison group

The comparison group is the most consequential choice. In order of
preference:

1. Units that were candidates for the change and missed it for a reason
   unrelated to the outcome: capacity, timing, an arbitrary boundary.
2. Units that will get the change later, used as comparisons until they do.
3. Units chosen to resemble the treated units in level and trend before the
   change. See [matching](matching.md).
4. Everything untreated. The weakest, because it includes units that have
   little in common with the treated ones.

Choose it before looking at outcomes after the change.

### Which scale

Parallel in what? If the comparison group grew by 10 units, the assumption
in levels says the treated group would have grown by 10 units. If the
comparison group grew by 12%, the assumption in ratios, which is estimated on
the logarithm of the outcome, says the treated group would have grown by
12%. When the groups differ in size, these give different answers, and both
cannot hold. Decide from the pre-period: check whether the gap was steady in
units or in percent. A coefficient *b* on the logarithm scale is a
proportional effect of e to the power *b*, less 1. Where the outcome can be
zero, aggregate to a level at which it is not, or use a model for ratios such
as Poisson regression.

### A change that rolls out over time

When units get the change on different dates, the two-way fixed effects
regression can go wrong. It ends up using units treated earlier as the
comparison for units treated later, and if the effect grows over time or
differs between units, the single coefficient it reports can be far from any
average of the real effects. Where the rollout is staggered, estimate the
effect separately for each group of units treated at the same time,
comparing each only with units not yet treated or never treated, and then
average. The papers by Goodman-Bacon and by Callaway and Sant'Anna in the
sources set this out.

### The weaker relatives

- **Before and after.** One group, two periods, no comparison. It assumes
  nothing else changed. Use it only to describe.
- **Interrupted time series.** One group, many periods. Fit the level and
  trend before the change, project them forward, and compare with what
  happened. It assumes the earlier pattern would have continued and that
  nothing else happened on that date. It is more credible when the change is
  sharp, the series is long, seasonality is modelled, and the effect is
  expected at once. Adding a comparison series turns it back into
  difference-in-differences.

Both belong in grade D or low in grade B of the
[grades of evidence](directional-versus-causal.md#grades-of-evidence).

## Building the outputs

Panel table

:   One row per unit and period. Columns: unit identifier, period, the
    outcome, a flag for whether the unit is in the treated group, the period
    in which the unit was first treated, and any variables that vary by unit
    and period. Every unit has a row for every period. A unit is in the same
    group throughout.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| The two groups over time | Period | Average outcome in each group | Two lines, with the date of the change marked. The first thing to draw and to show |
| Four averages | Group | Before, after, change | Table, with the difference of the changes beneath |
| Event study | Period relative to the change | Estimate of the gap, interval | Points with intervals, a line at zero, the last period before the change set to zero |
| Estimate | Specification | Effect, standard error, interval, number of units in each group | Table, with the main specification first |
| Placebo tests | Test | Estimate, interval | Table |
| What else happened | Date | Event, the group it touched | List, from the insights log and from the people who run the units |

Defaults, where nothing about the business decides otherwise:

| Choice | Default | Why |
|---|---|---|
| Pre-period | As many periods as are comparable, and at least a full year for a seasonal outcome | The pre-period is the only evidence for the assumption |
| Scale | Logarithm of the outcome when the groups differ in size | Growth in percent is the more common pattern in business series |
| Standard errors | Clustered by unit | Rows within a unit are related |
| Staggered rollout | An estimator built for it | The plain regression can mislead |
| Comparison group | Chosen and written down before outcomes are examined | To prevent choosing the group that gives the wanted answer |

## Checks

Run these before reading the estimate.

- The plot of the two groups shows them moving together before the change.
- The event-study estimates before the change are near zero and show no
  drift toward the effect. If they do drift, the comparison group is wrong
  for this purpose. Choose another without looking at outcomes after the
  change, or use [matching](matching.md) or
  [synthetic control](synthetic-control.md), or report the estimate with the
  drift beside it and no causal claim.
- **A placebo date.** Pretend the change happened earlier, within the
  pre-period, and estimate the effect. It should be near zero.
- **A placebo outcome.** Estimate the effect on an outcome the change could
  not have moved. It should be near zero.
- **A placebo group.** Estimate the effect on a set of untreated units as
  though they had been treated. It should be near zero.
- The panel is complete: every unit in every period, in one group
  throughout.
- The estimate is computed on both scales. Where they differ, the pre-period
  decides which is supported, as in the worked example, and where it cannot,
  both are reported.
- The estimate is of a similar size with one comparison unit removed at a
  time, and with a different reasonable comparison group. Where it is not,
  report the range.
- The number of units in each group is stated beside the estimate.

## Pitfalls

- **Counting rows, not units.** Thousands of customer-weeks in eight stores
  is eight observations. Intervals that ignore this are far too narrow.
- **Treated units chosen for a reason.** If the reason relates to where the
  outcome was heading, the estimate is biased, and the pre-period may not
  show it.
- **A dip before treatment.** Units often get a remedy just after an unusual
  bad period. They would have recovered anyway. The estimate takes the
  recovery as the effect.
- **Choosing the comparison group, the scale, or the window after seeing the
  result.** Each choice is defensible, and together they can produce nearly
  any answer.
- **Passing the pre-trend test and stopping.** A test that fails to find a
  difference in trend has not shown there is none.
- **A staggered rollout in a plain regression.** See above.
- **Composition changing.** If the change draws new customers into the
  treated stores, the average customer after is not the average customer
  before. Decide whether the outcome is per store or per customer and what
  the question is.
- **The comparison group reacting.** Customers switching from untreated to
  treated stores lower the comparison and double-count the effect.
- **Reading a short-run effect as permanent.** The periods after the change
  show only as far as they go.

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data. A new layout was installed in a group of stores. Average
weekly sales per store, in thousands:

| Group | Two periods before | One period before | After |
|---|---|---|---|
| New layout | 95 | 100 | 120 |
| Comparison | 76 | 80 | 90 |

**In levels.** The treated stores rose by 20 and the comparison stores by
10. The estimate is 20 − 10 = 10. This says the treated stores would have
reached 110.

**In ratios.** The comparison stores rose by 12.5%. Had the treated stores
done the same, they would have reached 112.5. The estimate is 120 − 112.5 =
7.5, or 6.7% above where they would have been.

**Which to believe.** Use the periods before. From two periods before to one
period before, the treated stores rose by 5 and the comparison stores by 4:
not equal. In percent, both rose by 5.3%. The groups were moving in parallel
in ratios, not in levels, so the estimate in ratios is the one the evidence
supports: about 7.5, and not 10. The same check on the earlier periods is
also a placebo test. On the ratio scale it gives an effect of zero where
there was no change, as it should.

Two points the arithmetic does not show. With one earlier period this is thin
evidence, and a real analysis would use many. And the interval depends on
how many stores are in each group, which a table of averages hides.

## Where it applies to our data

*Add: the kinds of change the business makes that reach some units and not
others, such as store, region, product line, or customer tier, and the unit
each is rolled out by.* Why: the unit of rollout is the unit of analysis.

*Add: the datasets that give the outcome by unit and period, linked to their
pages under Data, and how far back each is comparable.* Why: the pre-period
is the evidence.

*Add: where the dates of changes are recorded: price changes, launches,
system changes.* Why: the estimate is only as good as the list of what else
happened on that date. The insights index under
[Oversight](../oversight/index.md) is the place for it.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Angrist, Joshua D., and Jörn-Steffen Pischke. *Mostly Harmless Econometrics:
An Empiricist's Companion.* Princeton University Press, 2009. The chapter on
fixed effects and differences-in-differences is the standard introduction.

Card, David, and Alan B. Krueger. "Minimum Wages and Employment: A Case Study
of the Fast-Food Industry in New Jersey and Pennsylvania." *American Economic
Review* 84, no. 4 (1994): 772–793. The best-known application: restaurants
either side of a state border, before and after a change in one state.

Bertrand, Marianne, Esther Duflo, and Sendhil Mullainathan. "How Much Should
We Trust Differences-in-Differences Estimates?" *The Quarterly Journal of
Economics* 119, no. 1 (2004): 249–275. Why standard errors must be clustered
by unit, and how badly they mislead when they are not.

Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. "What's
Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics
Literature." *Journal of Econometrics* 235, no. 2 (2023): 2218–2244. The
current state of the method in one place: staggered rollouts, testing
parallel trends, and what to do when it may not hold. Read this after the
textbook chapter.

Goodman-Bacon, Andrew. "Difference-in-Differences with Variation in Treatment
Timing." *Journal of Econometrics* 225, no. 2 (2021): 254–277. What the plain
regression is really averaging when units are treated at different times.

Callaway, Brantly, and Pedro H. C. Sant'Anna. "Difference-in-Differences with
Multiple Time Periods." *Journal of Econometrics* 225, no. 2 (2021):
200–230. An estimator for staggered rollouts.

Roth, Jonathan. "Pretest with Caution: Event-Study Estimates after Testing
for Parallel Trends." *American Economic Review: Insights* 4, no. 3 (2022):
305–322. Why a passed pre-trend test is weak reassurance.

Lopez Bernal, James, Steven Cummins, and Antonio Gasparrini. "Interrupted
Time Series Regression for the Evaluation of Public Health Interventions: A
Tutorial." *International Journal of Epidemiology* 46, no. 1 (2017):
348–355. A worked tutorial on the single-series design.
