---
title: "Framing and evaluating a prediction"
type: method
depth: build
owner: ds-lead
audience: [ds, mle, analyst]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [predictive, evaluation, modeling]
sources:
  - "Provost and Fawcett, Data Science for Business, O'Reilly, 2013"
  - "Kaufman, Rosset, Perlich, and Stitelman, Leakage in Data Mining: Formulation, Detection, and Avoidance, ACM Transactions on Knowledge Discovery from Data 6(4), 2012"
---

# Framing and evaluating a prediction

The two ends of every modelling project: stating exactly what is to be
predicted, for whom, when, and for what decision; and showing that the model
does it better than what the business does now. Every model page on this
site leans on this one. Most models that fail in use were framed wrongly or
evaluated on data they had already seen, and no choice of algorithm repairs
either.

## What it is

A discipline with two parts. **Framing** turns a business request, such as
"predict churn", into a prediction problem that can be built and checked: a
unit, a moment at which the prediction is made, an outcome with a definition
and a window, the information available at that moment, and the decision the
prediction feeds. **Evaluation** estimates how well the model will do on
cases it has not seen, at the moment it will be used, measured in terms that
relate to the decision, and compared with a simple baseline. The two are one
subject because the evaluation can only be as honest as the framing is
exact. A model evaluated on the wrong population, or with information it
will not have in use, has a score that describes nothing.

## When it is the right choice

- Before any model is built, however simple.
- When a model built by someone else, a vendor's score for instance, is
  proposed for use.
- When a model in use is retrained or replaced, to show the new one is
  better on the same terms.
- When a request arrives as "can we predict X", to find out whether a
  decision is waiting for the answer.

## When it is not

- **The question is what an action will change.** A prediction says what
  will happen. It does not say what would happen if the business
  intervened. See [directional versus causal](directional-versus-causal.md)
  and [uplift modeling](uplift-modeling.md).
- **No decision depends on it.** A prediction nobody acts on has no value to
  measure. Frame the decision first: the [decision
  inventory](../business/decisions.md) is where the business's decisions are
  listed.
- **The question is about a group, not individuals.** How many customers
  will leave next quarter is a forecast: see
  [time-series forecasting](time-series-forecasting.md).

## The framing

Written down before any data is pulled. Each item is a choice, and most
projects that go wrong went wrong at one of them.

| Item | The question | Example |
|---|---|---|
| Decision | What will be done differently for a high prediction than a low one, by whom, how often? | The retention team calls 1,000 customers a month |
| Unit | One row is one what? | A customer, as of a date |
| As-of date | At what moment is the prediction made? | The first day of each month |
| Population | Which units are scored? | Customers with an order in the last 120 days, not already in a retention programme |
| Outcome | What exactly is predicted, defined from which data? | No purchase in the 120 days after the as-of date |
| Outcome window | Over what period is the outcome observed? | 120 days |
| Gap | How long between the as-of date and when the prediction can be acted on? Where it is long, the outcome window starts when it ends | 7 days for the list to reach the team |
| Observation window | How far back may features look? | 24 months before the as-of date |
| Capacity and cost | How many can be acted on, and what does one action cost? | 1,000 a month, 5 each |
| Baseline | What decides today? | A rule: the customers longest since their last order |
| Success | What must be true for the model to be used? | More true leavers among the 1,000 called than the rule finds |

