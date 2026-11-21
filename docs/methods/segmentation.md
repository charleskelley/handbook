---
title: "Segmentation"
type: method
depth: guide
owner: ds-lead
audience: [ds, analyst, product]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [descriptive, customers, clustering]
sources:
  - "Wedel and Kamakura, Market Segmentation: Conceptual and Methodological Foundations, 2nd ed., Kluwer Academic Publishers, 2000"
  - "Dolnicar, Grün, and Leisch, Market Segmentation Analysis, Springer, 2018"
---

# Segmentation

Dividing customers into groups that will be treated differently. The
statistics are the easy part. The hard part is ending with groups the
business can find, reach, and act on.

## What it is

Any rule that assigns each customer to one of a small number of groups, with
the intent that customers in a group are alike in a way that matters and
different from the other groups. The rule can be written by hand, such as
spend above a threshold, or found from data by a clustering algorithm. Either
way the output is the same: an assignment for every customer, a description
of each group, and a reason to treat the groups differently. A segmentation
is a tool for a decision. It is not a discovery about the customers, and a
clustering algorithm will return groups from any data, including data with no
groups in it.

## When it is the right choice

- The business is about to treat customers differently, in offers, service,
  contact frequency, or price, and needs a small number of groups to design
  for.
- A report on the customer base needs a breakdown that stays the same from
  one period to the next.
- A first look at a new customer base, as exploration, with the result read
  as a description and not yet as groups to act on.

## When it is not

- **Nobody will act on the groups.** A segmentation that changes no decision
  is a slide. Ask what will be done differently for each group before
  building it.
- **The decision is about individuals.** If each customer can be scored and
  treated one by one, a model that predicts the outcome for each customer
  does better than a handful of groups. See
  [churn and propensity models](churn-and-propensity.md).
- **The question is who will respond to an action.** Groups built on past
  behaviour say who buys, not who can be changed. That is
  [uplift modeling](uplift-modeling.md), and it needs an experiment.
- **A simple rule already does the job.** If recency and frequency separate
  the customers the business cares about, [RFM analysis](rfm-analysis.md) is
  the segmentation.

## What makes a segment useful

A set of segments is judged on these. They come from the marketing
literature, and they are stricter than any statistical measure of how good
the clusters are.

| Test | The question |
|---|---|
| Actionable | Is there something the business would do differently for this group? |
| Identifiable | Can each customer be assigned from data the business holds, including a new customer? |
| Reachable | Can the group be addressed through a channel the business has? |
| Substantial | Is the group large enough, in customers or value, to be worth a separate treatment? |
| Differently responsive | Do the groups respond differently to what the business does? This is the test most often skipped and the one that matters most |
| Stable | Does a customer stay in a group long enough for the treatment to apply, and do the groups reappear when the analysis is rerun? |

## What to segment on

| Basis | Examples | Strength | Weakness |
|---|---|---|---|
| Who they are | Age, region, industry, company size | Easy to identify and reach | Often a weak guide to behaviour |
| What they did | Recency, frequency, categories bought, channel used, response to offers | In the data, and predictive of what they do next | Describes the past, including the effect of past marketing |
| What they are worth | Profit to date, predicted value | Ties directly to how much to spend on them | Says nothing about why, or what they want |
| What they need | Stated preferences, reasons for buying, from a survey | Closest to why they buy | Known only for those surveyed. Hard to assign to the rest |
| Where they are in their life with the business | New, active, lapsing, lapsed | Maps to actions the business already takes | Needs agreed definitions |

Mixing bases in one clustering usually gives groups that are hard to
describe. A common pattern is to segment on one basis and profile on the
others.

## Common approaches

| Approach | What it needs | What it rests on | Main weakness |
|---|---|---|---|
| Business rules: thresholds set by hand | A few measures and agreed cut points | Judgment about where the cuts belong | The cuts are arbitrary until tested against behaviour |
| Value tiers: deciles or bands of spend or profit | A value for each customer | That value alone is the dimension that matters | Customers of equal value can need opposite treatment |
| [RFM](rfm-analysis.md) grid | Transaction history | Recency and frequency as the main signs of activity | No view of what customers buy or want |
| K-means clustering | Numeric features, scaled; a chosen number of clusters | Clusters that are roughly round and of similar size in the scaled space | Returns the number of clusters asked for whether or not they exist. Sensitive to scaling and to outliers |
| Hierarchical clustering | A distance between customers | The distance measure chosen | Does not scale to large customer counts without sampling. An early merge is never undone |
| Model-based clustering: mixture and latent class models | A probability model for the features | That the model's form fits | More to specify and check. Gives each customer a probability of belonging to each group, which is more honest and harder to use |
| Tree-based segments: a decision tree on an outcome | An outcome to split on | That the outcome is the right one to separate customers by | The segments are built to differ on one outcome and may not differ on anything else |
| Needs-based segmentation from a survey | A survey, and a way to assign unsurveyed customers | That stated needs are real and stable | The link from survey segment to customer record is usually weak |

Start with rules or RFM. Move to clustering when there are more than three
or four dimensions that matter and no obvious way to cut them by hand.

### Clustering in practice

The steps are the same whichever algorithm is used, and each is a choice that
changes the answer.

