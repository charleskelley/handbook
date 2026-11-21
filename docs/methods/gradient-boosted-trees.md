---
title: "Gradient-boosted trees"
type: method
depth: guide
owner: ds-lead
audience: [ds, mle]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [predictive, modeling, machine-learning]
sources:
  - "Friedman, Greedy Function Approximation: A Gradient Boosting Machine, The Annals of Statistics 29(5), 2001"
  - "Hastie, Tibshirani, and Friedman, The Elements of Statistical Learning, 2nd ed., Springer, 2009"
---

# Gradient-boosted trees

The default algorithm for prediction from tables of customer, order, and
product data, and the step up from a [regression](regression.md) baseline
when the regression is not enough. This page is a guide to what the method
does, what its settings mean, and how to read a model someone else built with
it. The mathematics is in the reading at the end.

## What it is

A gradient-boosted tree model is a large collection of small decision trees
whose predictions are added together. A decision tree splits the data by a
sequence of yes-or-no questions about the inputs, such as whether recency is
above 60 days, and predicts a value for each resulting group. One small tree
is a crude model. Boosting builds many in sequence, each one fitted to the
errors left by the sum of those before it, and each added with a small
weight so that no single tree dominates. After a few hundred or a few
thousand trees, the sum can represent curved relationships and interactions
between inputs that a regression would need to be told about by hand. In
most implementations it works on numeric and categorical inputs on any scale
and tolerates missing values, and on tabular data it is consistently among the most accurate
methods available.

## When it is the right choice

- A [regression](regression.md) baseline exists, and there is reason to
  think it is missing structure: thresholds, saturation, interactions.
- There are thousands of rows or more, and many candidate inputs.
- Predictive accuracy is what is being bought, and a full account of how
  each input enters is not required.
- The inputs are a mix of types and scales, with missing values.

## When it is not

- **Small data.** With a few hundred rows a flexible model fits noise. Use
  regression.
- **The model must be explained input by input** to a regulator, a customer,
  or a sceptical partner. The explanation tools below are approximations.
- **Predictions are needed outside the range of the training data.** A tree
  predicts a constant beyond the last split. It cannot continue a trend, so
  a tree model alone forecasts a growing series badly. See
  [time-series forecasting](time-series-forecasting.md).
- **The question is what would happen if an input were changed.** The model
  describes association in the training data. See
  [causal diagrams](causal-diagrams.md).
- **It does not beat the regression by enough to matter.** A more complex
  model costs more to run, monitor, and explain. Keep the simpler one.

## How it works

1. Start with a constant prediction: the average outcome.
2. Compute, for every row, how far off the current prediction is and in
   which direction. For a squared-error objective this is the residual. For
   other objectives it is the gradient of the loss, which is where the name
   comes from.
3. Fit a small tree to those errors.
4. Add that tree's predictions to the model, multiplied by a small number,
   the learning rate.
5. Repeat from step 2, hundreds or thousands of times.
6. Stop when performance on held-out validation data stops improving.

Each tree corrects a little of what is still wrong. Small steps, many of
them, and stopping at the right time are what keep the model from simply
memorising the training data.

## The settings that matter

Implementations expose dozens of settings. A handful decide most of the
result.

| Setting | What it controls | Guidance |
|---|---|---|
| Number of trees | How long boosting runs | Do not choose it. Set it high and let early stopping decide |
| Learning rate | The weight on each tree | Lower is generally better and needs more trees. A value between 0.01 and 0.1 is typical |
| Early stopping | Halts when the validation measure has not improved for a set number of rounds, each round adding one tree | Always on. The validation data must come after the training data in time. The final model is commonly refitted on training and validation data together with the number of trees found |
| Tree size | Depth, or number of leaves | The main control on complexity. Small trees, of depth 3 to 8, are usual. Deeper trees capture higher-order interactions and overfit sooner |
| Minimum rows per leaf | The smallest group a tree may predict for | Raise it for small or noisy data |
| Row and column sampling | Each tree sees a random share of rows and inputs | Values a little below 1 reduce overfitting and speed up fitting |
| Objective | What is being minimised | Logistic loss for yes-or-no, squared error for amounts, and others for counts, skewed amounts, and quantiles. Match it to the outcome |
| Monotonic constraints | Force the prediction to rise, or fall, with a given input | Use where the direction is known. It stabilises the model and makes it easier to defend |

