---
title: "Marketing mix modeling"
type: method
depth: guide
owner: ds-lead
audience: [ds, analyst, product, leadership]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [causal, marketing, observational, time-series]
sources:
  - "Chan and Perry, Challenges and Opportunities in Media Mix Modeling, Google, 2017"
  - "Hanssens, Parsons, and Schultz, Market Response Models: Econometric and Time Series Analysis, 2nd ed., Kluwer Academic Publishers, 2001"
---

# Marketing mix modeling

A regression of sales over time on marketing activity and everything else
that moves sales, used to say how much each channel contributed and where the
next unit of budget should go. Marketing teams commission these models, buy
them from agencies, and build them in vendor tools, and the data science team
is asked to interpret, check, and eventually improve them. This page is what
to know before doing any of those.

## What it is

A marketing mix model, also called a media mix model and usually shortened
to MMM, explains a time series of an outcome, usually weekly sales, by a set
of drivers measured over the same weeks: spend or exposure in each marketing
channel, price, promotions, distribution, season, holidays, and the economy.
The fitted relationship is then used to split past sales into a base that
would have happened anyway and an increment credited to each channel, to
compute a return for each channel, and to recommend a reallocation of
budget. It uses aggregate data only, so it needs no tracking of individuals
and covers channels that cannot be tracked, such as television and outdoor.
It is an observational causal analysis of the hardest kind: a handful of
correlated series, a hundred or two observations, and a business that set
its spending in response to the same demand it is trying to explain.

## When it is the right choice

- The question is the split of a budget across channels, including channels
  with no individual-level data.
- Spend in each channel has varied over time, and preferably has been varied
  on purpose.
- There are at least two or three years of consistent weekly data, and
  better still the same data by region.
- The answer needed is a broad one: which channels are over- or
  under-invested, by roughly how much.
- Experiments are being run alongside and can be used to check and anchor
  it.

## When it is not

- **A precise return for one campaign or one creative.** The model sees
  weekly totals by channel. It cannot resolve anything finer.
- **Spend that hardly varied,** or that always moved with another channel or
  with the season. The model has nothing to learn the effect from and will
  report one anyway.
- **A short or broken history.** A new business, a change of tracking, a
  merger, a period unlike any other.
- **A channel whose spend is set by demand.** Paid search on the brand's own
  name, retargeting, and affiliate payments rise when customers are already
  buying. The model credits them with the sales that triggered them.
- **As a substitute for a test that could be run.** Where a channel can be
  switched off in some regions, that
  [experiment](experiments-and-lift-tests.md) answers the question the model
  can only estimate.

## Assumptions

| Assumption | What it means | How it is checked |
|---|---|---|
| Spend was not set by what it is explaining | Changes in a channel's spend were not themselves a response to expected sales | Ask how each channel's budget was set. Usually it was set from a sales forecast or a share of revenue, which breaks this |
| Everything else that moved sales is in the model | Price, promotion, distribution, competitors, weather, and one-off events are included or did not coincide with marketing | A list of what happened, checked against the insights log. Never complete |
| Each channel varied independently enough | The model can tell one channel's effect from another's | Correlations between the channels' series. How the estimates move when one channel is dropped |
| The assumed shapes are right | Carryover and saturation follow the forms chosen | Compare fits under other forms. The data rarely decides |
| The relationship was stable | A unit of spend did the same thing throughout the period | Refit on parts of the period |
| No effect runs between channels unmodelled | Television that drives search is not credited to search | Rarely checkable. Stated as a limit |

Most of these fail to some degree in every real model. The practical
question is not whether the model is right but which of its outputs are
robust to the failures.

## What goes in

| Input | Grain | Notes |
|---|---|---|
| Outcome | Weekly, by region where possible | Sales, revenue, or new customers. One outcome per model |
| Marketing by channel | The same grain | Exposure, such as impressions or rating points, is better than spend, because the price of media changes |
| Price and promotion | The same grain | Average price paid, depth and coverage of discounts |
| Distribution and availability | The same grain | Stores, stock, site availability |
| Season and calendar | The same grain | Week of year, holidays, paydays, school terms |
| The wider environment | The same grain | Economy, weather, competitor activity where known |
| Events | Dated | Launches, outages, tracking changes |

A hundred and fifty weeks is a hundred and fifty observations. Ten channels,
each with an effect, a rate of carryover, and a saturation shape, are thirty
parameters before any of the other inputs. That ratio is the central
difficulty.

