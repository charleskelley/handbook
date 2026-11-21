---
title: "Anomaly detection"
type: method
depth: guide
owner: ds-lead
audience: [ds, mle, analyst]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [predictive, monitoring, modeling, outliers]
sources:
  - "Chandola, Banerjee, and Kumar, Anomaly Detection: A Survey, ACM Computing Surveys 41(3), 2009"
  - "Aggarwal, Outlier Analysis, 2nd ed., Springer, 2017"
---

# Anomaly detection

Finding the observations that do not fit: the day a metric broke, the order
that looks like fraud, the store whose numbers are unlike its peers. It is
asked for constantly and for good reason, and most of the work is not the
algorithm. It is deciding what normal means on data where the ordinary
values are themselves wildly uneven.

## What it is

Anomaly detection is any procedure that scores how unusual an observation is
against an expectation, and flags those beyond a threshold for someone to
look at. The expectation may be a fixed limit, the recent history of the
same series, the behaviour of similar units, or a model. There are usually
no labels saying which past observations were truly anomalous, so the
method cannot be trained and tested the way a classifier is. That shapes
everything: the detector's quality is judged by whether the people who
receive its alerts find them worth acting on, and a detector that raises too
many false alarms is switched off, whatever its statistical merits. Where
labels do exist, as with confirmed fraud, the problem is ordinary
classification with a rare outcome and belongs on the
[framing page](framing-and-evaluating-a-prediction.md).

## When it is the right choice

- A metric, a pipeline, or a model's inputs must be watched and someone will
  act when it goes wrong. See [monitoring](../oversight/monitoring.md).
- A table is to be cleaned before analysis, and the impossible or
  implausible values need finding.
- Among many units, such as stores, accounts, or suppliers, the ones
  behaving unlike their peers are to be reviewed by a person.
- Rare events with no reliable labels, such as new kinds of fraud or abuse,
  are being looked for.

## When it is not

- **Nobody will look at the alerts.** Detection without a named owner and
  an action is noise.
- **Labels exist.** Train a classifier.
- **The unusual observations are the business.** In customer data a small
  share of customers legitimately account for most of the value. They are
  extreme and not anomalous. Flagging them is a failure to understand the
  distribution. See the [customer-base audit](customer-base-audit.md).
- **The question is why the metric moved.** Detection says that it did.
  Explanation is [decomposing a change](decomposing-a-change.md).
- **Normal is not stable.** A new product or a business in rapid change has
  no baseline to depart from.

## Four words that are not the same

| Word | Meaning |
|---|---|
| Outlier | A value far from the bulk of the data. A statistical description |
| Error | A value that is wrong: a mis-keyed amount, a duplicated row, a unit mix-up |
| Anomaly | An observation that does not fit the expected pattern and that someone would want to know about |
| Incident | Something that went wrong in the world: an outage, a fraud, a failed job |

An outlier may be a correct and important value. An error may sit in the
middle of the distribution. An incident may show as an absence, such as no
orders from one region for an hour, with no extreme value anywhere.
Detectors find outliers. The job is to arrange things so that the outliers
they find are mostly anomalies.

## Three settings

| Setting | The question | Normal is defined by | Typical methods |
|---|---|---|---|
| A metric over time | Is today's value unusual for this series? | The series' own history: level, trend, season, day of week | Limits on the residual from a [forecast](time-series-forecasting.md), control charts, change-point detection |
| Rows in a table | Is this record unusual among records? | The joint distribution of the fields | Rules, robust limits on each field, isolation forest, distance and density methods |
| Units compared with peers | Is this store, account, or supplier unlike the others like it? | A peer group, chosen first | Robust limits within the peer group. A model of the expected value given the unit's characteristics |

Anomalies are also sorted by kind. A **point** anomaly is one extreme value.
A **contextual** anomaly is a value that is ordinary in general and wrong
for its context: heavy sales on a day the shops were shut. A **collective**
anomaly is a run of values, none extreme, that together are wrong: a week of
gently declining orders. The second and third are the ones simple limits
miss, and the ones that matter most in business monitoring.

## Skewed data comes first

Order values, customer spend, session lengths, and counts of almost anything
are heavily skewed: most values small, a few enormous. The textbook rule,
flag anything more than three standard deviations from the mean, fails on
such data in two ways.

- **The extremes inflate the yardstick.** The mean and the standard
  deviation are themselves pulled by the extreme values, which then hide
  behind the spread they created. The worked illustration below shows it.
- **The tail is normal.** On a skewed distribution, values many standard
  deviations out occur routinely and legitimately.

