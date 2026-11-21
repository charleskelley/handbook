---
title: "Synthetic control"
type: method
depth: guide
owner: ds-lead
audience: [ds, analyst, product]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [causal, quasi-experiment, observational, time-series]
sources:
  - "Abadie, Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects, Journal of Economic Literature 59(2), 2021"
  - "Abadie, Diamond, and Hainmueller, Synthetic Control Methods for Comparative Case Studies, Journal of the American Statistical Association 105(490), 2010"
---

# Synthetic control

A way to estimate the effect of a change on one unit, such as a region, a
market, or a product line, by building its comparison out of a weighted mix
of units that did not get the change. It is the idea behind most
after-the-fact measurement of a KPI when a single market was treated and no
holdout was kept.

## What it is

When only one unit is treated, there is no group to average over and no
single untreated unit is a convincing twin. The synthetic control method
builds the twin. It takes a pool of untreated units, called the donor pool,
and finds a set of weights such that the weighted average of the donors
tracks the treated unit closely over a long period before the change. That
weighted average, the synthetic control, is then carried forward past the
date of the change. The difference between what the treated unit did and what
its synthetic control did is the estimated effect. The weights are found
using data from before the change only, they are restricted to be
non-negative and to add up to one, and they are reported, so that anyone can
see which units the comparison is made of.

## When it is the right choice

- One unit, or a handful, got the change: a campaign in one region, a new
  price in one market, a launch in one country.
- There are many similar units that did not, and the change did not reach
  them.
- The outcome is recorded for all of them over a long period before the
  change, at least several times as long as the period to be evaluated.
- The treated unit is not an extreme: its history can be reproduced by a mix
  of the others.

## When it is not

- **Many units were treated.** With many treated and untreated units,
  [difference-in-differences](difference-in-differences.md) uses the data
  better and has ordinary standard errors.
- **The history before the change is short.** A few periods can be matched by
  chance. The fit then means nothing.
- **The treated unit is unlike all the others.** The largest market cannot
  be built from smaller ones, because the weights cannot exceed one.
  Rescaling the outcome, per head or as an index to a base period, sometimes
  brings it within range.
- **Every unit was affected.** A national campaign, or a change whose effect
  spills into neighbouring regions, leaves no clean donors.
- **A donor had a shock of its own** in the period after the change. The
  synthetic control inherits it.
- **The effect is expected to be small against the series' own variation.**
  The method has little power, and a null result will be uninformative.

## Assumptions

| Assumption | What it means | How it is checked |
|---|---|---|
| The fit would have continued | A mix of donors that reproduced the treated unit for a long time before the change would have gone on doing so without it | Cannot be checked for the period after. Supported by a close fit over a long period, and by fitting on the early part of that period and checking the later part |
| Donors are untouched | The change did not affect the donor units | Knowledge of the business. Leave out neighbours and any unit that could have picked up displaced demand |
| No shocks to individual donors | Nothing unusual happened to a donor after the change | Check the insights log. Rerun leaving each donor out in turn |
| No anticipation | The treated unit did not respond before the date | Set the date at the announcement if behaviour could have changed then |
| The treated unit lies within the donors | Its values are within the range the donors span | Check the fit. A persistent gap before the change means it does not |

## How it works

