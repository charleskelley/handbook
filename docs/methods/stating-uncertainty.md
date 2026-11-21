---
title: "Stating uncertainty"
type: general
owner: ds-lead
audience: [all]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [principles, statistics, experimentation]
sources:
  - "Wasserstein and Lazar, The ASA Statement on p-Values: Context, Process, and Purpose, The American Statistician 70(2), 2016"
  - "Greenland and others, Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations, European Journal of Epidemiology 31(4), 2016"
---

# Stating uncertainty

Every number the team reports is an estimate. This page is the standard for
saying how far each one can be trusted: what to report beside it, what the
usual statistical statements do and do not mean, and the ways an honest
analysis still ends up overconfident.

## The standard

An estimate that will inform a decision is reported with five things.

| Item | Example |
|---|---|
| The estimate, in the units of the decision | 450 more buyers |
| An interval | Between 40 and 860 |
| What the interval covers | Sampling variation only |
| The number of independent units behind it | 100,000 customers, 10,000 of them held out |
| The grade of the design | A randomized holdout |

"Conversion rose 10%" with none of these is not a finding. The interval
matters more than the point: a decision that would be the same at both ends
of the interval is settled as far as sampling variation goes, and one that
flips within it is not.

## Where uncertainty comes from

| Source | What it is | Does an interval cover it? |
|---|---|---|
| Sampling | A different set of customers, or a different random split, would have given a different number | Yes. This is all a standard interval covers |
| Measurement | The outcome is recorded with error, late, or incompletely | No |
| Choices in the analysis | Another reasonable analyst would have defined the outcome, the window, or the exclusions differently | No |
| Bias in the design | The comparison group is not a fair stand-in. See [directional versus causal](directional-versus-causal.md) | No |
| The world moving | The effect measured last quarter is not the effect next quarter | No |

An interval is therefore a floor on the uncertainty, not a measure of it. A
narrow interval around a biased estimate is the most misleading output an
analysis can produce, and very large data makes it more likely, not less.

## Standard errors and intervals

The **standard error** of an estimate is how much it would vary from sample
to sample. A **95% confidence interval** is, in most practical cases, the
estimate plus or minus two standard errors.

The interval is a range of values for the true quantity that are compatible
with the data. The procedure that makes it will capture the true value in
about 95 of 100 repetitions. It is the single most useful thing to report
because it carries both the size of the effect and its precision.

Three formulas cover a large share of everyday cases:

- For a mean over *n* independent units, the standard error is the standard
  deviation of the units ÷ the square root of *n*.
- For a proportion *p* measured on *n* independent units, the standard error
  is the square root of *p* × (1 − *p*) ÷ *n*.
- For the difference between two independent estimates, the standard error
  is the square root of the sum of their squared standard errors.

So a conversion rate of 5% on 10,000 customers has a standard error of about
0.22 points and an interval of about 4.6% to 5.4%. Precision improves with
the square root of the sample: four times the customers for half the
interval.

## p-values

A **p-value** is the probability of a result at least as far from "no
effect" as the one observed, if there were truly no effect and every other
assumption of the analysis held. A small p-value says the data would be
surprising if nothing were going on.

It is misread more often than not. A p-value of 0.03 does **not** mean:

- that there is a 3% chance the effect is zero, or a 97% chance it is real;
- that the effect is large or matters;
- that the result will repeat;
- that the analysis was free of bias.

And a p-value of 0.30 does not mean there is no effect. It means this data
could not tell. "Not significant" from a small test is absence of evidence.
The interval shows the difference: a non-significant result with an interval
from −0.1 to +0.2 points has ruled out a large effect, and one with an
interval from −3 to +5 points has ruled out nothing.

Report the estimate and the interval. Give the p-value if a reader expects
it. Do not sort results into significant and not significant and stop there.

## Statistical and practical significance

Whether an effect is distinguishable from zero and whether it is large enough
to act on are different questions. Decide the smallest effect that would
change the decision before the analysis, then read the interval against it.

| The interval | Reading |
|---|---|
| Lies wholly above the size that matters | Act |
| Lies wholly above zero and includes the size that matters | The action does something. Whether it does enough is not settled |
| Lies wholly between zero and the size that matters | Real, and too small to act on |
| Lies wholly below zero | The action does harm |
| Includes zero and lies wholly below the size that matters | No effect large enough to matter. A finding in its own right |
| Stretches from below zero to above the size that matters | Inconclusive. The data cannot answer the question, and the right statement is that it cannot |

With millions of customers almost any difference is statistically
significant, so the second row is common. With a few hundred the last row
is.

## The unit behind the number

Standard errors assume independent observations. Customer data rarely has
them at the row level: one customer places many orders, one store has many
weeks. Treating 500,000 orders from 20,000 customers as 500,000 independent
observations gives intervals far too narrow.

