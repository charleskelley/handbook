---
title: "Decomposing a change"
type: method
depth: build
owner: ds-lead
audience: [ds, analyst, product]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [descriptive, kpis, variance-analysis]
sources:
  - "Kitagawa, Components of a Difference Between Two Rates, Journal of the American Statistical Association 50(272), 1955"
  - "Ang, The LMDI approach to decomposition analysis: a practical guide, Energy Policy 33(7), 2005"
---

# Decomposing a change

How to split the movement in a number between two periods into the parts that
add up to it. It is the first answer to "why did the number move", and the
most common request a new team receives from finance and operations.

## What it is

An accounting exercise. A headline number is a total over segments, or a rate
that is an average over segments, or a product of components. In each case
the change between two periods can be written as a sum of named effects that
add up to the change exactly: so much from each segment, so much from the mix
of segments and so much from the rates within them, so much from price and so
much from volume. The method is arithmetic and involves no model. It says
where the change is. It does not say what caused it, and that limit is the
main thing to keep in view when presenting it.

## When it is the right choice

- A KPI has moved and the first question is where: which segments, which
  component.
- A rate has moved and it is not clear whether behaviour changed or the mix of
  customers, products, or channels did.
- Finance asks for a bridge from last period's revenue or margin to this
  period's.
- Before any causal analysis, to find the part of the business the question
  is really about.

## When it is not

- **The question is what caused the change.** A decomposition shows that
  conversion fell in one channel. It cannot show that a campaign, a price, or
  a competitor did it. That needs a design:
  see [directional versus causal](directional-versus-causal.md).
- **The change is within the noise.** Splitting a movement that is no larger
  than the number's usual period-to-period variation gives confident-looking
  parts of nothing. Check the size of the change against history first: see
  [stating uncertainty](stating-uncertainty.md).
- **The definitions changed between the periods.** A new segment scheme, a
  restated metric, or a tracking change makes the two periods incomparable.
  Fix or restate before decomposing.

## The identity comes first

Every decomposition starts from a way of writing the number that is always
true. The identity decides which method applies.