![A timeline. A long bar on the left is the observation window, from which features are built. A vertical line marks the as-of date, when the prediction is made. After a short gap, a bar on the right is the outcome window, from which the label is taken.](../assets/prediction-timeline-light.svg#only-light)
![A timeline. A long bar on the left is the observation window, from which features are built. A vertical line marks the as-of date, when the prediction is made. After a short gap, a bar on the right is the outcome window, from which the label is taken.](../assets/prediction-timeline-dark.svg#only-dark)

*Features come only from the left of the as-of date. The label comes only
from the right.*

The as-of date is the centre of it. A training set is built by choosing one
or more past as-of dates and, for each, reconstructing what was known on
that date and what happened afterwards. In use, the as-of date is today and
the outcome has not happened.

## Leakage

Leakage is information reaching the model in training that it will not have
when used. It is the most common reason a model looks excellent in
development and fails in use. Three kinds:

- **From the future.** A feature computed with data from after the as-of
  date: a customer's total orders taken from today's table, a status field
  that was updated when they cancelled, an account closure reason. The
  commonest form is building features from a current snapshot of a table
  and not from its state on the as-of date.
- **From the outcome.** A feature that is a consequence or a restatement of
  the outcome: "received a win-back offer" in a churn model, "has a
  delivery date" in a model of whether an order will ship.
- **Across the split.** The same customer in both the training and the test
  data, rows from the same period on both sides, or a preprocessing step,
  such as scaling or filling missing values, fitted on all the data before
  it was split.

The defence is the timeline: for every feature, know the moment its value
became known, and require that to be before the as-of date.

## Splitting the data

The test data stands in for the future. It must be related to the training
data as the future will be.

- **Split by time.** Train on earlier as-of dates and test on later ones. A
  random split of rows lets the model learn the conditions of a period and
  be tested on the same period, and overstates how well it will do next
  quarter.
- **Units that repeat.** Where the model will go on scoring the same units it
  was trained on, as a churn model scores the same customers month after
  month, a split by time is enough, and a customer appears on both sides at
  different dates. Where it will score units it has never seen, also keep
  each unit wholly on one side.
- **No training outcome from the test period.** Drop the training rows whose
  outcome window runs past the first validation or test as-of date. With
  monthly as-of dates and a 120-day window, those are the last four months
  of training dates. Otherwise the model is fitted with outcomes that had
  not happened when the test predictions were made.
- **Three sets, not two.** Training data to fit, validation data to choose
  between models and settings, and test data used once at the end. A test
  set that has been used to make choices is no longer a test.
- **More than one test period** where possible. Performance in one quarter
  can be luck or an unusual quarter.

## Baselines

A model's score means nothing alone. Compare with, in order:

1. **The base rate.** Predict the average for everyone.
2. **What the business does now.** The existing rule or list.
3. **A simple model.** [Logistic or linear regression](regression.md) on a
   handful of obvious features.

A complex model earns its place by beating the simple one by enough to
matter to the decision. Often it does not, and the simple model is the right
thing to deploy.

## Measures

Choose the measure from the decision. No single number serves every use.

**When the decision is to act on the top of a ranked list,** which is most
marketing and retention use:

| Measure | Definition |
|---|---|
| Precision at *k* | Of the *k* highest-scored units, the share that had the outcome |
| Recall at *k* | Of all units that had the outcome, the share found in the top *k* |
| Lift at *k* | Precision at *k* ÷ the base rate. A measure of ranking. It is not the lift of an [experiment](experiments-and-lift-tests.md), which is a difference from a control group |
| Cumulative gains | Recall at each depth of the list, drawn as a curve |

Set *k* to the capacity in the framing.

**When the decision is a yes or no for each unit** at a threshold:

| Measure | Definition |
|---|---|
| Precision | Of those predicted yes, the share that were |
| Recall | Of those that were, the share predicted yes |
| False positive rate | Of those that were not, the share predicted yes |
| Area under the ROC curve | The chance that a random unit with the outcome is scored above a random unit without it. Does not depend on a threshold |
| Area under the precision-recall curve | A summary of precision across levels of recall. More informative than the ROC curve when the outcome is rare |

Accuracy, the share of predictions that were right, is useless when the
outcome is rare: predicting "no" for everyone is 95% accurate when 5% say
yes.

**When the predicted probability itself is used,** in an expected value, a
price, or a forecast of totals:

| Measure | Definition |
|---|---|
| Calibration | Among units given a probability near *p*, the share that had the outcome is near *p*. Shown as predicted against observed, in about ten bands of equal count |
| Brier score | The average squared difference between the predicted probability and the 0 or 1 outcome |
| Log loss | The average of minus the logarithm of the probability given to what happened |

A model can rank well and be badly calibrated. Check both if both matter. A
miscalibrated model that ranks well is corrected by fitting a second, simple
model from its scores to the outcomes on validation data. The two usual
forms are Platt scaling and isotonic regression.

**When the outcome is a quantity:**

| Measure | Definition | Note |
|---|---|---|
| Mean absolute error | The average size of the error | In the outcome's units. Robust |
| Root mean squared error | The square root of the average squared error | Punishes large errors |
| Bias | The average of actual − predicted, keeping the sign | Should be near zero |
| Mean absolute percentage error | The average of the size of the error ÷ actual | Undefined at zero, and lopsided. Avoid |

Every measure is an estimate from a finite test set. Give it an interval, by
the bootstrap, and report it for the baseline too: see
[stating uncertainty](stating-uncertainty.md).

## From a score to a decision

The measure that matters in the end is the value of the decisions the model
leads to. For acting on a list:

value of acting on a unit = probability of the outcome × the chance the
action changes it × what a changed outcome is worth − the cost of the action

Act on units where this is positive, up to capacity.

The middle term, the chance the action changes the outcome, is not something
any prediction model or any evaluation on historical data can supply. It is a
causal quantity. It comes from an
[experiment](experiments-and-lift-tests.md): score customers, act on a random
half of the high scorers, and compare. A model with excellent precision is
worthless if the action does nothing for the customers it finds, and the
customers most certain to leave are often the ones least able to be
persuaded. Offline evaluation shows whether the model predicts. Only a test
shows whether using it helps.

## Building the outputs

Framing record

:   The table under [the framing](#the-framing), filled in, dated, and
    agreed with the person who owns the decision. Kept with the model.

Label table

:   One row per unit and as-of date. Columns: unit identifier, as-of date,
    the outcome, the end of the outcome window, and whether the window is
    complete. Rows whose outcome window has not ended are excluded from
    training and testing.

Feature table

:   One row per unit and as-of date. Columns: unit identifier, as-of date,
    and each feature. Each feature has a recorded definition and a recorded
    time at which its value is known. Built from the data as it stood on the
    as-of date.

Split

:   A column on both tables assigning each as-of date to training,
    validation, or test, with the rule stated.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| Summary of measures | Model, with the base rate, the current rule, and the simple model as rows | Each chosen measure, with its interval, on the test set | Table |
| Gains by decile | Decile of score, highest first | Units, outcomes, rate, lift, cumulative share of outcomes | Table and cumulative curve |
| Calibration | Band of predicted probability | Units, average prediction, observed rate | Table, and points against the diagonal |
| Performance over time | Test as-of date | The main measure | Line |
| Performance by slice | Segment, tenure band, channel, region | Units, base rate, the main measure | Table |
| Value | Depth of the list | Expected value under stated assumptions about cost, worth, and the effect of acting | Table |
| Features | Feature | Permutation importance on validation data, and the direction of its relation to the outcome | Table, read for surprises |

Defaults, where nothing about the business decides otherwise:

| Choice | Default | Why |
|---|---|---|
| Split | By time, with the latest periods as test | Use is always in the future |
| Main measure | Lift and precision at the capacity in the framing | It is the decision |
| Baseline | The current rule and a regression | The comparison the business cares about |
| Threshold | Set from capacity or expected value, never 0.5 | 0.5 has no meaning for a rare outcome |
| Class imbalance | Left as it is, with a measure that suits it | Resampling distorts the probabilities |
| Reporting | Every measure with an interval and beside the baseline | A score alone is not a finding |

## Checks

Run these before believing any score.

- Every feature's value was known before the as-of date. Check the highest
  ranked features one by one.
- No as-of date is on both sides of the split, and no training outcome
  window runs into the test period. Where the model will score units it has
  not seen, no unit is on both sides either.
- The outcome rate in the label table is steady across as-of dates and
  matches the rate the business reports.
- Every label's outcome window is complete.
- The score is not too good. A model far better than anyone expected has
  usually seen the answer. Find out how before celebrating.
- No single feature carries nearly all the performance. If one does, ask
  whether it is the outcome in disguise.
- The baseline and the model are scored on the same test rows.
- The population in the test set is the population in the framing.
- Performance on the test set is close to performance on the validation
  set. A large drop means either that choices were fitted to the validation
  data or that the test period differs. Find out which.
- The same code builds features for training and for use.

## Pitfalls

- **Features from today's table.** The most common leak. Build every
  feature from data as it stood on the as-of date.
- **A random split of time-ordered data.** Overstates performance, sometimes
  greatly.
- **Tuning on the test set.** Every choice made after looking at test
  performance spends some of its honesty.
- **A measure that does not match the decision.** A high area under the
  curve does not mean the top 1,000 are well chosen.
- **Evaluating on a population the model will not be used on.** Training on
  customers who were contacted in the past, then scoring everyone.
- **Predicting what is already known.** A model that finds customers who
  have in effect already left is accurate and useless. Check how many of the
  top scorers could still be acted on.
- **A changed world.** The model was right about last year. Monitor it in
  use: see [model monitoring](development/model-monitoring.md).
- **Acting on the scores changes the labels.** Once customers with high
  scores are treated, their outcomes no longer show what the model predicts.
  Keep a random group untreated, to measure the action and to retrain on.
- **Accuracy mistaken for value.** See
  [from a score to a decision](#from-a-score-to-a-decision).

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data. A churn model is tested on 10,000 customers, of whom 500
left: a base rate of 5%.

| Decile of score | Customers | Left | Rate | Lift | Cumulative share of leavers |
|---|---|---|---|---|---|
| 1 | 1,000 | 200 | 20% | 4.0 | 40% |
| 2 | 1,000 | 100 | 10% | 2.0 | 60% |
| 3 | 1,000 | 60 | 6% | 1.2 | 72% |
| 4 to 10 | 7,000 | 140 | 2% | 0.4 | 100% |

**Against the current rule.** The team can call 1,000 customers. The rule,
the 1,000 customers longest since their last order, contains 120 who left:
precision 12%, recall 24%, lift 2.4. The model's top 1,000 are the first
decile, with 200 who left: precision 20%, recall 40%, lift 4.0. At the same
number of calls the model finds 80 more of the customers who leave.

**As a decision.** A call costs 5. A customer kept is worth 400. Suppose a
call keeps 10% of the leavers it reaches.

| Decile | Working, per customer called | Value |
|---|---|---|
| 1 | 20% × 10% × 400 − 5 | +3 |
| 2 | 10% × 10% × 400 − 5 | −1 |
| 3 | 6% × 10% × 400 − 5 | −2.6 |

Only the first decile is worth calling: 1,000 calls for a gain of 3,000.

**What the evaluation cannot tell.** The 10% is an assumption. If a call
keeps 5% of leavers, the first decile is worth 20% × 5% × 400 − 5 = −1, and
no customer is worth calling, with the same model and the same lift of 4.
The model's accuracy was never the open question. The effect of the call is,
and only a test with a random group left uncalled measures it.

## Where it applies to our data

*Add: the prediction problems the team has framed, each with a link to its
framing record and to the decision in the [decision
inventory](../business/decisions.md).* Why: a model is traced from the
decision it serves.

*Add: how the team reconstructs data as of a past date: which datasets keep
history, which hold only the current state, linked to their pages under
Data.* Why: a dataset that holds only today's values cannot supply features
for a past as-of date, and using it leaks.

*Add: the base rates and capacities of the decisions modelled so far, in
`facts/`.* Why: lift and precision at capacity cannot be read without them.

*Add: where evaluations are recorded.* Why: a retrained model is compared
with the one it replaces on the same terms. See
[experiment tracking](development/experiment-tracking.md).

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Provost, Foster, and Tom Fawcett. *Data Science for Business: What You Need
to Know about Data Mining and Data-Analytic Thinking.* O'Reilly, 2013. The
best single book on framing: expected value, ranking and lift, and tying a
model to a decision. Start here.

Kaufman, Shachar, Saharon Rosset, Claudia Perlich, and Ori Stitelman.
"Leakage in Data Mining: Formulation, Detection, and Avoidance." *ACM
Transactions on Knowledge Discovery from Data* 6, no. 4 (2012): 1–21. The
standard treatment of leakage and the idea of what was legitimately
available at prediction time.

Kapoor, Sayash, and Arvind Narayanan. "Leakage and the Reproducibility Crisis
in Machine-Learning-Based Science." *Patterns* 4, no. 9 (2023): 100804. A
taxonomy of the kinds of leakage and how often each occurs in published
work.

Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. *The Elements of
Statistical Learning: Data Mining, Inference, and Prediction.* 2nd ed.
Springer, 2009. The chapter on model assessment and selection covers
training, validation, and test error and why they differ.

Saito, Takaya, and Marc Rehmsmeier. "The Precision-Recall Plot Is More
Informative than the ROC Plot When Evaluating Binary Classifiers on
Imbalanced Datasets." *PLOS ONE* 10, no. 3 (2015): e0118432. Which curve to
use when the outcome is rare.

Niculescu-Mizil, Alexandru, and Rich Caruana. "Predicting Good Probabilities
with Supervised Learning." In *Proceedings of the 22nd International
Conference on Machine Learning*, 625–632. ACM, 2005. Which kinds of model
give calibrated probabilities and how to correct those that do not.

Mitchell, Margaret, Simone Wu, Andrew Zaldivar, and others. "Model Cards for
Model Reporting." In *Proceedings of the Conference
on Fairness, Accountability, and Transparency*, 220–229. ACM, 2019. A
template for what to record about a model, including performance by slice.