The rule: the sample size is the number of units that were sampled or
assigned independently. If customers were randomized, the customer is the
unit, however many rows each has. If stores were, the store is. Analyse at
that level, or use a method that accounts for the grouping, such as
clustered standard errors, described on the
[regression page](regression.md#standard-errors), or the bootstrap below.

## The bootstrap

A general way to get a standard error or an interval without a formula.

1. Draw a sample of the same size from the data, with replacement.
2. Compute the estimate on it.
3. Repeat a few thousand times.
4. The standard deviation of those estimates is the standard error. The
   2.5th and 97.5th percentiles are a 95% interval.

It suits statistics with no simple formula: a median, a ratio, a share held
by the top decile, a difference in a model's accuracy. Two cautions. Resample
the independent unit, whole: customers, with all their orders, not orders.
And it does poorly for statistics driven by a few extreme values, such as a
maximum, or a mean dominated by a handful of very large customers.

A common special case is a ratio whose top and bottom both vary, such as
revenue per session when customers were randomized. Either bootstrap by
customer, or use the delta method, an approximation that builds the variance
of a ratio from the variances of its top and bottom and their covariance,
which the experimentation references below describe.

## Many comparisons

Each test at the 5% level has a one in twenty chance of a false alarm when
nothing is going on. Twenty tests are expected to produce one. Analyses run
many tests without counting them: every segment, every metric, every week
the results were checked.

- **Name one primary outcome before looking.** Everything else is
  secondary.
- **Treat a finding in one segment as a hypothesis.** "It worked for women
  aged 25 to 34 in the north" is the pattern chance produces. Confirm it on
  new data.
- **Correct when many tests are reported together.** The Bonferroni
  correction divides the threshold by the number of tests. It is strict.
  The Benjamini-Hochberg procedure controls the share of reported findings
  that are false: sort the p-values from smallest to largest, find the
  largest one that is no more than its rank ÷ the number of tests × the
  chosen rate, and report that one and all smaller.
- **Do not stop a test when it first looks good.** Checking repeatedly and
  stopping at the first significant result raises the false alarm rate well
  above 5%. See
  [experiments and lift tests](experiments-and-lift-tests.md#pitfalls).

The same problem arises without any formal test. An analyst who tries
several outcome definitions, windows, and exclusions, and reports the one
that works, has run many comparisons. Deciding the analysis before seeing the
outcome is the only protection.

## Winners are overstated

When an effect is estimated with a lot of noise, the estimates that happen to
clear the bar for significance are the ones that happened to come out large.
So a significant result from a small test overstates the true effect, often
by a wide margin, and sometimes has the wrong sign. The same applies to
picking the best of many campaigns, creatives, or stores: the winner was
partly lucky, and will do less well next time.

Expect the effect of a rolled-out winner to be smaller than the test showed.
Where it matters, rerun the winner alone.

## Intervals for predictions

Two different intervals are both called intervals. A confidence interval is
for an average or an effect: where the true mean lies. A prediction interval
is for a single future value: where next month's sales, or one customer's
spend, will fall. The second is always wider, because it includes the
variation of the thing itself as well as the uncertainty in the estimate.
A forecast is reported with prediction intervals: see
[time-series forecasting](time-series-forecasting.md).

A Bayesian analysis reports a credible interval, which is read directly as a
range the quantity lies in with a stated probability, given the model and the
prior. It is the statement most people think a confidence interval makes. It
depends on the prior, which must be stated.

## Saying it

| Instead of | Say |
|---|---|
| "The campaign lifted sales 10%" | "The campaign lifted sales by an estimated 10%, and the data is consistent with anything from 1% to 19%" |
| "There was no effect" | "We found no effect larger than 0.2 points" or "The test could not detect an effect smaller than 3 points" |
| "The result was significant" | The estimate and the interval |
| "Segment B responded best" | "Segment B had the largest estimate. The segments' intervals overlap, and we looked at eight" |
| "We are 95% confident it works" | "The interval excludes zero. That reflects sampling variation in a randomized test of 20,000 customers" |

## Further reading

Wasserstein, Ronald L., and Nicole A. Lazar. "The ASA Statement on p-Values:
Context, Process, and Purpose." *The American Statistician* 70, no. 2 (2016):
129–133. Six principles on what a p-value is and is not, from the American
Statistical Association. Short enough to send to a partner.

Greenland, Sander, Stephen J. Senn, Kenneth J. Rothman, John B. Carlin,
Charles Poole, Steven N. Goodman, and Douglas G. Altman. "Statistical Tests,
P Values, Confidence Intervals, and Power: A Guide to Misinterpretations."
*European Journal of Epidemiology* 31, no. 4 (2016): 337–350. A numbered list
of the common misreadings, each with the correction.

Gelman, Andrew, and John Carlin. "Beyond Power Calculations: Assessing Type S
(Sign) and Type M (Magnitude) Errors." *Perspectives on Psychological
Science* 9, no. 6 (2014): 641–651. Why significant results from noisy studies
overstate the effect.

Gelman, Andrew, and Eric Loken. "The Statistical Crisis in Science."
*American Scientist* 102, no. 6 (2014): 460. How choices made after seeing
the data produce false findings without anyone running many tests on
purpose.

Benjamini, Yoav, and Yosef Hochberg. "Controlling the False Discovery Rate: A
Practical and Powerful Approach to Multiple Testing." *Journal of the Royal
Statistical Society, Series B* 57, no. 1 (1995): 289–300. The procedure
described above.

Efron, Bradley, and Robert J. Tibshirani. *An Introduction to the Bootstrap.*
Chapman & Hall, 1993. The standard text. The original paper is Efron,
"Bootstrap Methods: Another Look at the Jackknife," *The Annals of
Statistics* 7, no. 1 (1979): 1–26.

Kohavi, Ron, Diane Tang, and Ya Xu. *Trustworthy Online Controlled
Experiments: A Practical Guide to A/B Testing.* Cambridge University Press,
2020. For the variance of ratio metrics and the delta method in practice.
