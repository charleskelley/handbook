---
title: "Time-series forecasting"
type: method
depth: build
owner: ds-lead
audience: [ds, mle, analyst, leadership]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [predictive, forecasting, time-series, modeling]
sources:
  - "Hyndman and Athanasopoulos, Forecasting: Principles and Practice, 3rd ed., OTexts, 2021"
  - "Hyndman and Koehler, Another look at measures of forecast accuracy, International Journal of Forecasting 22(4), 2006"
---

# Time-series forecasting

Predicting the future values of a number recorded over time, such as weekly
revenue, daily orders, or monthly sign-ups, from its own history and from
what is known about the periods ahead. It is the first modelling request
most teams get from finance and operations, and it needs no customer-level
features, which makes it a good early project while the data landscape is
still being built.

## What it is

A forecast is a statement about a future value with a statement of how
uncertain it is. Time-series methods produce one by finding the regular
structure in a series' past, its level, trend, seasonal pattern, and
response to known events, and carrying that structure forward. The methods
on this page are deliberately simple. On the kind of series a business has,
a few years of weekly or monthly history, simple methods are hard to beat,
and the discipline around them matters more than the method: a clear
statement of what is being forecast, an honest test against a naive
baseline, and an interval on every number.

## When it is the right choice

- A plan depends on a future quantity: staffing, stock, cash, a budget.
- The quantity has a history of at least two full seasonal cycles on a
  consistent definition.
- The future is expected to resemble the past in structure, or the ways it
  will differ are known and can be put in.
- The forecast will be made repeatedly, so its errors can be measured and
  the method improved.

## When it is not

- **The question is what an action will do.** A forecast says what will
  happen if things go on as they are. The effect of a price change or a
  campaign is a causal question: see
  [directional versus causal](directional-versus-causal.md).
- **There is no stable history.** A new product, a new market, a series
  whose definition keeps changing. Use judgment, analogies with similar
  launches, and a wide range, and say that is what was done.
- **The future will be unlike the past in ways nobody can specify.**
- **Which customers, not how many.** Predicting which individuals will buy
  is on the [churn and propensity](churn-and-propensity.md) page.
- **The number wanted is a target.** See the next section.

## A forecast, a plan, and a target

Three different things are called "the forecast" in a business. Keep them
apart, in the work and in every table.

| | What it is | Who owns it |
|---|---|---|
| Forecast | The best estimate of what will happen, given what is known, with its uncertainty | The team that produces it |
| Plan | What the business intends to do, and the outcome it expects from doing it | Management |
| Target | What the business wants to achieve | Management |

A forecast adjusted to match a target is no longer a forecast, and loses its
use as a warning. If the forecast and the target differ, that difference is
the most valuable thing the forecast has to say.

## What is being forecast