## The two shapes

Two transformations of each channel's series are what separate a marketing
mix model from a plain regression.

**Carryover.** Advertising seen this week still has some effect next week.
Each week's exposure is replaced by a weighted sum of that week's and
earlier weeks', with weights that decay. The transformed series is often
called adstock, and the rate of decay is a parameter: fast for a promotion,
slow for brand advertising.

**Saturation.** The hundredth exposure does less than the first. Each
channel's transformed series is passed through a curve that rises and
flattens, so that doubling spend less than doubles the effect. The curve is
what makes the model able to recommend a budget: it implies a marginal
return that falls as spend rises, and the best allocation equalises that
marginal return across channels.

Both shapes are assumptions imposed on the data, and with the amount of data
available many combinations of decay and curve fit about equally well while
implying different returns.

## What comes out

A channel's contribution in a period is the model's prediction with the
channel as it was, less its prediction with that channel set to zero. The
base is the prediction with all marketing set to zero. Where exposure is the
input, returns are worked out per unit of spend using what the exposure cost
in each period.

| Output | What it is | How far to trust it |
|---|---|---|
| Base and incremental | Sales split into what would have happened with no marketing and what marketing added | The split depends heavily on how trend and season are modelled |
| Contribution by channel | The increment credited to each channel in each period | Reasonable for large channels that varied. Weak for small or collinear ones |
| Return on investment | A channel's contribution ÷ its spend | An average over the period. Not the return on the next unit |
| Marginal return | The extra outcome from a small increase in a channel's spend | The number that matters for the budget, and the one most sensitive to the saturation curve |
| Response curve | Outcome against spend for each channel | Trustworthy only over the range of spend that occurred |
| Recommended allocation | The split of a fixed budget that maximises the modelled outcome | Read as a direction of travel, a shift of some budget from one channel toward another, and test it |

## What makes it more believable

- **Regional data.** The same model fitted across many regions has more
  observations and uses differences between regions that are not driven by
  national demand. Regions share national shocks, so the gain is less than
  the count of rows suggests.
- **Variation made on purpose.** A period in which a channel was cut or
  raised in some regions, for no reason related to demand, is worth more
  than years of business as usual.
- **Anchoring to experiments.** Where a lift test has measured a channel's
  effect, use it: as a check on the model's estimate, or as prior
  information in a Bayesian model. A model that contradicts a clean
  experiment has to be explained. The two may cover different periods, levels
  of spend, and windows. Where those do not account for the gap, the model
  is wrong about that channel.
- **Checks out of sample.** Fit on the earlier weeks and predict the later
  ones. This tests the model as a forecaster, which is necessary and not
  sufficient: a model can predict sales well from season alone and have every
  channel's effect wrong.
- **Stability.** Refit with a quarter more data, or with one channel's
  transformation changed. Estimates that swing are not known.
- **Simulation.** Generate data from a known set of effects with the same
  spending patterns, and check whether the method recovers them. This shows
  what the real data could ever reveal.

## Common approaches

| Approach | What it needs | What it rests on | Main weakness |
|---|---|---|---|
| Classical regression on transformed spend | Weekly national data, transformations chosen by hand or by search | The assumptions above, in full | Many specifications fit equally well. The one chosen is the analyst's or the client's preference |
| Bayesian model with carryover and saturation estimated | The same, plus prior distributions | The same, with the priors made explicit | With little data the priors largely determine the answer. That is honest, and must be stated |
| Hierarchical model across regions | The same data by region | That regions share a structure while differing in level | More data preparation. Regional media data is often poor |
| Experiment-calibrated model | Lift tests for at least the main channels | Experiments as the anchor, the model to fill in between them | Needs a testing programme first |
| Automated open-source and vendor tools | Clean input tables | Whatever the tool assumes, plus an automated search over specifications | Produces many candidate models and invites choosing by eye. Easy to run and hard to audit |
| Multi-touch attribution, as an alternative | Individual paths of ad exposures and clicks | That credit can be shared among the touches before a purchase | Not causal at all. Credits touches that happened on the way to a purchase that was coming anyway. Blind to untracked channels |

The team's position on the three ways of measuring marketing is that they
answer different questions and are used together: experiments for the
effect of one channel or campaign, measured properly; a mix model for the
allocation across all channels, anchored to those experiments; and
attribution reports as a description of the paths customers took, not as
measurement.