What to do instead:

- **Use the median and the median absolute deviation,** MAD, which extreme
  values barely move. The robust score is the distance from the median ÷
  (1.4826 × MAD). The constant makes it comparable with a standard deviation
  when the data is normal.
- **Or use quantiles.** Flag beyond a stated percentile, or beyond the
  quartiles by a multiple of the distance between them.
- **Transform first.** The logarithm of a skewed positive quantity is often
  close to symmetric, and limits set on it behave. Where zeros occur, use
  the logarithm of one plus the value.
- **Starting limits.** A robust score beyond about 3, or a value beyond the
  quartiles by 1.5 times the distance between them, are the usual places to
  start. Where more than half the values are identical the MAD is zero and
  the score fails. Use quantiles there.
- **Compare like with like.** A large order is unremarkable from a business
  account and remarkable from a new consumer account. Set limits within
  groups, or score the difference from what is expected for that kind of
  unit.
- **Look at the distribution before choosing anything.** A histogram on a
  logarithmic axis shows whether there is a bulk and a tail or several
  populations mixed together.

An illustration with made-up figures: thirty daily values, of which
twenty-seven lie between 9 and 11 and three are 95. The mean is 18.5 and the
standard deviation 25.9, so each 95 scores (95 − 18.5) ÷ 25.9 = 2.9 and is
not flagged at a limit of 3. The three extreme days have hidden one another.
The median is 10 and the MAD is 1, so the robust score is 85 ÷ 1.48 = 57.

## Common approaches

| Approach | What it needs | What it rests on | Main weakness |
|---|---|---|---|
| Rules and fixed limits | Knowledge of what is impossible or unacceptable | The rule being right | Finds only what was thought of in advance. Goes stale |
| Robust limits: median and MAD, quantiles | A reference sample | The bulk of the data being normal | One variable at a time. No sense of context |
| Control charts: limits around a running level, and cumulative-sum and moving-average versions that react to small sustained shifts | A stable process and a history | The process being in control during the reference period | Assumes no trend or season unless these are removed first |
| Forecast and residual | A [forecast](time-series-forecasting.md) of the series with intervals | The forecast capturing season, calendar, and trend | An anomaly in the recent past contaminates the next forecast, unless flagged values are replaced by their forecast before the next fit. Handles one series at a time |
| Seasonal decomposition, then limits on the remainder | A few seasonal cycles | The decomposition | The same |
| Change-point detection | A series | A change in level or trend being the thing of interest | Detects after the fact. Tells when, not why |
| Isolation forest | A table of numeric features | Anomalies being few and different, and so separated by fewer random splits | Flags a fixed share whether or not anything is wrong, when a share is what it is told to expect |
| Distance and density methods, such as local outlier factor | A meaningful distance between records | Anomalies lying in sparse regions | Distance loses meaning with many features. Sensitive to scaling |
| Reconstruction methods, such as autoencoders | A lot of data | Normal records being compressible and anomalies not | Hard to tune without labels, and hard to explain |
| Supervised classification | Labels | Past anomalies resembling future ones | Misses new kinds. See the [framing page](framing-and-evaluating-a-prediction.md) |

Contextual anomalies need a method whose expectation depends on the
context: a forecast and its residual, a decomposition, or limits within a
peer group. Collective anomalies need one that accumulates small departures:
cumulative-sum charts and change-point detection.

For metrics over time, start with a forecast and limits on its error. For
tables, start with rules and robust limits on each field within sensible
groups. Reach for the multivariate methods when unusual combinations, not
unusual single values, are what is being looked for.

## The alert budget

A detector is a test run many times, and the arithmetic of many tests
governs it.

Suppose 500 metrics are checked every day, and each check flags a normal day
1% of the time. That is 5 false alerts a day, 150 a month. If 3 real
incidents happen in a month and all are caught, 3 alerts in 153 are real.
The person on call learns to ignore the channel, and the real 3 are missed
with the rest.

- **Start from the number of alerts the owner can look at,** and set limits
  to deliver that many. This is the alert budget.
- **Watch fewer things.** Monitor the few metrics someone would act on, at
  the level they would act at.
- **Require persistence or corroboration.** Two periods in a row, or two
  related metrics together, before alerting.
- **Rank instead of flagging.** A daily list of the ten most unusual things
  is used. A stream of alerts is not.
- **Suppress what is already known.** A holiday, a planned outage, a launch.
  These are recorded as [insights](../oversight/index.md), and the detector
  should read them.

## Evaluating without labels

- **Replay known incidents.** Collect the past incidents people remember,
  and check that the detector would have caught each, and how soon.
