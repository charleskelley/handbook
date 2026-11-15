---
title: Maintaining the KPI driver tree
type: general
owner: analytics-lead
audience: [ds, mle, analyst, leadership]
status: draft
last_reviewed: 2026-11-15
review_cadence: 180d
sources: []
---

# Maintaining the KPI driver tree

The [KPI index](../business/kpis/index.md) is drawn as driver trees rather
than listed by category. This page says why, states the rules the trees
follow, and gives the steps for adding, splitting, and retiring a node, so the
trees can be extended by anyone on the team and still mean the same thing.

## Why a tree and not a list

A category tells a reader what kind of metric something is. A tree tells them
how the metrics relate, which is the question the team asks: if we move this,
what moves. Behavioural metrics are rarely a category of their own in a tree.
They are the leaves under the financial ones, which is the point the Business
section makes about outcomes. The tree is also the link between the landscape
and the KPI pages: the root is an outcome the loop is entered at, and the
leaves are the levers a decision can move.

## Conventions

One root per headline outcome
:   Each tree has one root, the lagging outcome the business is judged on.
    Expect two or three small trees, not one large one. A root has three to
    five direct inputs.

Children are mutually exclusive and collectively exhaustive
:   At every level the children account for the parent completely and
    without overlap, so adding or multiplying them gives the parent back.

Arithmetic first, causal second
:   Decompose with sums, products, and ratios as far as the arithmetic holds.
    Below that, add causal links where a child is believed to move the parent
    but no formula connects them. Arithmetic edges are solid and labelled with
    the operator. Causal edges are dashed.

Three to five levels, and stop at a lever
:   Output metrics at the top, controllable input metrics at the leaves. A
    leaf is a number a named team can move by a decision this quarter. If no
    owner can act on a node, it is not a leaf yet.

Each metric appears once
:   If two branches share a driver, it is drawn once and referenced, or the
    tree stops summing.

Each node is a KPI page
:   The node carries only a name and a link. Unit, direction, owner, cadence,
    formula, and current level live on the KPI page and in `facts/kpis.yaml`.

Rates below the top, counts only where they add
:   A count of customers is a factor in revenue. A count of logins as a
    driver of retention is a vanity metric and does not go in the tree.

A guardrail beside every driver that will be optimised
:   Any driver a team will push gets a paired counter-metric that catches the
    damage, such as conversion paired with refund rate. Guardrails are drawn
    in grey beside the driver, outside the arithmetic.

Leaves lead, the root lags
:   A tree with only lagging metrics gives the team nothing to predict.

Mark where the team already is
:   A node whose decision is made by a model or a rule is marked as having a
    loop. A node with a counterfactual is one where the loop can be measured.
    These marks are what connect the tree to the
    [decision inventory](../business/decisions.md).

## Adding a node

1. Write the KPI page from the `kpi` template and add its entry to
   `facts/kpis.yaml`. A node without a page does not go in the tree.
2. Set `parent` to the key of the metric it feeds and `edge` to how it feeds
   it: sum, product, ratio, or causal. A root has no parent.
3. If it is a guardrail, set `guardrail_for` to the driver it protects, and
   leave `parent` empty.
4. Set `has_loop` if a model or rule makes the decision that moves it.
5. Add the node and its edge to the Mermaid tree on the KPI index, with a
   `click` line linking to the page. Check that the parent's children still
   account for it completely.
6. The analytics lead reviews the edge. A causal edge needs one sentence on
   the KPI page, under What moves it, saying why it is believed.

## Splitting or retiring a node

Split a node when its owner cannot move it but could move its parts; the
parts become its children and must account for it completely. Retire a node
when no decision moves it any more or its page is deprecated; remove its
edge, keep the page with `status: deprecated`, and check that the parent's
remaining children still sum. A node is never silently renamed. Rename the
page, keep the key in `facts/kpis.yaml`, and note the old name on the page.

## Review

The trees are reviewed with the Business overview, every 180 days, by the
analytics lead with the owners of the root outcomes. The review asks three
questions of each tree: does the arithmetic still hold, has any leaf stopped
being a lever, and is any driver being optimised without a guardrail. The
answers change the facts file first and the diagram second.