Tune on validation data, never on the test data. A sensible untuned model
is usually within a small margin of a carefully tuned one, and the margin is
often smaller than the difference between two test periods. Time spent on
the inputs and on the framing pays more than time spent on settings.

## What it does and does not do for you

| It handles | It does not handle |
|---|---|
| Curved relationships and thresholds | Leakage. It will find and exploit any input that carries the answer, more eagerly than a regression would |
| Interactions between inputs | A changed world. It predicts from the patterns of the training period |
| Inputs on different scales, with no transformation | Extrapolation beyond the training range |
| Missing values, as a category of their own | Causal questions |
| Irrelevant inputs, mostly | Calibration, reliably. Check predicted probabilities against outcomes, above all if the classes were reweighted or resampled to deal with a rare outcome. The correction is on the [framing page](framing-and-evaluating-a-prediction.md#measures) |
| Skewed inputs | Categories with very many levels, such as product or postcode, without care: group the rare levels, or use an implementation built for them |

Everything on the page on
[framing and evaluating a prediction](framing-and-evaluating-a-prediction.md)
applies unchanged. The algorithm is the smallest part of a model.

## Reading the model

A boosted model has no coefficients. Three kinds of summary stand in for
them, and each can mislead.

- **Importance by gain or by split count.** How much each input contributed
  to the trees' splits. Built in and quick. It favours inputs with many
  distinct values, and says nothing about direction.
- **Permutation importance.** How much held-out performance falls when one
  input's values are shuffled. It measures what the model relies on. When
  two inputs carry the same information, shuffling one does little, and both
  look unimportant.
- **SHAP values.** For each prediction, an amount attributed to each input
  such that the amounts add up to the prediction's difference from the
  average. For a yes-or-no model the amounts are usually in log-odds, not
  probability. Averaged over rows they give an importance, and plotted against
  an input's value they show the shape of its relationship. They are the
  most informative of the three and the most over-read.

A fourth tool, the partial dependence plot, shows the average prediction as
one input is varied with the others left as they are.

The cautions are the same for all of them:

- **They describe the model, not the world.** A large attribution to
  "number of support contacts" means the model uses it to predict leaving.
  It does not mean that reducing contacts would reduce leaving.
- **Correlated inputs share credit arbitrarily.** The split of importance
  between recency and days since last visit is not a finding.
- **An input that dominates is a suspect.** The first question about the top
  feature is when its value becomes known.
- **A local explanation is not a reason code.** Telling a customer or an
  agent "you were flagged because of X" needs care that the attribution
  does not supply.

## Common approaches

| Approach | What it needs | What it rests on | Main weakness |
|---|---|---|---|
| A single decision tree | Little | One set of splits | Unstable and inaccurate. Useful as a picture, not as a model |
| Random forest | Little tuning | The average of many deep trees, each fitted to a random sample of rows and inputs | Usually a little less accurate than boosting. Large models |
| Gradient boosting, as first described | A learning rate and a tree size | Trees added in sequence to reduce a loss | Slow in its plain form |
| The widely used open-source implementations | The same, plus early stopping | The same idea with regularisation, faster ways of finding splits, and native handling of missing and categorical values | Many settings, and defaults that differ from one to another. Results are close when each is used well |
| Histogram-based boosting in general machine-learning libraries | Fewer settings | The same idea, with inputs binned for speed | Fewer features than the dedicated libraries |
| Neural networks on tabular data | Much more data and tuning | Learned representations | On typical business tables, generally no better than boosted trees and harder to run |

The choice among boosting implementations matters much less than using any
one of them carefully. Pick the one the platform supports and the team
knows: see [experiment tracking](development/experiment-tracking.md).

## Reading a result you did not produce

Questions to ask of a boosted model built by a vendor, a tool, or another
team.

- **What is it compared with?** Ask for the same measure for the current
  rule and for a logistic regression on the same inputs. A boosted model
  reported alone has not shown it was needed.
- **How was the data split?** If rows were split at random and the data
  spans time, the reported performance is optimistic.
- **What are the top inputs, and when is each known?** Go down the
  importance list asking whether each value would be available at the
  moment of prediction. This finds most leaks.
- **What was the validation data used for, and what was the test data used
  for?** If settings were tuned against the reported number, it is
  optimistic.
- **How many rows, how many positive outcomes, how many inputs?** Hundreds
  of inputs and a few hundred events is a model of noise.
- **Are the probabilities used as probabilities?** If so, ask for the
  calibration table.
- **How does it do by period and by segment?** An average can hide a
  segment where it fails.
- **Is an importance chart being read as a list of causes?** This is the
  most common misuse. See
  [regression](regression.md#coefficients-are-not-causes).
- **What happens when it is retrained?** If the ranking of inputs or of
  customers changes a great deal between two fits, the model is unstable.
- **How will it be monitored?** See
  [model monitoring](development/model-monitoring.md).

## Where it applies to our data

*Add: the models in use built with boosted trees, each with the baseline it
was compared with and by how much it won.* Why: the margin over the simple
model is the case for the complexity.

*Add: the implementation the platform supports and the settings the team
starts from.* Why: so that models differ in their inputs, not in arbitrary
defaults.

*Add: the inputs with a known direction of effect, for which monotonic
constraints are used.* Why: a constraint agreed once is applied the same way
each time.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Further reading

Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. *The Elements of
Statistical Learning: Data Mining, Inference, and Prediction.* 2nd ed.
Springer, 2009. The chapters on trees, on boosting and additive trees, and on
random forests are the standard textbook account. The gentler version is in
James, Witten, Hastie, and Tibshirani, *An Introduction to Statistical
Learning*, 2nd ed., Springer, 2021.

Friedman, Jerome H. "Greedy Function Approximation: A Gradient Boosting
Machine." *The Annals of Statistics* 29, no. 5 (2001): 1189–1232. The paper
that defined the method, and introduced partial dependence plots.

Breiman, Leo. "Random Forests." *Machine Learning* 45, no. 1 (2001): 5–32.
The other main way of combining trees, and permutation importance.

Chen, Tianqi, and Carlos Guestrin. "XGBoost: A Scalable Tree Boosting
System." In *Proceedings of the 22nd ACM SIGKDD International Conference on
Knowledge Discovery and Data Mining*, 785–794. ACM, 2016. The implementation
that made boosting the default for tabular data.

Ke, Guolin, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei
Ye, and Tie-Yan Liu. "LightGBM: A Highly Efficient Gradient Boosting Decision
Tree." In *Advances in Neural Information Processing Systems 30*, 3146–3154.
2017. Faster fitting on large data.

Prokhorenkova, Liudmila, Gleb Gusev, Aleksandr Vorobev, Anna Veronika
Dorogush, and Andrey Gulin. "CatBoost: Unbiased Boosting with Categorical
Features." In *Advances in Neural Information Processing Systems 31*. 2018.
Handling of categorical inputs, and a subtle leak of the outcome in how
boosting reuses its own training rows.

Lundberg, Scott M., and Su-In Lee. "A Unified Approach to Interpreting Model
Predictions." In *Advances in Neural Information Processing Systems 30*,
4765–4774. 2017. SHAP values. The version for trees is Lundberg and others,
"From Local Explanations to Global Understanding with Explainable AI for
Trees," *Nature Machine Intelligence* 2, no. 1 (2020): 56–67.

Grinsztajn, Léo, Edouard Oyallon, and Gaël Varoquaux. "Why Do Tree-Based
Models Still Outperform Deep Learning on Typical Tabular Data?" In *Advances
in Neural Information Processing Systems 35*, Datasets and Benchmarks track.
2022. A careful comparison of trees and neural networks on tables.
