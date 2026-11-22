---
title: Style guides
type: general
owner: mle-lead
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-02
review_cadence: 365d
tags: [style, python, sql, notebooks]
---

# Style guides

Guidelines on how code that is shared or runs in production is written.

!!! note "Style guide goals"

    The goal of style guides is to reduce conflict over personal style preferences
    and, more importantly, allow tools to take on the responsibility of reliably
    standardizing and maintaining code without human input.

## Rules of thumb

Style has two aspects. Formats are syntactic and easily enforced with tooling.
Approaches are philosophical and enforced through guidance and review.

Along these lines we use the following rules:

1. **One published guide per language per aspect.** If possible, a single
   popular tool or guide for syntactic formatting and one for philosophical
   approach. The guide is a community consensus, so it is already written, has
   already been argued over, and is likely familiar to new code reviewers.
2. **The tool's rules, rule.** In cases of disagreement between a syntactic tool
   and a philosophical approach, the tool's convention wins, so that the same
   rules can run on every machine and in CI with simple calls.
3. **This page holds only references and deviations.** Third party tool and
   philosophical approach documentation is the standard. Only deviations
   dictated by company or team workflow requirements are covered here.

## Language guides

| Language | Approach | Format | Deviations here |
|---|---|---|---|
| Python | [{{ platform.style.python.guide_name }}]({{ platform.style.python.guide_url }}) | {{ platform.style.python.tool_name }}, {{ platform.style.python.type_checker_name }} | Three |
| SQL | [{{ platform.style.sql.guide_name }}]({{ platform.style.sql.guide_url }}) | {{ platform.style.sql.tool_name }} | One |
| Notebooks | None | Nothing | None, by design |

## Python

The guide is the
[{{ platform.style.python.guide_name }}]({{ platform.style.python.guide_url }}).
[{{ platform.style.python.tool_name }}]({{ platform.style.python.tool_url }})
formats and lints every commit, and its configuration is the last word on
anything the two treat differently.

Team deviations and additions:

- **Every public function has a cogent docstring.** A linter can confirm it is
  there. A reviewer confirms it says what the function returns and what it
  assumes.
- **Type hints are required where types are static.** Library code and
  application infrastructure are fully annotated and must pass
  [{{ platform.style.python.type_checker_name }}]({{ platform.style.python.type_checker_url }}),
  chosen to align with `uv` and `ruff`. Modeling code, meaning a model
  project's own feature, training, and evaluation code, annotates function
  signatures, with a table annotated as its frame type and its columns left
  untyped, and is not gated on the checker. Notebooks are exempt. Test code is
  exempt, to avoid getting bogged down in scope issues and Python execution
  internals brought on by mocks and stubbing.
- **No logic lives only in a notebook.** Code that anything shared runs on, or
  that drives a repeatable external deliverable, is in the package, with a
  test. See [Path to production](path-to-production.md).

## SQL

For shared database objects, the team writes SQL as dbt models, and the guide is
dbt Labs' [{{ platform.style.sql.guide_name }}]({{ platform.style.sql.guide_url }}).
It governs how SQL text is written: case, indentation, line length, and how a
query is broken into named steps. The tool that enforces it is {{
platform.style.sql.tool_name }}.

Team deviations and additions:

- **Names and table shapes come from Conventions, not from the guide.** The
  guide's advice on naming is written for analytical data marts. The team's
  tables also feed a feature store, which asks more of a name and of a
  table's shape. Where the two differ, [Conventions](conventions.md) wins.

## Notebooks

No guide and no rules, by design. A notebook is where a data scientist works
in whatever way the work needs. Nothing shared and nothing in production
depends on a notebook, so nobody else has to read one as code, and no check
fails a notebook for its style.

Two rules touch notebooks, and neither is about style:

- Outputs are stripped before commit, because a displayed table is data. See
  [Development environments](environments.md).
- Code that anything shared depends on moves into the package, as under
  [Python](#python) above.

## Adding a language

When a project first needs another language, it gets a row in the table
above: one published guide, one tool that enforces it, both recorded in the
handbook's facts, and on this page only the team's deviations.