![Two lines over time. A solid line for the treated unit and a dashed line for its synthetic control follow each other closely until a vertical line marking the change. After the change the treated line rises above the synthetic line, and the gap between them is shaded.](../assets/synthetic-control-light.svg#only-light)
![Two lines over time. A solid line for the treated unit and a dashed line for its synthetic control follow each other closely until a vertical line marking the change. After the change the treated line rises above the synthetic line, and the gap between them is shaded.](../assets/synthetic-control-dark.svg#only-dark)

*A schematic. The weights are fitted on the period before the change. The
gap after it is the estimate.*

1. **Choose the donor pool.** Untreated units that are like the treated one
   in kind, that the change did not reach, and that had no large event of
   their own. Choose it before looking at outcomes after the change.
2. **Find the weights.** Non-negative, adding to one, chosen so the weighted
   donors match the treated unit's outcome over the period before the
   change, and optionally a few other characteristics. Most donors usually
   get a weight of zero and a few carry the comparison.
3. **Look at the fit.** Plot the treated unit and the synthetic control over
   the whole period before the change. If they do not track, stop. There is
   no estimate. As a yardstick, compare the typical gap between the two
   before the change with the size of effect that would matter. A gap of the
   same order means the method cannot see an effect that size.
4. **Read the gap.** After the change, the difference between the two lines
   in each period is the estimated effect in that period.
5. **Test it.** See the next section.

The restriction on the weights is the method's main safeguard. Because
weights cannot be negative or exceed one, the synthetic control is always an
average of real units and never an extrapolation beyond them. A
[regression](regression.md) of the treated unit on the donors would fit the
period before the change better and could do so with weights that have no
meaning.

## Judging whether the gap is real

With one treated unit there is no standard error in the ordinary sense. The
method's own test is a placebo test.

- **Placebo in space.** Pretend each donor in turn was the treated unit,
  build its synthetic control from the others, and compute its gap. This
  gives the distribution of gaps that arise when nothing happened. The
  treated unit's gap is convincing only if it is extreme within that
  distribution. Because donors with a poor fit before the change have large
  gaps after it for that reason alone, the usual statistic is the ratio of
  the size of the gap after the change to the size before, each measured as
  the root mean squared gap. It is known as the ratio of root mean squared
  prediction errors.
- **What the rank can say.** With 19 donors, the treated unit is one of 20,
  and the strongest possible result is that it ranks first of 20. That
  corresponds to 1 chance in 20. A small donor pool cannot give strong
  evidence however large the effect looks.
- **Placebo in time.** Pretend the change happened earlier, fit on the
  period before the pretend date, and check that no gap opens between the
  pretend date and the real one.
- **Leave one out.** Remove each donor with a positive weight in turn and
  refit. An estimate that depends on one donor is an estimate about that
  donor.

Report the fit before the change, the weights, the gap by period, and the
placebo results together. The gap on its own is not a finding. The treated
unit's rank among the placebos takes the place an interval would have in
another design.

With a few treated units, build a synthetic control for each and average the
gaps, or use synthetic difference-in-differences from the table below.

## Common approaches

| Approach | What it needs | What it rests on | Main weakness |
|---|---|---|---|
| Synthetic control, as first proposed | One treated unit, a donor pool, a long history | A convex mix of donors reproduces the treated unit | Fails when no mix fits. Inference limited by the number of donors |
| Bayesian structural time series | The treated series, and one or more control series the change did not affect | A time-series model of the treated unit given the controls would have kept holding | The control series can be anything, including series the change did affect, and nothing stops a poor choice. Intervals reflect the model, not the choice of controls |
| Augmented synthetic control | The same as synthetic control | Synthetic control, with a model correcting what the weights leave unmatched | Gives up the guarantee against extrapolation when the fit is poor |
| Synthetic difference-in-differences | Several treated units, donors, a long history | Weights on donors and on periods, then a difference-in-differences | Newer, with less accumulated practice |
| Generalized synthetic control | Many units, several treated, possibly at different times | A model with a few shared hidden factors drives all units | Depends on the number of factors chosen |
| Matched markets, then [difference-in-differences](difference-in-differences.md) | A few comparison markets chosen by their history | Parallel trends | Equal weights on a hand-picked set. See [matching](matching.md) |

The second row is the one most often met in a business, because a
well-known open-source implementation made it easy to run. It answers the
same question as synthetic control, by regression on control series and not
by a constrained average of donors. It is convenient and produces a tidy
interval. That convenience is the risk: it will return a confident answer
from control series that are unsuitable, and the choice of controls is the
whole analysis.

## Reading a result you did not produce

Questions to ask of a chart showing an actual line above a "predicted" or
"counterfactual" line.

- **What is the comparison made of?** Ask for the donor units or control
  series and their weights. If nobody can list them, nobody has checked
  them.
- **Could the change have affected any of them?** Neighbouring regions,
  other products the customer might have bought otherwise, another channel
  that carries the same campaign, a total that includes the treated unit.
  Using a series the change moved as a control cancels part of the effect or
  invents one.
- **How good is the fit before the change, and over how long?** Ask to see
  the two lines for the whole period before. A fit over eight weeks is not
  evidence.
- **Was the fit checked on a period it was not built on?**
- **Who chose the donors, and when?** A donor pool adjusted after seeing the
  result is a search for an answer.
- **Is there a placebo test?** What does the same method give for units
  where nothing happened, and for a date when nothing happened?
- **What does the interval cover?** In the regression-based version, the
  interval assumes the model and the controls are right. It is narrower than
  the truth.
- **What else happened to the treated unit then?** The method attributes
  everything that differs after the date to the change.
- **Does the gap behave like the action?** An effect that starts before the
  action, or continues unchanged long after a short campaign ended, is more
  likely a drifting comparison than an effect.
- **Was this unit picked for evaluation because its numbers looked good?**
  If ten markets ran the campaign and one is presented, ask for the other
  nine.

## Where it applies to our data

*Add: the units the business acts on one at a time, such as regions,
markets, or product lines, and how many comparable untreated units exist for
each.* Why: the number of donors sets the strongest evidence the method can
give.

*Add: the datasets that give the outcome by unit and period, linked to their
pages under Data, and how far back each is comparable.* Why: the method
needs a long history on a consistent definition.

*Add: which units affect one another, such as neighbouring regions or
products that substitute.* Why: they cannot be donors for each other.

*Add: any tools in use in the business that produce a "causal impact" chart,
and the control series each is given.* Why: the choice of controls is the
analysis.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Further reading

Abadie, Alberto. "Using Synthetic Controls: Feasibility, Data Requirements,
and Methodological Aspects." *Journal of Economic Literature* 59, no. 2
(2021): 391–425. The practical guide by the method's originator: when it
applies, what data it needs, and how to run and report it. Start here.

Abadie, Alberto, Alexis Diamond, and Jens Hainmueller. "Synthetic Control
Methods for Comparative Case Studies: Estimating the Effect of California's
Tobacco Control Program." *Journal of the American Statistical Association*
105, no. 490 (2010): 493–505. The paper that set out the method and the
placebo test, on a state-level policy.

Abadie, Alberto, and Javier Gardeazabal. "The Economic Costs of Conflict: A
Case Study of the Basque Country." *American Economic Review* 93, no. 1
(2003): 113–132. The first use.

Brodersen, Kay H., Fabian Gallusser, Jim Koehler, Nicolas Remy, and Steven L.
Scott. "Inferring Causal Impact Using Bayesian Structural Time-Series
Models." *The Annals of Applied Statistics* 9, no. 1 (2015): 247–274. The
regression-based version, written for measuring marketing campaigns.

Arkhangelsky, Dmitry, Susan Athey, David A. Hirshberg, Guido W. Imbens, and
Stefan Wager. "Synthetic Difference-in-Differences." *American Economic
Review* 111, no. 12 (2021): 4088–4118.

Ben-Michael, Eli, Avi Feller, and Jesse Rothstein. "The Augmented Synthetic
Control Method." *Journal of the American Statistical Association* 116, no.
536 (2021): 1789–1803.

Xu, Yiqing. "Generalized Synthetic Control Method: Causal Inference with
Interactive Fixed Effects Models." *Political Analysis* 25, no. 1 (2017):
57–76.
