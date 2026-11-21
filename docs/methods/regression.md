---
title: "Linear and logistic regression"
type: method
depth: build
owner: ds-lead
audience: [ds, mle, analyst]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [predictive, descriptive, modeling, regression]
sources:
  - "Gelman, Hill, and Vehtari, Regression and Other Stories, Cambridge University Press, 2020"
  - "Harrell, Regression Modeling Strategies, 2nd ed., Springer, 2015"
---

# Linear and logistic regression

The workhorse. Regression is the adjustment tool inside most of the analysis
pages on this site, and it is the baseline every predictive model here has to
beat. A team that uses it well needs little else for its first year.

## What it is

A regression model writes an outcome as a weighted sum of input variables
plus noise, and estimates the weights from data. **Linear regression** does
this for a numeric outcome such as spend. **Logistic regression** does it for
a yes-or-no outcome such as whether a customer bought, by modelling the
logarithm of the odds of yes as the weighted sum. Both belong to a family,
generalized linear models, that covers counts and other kinds of outcome in
the same way. The weights, called coefficients, say how the expected outcome
differs between units that differ in one input and are alike in the others.
That one sentence is the method's strength and the source of nearly every
misuse of it: "differs between units that differ" is a statement about
comparison, and it becomes a statement about cause only when a design makes
it one.

## When it is the right choice

- To summarise how an outcome varies with several characteristics at once.
- To adjust a comparison for measured differences between groups, inside a
  design that justifies it: an experiment,
  [difference-in-differences](difference-in-differences.md), a
  [matched](matching.md) comparison.
- As the first predictive model for any outcome, and as the baseline for any
  later one.
- When the model must be explained to the people who will act on it or to
  those who must approve it.
- When data is limited. A model with ten coefficients can be fitted
  reliably on data that would badly overfit a flexible one.

## When it is not

- **The relationship is strongly non-linear or full of interactions,** there
  is plenty of data, and only predictive accuracy matters. Tree-based
  models find such structure without being told: see
  [gradient-boosted trees](gradient-boosted-trees.md).
- **The coefficients will be read as effects, and there is no design.** A
  regression on observational data does not show what would happen if an
  input were changed. See [causal diagrams](causal-diagrams.md).
- **The outcome is a time until something happens,** with some subjects not
  yet having had it happen. See [survival analysis](survival-analysis.md).
- **The observations form a time series** to be forecast. See
  [time-series forecasting](time-series-forecasting.md).

## Two uses, two standards

The same fitted model is judged differently depending on what it is for.
Decide which before building it.

| | To explain or adjust | To predict |
|---|---|---|
| The goal | A coefficient that means something | Accurate predictions for new units |
| Which variables go in | Chosen by reasoning about what must be held fixed | Whatever improves prediction on held-out data and will be available in use |
| What is reported | Coefficients with intervals | Performance on a test set |
| What makes it wrong | A variable that should have been held fixed and was not, or one that should not have been and was | Overfitting, and information that will not be there in use |
| Correlated inputs | A problem: the coefficients cannot be separated | Harmless to prediction |
| Regularization | Biases the coefficients. Avoid, except as the remedy for separation below | Usually helps |

A model built to predict has coefficients, and they are not explanations. A
model built to explain makes predictions, and they are usually not the best
available.

## Linear regression

The model: the expected outcome is an intercept plus, for each input, a
coefficient times the input's value.

**Reading a coefficient.** Among units alike on every other input in the
model, those one unit higher on this input have an expected outcome higher by
the coefficient. The phrase "alike on every other input in the model" is
part of the meaning. Change what else is in the model and the coefficient
means something else.

**Categories.** An input with categories, such as region, enters as one
indicator for each category but one. The one left out is the reference, and
each coefficient is the difference from it. Choose the reference on purpose:
the largest category or the natural baseline.

**Interactions.** A product of two inputs lets the relation of one to the
outcome depend on the other. Once an interaction is in the model, the
coefficient on either input alone is its relation when the other is zero,
which may be a value no unit has. Centre the inputs, or read the model from
predicted values at chosen combinations.

**Logarithms.** Outcomes such as spend are skewed and their relations are
often proportional. Taking logarithms changes what a coefficient means:

| Outcome | Input | The coefficient *b* means |
|---|---|---|
| As it is | As it is | One more unit of the input goes with *b* more units of the outcome |
| Logarithm | As it is | One more unit of the input goes with a change in the outcome of about 100 × *b* percent, for small *b* |
| Logarithm | Logarithm | 1% more of the input goes with *b* percent more of the outcome, for small changes. An elasticity |