1. **Choose features for the decision.** Every feature included has a vote.
   Ten features about product mix and one about value will give segments
   about product mix.
2. **Transform and scale.** Spend and order counts are heavily skewed. Left
   alone, a few very large customers define the clusters. Take logarithms or
   ranks, then put the features on a common scale. Features that measure the
   same thing twice count twice.
3. **Choose the number of clusters.** There is no correct number. Indices
   such as the silhouette width and the gap statistic compare solutions.
   They often disagree, and often show no clear winner, which is itself
   information: the customers may lie along a continuum with no gaps. In
   that case any number of clusters is a convenient cut, not a structure,
   and should be presented as one.
4. **Check stability.** Rerun on resamples of the customers and with
   different starting points. For each original cluster, find the cluster in
   the rerun that shares most of its customers and measure the overlap.
   Clusters that do not reappear are not there.
5. **Profile on what was left out.** Describe each cluster by variables not
   used to build it: value, later behaviour, response to past campaigns. If
   the clusters differ only on the features that built them, they have shown
   nothing.
6. **Name by what distinguishes.** A name is a claim. Define each segment by
   its rule or its centre, and keep the name close to the numbers.
7. **Write the assignment rule.** A new customer, and next month's version
   of an existing one, must be assignable without refitting. Refitting moves
   every boundary. For a clustering, the rule is the stored transformation
   and scaling followed by assignment to the nearest cluster centre, or a
   simple classifier trained to reproduce the clusters.
8. **Track movement.** With a fixed assignment rule, the number of customers
   moving between segments each period shows whether the segments are stable
   enough to act on.

## Reading a result you did not produce

Questions to ask of a segmentation from an agency, a tool, or another team.

- **What decision was it built for, and who makes it?** If the answer is
  general understanding, expect it not to be used.
- **What went in?** Ask for the feature list, how each was scaled, and how
  outliers were treated. The segments are a restatement of those choices.
- **How was the number of segments chosen?** "Five felt right" is an honest
  answer. A claim that the data contains five segments needs the evidence:
  the indices, and the stability checks.
- **Do the segments differ on anything that was not used to build them?**
  Ask for value, retention, and response by segment.
- **Do they respond differently?** A segmentation is worth separate
  treatments only if a treatment works better in one segment than another.
  That is a claim about cause, and only a test by segment shows it.
- **Can every customer be assigned today?** A survey-based segmentation with
  no rule for the unsurveyed covers only the sample. Ask what share of
  customers the assignment rule classifies, and how often it is right for
  those surveyed.
- **How big is each segment, in customers and in value?** One segment with
  most of the customers and four slivers is a threshold, not a segmentation.
- **How long does a customer stay in a segment?** Ask for the movement table
  between two dates.
- **Are the names doing the work?** Read the table of segment averages with
  the names covered. If the differences are small, the names are the
  finding.
- **Is it a snapshot of marketing?** Behaviour reflects what the business
  did to each customer. Customers who received offers bought on offer.

## Where it applies to our data

*Add: the segmentations in use in the business, where each is defined, who
owns it, and the decision it serves.* Why: a new segmentation competes with
the ones already in people's heads.

*Add: for each, the assignment rule and the dataset that carries the
assignment, linked to its page under Data.* Why: a segment that cannot be
looked up for a customer cannot be acted on.

*Add: the evidence, if any, that the segments respond differently to an
action.* Why: this is what separates a segmentation from a description.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Further reading

Smith, Wendell R. "Product Differentiation and Market Segmentation as
Alternative Marketing Strategies." *Journal of Marketing* 21, no. 1 (1956):
3–8. Where the idea comes from. Segmentation as a strategy choice, not a
statistical procedure.

Wedel, Michel, and Wagner A. Kamakura. *Market Segmentation: Conceptual and
Methodological Foundations.* 2nd ed. Kluwer Academic Publishers, 2000. The
reference for the criteria a segmentation is judged on and for model-based
methods.

Dolnicar, Sara, Bettina Grün, and Friedrich Leisch. *Market Segmentation
Analysis: Understanding It, Doing It, and Making It Useful.* Springer, 2018.
A step-by-step account of a whole segmentation project, strong on the point
that clusters are usually constructed, not found.

Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. *The Elements of
Statistical Learning: Data Mining, Inference, and Prediction.* 2nd ed.
Springer, 2009. The chapter on unsupervised learning covers the clustering
algorithms themselves.

Tibshirani, Robert, Guenther Walther, and Trevor Hastie. "Estimating the
Number of Clusters in a Data Set via the Gap Statistic." *Journal of the Royal
Statistical Society, Series B* 63, no. 2 (2001): 411–423. One of the standard
indices for choosing the number of clusters, and a clear statement of why the
problem is hard.

Rousseeuw, Peter J. "Silhouettes: A Graphical Aid to the Interpretation and
Validation of Cluster Analysis." *Journal of Computational and Applied
Mathematics* 20 (1987): 53–65. The silhouette width.

Hennig, Christian. "Cluster-Wise Assessment of Cluster Stability."
*Computational Statistics & Data Analysis* 52, no. 1 (2007): 258–271. How to
test whether each cluster reappears under resampling.
