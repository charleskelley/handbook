---
title: "Matching"
type: method
depth: guide
owner: ds-lead
audience: [ds, analyst, product]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [causal, observational, experimentation, propensity-score]
sources:
  - "Stuart, Matching Methods for Causal Inference: A Review and a Look Forward, Statistical Science 25(1), 2010"
  - "Imai, King, and Stuart, Misunderstandings Between Experimentalists and Observationalists about Causal Inference, Journal of the Royal Statistical Society Series A 171(2), 2008"
---

# Matching

Making two groups alike before comparing them. It has two uses, and this page
covers both: after the fact, to build a fair comparison group from customers
or units that were not treated; and before the fact, to design a test when
there are too few units for randomization alone to balance them.

## What it is

Matching selects, or weights, untreated units so that as a group they
resemble the treated units on characteristics fixed before the action. In an
observational study, the matched untreated units become the comparison
group, and the claim is that once the groups are alike on what was measured,
the remaining difference in outcomes is the effect. In a designed test,
units are paired or grouped on their characteristics first and the action is
then assigned within each pair, so the groups are balanced by construction.
The two uses share their machinery, a measure of how alike two units are and
a rule for pairing them, and differ completely in what they can claim.
Matching for analysis assumes nothing unmeasured separates the groups.
Matching for design, followed by randomization, assumes nothing of the kind.

## When it is the right choice

- An action was given to some customers and not others, the reasons are
  known and measured, and there are many untreated customers to choose
  from.
- As the first step before
  [difference-in-differences](difference-in-differences.md), to pick a
  comparison group that starts out alike.
- A test must be run across a small number of stores, regions, or accounts,
  where chance alone could put the largest ones in the same arm.
- The business has chosen where a pilot will run and comparison units are
  needed for it.

## When it is not

- **What decided treatment is not in the data.** A sales representative's
  judgment, a customer's own motivation to enrol, a targeting model whose
  inputs were not kept. Matching on everything else does not help.
- **Treated and untreated units do not overlap.** If every large account was
  treated, no small account is a match for one.
- **Randomization of many units is possible.** With thousands of customers,
  simple randomization balances everything, and matching adds little.
- **The matching variables are measured after the action.** Matching on
  anything the action could have changed removes part of the effect or adds
  bias. See [causal diagrams](causal-diagrams.md).

## Assumptions

For matching as an analysis of observational data:

| Assumption | What it means | How it is checked |
|---|---|---|
| No unmeasured confounding | Among units alike on the matching variables, who was treated is unrelated to what their outcome would have been | Cannot be checked from the data. Argued from how treatment was assigned, and probed by sensitivity analysis and placebo outcomes |
| Overlap | Every treated unit has untreated units like it | Compare the distributions of the matching variables. Count the treated units left without a match |
| Variables fixed before the action | Nothing matched on was affected by the action | Check the date each variable was fixed |
| No interference | Matched comparison units were not affected by the action | Knowledge of the business |

For matching as the design of a randomized test, only the last applies. The
random assignment within pairs does the rest.

## The goal is balance

Matching is judged by one thing: whether the treated and comparison groups
end up alike on the characteristics that matter, measured before the action.
It is not judged by how well a model predicts who was treated. A model of
treatment that predicts very well is a warning, because it means the two
groups barely overlap.

Balance is checked directly, variable by variable, after matching:

- The **standardized mean difference** for each variable: the difference in
  means between the groups ÷ the standard deviation in the treated group.
  Below 0.1 is the usual target.
- The spread of each variable in the two groups, not only the mean.
- For the most important variables, such as the outcome's own history, the
  full distributions side by side.

If balance is poor, change the matching and check again. This loop is
legitimate because it uses no outcome data. Looking at outcomes before the
matching is final is not.

## Matching to analyse observational data

### What to match on

Variables that were fixed before the action and that affect both who was
treated and the outcome. In customer data the most valuable is nearly always
the outcome's own history: a customer's spend in each of the months before
is a better guide to their spend after than any demographic. Add the
variables the targeting used, tenure, and anything else the
[causal diagram](causal-diagrams.md) marks as a common cause. Leave out
anything measured afterwards. A variable that drove treatment and has no
bearing on the outcome need not be matched on: it removes no bias and uses
up matches. When unsure whether it bears on the outcome, match on it.

### Who the estimate is about

Matching usually finds comparisons for the treated units, and so estimates
the effect on those who were treated, not the effect the action would have on
everyone. The first is called the average treatment effect on the treated,
and the second the average treatment effect. Treated units with no acceptable match are dropped, and the
estimate is then about the treated units that remain. Report how many were
dropped and how they differ. An estimate that covers the 60% of treated
customers who resemble untreated ones says nothing about the other 40%.

### How units are compared and paired