Written down before any modelling. It is the forecasting version of the
[framing](framing-and-evaluating-a-prediction.md#the-framing) for any
prediction.

| Item | The question | Example |
|---|---|---|
| Series | Exactly which number, defined how? | Net revenue after returns, all channels |
| Frequency | In what periods? | Weekly, weeks starting Monday |
| Level | For the whole business, or by region, category, store? | By region, and in total |
| Horizon | How far ahead? | 1 to 13 weeks |
| Origin | When is the forecast made, and with data up to when? | Each Monday, with data to the previous Sunday |
| Use | What decision does it feed, and what does an error in each direction cost? | Staffing. Too low costs sales, too high costs wages |
| Known future | What is known about the periods ahead at the origin? | Holidays, planned promotions, price changes, store openings |
| Baseline | What is used today? | Last year's figure plus a growth percentage |

The horizon and the level change the problem. Next week's total is easy. A
single store's sales in a week six months out is not.

## What a series is made of

| Part | What it is | How it is handled |
|---|---|---|
| Level | Where the series sits now | Estimated from recent values |
| Trend | A sustained rise or fall | Estimated, and usually damped so it flattens further out |
| Seasonality | A pattern that repeats with the calendar: week of year, day of week, hour of day | Estimated from at least two cycles. A series can have more than one |
| Calendar effects | Holidays, paydays, the number of trading days in a month, a 53rd week | Put in explicitly. Holidays that move, such as Easter, need their dates |
| Known events | Promotions, price changes, launches, outages | Put in as inputs when their dates are known, in the past and ahead |
| Level shifts | A lasting step from a change in the business or in how the number is recorded | Dated and modelled, or the history before it is adjusted or dropped |
| Noise | What is left | Its size sets the width of the interval |

Exponential smoothing takes no outside inputs. To use it on a series with
known events, adjust the history for them first and add them back to the
forecast, or move up to regression with time-series errors.

Plot the series before anything else: the whole history, one year laid over
another, and the changes from period to period. Most of what a model will
find is visible, and so are the data errors.

## Baselines

Every forecast is judged against a naive one that costs nothing.

| Baseline | The forecast for a future period is |
|---|---|
| Naive | The last observed value |
| Seasonal naive | The value from the same period one season ago |
| Seasonal naive with drift | The same, plus the average change from one seasonal cycle to the next, such as year on year |
| Mean | The average of the history |

For a seasonal business series, the seasonal naive forecast is the one to
beat. A method that cannot beat it over a proper test is not adding
anything, and a surprising number of elaborate ones do not.

## Methods

A ladder. Climb only as far as the test justifies.

Exponential smoothing, the first rung, keeps a running estimate of the
level, and where needed of the trend and of each season's effect. Each is
updated every period as a weighted average of its old value and what the new
observation implies, with a weight between 0 and 1 that is estimated from
the data. A weight near 1 follows recent periods closely. The seasonal
effect can be an amount added or a proportion multiplied, and the trend can
be damped so that it flattens. "Chosen automatically" means the software
fits each of these combinations and keeps the one with the best fit after a
penalty for its number of parameters.

| Method | What it does | Suits | Limits |
|---|---|---|---|
| Exponential smoothing | Carries forward a level, a trend, and a seasonal pattern, each updated as a weighted average that favours recent periods | Most business series. The default first model | Uses only the series' own history. No outside inputs in its basic form |
| ARIMA | Models each value from earlier values and earlier errors, after differencing, which is taking changes from one period to the next, to remove trend and season | Series with strong period-to-period dependence | Harder to specify and explain. Automatic selection helps |
| Regression with time-series errors | A regression on calendar terms and known inputs, such as price and promotion, with the leftover modelled as a time series | Series driven by known, plannable events | Needs the inputs' future values. A forecast of the inputs brings its own error |
| Decomposition models | Fit trend, seasons, and holidays as separate additive curves | Daily series with several seasonal patterns and many holidays | Easy to run without checking. Test it like any other |
| Machine learning on lagged values | A model such as [gradient-boosted trees](gradient-boosted-trees.md) trained on features built from past values and the calendar, across many series at once | Many related series, such as products by store, with rich inputs | Needs many series and careful testing. Not a first project |

Two further techniques matter once the basics work:

- **Combining forecasts.** The average of several reasonable methods is
  usually more accurate than most of them, and rarely much worse than the
  best. It is the cheapest improvement available.
- **Reconciling levels.** Forecasts made separately for regions will not
  add up to the forecast for the total. Either forecast at one level and
  split or sum, or use a reconciliation method so every level agrees.

### Forecasting from the customer base

Revenue can also be forecast from its parts. The
[customer-base audit](customer-base-audit.md#lens-5-the-whole-base) lays
each period's revenue out by cohort. Each existing cohort's revenue follows
a decay curve that is fairly stable from one cohort to the next, and new
cohorts add to it. A forecast built as existing cohorts carried down their
curves, plus an assumption about the number and quality of customers to be
acquired, shows what the total depends on, and separates what is nearly
certain from what rests on acquisition. It is a useful second forecast to
set beside the time-series one. Where they disagree, find out why.

## Testing a forecast

Fit to the past and accuracy on the future are different things, and only
the second matters. The test copies how the forecast will be used.

![Four rows, each a bar of history used to fit followed by a short bar of periods that are scored. From one row to the next the history grows longer and the scored periods move later.](../assets/rolling-origin-light.svg#only-light)
![Four rows, each a bar of history used to fit followed by a short bar of periods that are scored. From one row to the next the history grows longer and the scored periods move later.](../assets/rolling-origin-dark.svg#only-dark)

*A rolling-origin test. Each row is one forecast, made with only the history
to its left.*

1. Choose a series of past origins, spread over at least a year so every
   season is tested. With only two or three years of history the earliest
   origins leave little to fit on, and the test is weak. Say so.
2. At each origin, fit the method using only data up to the origin, and
   forecast the full horizon. Any choice the method makes, such as its
   parameters or which inputs to use, is made from that data only.
3. Compare each forecast with what happened.
4. Summarise the errors by horizon, for the method and for the baseline.

This is called a rolling-origin evaluation or time-series cross-validation.
A random split of periods into training and test is wrong here: it lets the
method see the future on both sides of every test point.

**Measures.**

| Measure | Definition | Use |
|---|---|---|
| Error | Actual − forecast | The raw material. Keep every one |
| Bias | The average error | Persistent over- or under-forecasting. Should be near zero |
| Mean absolute error | The average size of the error | The main measure, in the series' own units |
| Root mean squared error | The square root of the average squared error | When large errors cost disproportionately |
| Mean absolute scaled error | Mean absolute error ÷ the mean absolute error of the seasonal naive forecast over the history | Below 1 is better than the naive forecast did within the history. Compute the baseline's own scaled error on the test periods and compare. Comparable across series of different size |
| Mean absolute percentage error | The average of the size of the error ÷ the actual | Familiar to partners. Breaks when actuals are near zero, and treats over- and under-forecasts unequally |
| Interval coverage | The share of actuals that fell inside the stated interval | An 80% interval should hold about 80% of them |

Report accuracy by horizon. An average over horizons hides the fact that
week one is good and week thirteen is not.

**Intervals.** Every forecast carries a prediction interval, at a stated
level such as 80%. The interval widens with the horizon. Model-based
intervals are usually too narrow, because they assume the model is right, so
check their coverage in the rolling-origin test and widen them if needed.
The spread of past errors at each horizon is a simple and honest interval:
for an 80% interval, add the 10th and 90th percentiles of the test errors at
that horizon to the point forecast. It needs a few dozen origins. A forecast
made on the logarithm scale is turned back by exponentiating the point and
both bounds, and the point is then a median.

## Adjusting by judgment

People who run the business know things the series does not: a contract
about to end, a competitor closing. Adjustments for such knowledge can
improve a forecast. Adjustments made because the number looks too low
generally do not.

- Record the statistical forecast, the adjusted forecast, who adjusted it,
  and why.
- Measure both against the outcome. Keep the kinds of adjustment that help.

## Building the outputs

Series table

:   One row per series, period, and the date the value was recorded.
    Columns: series identifier, period, value, as-known date. Past values
    get revised, as returns and late orders arrive, and a test must use the
    values as they stood at each origin. Where only the latest values are
    kept, say so, and treat the test as optimistic. Only complete periods
    are included.

Calendar and events table

:   One row per period. Columns: period, holiday and calendar flags, and
    planned events with the date each became known.

Forecast table

:   One row per series, origin, and target period. Columns: series
    identifier, origin, target period, horizon, point forecast, lower and
    upper bounds, the level of the interval, method and version, and any
    adjusted forecast with its reason. Never overwritten. It is the record
    accuracy is later measured from.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| The series | Period | Value | Line over the whole history, and years overlaid |
| Forecast | Target period | Point, lower, upper | Line continuing the history, with a band |
| Test by horizon | Horizon | Bias, mean absolute error, scaled error, coverage, for each method and the baseline | Table, and error against horizon as lines |
| Test over time | Origin | Error at a fixed horizon | Line. Shows when the method failed |
| Components | Period | Trend, seasonal, and event parts | Stacked panels |
| Forecast against actual, in use | Target period | Forecast made at each horizon, the actual, the error | Table, added to every period |

Defaults, where nothing about the business decides otherwise:

| Choice | Default | Why |
|---|---|---|
| Baseline | Seasonal naive | The one to beat |
| First method | Exponential smoothing with a damped trend, chosen automatically | Robust, and little to get wrong |
| Test | Rolling origin over the last year or more, by horizon | Copies real use across every season |
| Main measure | Mean absolute scaled error, with bias beside it | Readable against the baseline |
| Interval | 80%, checked for coverage | Wide enough to be right, narrow enough to plan with |
| Transformation | Logarithm for series whose swings grow with their level | Keeps the seasonal pattern proportional |
| History used | All of it since the last level shift | Older structure may no longer apply |

## Checks

- The last period in the data is complete. A part-week reads as a collapse.
- No periods are missing, and none is duplicated.
- At every test origin, nothing dated after the origin was used: not values,
  not inputs, not the choice of method or its settings.
- The method beats the seasonal naive baseline at the horizons that matter,
  by more than the variation between origins: compare the average difference
  in absolute error between the two, across origins, with its standard
  error.
- Bias is near zero at each horizon.
- Interval coverage in the test is close to the stated level.
- The errors that remain show no pattern: not by season, not by day of week,
  not from one period to the next.
- Forecasts for the parts add up to the forecast for the whole, or the
  difference is reconciled.
- Any input used has a future value that will really be known at the
  origin.

## Pitfalls

- **Judging by fit to history.** A flexible method can follow the past
  exactly and forecast badly. Only held-out accuracy counts.
- **One test origin.** A single good quarter proves little. Test across a
  year of origins.
- **Inputs from the future.** A model that uses actual marketing spend or
  weather to "forecast" a past period looks excellent. In use those values
  are unknown.
- **Percentage errors on small numbers.** An error of 5 on an actual of 2 is
  250%. Averages of such figures are meaningless.
- **Ignoring level shifts.** A price change, a store closure, a change of
  definition. Models read them as trend or noise. Date them, from the
  insights log.
- **An unusual period treated as normal.** A stock-out or a one-off surge
  becomes part of next year's seasonal pattern unless it is marked.
- **Holidays that move.** Easter, and any week numbering that shifts
  against the calendar. Year-on-year comparisons of weeks go wrong at the
  same points every year.
- **A point forecast with no interval.** It will be read as a promise.
- **Too far ahead.** Past a few seasons the interval is as wide as the
  series' whole range, and the honest forecast is the long-run pattern.
- **Forecasting what the business controls.** If sales are capped by stock
  or capacity, the history records supply, not demand.
- **Measuring accuracy on adjusted actuals.** If the outcome was affected by
  actions taken because of the forecast, the error no longer measures the
  forecast.

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data. Quarterly revenue:

| | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Year 1 | 100 | 120 | 110 | 150 |
| Year 2 | 110 | 130 | 125 | 160 |
| Year 3, actual | 120 | 138 | 140 | 172 |

At the end of Year 2, forecast Year 3.

**Seasonal naive.** Each quarter of Year 3 is forecast as the same quarter
of Year 2.

| | Q1 | Q2 | Q3 | Q4 | Average |
|---|---|---|---|---|---|
| Forecast | 110 | 130 | 125 | 160 | |
| Error | 10 | 8 | 15 | 12 | Bias +11.25 |
| Size of error | 10 | 8 | 15 | 12 | Mean absolute error 11.25 |

The bias equals the mean absolute error: every forecast was too low. The
method has no trend.

**The scale.** Within the history, the seasonal naive forecast of Year 2
from Year 1 was off by 10, 10, 15, and 10, an average of 11.25. That is the
denominator of the scaled error. The seasonal naive forecast of Year 3
therefore has a scaled error of 11.25 ÷ 11.25 = 1.00: in Year 3 it did
exactly as well as it had within the history.

**Seasonal naive with drift.** Add the average rise from one year to the
next, 11.25, to each quarter.

| | Q1 | Q2 | Q3 | Q4 | Average |
|---|---|---|---|---|---|
| Forecast | 121.25 | 141.25 | 136.25 | 171.25 | |
| Error | −1.25 | −3.25 | 3.75 | 0.75 | Bias 0.00 |
| Size of error | 1.25 | 3.25 | 3.75 | 0.75 | Mean absolute error 2.25 |

The scaled error is 2.25 ÷ 11.25 = 0.20. One added term removed the bias and
four fifths of the error.

**What this does not show.** It is one origin and four numbers. A real test
repeats it from many origins, and reports the error at each horizon with
the variation between origins. And the zero bias here is luck of the
made-up figures: on a real series the trend estimated from one year's rise
would be noisy.

## Where it applies to our data

*Add: the series the team forecasts, each with its definition, frequency,
level, horizon, origin, and the decision it feeds.* Why: accuracy is only
meaningful for a stated series at a stated horizon.

*Add: for each, the baseline in use before the team's forecast, and its
measured accuracy.* Why: the improvement over the baseline is the forecast's
value.

*Add: the datasets each series is read from, linked to their pages under
Data, whether past values are revised, and whether earlier versions are
kept.* Why: a test on revised data overstates accuracy.

*Add: the calendar the business runs on: week definition, fiscal periods,
53-week years, and the holidays that matter.* Why: calendar errors recur
every year.

*Add: dated level shifts and unusual periods, from the insights index under
[Oversight](../oversight/index.md).* Why: the model treats all history as
typical unless told.

*Add: where the forecast table is kept and who reviews forecast against
actual.* Why: a forecast whose errors are never looked at does not improve.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Hyndman, Rob J., and George Athanasopoulos. *Forecasting: Principles and
Practice.* 3rd ed. OTexts, 2021. The standard introduction, free to read
online: baselines, decomposition, exponential smoothing, ARIMA, regression,
reconciliation, and evaluation. Start here, and for most needs finish here.

Hyndman, Rob J., and Anne B. Koehler. "Another Look at Measures of Forecast
Accuracy." *International Journal of Forecasting* 22, no. 4 (2006): 679–688.
The scaled error, and what is wrong with percentage errors.

Tashman, Leonard J. "Out-of-Sample Tests of Forecasting Accuracy: An Analysis
and Review." *International Journal of Forecasting* 16, no. 4 (2000):
437–450. Rolling-origin evaluation and why it is needed.

Makridakis, Spyros, Evangelos Spiliotis, and Vassilios Assimakopoulos. "The
M4 Competition: 100,000 Time Series and 61 Forecasting Methods."
*International Journal of Forecasting* 36, no. 1 (2020): 54–74. Evidence, at
scale, on which methods forecast well, and on the value of combining them.

Hyndman, Rob J., Anne B. Koehler, J. Keith Ord, and Ralph D. Snyder.
*Forecasting with Exponential Smoothing: The State Space Approach.* Springer,
2008. The full treatment of exponential smoothing, including its prediction
intervals.

Box, George E. P., Gwilym M. Jenkins, Gregory C. Reinsel, and Greta M. Ljung.
*Time Series Analysis: Forecasting and Control.* 5th ed. Wiley, 2015. The
classic text on ARIMA models.

Hyndman, Rob J., and Yeasmin Khandakar. "Automatic Time Series Forecasting:
The forecast Package for R." *Journal of Statistical Software* 27, no. 3
(2008). How exponential smoothing and ARIMA models can be selected
automatically.

Taylor, Sean J., and Benjamin Letham. "Forecasting at Scale." *The American
Statistician* 72, no. 1 (2018): 37–45. The decomposition model with several
seasons and holidays that is widely used for daily business series.

Petropoulos, Fotios, and others. "Forecasting: Theory and Practice."
*International Journal of Forecasting* 38, no. 3 (2022): 705–871. An
encyclopedic review of the field, to look things up in.
