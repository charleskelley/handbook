---
title: "Uplift modeling"
type: method
depth: guide
owner: ds-lead
audience: [ds, mle, analyst]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [causal, predictive, marketing, modeling]
sources:
  - "Radcliffe and Surry, Real-World Uplift Modelling with Significance-Based Uplift Trees, Portrait Technical Report TR-2011-1, Stochastic Solutions, 2011"
  - "Gutierrez and Gérardy, Causal Inference and Uplift Modelling: A Review of the Literature, Proceedings of Machine Learning Research 67, 2017"
---

# Uplift modeling

Models that predict, for each customer, how much an action would change
their behaviour, so that the action can be aimed at the customers it works
on. It is the modelling counterpart of a lift test, and it should not be
attempted without one.

## What it is

An uplift model estimates the difference an action makes for each customer:
the probability they buy if contacted less the probability they buy if not.
An ordinary propensity model predicts who will buy. An uplift model predicts
whose buying depends on the contact. The two rankings differ, and the
second is the one a campaign should be targeted by, because contacting a
customer who would have bought anyway costs money and adds nothing. The
difficulty is that the quantity being predicted is never observed for any
individual: each customer is either contacted or not, never both. Uplift can
only be learned from groups, by comparing customers who were treated with
similar customers who were not, and the only trustworthy source of such data
is a randomized experiment. In the academic literature the same problem is
called estimating heterogeneous, or conditional average, treatment effects.

## When it is the right choice

- An action has been tested with a random control group, at scale, and
  features were recorded for every customer before assignment.
- The action costs something for each customer treated, or can do harm, so
  that treating fewer customers better is worth it.
- The test showed, or there is reason to expect, that the effect differs
  between customers.
- The action will be repeated in much the same form.

## When it is not

- **There is no randomized data.** Train on customers who were targeted by
  judgment or by a model, and the uplift model learns the targeting. Run the
  [experiment](experiments-and-lift-tests.md) first.
- **The test was small.** Differences in effect between customers are much
  smaller and noisier than the average effect. A test barely able to detect
  the average cannot support a model of who it differs for. To measure lift
  within each tenth of customers as precisely as the whole test measured the
  average takes ten times the customers.
- **The action is nearly free and harmless.** If it costs nothing to treat
  everyone and the average effect is positive, treat everyone.
- **The average effect is zero and there is no reason to expect it to
  differ.** A model will find subgroups by chance.
- **The question is whether the campaign worked.** That is lift
  measurement, on the experiments page, and comes first.

## Assumptions

