---
title: "Recommenders"
type: method
depth: guide
owner: ds-lead
audience: [ds, mle, product]
status: draft
last_reviewed: 2026-11-21
review_cadence: 180d
tags: [predictive, personalization, modeling]
sources:
  - "Ricci, Rokach, and Shapira (eds.), Recommender Systems Handbook, 3rd ed., Springer, 2022"
  - "Koren, Bell, and Volinsky, Matrix Factorization Techniques for Recommender Systems, Computer 42(8), 2009"
---

# Recommenders

Systems that choose, for each customer, which few items to show out of many:
products on a home page, the next thing to buy in an email, articles,
offers. They are the centre of personalization, they will be asked for, and
the gap between a system that looks accurate and one that adds sales is
wider here than anywhere else on this site.

## What it is

A recommender takes a customer, and usually a context such as the page or
the basket, and returns a short ranked list of items. It learns from records
of what customers have looked at, bought, or rated, on the idea that
customers who behaved alike before will want similar things, and that items
chosen together are related. The methods range from "show the best sellers"
to large neural networks, and on the data most businesses have the simple
end of that range is hard to beat. A recommender is a prediction model with
three complications: it predicts for every pair of customer and item, almost
all of which have no data; it is judged on a ranked list, not on single
predictions; and what it shows changes what customers do, so its own output
becomes its next training data.

## When it is the right choice

- There are more items than a customer can browse, and customers differ in
  what they want.
- There is a surface to show recommendations on, and it gets enough traffic
  to test changes.
- Interactions are recorded per customer and per item, in volume: many
  customers with several interactions each.
- The business can say what it wants more of: discovery, basket size, repeat
  visits, margin.

## When it is not

- **A small catalogue.** With a few dozen items, merchandising by hand and a
  best-seller list do the job.
- **Customers who buy rarely.** With one or two purchases per customer there
  is little to personalise on. Item-to-item suggestions on the product page,
  which need no customer history, are the most that will work.
- **No way to test.** Without an [experiment](experiments-and-lift-tests.md)
  on the live surface, there is no way to know whether the recommender adds
  anything.
- **The goal is to pick who receives an offer.** That is a
  [propensity](churn-and-propensity.md) or [uplift](uplift-modeling.md)
  problem.
- **The items must be right, not merely likely.** Advice with consequences,
  such as financial or medical products, needs rules and review that a
  ranking model does not supply.

## The parts of the problem

| Part | What it is | The choices to make |
|---|---|---|
| Customers | Who is being recommended to | Signed-in customers, anonymous sessions, or both. What is known about a new one |
| Items | What can be recommended | The level: product, variant, category, brand. What is eligible: in stock, in the customer's market, not already owned |
| Interactions | The evidence | Explicit, such as ratings, which are rare. Or implicit, such as views, additions to basket, and purchases, which are plentiful and ambiguous: not buying is not disliking |
| Context | The situation | The page, the current basket, the device, the season |
| Candidate generation | Narrowing the catalogue to a few hundred plausible items | Usually a fast, simple method |
| Ranking | Ordering the candidates | A model using customer, item, and context features |
| Business rules | What is applied after the model | Stock, margin, exclusions, diversity, things the customer just bought |
| The objective | What the list is ranked for | Clicks, purchases, margin, long-run engagement. They disagree |

Large systems separate candidate generation from ranking. A first system can
be one step.

## Common approaches