## Reading a result you did not produce

Questions to ask of a mix model from an agency, a vendor, or a tool.

- **What question was it built to answer, and who chose the final model?**
  If the builder also buys the media, note it.
- **How many models were fitted before this one was chosen, and how?** Ask
  to see the range of each channel's return across the candidates that fit
  about as well. That range is the real uncertainty.
- **What variation lets the model tell each channel's effect apart?** Ask for each channel's spend
  over time on one chart. A channel that was flat, or that rose and fell
  with the season or with another channel, has no identifiable effect.
- **How was each channel's budget set during the period?** If spend followed
  the sales forecast, the model has the direction of cause partly backwards.
- **How are brand search, retargeting, and affiliates treated?** A large
  return on these is the expected result of the bias, not evidence of
  effectiveness.
- **What is in the base?** Ask how trend and season were modelled. A
  flexible base absorbs marketing's effect. A rigid one hands seasonal sales
  to whatever was advertised in season.
- **Are price, promotion, and distribution in the model?** Leaving them out
  credits marketing with their effect.
- **Do the returns come with intervals?** A table of returns to one decimal
  place and no intervals has left the uncertainty out.
- **Does it agree with any experiment?** For any channel that has been
  tested, compare. Disagreement on a tested channel lowers confidence in the
  untested ones.
- **Is the recommended allocation inside the range of spend that was
  observed?** A recommendation to triple a channel extrapolates the
  saturation curve beyond the data.
- **What happened when it was last refreshed?** Returns that changed sharply
  with three more months of data were never pinned down.
- **Did anyone act on the last one, and what happened?** A recommendation
  that was followed is a prediction that can be checked.

## Where it applies to our data

*Add: the mix models in use or commissioned in the business, who built each,
when, on what data, and who acts on it.* Why: the team will be asked to
interpret them.

*Add: the marketing channels, how each one's budget is set, and where spend
and exposure by week and region are recorded, linked to their pages under
Data.* Why: how budgets are set decides whether the model can be believed for
that channel.

*Add: the lift tests on record by channel, with their results.* Why: they
are the anchors.

*Add: the dates of events that moved sales for reasons other than
marketing.* Why: the model credits marketing with anything it is not told
about. The insights index under [Oversight](../oversight/index.md) is the
place for it.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Further reading

Chan, David, and Michael Perry. "Challenges and Opportunities in Media Mix
Modeling." Google, 2017. A short, candid account by practitioners of why
these models often fail to give valid answers: limited data, selection in how
spend was set, and modelling choices. Read this first.

Jin, Yuxue, Yueqing Wang, Yunting Sun, David Chan, and Jim Koehler. "Bayesian
Methods for Media Mix Modeling with Carryover and Shape Effects." Google,
2017. The standard statement of the Bayesian model with carryover and
saturation, including a simulation showing how strongly the priors drive the
result when data is short.

Hanssens, Dominique M., Leonard J. Parsons, and Randall L. Schultz. *Market
Response Models: Econometric and Time Series Analysis.* 2nd ed. Kluwer
Academic Publishers, 2001. The academic foundation: response functions,
carryover, and the econometrics of marketing time series.

Borden, Neil H. "The Concept of the Marketing Mix." *Journal of Advertising
Research* 4, no. 2 (1964): 2–7. Where the term comes from.

Lewis, Randall A., and Justin M. Rao. "The Unfavorable Economics of Measuring
the Returns to Advertising." *The Quarterly Journal of Economics* 130, no. 4
(2015): 1941–1973. Why advertising effects are hard to measure even with
experiments, which sets expectations for what a regression on weekly totals
can do.

Blake, Thomas, Chris Nosko, and Steven Tadelis. "Consumer Heterogeneity and
Paid Search Effectiveness: A Large-Scale Field Experiment." *Econometrica*
83, no. 1 (2015): 155–174. The study behind the caution on brand search.

Brodersen, Kay H., Fabian Gallusser, Jim Koehler, Nicolas Remy, and Steven L.
Scott. "Inferring Causal Impact Using Bayesian Structural Time-Series
Models." *The Annals of Applied Statistics* 9, no. 1 (2015): 247–274. A
method for measuring a single campaign or a regional test, the kind of
result a mix model should be checked against.
