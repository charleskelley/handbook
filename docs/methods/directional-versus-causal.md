---
title: "Directional versus causal"
type: general
owner: ds-lead
audience: [all]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [causal, principles, experimentation]
sources:
  - "Holland, Statistics and Causal Inference, Journal of the American Statistical Association 81(396), 1986"
  - "Gordon, Zettelmeyer, Bhargava, and Chapsky, A Comparison of Approaches to Advertising Measurement, Marketing Science 38(2), 2019"
---

# Directional versus causal

The principle the experiment and causal pages rest on: what separates a
statement that something moved from a statement that an action moved it, and
what evidence each one needs. Every analyst and every partner who reads an
analysis should be able to tell which kind of statement they are looking at.

## Three kinds of statement

| Kind | What it says | Example | What it needs |
|---|---|---|---|
| Descriptive | What happened | Customers who received the email spent 12% more than those who did not | Correct data and a correct calculation |
| Directional | What the evidence leans toward, without a design that rules out other explanations | The email was probably worth sending | A description, and a judgment that nothing else obvious explains it |
| Causal | What the action changed, compared with what would have happened without it | The email raised spend by 3%, give or take 2 | A comparison group that stands in for what would have happened, and a reason to believe it does |

Most disputes over an analysis come from a descriptive result being read as a
causal one. The 12% and the 3% above can both be true of the same campaign.
The first includes every reason the two groups differ. The second is the
email's own contribution.

Directional is a legitimate grade of evidence, and often all there is. The
failure is not in giving a directional answer. It is in giving one without
saying so.

## What a causal claim is

A causal claim compares two worlds: the one in which the action was taken and
the one in which it was not, for the same customers over the same time. Only
one of them is ever observed. A customer either got the email or did not.
The outcome in the world that did not happen is called the counterfactual,
and every method of causal analysis is a way of estimating it.

Two consequences follow.

- **Effects are for groups.** The effect on one customer cannot be observed.
  The average effect over a group can be estimated, if a second group stands
  in for the first group's counterfactual.
- **The comparison group is the whole question.** The untreated group must be
  what the treated group would have been without the treatment. Every reason
  it might not be is a reason the estimate is wrong, and the list of such
  reasons is the same from one analysis to the next.

## Why a plain comparison misleads

| Reason | What happens | A business case | The sign of it |
|---|---|---|---|
| Selection | Those who got the action were chosen, or chose themselves, for reasons tied to the outcome | Marketing sends the offer to its best customers, who then spend more than the rest | The groups already differed before the action |
| It would have happened anyway | The action is aimed at people about to do the thing | A discount shown to customers already at checkout. An ad shown to people searching for the brand by name | The effect disappears when the action is withheld from a random few |
| Confounding | Something else drives both the action and the outcome | Stores that got the new layout are also the ones in growing towns | A third factor differs between the groups |
| Reverse causation | The outcome drives the action | Heavy users contact support more. Contacting support did not make them heavy users | The order in time is unclear or the wrong way round |
| Regression to the mean | Units picked because they were extreme are less extreme next time, with no action at all | The worst-performing stores improve after an intervention. So do the worst-performing stores that got none | The group was selected on the outcome |
| Trend and season | The outcome was moving anyway | Sales after the campaign are higher than before. It launched in November | Before and after are different times of year, or the line was already rising |
| Survivorship | Only those who lasted are observed | Long-standing customers are more satisfied. The dissatisfied ones left | The group is defined by something that happened after the start |
| A change in measurement | The way the outcome is recorded changed | Conversions rise the week a new tracking tag goes live | The step is sudden and coincides with a system change |

Larger data does not help with any of these. A biased comparison on ten
million customers is a precise estimate of the wrong number.

## Grades of evidence

What stands in for the counterfactual sets the grade. The grade sets what may
be said.

| Grade | Design | What stands in for the counterfactual | What must be believed | Page |
|---|---|---|---|---|
| A | Randomized experiment | A group left out by chance | That the randomization and the measurement were carried out as designed | [Experiments and lift tests](experiments-and-lift-tests.md) |
| B | A quasi-experiment with its assumptions checked | A comparison group that moved in step with the treated one beforehand, or a rule that assigned treatment at a threshold | That the two would have kept moving in step, or that units either side of the threshold are alike | [Difference-in-differences](difference-in-differences.md), [synthetic control](synthetic-control.md) |
| C | Observational adjustment | Untreated units made alike on measured characteristics | That nothing unmeasured drove both the action and the outcome | [Matching](matching.md) |
| D | Before and after, or treated against untreated, unadjusted | The past, or whoever was not treated | That nothing else changed, or that the groups were alike. Usually false | [Measuring impact without an experiment](measuring-impact-without-an-experiment.md) |
| E | Attribution reports and anecdote | Nothing | That every sale touched by the action was caused by it | |

Grades A and B support a causal statement, B with its assumption attached.
Grade C supports a directional statement. Grades D and E describe, and
support a directional statement only when nothing else could plausibly
explain the result. Designs not in the table are graded on
[measuring impact without an experiment](measuring-impact-without-an-experiment.md):
a cut-off rule and a randomized invitation belong in grade B, plain
regression adjustment and a marketing mix model in grade C.

A grade is not a ranking of effort or of statistical sophistication. A simple
difference in means from a randomized test outranks an elaborate model fitted
to observational data. And a lower grade is not a different estimate of the
same thing with wider error bars: it can be wrong in sign.

## Saying it

The wording carries the grade. Use the row that matches the design.