The logarithm of zero does not exist. Do not add a small constant without
checking that the answer does not depend on which constant. For an input
that is often zero, such as a count of orders, use the logarithm of one plus
the count, or bands with zero as a band of its own. For an outcome that is
often zero, see [other outcomes](#other-outcomes).

A prediction made on the logarithm scale and then exponentiated estimates
the median of the outcome, not its mean, and so understates the mean. Where
the mean matters, as in a total, model the amount itself with a logarithmic
link, by Gamma or Poisson regression, or apply the correction known as
smearing.

**What the model assumes.** In order of how much each matters:

1. The inputs that matter are in the model and the form is roughly right.
   Check by plotting what the model leaves over, the residuals, against the
   predictions and against each input.
2. The observations are independent, or the standard errors account for the
   way they are not. See below.
3. The spread of the residuals is about the same across the range. If not,
   use robust standard errors, or model the logarithm.
4. The residuals follow a normal distribution. This matters only for
   intervals in small samples, and is the least important of the four,
   though the one most often tested.

## Logistic regression

The model: the logarithm of the odds of the outcome is an intercept plus a
coefficient times each input. The odds are the probability of yes ÷ the
probability of no.

**Reading a coefficient.** A coefficient *b* means that one more unit of the
input multiplies the odds by e to the power *b*. That number is the odds
ratio. An odds ratio of 1.22 means the odds are 22% higher.

**Odds are not probabilities.** Multiplying the odds by 1.22 moves a
probability of 5% to about 6%, and a probability of 31% to about 35%. The
same coefficient is a change of 1 point for one customer and 4 for another.
So do not translate an odds ratio into "22% more likely" unless the outcome
is rare across the whole range. Report what a partner can use:

- **Predicted probabilities** at a few chosen values of the input, with the
  other inputs at typical values.
- **The average marginal effect:** change the input by one unit for every
  unit in the data, recompute each predicted probability, and average the
  change. For a category, switch every unit from the reference to the
  category. It is in percentage points and can be said in a sentence.

**Rare outcomes and separation.** With few yes outcomes, the model supports
few coefficients. A common rule of thumb is ten or more outcomes of the rarer
kind for each coefficient, and it is a floor, not a comfort. If some
combination of inputs predicts the outcome perfectly, the fitting procedure
fails or returns enormous coefficients. That is called separation, and it
calls for fewer inputs or a penalty.

Logistic regression's predicted probabilities are usually well calibrated on
the data it was fitted to, which is one reason it makes a good baseline.

## Other outcomes

| Outcome | Model | A coefficient means |
|---|---|---|
| A count, such as orders | Poisson regression, or negative binomial where the counts vary more than a Poisson model allows, which is usual | A multiplier on the expected count |
| A positive, skewed amount, such as spend among buyers | Gamma regression, or linear regression on the logarithm | A multiplier on the expected amount |
| An amount that is often zero | Two models: whether it is above zero, and how much if so | Read separately |
| Ordered categories | Ordinal regression | A multiplier on the odds of being in a higher category |
| Time to an event | See [survival analysis](survival-analysis.md) | A multiplier on the hazard |

## Standard errors

The default standard errors assume independent rows with equal spread.
Customer data breaks both.

- **Robust standard errors** allow unequal spread. Use them routinely.
- **Clustered standard errors** allow rows within a group to be related:
  many orders by one customer, many weeks for one store. Cluster at the
  level that was sampled or assigned. The number of clusters, not rows, then
  governs precision. With fewer than a few dozen clusters, clustered
  standard errors are themselves unreliable: see
  [difference-in-differences](difference-in-differences.md#standard-errors).

Leaving this out does not change the coefficients. It makes their intervals
too narrow, often by a great deal.

## Regularization

For prediction with many inputs, a penalty on the size of the coefficients
reduces overfitting. Ridge regression shrinks all coefficients toward zero.
The lasso shrinks them and sets some exactly to zero, which selects inputs.
The elastic net mixes the two. In each case:

- Put the inputs on a common scale first, since the penalty treats all
  coefficients alike.
- Choose the strength of the penalty by cross-validation on the training
  data.
- Do not read the surviving coefficients as findings. Which of two
  correlated inputs the lasso keeps is close to arbitrary, and the usual
  intervals do not apply after selection.

Choosing inputs by adding and removing them according to their p-values,
known as stepwise selection, has the same problem without the benefits. Do
not use it.

## Coefficients are not causes

Three errors account for most misreadings.

- **Reading every coefficient as an effect.** A model built to estimate the
  effect of one input, with other inputs included to adjust for
  confounding, says nothing reliable about the effect of those other inputs.
  Each would need its own set of adjustments. Presenting the whole table of
  coefficients as a list of drivers is common enough to have a name, the
  Table 2 fallacy.
- **Adjusting for the wrong things.** Including an input that lies on the
  path from the cause to the outcome removes part of the effect. Including
  one that both the cause and the outcome influence creates a relationship
  that is not there. More controls are not safer. See
  [causal diagrams](causal-diagrams.md#the-three-structures).
- **"Key driver analysis".** Ranking inputs by the size of their
  coefficients, or by how much each adds to the fit, describes which inputs
  predict the outcome in this data. It does not say which the business
  should change. An input can predict strongly because it is a symptom.

A coefficient earns a causal reading from the design the regression sits
inside, never from the regression.

## Building the outputs

Model specification

:   Written before fitting. Fields: the purpose, to explain or to predict;
    the unit of a row; the outcome and its definition; each input, its
    coding, its reference category, and why it is in the model; the
    interactions; the kind of model; how standard errors are computed; and
    for an explanatory model, the one coefficient the model exists to
    estimate.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| Coefficients | Input | Estimate, standard error, interval. For logistic regression, also the odds ratio and the average marginal effect | Table. For an explanatory model, the coefficient of interest first and the adjustment variables set apart |
| Predicted values | Chosen combinations of inputs | Predicted outcome or probability, interval | Table or lines. The form to give a partner |
| Fit | Model | Number of rows, number of clusters, and a measure of fit: R-squared for a linear model, log loss for a logistic one, on held-out data where the model is to predict | Table |
| Residuals | Fitted value, and each main input | Residual | Scatter with a smoothed line, which should be flat |
| Calibration, for logistic regression | Band of predicted probability | Average prediction, observed rate | Points against the diagonal |
| Performance on held-out data, for a predictive model | As on the [evaluation page](framing-and-evaluating-a-prediction.md#building-the-outputs) | | |

Defaults, where nothing about the business decides otherwise:

| Choice | Default | Why |
|---|---|---|
| Standard errors | Robust, and clustered by customer or by the unit assigned | Rows are rarely independent |
| Skewed positive outcomes and inputs | Logarithms | Relations in business data are mostly proportional |
| Numeric inputs | Centred. For prediction, also scaled | Makes the intercept and interactions readable |
| Non-linear relations | A few bands, or a spline | A straight line through a curve misleads at both ends |
| Reporting logistic models | Predicted probabilities and average marginal effects | Odds ratios are misread |
| Choice of inputs for prediction | A penalty chosen by cross-validation | Not stepwise selection |

## Checks

- The number of rows used equals the number expected. Rows with a missing
  value in any input are dropped silently by most software. Decide what is
  done with them: a category of its own for a categorical input, a filled
  value and a flag for a numeric one.
- The coefficients have plausible signs and sizes. A surprising sign is more
  often a coding error or two inputs measuring the same thing than a
  discovery.
- The residual plots show no curve and no funnel.
- No pair of inputs is close to a copy of another, where the coefficients
  are to be read. Check correlations and variance inflation factors, where a
  value above about 5 to 10 is the usual sign of trouble.
- The result does not rest on a few rows. Refit without the most extreme
  ones.
- For logistic regression, predictions are calibrated on held-out data, and
  no coefficient is enormous.
- The coefficient of interest is stable when reasonable adjustment variables
  are added or removed. If it is not, say so and give the range.
- For a predictive model, every check on the
  [evaluation page](framing-and-evaluating-a-prediction.md#checks) passes.

## Pitfalls

- **Percent and percentage points.** A rise from 5% to 6% is one percentage
  point and 20 percent. State which.
- **Extrapolating.** The line is fitted where the data is. Predictions for
  input values outside that range have no support.
- **Treating many rows as much evidence.** A million rows from 200 stores
  carry about 200 stores' worth of evidence about anything that varies by
  store.
- **Chasing fit.** A higher R-squared from more inputs is not a better
  model for either purpose.
- **Reading a non-significant coefficient as no relationship.** See
  [stating uncertainty](stating-uncertainty.md).
- **Trying specifications until one works.** The interval reported at the
  end does not account for the search.
- **Interpreting the main coefficient of an interacted input** as though
  the interaction were not there.
- **A model fitted on those who were selected.** Spend among customers who
  bought says nothing about those who did not.
- **Using a predictive model's coefficients as findings,** above all after
  regularization.

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data.

**A logistic coefficient in three forms.** A model of whether a customer
lapses has an intercept of −3.0 and a coefficient of 0.20 on months since
the last order.

- *As an odds ratio.* e to the power 0.20 is 1.22. Each further month
  multiplies the odds of lapsing by 1.22.
- *As probabilities.* The logarithm of the odds is −3.0 + 0.20 × months, and
  the probability is 1 ÷ (1 + e to the power minus that).

| Months since last order | Logarithm of the odds | Probability of lapsing |
|---|---|---|
| 0 | −3.0 | 4.7% |
| 1 | −2.8 | 5.7% |
| 6 | −1.8 | 14.2% |
| 11 | −0.8 | 31.0% |
| 12 | −0.6 | 35.4% |

- *As a change in probability.* One more month adds 1.0 point for a customer
  who has just ordered, from 4.7% to 5.7%, and 4.4 points for one at eleven
  months, from 31.0% to 35.4%. The odds ratio is the same in both cases.
  "22% more likely per month" is close for the first, where lapsing is
  rare, at 21%, and wrong for the second, at 14%.

**An elasticity.** A regression of the logarithm of units sold on the
logarithm of price, within a design that supports reading it this way, gives
a coefficient of −1.5. A price 10% higher goes with units lower by a factor
of 1.10 to the power −1.5, which is 0.867: a fall of 13%. Revenue changes by
1.10 × 0.867 = 0.953, a fall of about 5%.

## Where it applies to our data

*Add: the regression models in regular use, each with its specification, its
purpose, and the page of the analysis or decision it serves.* Why: a
coefficient is quoted long after anyone remembers what else was in the
model.

*Add: the level at which the team clusters standard errors for each kind of
data, such as customer, store, or region.* Why: it decides the width of
every interval, and it should not be chosen analysis by analysis.

*Add: the standard transformations for the outcomes the team models most,
such as spend and order counts.* Why: two analyses of the same outcome on
different scales cannot be compared.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Gelman, Andrew, Jennifer Hill, and Aki Vehtari. *Regression and Other
Stories.* Cambridge University Press, 2020. The best modern introduction:
regression as comparison, built up with real examples, with causal
interpretation kept separate and treated properly. Start here.

Harrell, Frank E., Jr. *Regression Modeling Strategies: With Applications to
Linear Models, Logistic and Ordinal Regression, and Survival Analysis.* 2nd
ed. Springer, 2015. The reference for building a model honestly: how many
inputs the data supports, why stepwise selection fails, splines, validation.

James, Gareth, Daniela Witten, Trevor Hastie, and Robert Tibshirani. *An
Introduction to Statistical Learning: With Applications in R.* 2nd ed.
Springer, 2021. Regression as a predictive method, with regularization and
cross-validation.

Hosmer, David W., Stanley Lemeshow, and Rodney X. Sturdivant. *Applied
Logistic Regression.* 3rd ed. Wiley, 2013. The standard text on logistic
regression.

Shmueli, Galit. "To Explain or to Predict?" *Statistical Science* 25, no. 3
(2010): 289–310. Why the two purposes lead to different models and are
judged differently.

Westreich, Daniel, and Sander Greenland. "The Table 2 Fallacy: Presenting and
Interpreting Confounder and Modifier Coefficients." *American Journal of
Epidemiology* 177, no. 4 (2013): 292–298. Why the coefficients of adjustment
variables are not effects.

Tibshirani, Robert. "Regression Shrinkage and Selection via the Lasso."
*Journal of the Royal Statistical Society, Series B* 58, no. 1 (1996):
267–288. The lasso.

Peduzzi, Peter, John Concato, Elizabeth Kemper, Theodore R. Holford, and
Alvan R. Feinstein. "A Simulation Study of the Number of Events per Variable
in Logistic Regression Analysis." *Journal of Clinical Epidemiology* 49, no.
12 (1996): 1373–1379. The origin of the rule of thumb of ten events for each
coefficient.