| Approach | What it needs | What it rests on | Main weakness |
|---|---|---|---|
| Popularity | Sales or views by item, perhaps by segment or context | Most customers want what most customers want | Not personal. Reinforces what is already popular. Still the baseline everything must beat, and on sparse data hard to beat |
| Item-to-item co-occurrence | Baskets or sessions | Items chosen together are related | Dominated by popular items unless the count of each pair is divided by how often each item occurs on its own, as lift and cosine similarity do. Says "bought together", which may mean "already has it" |
| Neighbourhood collaborative filtering | A customer-by-item interaction table | Customers who agreed before will agree again | Sparse data gives unreliable neighbours. Nothing to offer for a new customer or item |
| Matrix factorization | The same table | Customers and items can each be described by a few hidden factors | The same cold-start problem. Implicit data needs a version built for it |
| Content-based | Descriptions or attributes of items | A customer wants more of what resembles what they chose | Narrow. Recommends the same kind of thing. Depends on the quality of item data |
| Ranking with features, such as [gradient-boosted trees](gradient-boosted-trees.md) | One row per customer and candidate item, with features of the customer, the item, and the pair. Items chosen are the positive rows, and a sample of items shown or available and not chosen are the negative ones | The features | Feature engineering, and care over leakage and time |
| Sequence and session models | Ordered events within a session | The next action depends on the recent ones | More data and engineering. Suited to anonymous browsing |
| Neural retrieval and ranking | Very large interaction data, and infrastructure | Learned representations of customers and items | Heavy. On ordinary data, often no better than well-tuned simple methods |
| Bandits | The ability to choose what to show and observe the response, live | Balancing showing what is known to work against trying what might | Needs live control of the surface. Slow with many items |

Build in this order: popularity by context, then item-to-item on product and
basket pages, then a factorization or feature-based ranker. Measure each
step in a live test before taking the next.

## Evaluating

**Offline,** on past data:

- Split by time. Train on interactions before a date and test on what each
  customer did after it. A random split leaks the future.
- Measure on the top of the list: precision and recall in the first *k*
  items, and measures that weight higher positions more, such as normalised
  discounted cumulative gain.
- Compare with popularity. Many published gains vanish against a properly
  tuned simple baseline.
- Look beyond accuracy: **coverage**, the share of the catalogue that is
  ever recommended; **diversity** within a list; **novelty**, how far the
  list departs from what is popular.

Offline evaluation rewards predicting what customers did under the old
system. It cannot credit a recommendation the customer would have loved and
was never shown. Offline and live results often disagree.

**Live,** with an experiment:

- Randomize customers between the new recommender and the current one, or
  none.
- The outcome is revenue or margin per customer over all their activity, not
  clicks on the recommendations. A recommendation can win the click and
  merely redirect a purchase the customer was about to make from another
  page.
- Include guardrails: returns, repeat visits, the breadth of what is sold.
- Run long enough for novelty to wear off.

Three groups of traffic serve three different purposes, and a mature system
has all of them: a control on the current system, to test a change; a
holdout shown no recommendations, to measure what recommending adds at all;
and a small share shown random or exploratory items, to collect data the
model did not shape.

## Known problems

- **Cold start.** A new customer or a new item has no interactions. Fall
  back on popularity for the first and on item attributes for the second,
  and plan how each gathers its first data.
- **Popularity bias.** Popular items have the most data and so are
  recommended more, which makes them more popular. The tail of the catalogue
  disappears unless deliberately kept.
- **The feedback loop.** Customers can only choose from what they are shown.
  A model trained on those choices learns its own past decisions. Keep a
  small share of traffic on random or exploratory recommendations, to supply
  data the model did not shape.
- **Position.** Items shown first are chosen more because they are first.
  Treating a click as pure preference rewards whatever was already at the
  top. The remedies are to randomize the order for a small share of traffic,
  or to give the model the position as an input in training and fix it when
  scoring.
- **Recommending the obvious.** The items a customer was certain to buy are
  the easiest to predict and the least useful to show. Accuracy rewards them.
- **What was just bought.** Recommending a second washing machine to
  someone who has just bought one is the classic failure. Handle it with
  rules.
- **Conflicting objectives.** The list that maximises clicks, the one that
  maximises margin, and the one that best serves the customer are different.
  Decide which, in writing.

## Reading a result you did not produce

Questions to ask of a recommender from a vendor, a platform feature, or
another team.

- **"Recommendations drive X% of revenue."** This is the share of sales in
  which a recommended item was clicked. It is attribution, not effect. Ask
  how much of it would have been bought anyway. Studies that have measured
  this find that a large share of clicks on recommendations would have
  happened without them. Only a holdout that gets no recommendations
  answers it.
- **Was it tested live, against what, on which outcome?** Against no
  recommendations, or against the previous system? On clicks, or on total
  margin per customer?
- **What is the offline baseline?** If the comparison is not with
  popularity and a simple item-to-item method, both tuned, the reported gain
  is not informative.
- **How was the offline split made?** By one date for everyone, with what
  each customer did after it as the test.