| Assumption | What it means | How it is checked |
|---|---|---|
| Random assignment in the training data | Who was treated was decided by chance | The checks on the [experiments page](experiments-and-lift-tests.md#checks): the split, and balance before the test |
| Features fixed before assignment | Nothing used as an input could have been affected by the treatment | Check the date each feature was fixed |
| No interference | One customer's treatment does not change another's outcome | By the choice of unit |
| The next campaign is like the tested one | The same action, a similar population, similar conditions | Judgment. Retest when the action changes |

Methods exist for learning uplift from non-randomized data. They add the
assumption that everything driving who was treated is measured, which is the
assumption of [matching](matching.md), and they inherit its weakness.

## Lift, propensity, and uplift

Three things with similar names.

| | What it is | Per | Needs | Page |
|---|---|---|---|---|
| Lift | The measured effect of an action: outcome in the treated group less outcome in the control | Campaign | A randomized control group | [Experiments and lift tests](experiments-and-lift-tests.md) |
| Propensity | The predicted probability that a customer does something | Customer | Past outcomes | [Churn and propensity models](churn-and-propensity.md) |
| Uplift | The predicted effect of an action on a customer | Customer | A randomized test with features | This page |

A tool that reports "lift" has measured, or claims to have measured, the
first. A tool that scores customers "most likely to respond" is usually
offering the second. Neither is the third, whatever the label says.

Customers fall into four groups by what the action does to them: the
persuadable, who act only if treated; those who act either way; those who
do not act either way; and those the action puts off. The table is on the
[churn and propensity page](churn-and-propensity.md#from-a-score-to-an-action).
In the literature they are called persuadables, sure things, lost causes,
and sleeping dogs. A model of a wanted outcome, such as propensity to buy,
ranks the persuadables and the sure things together at the top. A model of
an unwanted one, such as churn, ranks the persuadables with the lost causes.
An uplift model is an attempt to rank the persuadables alone at the top and
the sleeping dogs at the bottom.

## Why it is hard

- **No customer has a label.** In ordinary prediction, each row has an
  outcome to learn from. Here the thing to predict, the difference between
  two outcomes for the same customer, is missing for every row.
- **The signal is a difference of differences.** The model must find how the
  gap between treated and control varies across customers. That is far
  noisier than either group's outcome, so uplift models need much more data
  than propensity models, and overfit readily.
- **Evaluation is indirect.** A prediction cannot be compared with the
  truth row by row. It can only be checked on groups.
- **Strong predictors of the outcome are a distraction.** Recency predicts
  buying very well. It may say nothing about who is persuadable. A method
  that is good at predicting outcomes is not thereby good at predicting
  effects.

## Common approaches

| Approach | What it needs | What it rests on | Main weakness |
|---|---|---|---|
| Uplift by segment, read from the experiment | A test, and a few segments named in advance | The experiment alone | Coarse. Limited to a few segments before the groups get too small. The baseline for everything below |
| Two models | A model of the outcome fitted to the treated group and another to the control. Uplift is the difference of their predictions | Each model being right about its group | Each model spends its effort on predicting the outcome. The difference of two noisy predictions is noisier still |
| One model with treatment as an input | One model of the outcome with a treatment flag and its interactions with the features | The model finding the interactions | With a flexible model the treatment flag is easily ignored, and predicted uplift collapses toward zero |
| Transformed outcome | A new outcome constructed so that its expected value is the uplift, then any ordinary model | The algebra of the transformation under random assignment | Very noisy. Sensitive to the share of customers who were treated |
| Uplift trees and forests | Trees whose splits are chosen to separate customers by the difference between treated and control, not by the outcome | The splitting rule | Individual trees are unstable. Use forests |
| Meta-learners, such as the X-learner and R-learner | A recipe that combines several ordinary models to target the effect directly | The component models, and the recipe's correction for their errors | More moving parts to get wrong |
| Causal forests | A forest built to estimate the effect for each customer, with intervals | Honest estimation: separate data to choose splits and to estimate | Slower, and the intervals are wide, as they should be |

Start with the first row. If the experiment shows no difference in lift
across a handful of sensible segments, such as recency bands, value tiers,
or new against established customers, a model is unlikely to find one that
is real.

## Evaluating an uplift model

On randomized data the model has not seen. With one experiment, a random
split of its customers into a part to train on and a part to evaluate on is
acceptable, because assignment was random. A later campaign is better.

1. Score every customer, treated and control alike.
2. Sort by predicted uplift and cut into bands, such as deciles.
3. In each band, compute the measured lift: the outcome rate among treated
   customers less the rate among control customers.

A model that works shows measured lift highest in the top band and falling
through the bands. The **uplift curve**, and its close relative the Qini
curve, which scales the control group differently, plot the cumulative
incremental outcomes gained as customers are treated in order of predicted
uplift, against treating the same number at random. Incremental outcomes to
a given depth are the outcomes among treated customers so far, less the
outcomes among control customers so far scaled up to the same number of
customers. The area
between the two summarises the model.

An illustration with made-up figures, not this business's data:

| Band of predicted uplift | Rate, treated | Rate, control | Measured lift |
|---|---|---|---|
| Top tenth | 12% | 6% | +6 points |
| Second tenth | 9% | 6% | +3 points |
| Third to ninth tenths | 6% | 5% | +1 point |
| Bottom tenth | 4% | 6% | −2 points |

The campaign's average lift is 1.4 points. About two thirds of it comes from
a fifth of the customers, and in the bottom tenth the contact does harm.
Treating only the top fifth keeps two thirds of the gain at a fifth of the
cost, and leaving out the bottom tenth adds to the gain.

Three cautions:

- Each band's lift is a difference between two small groups, with a wide
  interval. Show the intervals. A jagged pattern across bands is noise.
- Evaluate on data from a different period or campaign where possible.
  Uplift patterns are less stable than outcome patterns.
- The decisive test is a new experiment: target one random group by the
  uplift model, another by the current method, and compare total incremental
  outcome and cost.

## Reading a result you did not produce

Questions to ask of a model or a vendor feature described as uplift,
incremental, or persuadability scoring.

- **What data was it trained on?** If there was no randomized control group,
  it is a propensity model or an observational estimate, whatever it is
  called. Ask how the control group was formed.
- **What exactly does a score mean?** A probability of responding is
  propensity. A difference between two probabilities is uplift.
- **How was it evaluated?** Ask for measured lift by band of predicted
  uplift, on held-out randomized data, with intervals. A lift chart of
  response rates by score, with no control group, evaluates propensity.
- **How large was the test, and how large is each band?** Bands of a few
  hundred treated and a few dozen control customers show nothing.
- **Does the measured lift fall steadily across bands?** If not, the model
  has not found a pattern.
- **How does it compare with simple segments?** If recency bands do as
  well, use them.
- **Was the targeting policy itself tested?** A model can look good on old
  data and add nothing when used.
- **Is the bottom band negative, and is that believable?** Customers put
  off by a contact are real in some settings, such as reminders to
  subscribers. Elsewhere a negative band is often noise.
- **Is cost included?** The decision is predicted uplift × value against
  the cost of treating, not predicted uplift alone.

## Where it applies to our data

*Add: the actions for which randomized test data with customer features
exists, with the size of each test and where its assignments are kept.* Why:
uplift can only be modelled where this exists.

*Add: for each tested action, the measured lift by the few segments the
business already uses.* Why: it is the baseline, and it shows whether there
is variation worth modelling.

*Add: the cost of each action per customer, and whether the action can do
harm.* Why: they decide whether targeting by uplift is worth more than
treating everyone.

*Add: any vendor or tool feature in use that claims to score incrementality,
and what is known of its training data.* Why: it is the first question to
ask of it.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Further reading

Radcliffe, Nicholas J., and Patrick D. Surry. "Real-World Uplift Modelling
with Significance-Based Uplift Trees." Portrait Technical Report TR-2011-1.
Stochastic Solutions, 2011. A practitioner's account from the people who
developed the method commercially: the four groups, uplift trees, the Qini
measure, and what goes wrong in practice. Start here.

Gutierrez, Pierre, and Jean-Yves Gérardy. "Causal Inference and Uplift
Modelling: A Review of the Literature." *Proceedings of Machine Learning
Research* 67 (2017): 1–13. A short review that sorts the methods into the
two-model, transformed-outcome, and direct approaches and ties them to the
causal inference literature.

Lo, Victor S. Y. "The True Lift Model: A Novel Data Mining Approach to
Response Modeling in Database Marketing." *ACM SIGKDD Explorations
Newsletter* 4, no. 2 (2002): 78–86. An early statement of the problem and of
the single-model approach.

Radcliffe, Nicholas J. "Using Control Groups to Target on Predicted Lift:
Building and Assessing Uplift Models." *Direct Marketing Analytics Journal*
(2007): 14–21. Where the Qini measure for evaluating uplift models is set
out.

Devriendt, Floris, Darie Moldovan, and Wouter Verbeke. "A Literature Survey
and Experimental Evaluation of the State-of-the-Art in Uplift Modeling: A
Stepping Stone toward the Development of Prescriptive Analytics." *Big Data*
6, no. 1 (2018): 13–41. A comparison of the methods on several datasets.

Rzepakowski, Piotr, and Szymon Jaroszewicz. "Decision Trees for Uplift
Modeling with Single and Multiple Treatments." *Knowledge and Information
Systems* 32, no. 2 (2012): 303–327. Uplift trees.

Künzel, Sören R., Jasjeet S. Sekhon, Peter J. Bickel, and Bin Yu.
"Metalearners for Estimating Heterogeneous Treatment Effects Using Machine
Learning." *Proceedings of the National Academy of Sciences* 116, no. 10
(2019): 4156–4165. The two-model and single-model approaches under their
academic names, and the X-learner.

Nie, Xinkun, and Stefan Wager. "Quasi-Oracle Estimation of Heterogeneous
Treatment Effects." *Biometrika* 108, no. 2 (2021): 299–319. The R-learner.

Wager, Stefan, and Susan Athey. "Estimation and Inference of Heterogeneous
Treatment Effects Using Random Forests." *Journal of the American
Statistical Association* 113, no. 523 (2018): 1228–1242. Causal forests,
with intervals.

Ascarza, Eva. "Retention Futility: Targeting High-Risk Customers Might Be
Ineffective." *Journal of Marketing Research* 55, no. 1 (2018): 80–98. A
field demonstration that targeting by risk and targeting by uplift choose
different customers, and that the second works.