| The number is | Identity | Method |
|---|---|---|
| A total over segments | Total = sum of the segments | [Contribution by segment](#a-total-contribution-by-segment) |
| A rate or an average | Rate = sum over segments of share × segment rate | [Rate and mix](#a-rate-rate-and-mix) |
| A product of components | Revenue = customers × orders per customer × spend per order | [Component effects](#a-product-component-effects) |
| Revenue or margin by product | Revenue = sum over products of quantity × price | [Price, volume, and mix](#revenue-price-volume-and-mix) |

The identities the business already uses are in its
[KPI driver tree](../business/kpis/index.md), and the customer-side identity
is the [profit decomposition](customer-base-audit.md#the-profit-decomposition)
on the customer-base audit page. Use those where they fit, so that the parts
have names people already know.

### A total: contribution by segment

The change in a total is the sum of the changes in its segments. Each
segment's contribution is its own change, and its share of the change is that
divided by the total change. A segment can contribute more than 100% when
others fell.

### A rate: rate and mix

A rate for the whole, such as conversion, margin, or average order value, is
a weighted average of the rates of its segments, weighted by each segment's
share of the denominator. It can move for two reasons: the rates within
segments changed, or the shares shifted between segments with different
rates. For each segment:

| Effect | Definition |
|---|---|
| Rate effect | Change in the segment's rate × the average of its share in the two periods |
| Mix effect | Change in the segment's share × (the average of its rate in the two periods − the average of the overall rate in the two periods) |

The rate effects and mix effects, summed over all segments, equal the change
in the overall rate exactly.

Two points about this form:

- **Averages of the two periods are used as weights.** The alternative
  weights by the first period only, and leaves a third term, the change in
  share × the change in rate, called the interaction. It is hard to explain
  and is often quietly added to one of the other two. The averaged form has
  no third term.
- **The mix effect is measured against the overall rate.** Taking the overall
  rate away does not change the total, because the changes in share add up to
  zero. It makes each segment's line readable: a segment that gained share
  and has a rate below the overall rate pulled the overall rate down.

A segment present in only one of the two periods has no rate in the other.
Report it as a line of its own, as for new and discontinued products below.

When the rates rise in every segment and the overall rate falls, or the
reverse, the mix effect has outweighed the rate effect. This is Simpson's
paradox, and it is common wherever a fast-growing segment has a rate unlike
the rest.

### A product: component effects

Where the number is a product of components, the fractional changes
multiply: a rise of 10% in customers, a fall of 5% in orders per customer,
and a rise of 4% in spend per order give 1.10 × 0.95 × 1.04 = 1.087, a rise
of 8.7%. There are two ways to turn that into an amount for each component.

- **By logarithms.** The logarithm of the ratio of the totals is the sum of
  the logarithms of the ratios of the components. Each component's share of
  the change is its logarithm ÷ the total logarithm, and its amount is that
  share × the change in the total. The result does not depend on any
  ordering. This is the default.
- **By swapping one at a time.** Change the first component from its old
  value to its new one and record the change in the total, then the second,
  and so on. The amounts add up, and they depend on the order chosen. Where
  this is used, state the order.

The logarithm method needs every component to be positive in both periods,
and the total to have changed: with no change in the total there is nothing
to share out.

### Revenue: price, volume, and mix

Finance reads a change in revenue or margin as three effects. There are
several conventions. This is the one used here unless a page says otherwise.

| Effect | Definition | Reads as |
|---|---|---|
| Volume | Change in total quantity × the average price in the first period | More or fewer units, at the old average price |
| Mix | (Sum over products of the second period's quantity × the first period's price) − (the second period's total quantity × the first period's average price) | Units shifting between dearer and cheaper products |
| Price | Sum over products of the second period's quantity × the change in price | The same units at new prices |

The three add up to the change in revenue. The average price is revenue ÷
total quantity. Because the price effect uses the second period's
quantities, this convention puts the part due to price and quantity changing
together into the price effect. A total quantity only means something where the products
share a unit. Where they do not, decompose within groups that do.

A product sold in only one of the two periods has no price in the other.
Report new and discontinued products as lines of their own, outside the three
effects.

### Which customers changed it

The same change can be split by customer and not by product: revenue from
customers who are new, less revenue lost with customers who left, plus the
change among those present in both periods. That decomposition is Lens 2 of
the [customer-base audit](customer-base-audit.md#lens-2-two-periods).

## Building the outputs

Built from a table with one row per segment and period.

Segment-period table

:   One row per segment and period. Columns: segment, period, and the
    additive quantities the number is built from. For a rate these are its
    numerator and its denominator, never the rate itself. For price, volume,
    and mix they are quantity and revenue. Every unit of the business falls
    in exactly one segment, with a named segment for the unclassified.

| Output | Rows | Columns | Shown as |
|---|---|---|---|
| Bridge | The starting value, each effect, the ending value | Amount, share of the change | Waterfall chart, with the table beneath |
| Segment detail | Segment | Value in each period, share in each period, rate effect, mix effect, total effect | Table, sorted by the size of the total effect |
| Component detail | Component | Value in each period, change in percent, amount attributed | Table |
| History of the number | Period | The number, for at least the last eight periods | Line, to show the change against its usual variation |

Defaults, where nothing about the business decides otherwise:

| Choice | Default | Why |
|---|---|---|
| Periods compared | The same period a year apart, both complete | Adjacent periods differ by season |
| Weights for rate and mix | The average of the two periods | No interaction term to explain |
| Method for a product | Logarithms | No ordering to defend |
| Number of segments shown | The largest effects by size, the rest as one line | A bridge with thirty bars is not read |
| Segmentation | The one the business already reports by | The parts need names people act on |

## Checks

Run these before reading any output. A failure is a fault in the table, not a
finding.

- The effects add up to the change in the number, to rounding.
- The segments' numerators and denominators add up to the reported totals in
  both periods.
- The shares add up to 100% in both periods.
- No unit is in two segments, and the unclassified segment is small and
  about the same size in both periods.
- The same definitions of the number and of the segments apply in both
  periods.
- The decomposition done on a second, different segmentation gives the same
  total. Where its story differs from the first, both are reported.

## Pitfalls

- **Reading an effect as a cause.** "Mix cost us a point of margin" describes
  the arithmetic. Why the mix shifted is a separate question, and the answer
  may be a decision the business made on purpose.
- **A rate averaged without weights.** The overall rate is not the plain
  average of the segment rates. Always carry numerators and denominators.
- **One segmentation.** The same change looks like mix under one cut and like
  rate under another. A finding that holds under only one cut is a property
  of the cut.
- **The interaction term.** With first-period weights, the term that is
  neither rate nor mix can be large when both moved. Do not fold it into one
  of them without saying so.
- **Percent and percentage points.** A rate that goes from 4.0% to 3.3% fell
  by 0.7 percentage points and by 18 percent. Say which.
- **Small segments with large swings.** A segment with few units can show a
  large change in rate from a handful of events. Its effect on the total is
  small, and its line should not lead the story.
- **Too fine a split.** Each further split looks more precise and has fewer
  units behind each part.
- **Logarithms where a component is zero or negative.** The method does not
  apply. Profit that changes sign cannot be decomposed this way.

## Worked examples

The figures here are made up to show the arithmetic. They are not this
business's data.

**A rate, and Simpson's paradox.** Conversion fell from 4.000% to 3.275%, a
fall of 0.725 points, while it rose in both channels.

| Channel | Visits, before | Orders, before | Rate, before | Visits, after | Orders, after | Rate, after |
|---|---|---|---|---|---|---|
| Paid | 1,000 | 20 | 2.00% | 3,000 | 66 | 2.20% |
| Organic | 1,000 | 60 | 6.00% | 1,000 | 65 | 6.50% |
| Total | 2,000 | 80 | 4.00% | 4,000 | 131 | 3.28% |

Paid's share of visits went from 50% to 75%. The average of the overall rate
in the two periods is 3.6375%.

| Channel | Rate effect | Mix effect | Total |
|---|---|---|---|
| Paid | 0.20 × 62.5% = +0.125 | +25% × (2.10 − 3.6375) = −0.384 | −0.259 |
| Organic | 0.50 × 37.5% = +0.188 | −25% × (6.25 − 3.6375) = −0.653 | −0.466 |
| Total | +0.313 | −1.038 | −0.725 |

In percentage points, to three places, with totals taken before rounding.
Both channels converted better, worth +0.31 points. The shift of visits toward paid, which converts at a third of
the rate of organic, cost 1.04 points. Whether that is bad news depends on
what the extra paid visits cost and whether the 51 extra orders were worth
it, which the decomposition does not say.

**A product.** Revenue rose from 100,000 to 108,680.

| Component | Before | After | Change | Logarithm of the ratio | Share | Amount |
|---|---|---|---|---|---|---|
| Customers | 1,000 | 1,100 | +10% | 0.0953 | 115% | +9,939 |
| Orders per customer | 2.0 | 1.9 | −5% | −0.0513 | −62% | −5,349 |
| Spend per order | 50 | 52 | +4% | 0.0392 | 47% | +4,090 |
| Revenue | 100,000 | 108,680 | +8.7% | 0.0832 | 100% | +8,680 |

The amounts add to 8,680. Swapping one at a time, customers
first, gives +10,000, −5,500, and +4,180, which also add to 8,680. Swapped in
another order the three amounts differ again, which is why the order is
stated when that method is used.

**Price, volume, and mix.** Revenue rose from 3,000 to 3,450.

| Product | Quantity, before | Price, before | Quantity, after | Price, after |
|---|---|---|---|---|
| A | 100 | 10 | 150 | 11 |
| B | 100 | 20 | 90 | 20 |

The average price before is 3,000 ÷ 200 = 15.

| Effect | Working | Amount |
|---|---|---|
| Volume | (240 − 200) × 15 | +600 |
| Mix | (150 × 10 + 90 × 20) − 240 × 15 | −300 |
| Price | 150 × (11 − 10) + 90 × (20 − 20) | +150 |
| Total | 3,450 − 3,000 | +450 |

More units were sold, they were more of the cheaper product, and that product
cost a little more.

## Where it applies to our data

*Add: the headline numbers the team is asked to explain most often, each with
its identity from the [KPI driver tree](../business/kpis/index.md).* Why: a
bridge built on the business's own identity uses names its readers already
know.

*Add: the segmentations the business reports by, and the dataset that carries
each, linked to its page under Data.* Why: a segment nobody owns is a segment
nobody acts on.

*Add: the convention finance uses for price, volume, and mix, if it differs
from the one on this page.* Why: two bridges for the same change that do not
agree destroy trust in both.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Sources

Kitagawa, Evelyn M. "Components of a Difference Between Two Rates." *Journal
of the American Statistical Association* 50, no. 272 (1955). The original
treatment of splitting a difference in rates into a rate part and a
composition part.

Ang, B. W. "The LMDI Approach to Decomposition Analysis: A Practical Guide."
*Energy Policy* 33, no. 7 (2005): 867–871. The logarithm method for a product
of components, from energy analysis, where it is standard. Short and
practical.

Simpson, E. H. "The Interpretation of Interaction in Contingency Tables."
*Journal of the Royal Statistical Society, Series B* 13, no. 2 (1951):
238–241. The paradox that bears his name.