- **What share of customers and of items does it cover?** Ask what a new
  customer sees, and what share of the catalogue is ever shown.
- **What does it optimise?** Clicks, conversion, revenue, margin. Then ask
  whether that is what the business wants more of.
- **What rules are applied after the model?** Often the rules, not the
  model, decide most of what is shown.
- **How fresh is it?** How soon a new item can be recommended, and how soon
  a purchase stops the item being shown.
- **Is any traffic held out with no recommendations, and is any shown
  random ones?** Without the first there is no ongoing measurement, and
  without the second no clean data to retrain on.

## Where it applies to our data

*Add: the surfaces where recommendations are or could be shown, their
traffic, and who owns each.* Why: a recommender is only as useful as the
place it appears, and a test needs traffic.

*Add: the interaction data available, linked to its pages under Data: which
events are recorded, for signed-in and anonymous customers, and how far
back.* Why: the method that can work depends on how many interactions each
customer has.

*Add: the catalogue's size and how fast it turns over, and the quality of
item attributes.* Why: these decide how much cold start matters.

*Add: any recommender already in use, from a vendor or a platform, what it
optimises, and whether a holdout exists.* Why: the first job is usually to
measure what is there.

*Add: the objective the business has chosen for recommendations, and the
rules that must apply.* Why: without a stated objective the model optimises
whatever is easiest to measure.

## Lessons learned

None recorded yet.

## Reference implementations

None yet.

## Further reading

Ricci, Francesco, Lior Rokach, and Bracha Shapira, eds. *Recommender Systems
Handbook.* 3rd ed. Springer, 2022. The reference work, with a chapter for
each family of methods and for evaluation. Aggarwal, Charu C. *Recommender
Systems: The Textbook.* Springer, 2016, covers the same ground as a single
continuous text.

Linden, Greg, Brent Smith, and Jeremy York. "Amazon.com Recommendations:
Item-to-Item Collaborative Filtering." *IEEE Internet Computing* 7, no. 1
(2003): 76–80. Five pages on the simple method that ran one of the largest
recommenders for years. Start here.

Koren, Yehuda, Robert Bell, and Chris Volinsky. "Matrix Factorization
Techniques for Recommender Systems." *Computer* 42, no. 8 (2009): 30–37. A
readable account of factorization from the team that won the Netflix Prize.

Hu, Yifan, Yehuda Koren, and Chris Volinsky. "Collaborative Filtering for
Implicit Feedback Datasets." In *2008 Eighth IEEE International Conference on
Data Mining*, 263–272. IEEE, 2008. Factorization for views and purchases
where there are no ratings, which is the usual case.

Herlocker, Jonathan L., Joseph A. Konstan, Loren G. Terveen, and John T.
Riedl. "Evaluating Collaborative Filtering Recommender Systems." *ACM
Transactions on Information Systems* 22, no. 1 (2004): 5–53. What to measure,
including coverage, novelty, and the limits of accuracy.

Ferrari Dacrema, Maurizio, Paolo Cremonesi, and Dietmar Jannach. "Are We
Really Making Much Progress? A Worrying Analysis of Recent Neural
Recommendation Approaches." In *Proceedings of the 13th ACM Conference on
Recommender Systems*, 101–109. ACM, 2019. Published neural methods retested
against well-tuned simple baselines, which mostly held their own.

Sharma, Amit, Jake M. Hofman, and Duncan J. Watts. "Estimating the Causal
Impact of Recommendation Systems from Observational Data." In *Proceedings of
the Sixteenth ACM Conference on Economics and Computation*, 453–470. ACM,
2015. How much of the traffic credited to recommendations they actually
caused.

Gomez-Uribe, Carlos A., and Neil Hunt. "The Netflix Recommender System:
Algorithms, Business Value, and Innovation." *ACM Transactions on Management
Information Systems* 6, no. 4 (2015): 1–19. How a large recommender is run as
a business system, and why its builders rely on live tests over offline
measures.

Covington, Paul, Jay Adams, and Emre Sargin. "Deep Neural Networks for
YouTube Recommendations." In *Proceedings of the 10th ACM Conference on
Recommender Systems*, 191–198. ACM, 2016. The two-stage design of candidate
generation and ranking at very large scale.