| Grade | Say | Do not say |
|---|---|---|
| A | "The offer raised conversion by 0.5 points, with an interval from 0.05 to 0.95" | |
| B | "We estimate the change raised sales by about 6%, on the assumption that the two regions would otherwise have moved together, which they did for the prior year" | "The change raised sales by 6%" |
| C | "Among customers alike on tenure, spend, and region, those in the programme spent 4% more. We cannot rule out differences we did not measure" | "The programme drives a 4% lift" |
| D | "Sales rose 9% after the launch. We have no basis for saying how much was the launch" | "The launch drove a 9% increase" |
| E | "The tool credits the campaign with 4,950 orders. That is the number of buyers who were sent it, not the number it added" | "The campaign generated 4,950 orders" |

The verbs *drove*, *caused*, *raised*, *lifted*, *generated*, and *impact*
are causal claims. *Was associated with*, *moved with*, and *was followed by*
are not.

## When directional is enough

Whether a decision needs causal evidence depends on the decision, not on the
taste of the analyst.

- **Directional is enough** when the action is cheap, easy to reverse, and
  the cost of being wrong is small, or when the decision would be the same
  across the whole plausible range of the effect.
- **Causal evidence is needed** when money is being moved on the strength of
  the number: a budget reallocated, a programme scaled or cut, a price
  changed. It is also needed when the same directional result will be quoted
  again as a fact, and when the people who took the action are the ones
  measuring it.

Where causal evidence is needed and an experiment is possible, running one is
often cheaper than the argument over an observational estimate.

## Before the analysis

Write these down before looking at outcomes. Choosing them afterwards, with
the results in view, is how an analysis ends up finding what was hoped for.

| Item | The question |
|---|---|
| The decision | What will be done differently depending on the answer? |
| The action | What exactly was done, or would be done, to whom? |
| The comparison | Against what: nothing, the usual treatment, the previous version? |
| The units | Customers, stores, regions, weeks? |
| The outcome | Which measure, over what window, from what dataset? |
| The size that matters | What is the smallest effect that would change the decision? |
| The design | Which grade above, and why not a higher one? |
| What would count against it | What result would show the comparison group was not a fair stand-in? |

## What experiments have shown about marketing measurement

Three studies are worth knowing by name, because they tested the usual
methods against experiments at scale.

- Gordon, Zettelmeyer, Bhargava, and Chapsky (2019) took advertising
  experiments run at Facebook and re-analysed them with the observational
  methods in common use, to see whether those methods recovered the
  experimental answer. They often did not, even with rich data on each user.
- Blake, Nosko, and Tadelis (2015) studied what happened when eBay switched
  off paid search advertising: advertisements on searches for the brand's
  own name on some search engines, and other search advertisements in a
  random set of regions. For searches on the brand's name, the traffic
  arrived anyway through unpaid results. The clicks the ads had been credited
  with were largely customers who would have come regardless.
- Lewis and Rao (2015) showed, from a set of large advertising experiments,
  that the effect of a campaign is small compared with the natural variation
  in what individual customers spend. Even an experiment with millions of
  customers can leave the return on a campaign uncertain, and an
  observational estimate is very unlikely to resolve it.

The lesson is not that marketing does not work. It is that the size of its
effect cannot be read from who bought.

## Related pages

- [Causal diagrams](causal-diagrams.md): a way to draw the reasons in the
  table above for a particular analysis and decide what to adjust for.
- [Stating uncertainty](stating-uncertainty.md): how to report the "give or
  take" that every estimate carries.
- [Experiments and lift tests](experiments-and-lift-tests.md): the design that
  earns grade A, and how to read a lift reported by a tool.
- [Measuring impact without an experiment](measuring-impact-without-an-experiment.md):
  how to choose a design when randomization is not possible.
- [Decomposing a change](decomposing-a-change.md): a descriptive method often
  mistaken for a causal one.

## Further reading

Holland, Paul W. "Statistics and Causal Inference." *Journal of the American
Statistical Association* 81, no. 396 (1986): 945–960. The clearest statement
of why a causal effect on one unit cannot be observed and what follows from
that.

Hernán, Miguel A., and James M. Robins. *Causal Inference: What If.* Chapman
& Hall/CRC, 2020. Part I is the best plain introduction to counterfactuals,
randomized experiments, and what observational analysis has to assume.

Angrist, Joshua D., and Jörn-Steffen Pischke. *Mostly Harmless Econometrics:
An Empiricist's Companion.* Princeton University Press, 2009. The applied
economist's view of the same ground, organised by research design. Their
*Mastering 'Metrics* (Princeton University Press, 2014) is the gentler
version.

Cunningham, Scott. *Causal Inference: The Mixtape.* Yale University Press,
2021. A readable tour of the designs with worked examples.

Pearl, Judea, and Dana Mackenzie. *The Book of Why: The New Science of Cause
and Effect.* Basic Books, 2018. A non-technical account, good to share with a
partner outside the team.

Gordon, Brett R., Florian Zettelmeyer, Neha Bhargava, and Dan Chapsky. "A
Comparison of Approaches to Advertising Measurement: Evidence from Big Field
Experiments at Facebook." *Marketing Science* 38, no. 2 (2019): 193–225.

Blake, Thomas, Chris Nosko, and Steven Tadelis. "Consumer Heterogeneity and
Paid Search Effectiveness: A Large-Scale Field Experiment." *Econometrica*
83, no. 1 (2015): 155–174.

Lewis, Randall A., and Justin M. Rao. "The Unfavorable Economics of Measuring
the Returns to Advertising." *The Quarterly Journal of Economics* 130, no. 4
(2015): 1941–1973.