- **Inject anomalies.** Add artificial spikes, drops, and shifts of known
  size to real history and measure what is caught. This gives the smallest
  change the detector can see.
- **Count alerts on quiet history.** Run it over a period believed to be
  normal. The alerts are an estimate of the false alarm rate.
- **Review a sample.** Have the owner mark a few weeks of alerts as useful
  or not. The share that are useful is the measure that decides whether the
  detector survives.
- **Keep the labels.** Every reviewed alert is a label. After a while there
  are enough to tune limits properly, and perhaps to train a classifier.

## Reading a result you did not produce

Questions to ask of an anomaly detection tool, dashboard feature, or model.

- **What does it take as normal?** A fixed limit, a trailing average, a
  seasonal model, a peer group. A trailing average with no seasonality
  alerts every Monday.
- **Was the reference period itself clean?** A baseline that includes past
  incidents treats them as normal.
- **How is the threshold set?** If it is a share of records to flag, the
  detector will flag that share for ever, anomalous or not.
- **How does it handle skew?** Ask whether limits are on the raw value or a
  transformed one, and whether they use the mean and standard deviation.
- **How many alerts does it raise, and what share were worth acting on?** If
  nobody knows, nobody is looking at them.
- **How many things is it watching?** The false alarm rate per check,
  multiplied by the number of checks, is the number of false alerts.
- **What did it miss?** Ask about the last incident found some other way.
- **Does an alert say what to do, and who does it?** An alert with no owner
  and no runbook is a notification.
- **Does it know about planned events?**
- **For a row-level detector: are the flagged records errors, frauds, or
  just large customers?** Read fifty of them.

## Where it applies to our data

*Add: the metrics and pipelines that are monitored, the method and limits
for each, and who owns the alerts.* Why: a detector without an owner is not
in use. The policy is on the [monitoring](../oversight/monitoring.md) page,
and the practice for models on the
[model monitoring](development/model-monitoring.md) page.

*Add: the fields known to be heavily skewed, and the transformation and
grouping the team uses for limits on each.* Why: so that limits are set the
same way each time.

*Add: the peer groups used for comparing units, such as store formats or
account tiers.* Why: "unlike its peers" depends on who the peers are.

*Add: the record of past incidents with their dates.* Why: it is the only
test set there is.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Further reading

Chandola, Varun, Arindam Banerjee, and Vipin Kumar. "Anomaly Detection: A
Survey." *ACM Computing Surveys* 41, no. 3 (2009): 1–58. The standard map of
the field: the kinds of anomaly, the families of method, and the assumption
each family makes. Start here.

Aggarwal, Charu C. *Outlier Analysis.* 2nd ed. Springer, 2017. The textbook,
with a chapter for each family of methods and for time series.

Leys, Christophe, Christophe Ley, Olivier Klein, Philippe Bernard, and
Laurent Licata. "Detecting Outliers: Do Not Use Standard Deviation around the
Mean, Use Absolute Deviation around the Median." *Journal of Experimental
Social Psychology* 49, no. 4 (2013): 764–766. Three pages on the robust
score used above.

Tukey, John W. *Exploratory Data Analysis.* Addison-Wesley, 1977. The source
of the box plot and its rule for flagging values by their distance beyond the
quartiles, and of the habit of looking before computing.

Montgomery, Douglas C. *Introduction to Statistical Quality Control.* Wiley.
The standard text on control charts, in many editions.

Page, E. S. "Continuous Inspection Schemes." *Biometrika* 41, no. 1/2
(1954). The cumulative-sum chart, for detecting small sustained shifts.

Cleveland, Robert B., William S. Cleveland, Jean E. McRae, and Irma
Terpenning. "STL: A Seasonal-Trend Decomposition Procedure Based on Loess."
*Journal of Official Statistics* 6 (1990): 3–73. The usual way to remove
season and trend before setting limits.

Killick, R., P. Fearnhead, and I. A. Eckley. "Optimal Detection of
Changepoints with a Linear Computational Cost." *Journal of the American
Statistical Association* 107, no. 500 (2012): 1590–1598. A widely used
change-point method.

Liu, Fei Tony, Kai Ming Ting, and Zhi-Hua Zhou. "Isolation Forest." In *2008
Eighth IEEE International Conference on Data Mining*, 413–422. IEEE, 2008.

Breunig, Markus M., Hans-Peter Kriegel, Raymond T. Ng, and Jörg Sander.
"LOF: Identifying Density-Based Local Outliers." *ACM SIGMOD Record* 29, no.
2 (2000): 93–104.
