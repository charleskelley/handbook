---
title: Development tools
type: general
owner: platform-owner
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-02
review_cadence: 180d
---

# Development tools

The tools the team develops with, and what each one is for.

*Add: editors, notebooks, version control, CI, and assistants, each with a link to
its setup how-to.*

## Data contracts

Data contracts are written in the
[{{ platform.contracts.standard_name }}]({{ platform.contracts.standard_url }})
and checked with
[{{ platform.contracts.tool_name }}]({{ platform.contracts.tool_url }}). The
tool validates a contract, tests a built object against it, compares two
versions of a contract, and builds a catalog from a project's contract
files. The rule for when a contract is needed is on
[Conventions](../methods/development/conventions.md#data-contracts).