The table under [common approaches](#common-approaches) lists the main
choices. Three decisions sit under all of them:

- **The measure of closeness.** Exactly equal on a few variables, close on a
  weighted distance over many, or close on the propensity score, which is
  the estimated probability of being treated given the variables.
- **How many, and whether reused.** One comparison for each treated unit or
  several. Reusing a comparison unit for more than one treated unit improves
  closeness and lowers the number of independent comparisons.
- **How close is close enough.** A caliper is a maximum distance beyond
  which a treated unit is left unmatched. Tighter calipers give better
  balance and drop more units.

Weighting is the alternative to pairing. Every untreated unit is kept and
given a weight so that the weighted group resembles the treated one. It uses
more of the data and is sensitive to a few units with very large weights.

### Estimating after matching

Once balance is acceptable, the outcome is compared. In order of preference
where the data allows:

1. [Difference-in-differences](difference-in-differences.md) on the matched
   set, which also removes fixed differences the matching missed.
2. A [regression](regression.md) of the outcome on treatment and the
   matching variables within the matched set, which cleans up small
   remaining imbalances.
3. A plain difference in means between the matched groups.

Standard errors must reflect the matching: pairs, and any comparison unit
used more than once. For pairs, analyse the differences within pairs. For
other matching, use standard errors derived for it, as in Abadie and Imbens
in the reading below.

### What it cannot do

Matching balances what was measured. A customer who enrolled in a programme
and a customer who did not, alike on every recorded variable, still differ
in whatever made one of them enrol. A sensitivity analysis asks how strong
such an unmeasured difference would need to be to remove the result, and
gives a number that can be argued over. Rosenbaum's bounds are the usual
form. It belongs in any write-up that
makes a causal claim from matched data.

## Matching to design a test

With thousands of customers, random assignment produces two groups alike on
everything, within chance. With twenty stores or twelve regions it does not: one arm can
easily end up with the three largest. Matching before assignment removes that
risk.

### Pair, then randomize

1. For each unit, gather its outcome over a long period before the test and
   a few characteristics that drive it: size, region, format.
2. Form pairs, or small groups, of units that are closest.
3. Within each pair, assign one to treatment by a random draw.
4. Analyse the differences within pairs.

This is a matched-pair design, and with groups larger than two it is called
blocking. It is still a randomized experiment and carries an experiment's
guarantees, with more precision than an unpaired test of the same size
because differences between pairs drop out. The well-known advice is to block
on what can be measured and randomize the rest.

A related method, rerandomization, draws the whole assignment at random,
checks balance, and redraws until balance is acceptable. The acceptance rule
is set before any draw, and the analysis accounts for it, by a randomization
test that redraws assignments under the same rule.

### When the business picks the test units

Often the test sites are not random. A pilot runs where a manager is keen, or
in the markets where a media buy was available. Matching can still supply
comparison units:

1. For each chosen unit, select untreated units whose outcome tracked it
   most closely over a long period before, on level and on movement.
2. Hold back the last part of that period. Check that the selected
   comparisons, chosen on the earlier part, also track the test units in the
   part held back. If they do not, they will not after the test starts
   either.
3. Estimate the effect by
   [difference-in-differences](difference-in-differences.md), or by
   [synthetic control](synthetic-control.md) where there are few test units.

This is no longer an experiment. Whatever led the business to choose those
units is not balanced by any amount of matching on history, and a manager's
enthusiasm is itself a treatment. The result is grade B evidence at best on
the [grades of evidence](directional-versus-causal.md#grades-of-evidence),
and the write-up says so. Where there is any freedom at all, ask for two
candidate units for each test and assign one at random. That one change
turns the study back into an experiment.

### Planning the size

In both designs, the history before the test says how large an effect can be
detected. Apply the planned analysis to past periods in which nothing was
done, many times over with different pretend start dates. The spread of
those pretend effects is the noise the real effect has to exceed, by about
2.8 times its standard deviation for a test that detects it four times in
five, as on the
[experiments page](experiments-and-lift-tests.md#worked-examples).

## Common approaches

| Approach | What it needs | What it rests on | Main weakness |
|---|---|---|---|
| Exact matching | A few variables in categories | Units equal on those variables are comparable | Runs out of matches as soon as there are many variables or any continuous one |
| Coarsened exact matching | Variables cut into bands, then matched exactly on the bands | The bands are fine enough | The bands are a judgment. Many units dropped when there are many variables |
| Distance matching | Numeric variables and a distance, commonly the Mahalanobis distance | Closeness on the distance means comparable | Degrades with many variables |
| Propensity score matching | A model of treatment given the variables | Units with the same probability of treatment are comparable on average, if the model is right and nothing is unmeasured | Balances on average only. Can leave individual variables unbalanced, so balance must be checked variable by variable |
| Inverse probability weighting | The same model | The same | A few extreme weights can dominate. Trim them and report it |
| Balancing weights, such as entropy balancing | The variables to balance | Weights chosen so the groups' averages match exactly | Balances what it is told to and nothing else |
| Matching on the outcome's history | A long series of the outcome before the action | Units that moved together will keep doing so | Selects on noise if the history is short, and the comparison then drifts |
| Matched pairs or blocking, then randomizing | Characteristics before the test, and control of assignment | Randomization | Losing one unit of a pair loses the pair |
| Matched markets with assignment chosen by the business | Outcome history by market | The parallel-trends assumption | Not an experiment |

There is a long-running argument over the propensity score. Its attraction
is that it reduces many variables to one. The objection, set out by King and
Nielsen in the reading below, is that matching on that one number can make
balance on the original variables worse. The practical resolution is the
rule already given: whatever method produces the match, judge it by the
balance it achieves on each variable.

## Reading a result you did not produce

Questions to ask of a comparison that says its groups were matched.

- **What were they matched on, and when was each variable measured?**
  Anything from after the action invalidates the match.
- **Is the outcome's own history among the matching variables?** If not, ask
  why.
- **Where is the balance table?** Means and standardized differences for
  every matching variable, before and after matching. A matched analysis
  with no balance table has not shown that the matching worked.
- **How many treated units were dropped, and which?** The estimate describes
  the ones that remain.
- **Why were the treated units treated?** If the honest answer includes
  something not in the data, the estimate is biased by an unknown amount.
- **Were comparison units reused, and how often?** A comparison group that
  is mostly the same hundred customers many times over is a small sample.
- **How was the method chosen?** If several matching methods were tried and
  the outcome was examined under each, the result reported is the preferred
  one of several.
- **Is there a sensitivity analysis or a placebo outcome?**
- **For matched markets: who chose the test markets, and was the match
  checked on a period it was not built on?** Comparison markets that fit the
  period they were chosen on, and no other, are fitted to noise.
- **For a designed test: was assignment within pairs random, and does the
  analysis use the pairs?**

## Where it applies to our data

*Add: the actions for which the team builds matched comparison groups, the
variables matched on for each, and why.* Why: the matching variables are the
assumption.

*Add: the datasets that give each unit's history before an action, linked to
their pages under Data, and how far back each is reliable.* Why: the
outcome's history is the most valuable thing to match on.

*Add: the units the business tests on when it cannot test on customers, such
as stores, regions, or markets, how many there are, and whether the team
controls assignment.* Why: this decides between a matched-pair experiment and
a matched comparison.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Further reading

Stuart, Elizabeth A. "Matching Methods for Causal Inference: A Review and a
Look Forward." *Statistical Science* 25, no. 1 (2010): 1–21. The best single
overview of the choices and the order to make them in. Start here.

Rosenbaum, Paul R., and Donald B. Rubin. "The Central Role of the Propensity
Score in Observational Studies for Causal Effects." *Biometrika* 70, no. 1
(1983): 41–55. The paper that introduced the propensity score.

Ho, Daniel E., Kosuke Imai, Gary King, and Elizabeth A. Stuart. "Matching as
Nonparametric Preprocessing for Reducing Model Dependence in Parametric
Causal Inference." *Political Analysis* 15, no. 3 (2007): 199–236. The case
for matching first and modelling second.

Austin, Peter C. "An Introduction to Propensity Score Methods for Reducing
the Effects of Confounding in Observational Studies." *Multivariate
Behavioral Research* 46, no. 3 (2011): 399–424. A practical walk through
matching, weighting, and balance diagnostics.

King, Gary, and Richard Nielsen. "Why Propensity Scores Should Not Be Used
for Matching." *Political Analysis* 27, no. 4 (2019): 435–454. The objection
to propensity score matching.

Iacus, Stefano M., Gary King, and Giuseppe Porro. "Causal Inference without
Balance Checking: Coarsened Exact Matching." *Political Analysis* 20, no. 1
(2012): 1–24. Coarsened exact matching.

Hainmueller, Jens. "Entropy Balancing for Causal Effects: A Multivariate
Reweighting Method to Produce Balanced Samples in Observational Studies."
*Political Analysis* 20, no. 1 (2012): 25–46. Weights that balance by
construction.

Rosenbaum, Paul R. *Design of Observational Studies.* Springer, 2010.
Matching as design, and sensitivity analysis for what was not measured.

Imai, Kosuke, Gary King, and Elizabeth A. Stuart. "Misunderstandings Between
Experimentalists and Observationalists about Causal Inference." *Journal of
the Royal Statistical Society, Series A* 171, no. 2 (2008): 481–502. What
matching and randomization each contribute, and why matched pairs help even
in an experiment.

Bruhn, Miriam, and David McKenzie. "In Pursuit of Balance: Randomization in
Practice in Development Field Experiments." *American Economic Journal:
Applied Economics* 1, no. 4 (2009): 200–232. Pairing, stratifying, and
rerandomizing compared, with advice for small experiments.

Morgan, Kari Lock, and Donald B. Rubin. "Rerandomization to Improve Covariate
Balance in Experiments." *The Annals of Statistics* 40, no. 2 (2012):
1263–1282. Rerandomization and how to analyse it.

Abadie, Alberto, and Guido W. Imbens. "Large Sample Properties of Matching
Estimators for Average Treatment Effects." *Econometrica* 74, no. 1 (2006):
235–267. The standard errors of matching estimators.
