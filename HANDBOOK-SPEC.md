# Handbook specification

**Version 0.1.0 · Draft**

This document is the contract for everything under `docs/`. People and automated
assistants follow it when they add or change a page. If a page does not fit a
page type defined here, the spec is changed first and the page second.

## 1. Purpose

The handbook is the single reference for how a data science and machine
learning team works inside its company: how the business makes money and what
it measures, the technology the team runs on, the modeling knowledge it has
accumulated, the conventions it follows, and how the team itself operates. It
serves three audiences at once: a new hire in their first month, a current team
member looking something up, and a cross-functional partner trying to
understand what the team does and why.

It is a static website generated from Markdown held in a git repository.
Interactive material (dashboards, apps, notebooks) lives elsewhere and is
linked from here through the app registry.

## 2. Principles

1. **Markdown is the source.** Every page is a Markdown file. The renderer is a
   detail and can be replaced. No page may depend on syntax outside the allowed
   subset in section 6.
2. **A fact appears once.** Numbers, names, quotas, URLs, and anything else that
   changes live in `facts/*.yaml` and are rendered into pages with macros. Prose
   never carries a number that could go stale.
3. **Every page has an owner and a review date.** Front matter records who is
   accountable and when the page was last confirmed correct. Pages past their
   review cadence are reported by CI.
4. **Every page has a type.** The type fixes the required sections, so a reader
   knows what to expect and an assistant knows what to write.
5. **Unverified is labeled.** A claim that has not been confirmed against a
   source is marked as such in the text, never silently presented as fact.
6. **Small pages, strong links.** One topic per page. Prefer linking to an
   existing page over repeating its content.

## 3. Sections

| Section | Directory | What lives here | Page types |
|---|---|---|---|
| Home | `docs/index.md` | What the handbook is, how to use it, the onboarding paths | `landing` |
| Business | `docs/business/` | How the company and its products make money, the strategies that matter, the KPIs and what they mean | `economics`, `strategy`, `kpi` |
| Technology | `docs/technology/` | The platform, environments, local setup, access control | `platform`, `setup-guide`, `access` |
| Modeling | `docs/modeling/` | Model families in use and their lessons, the features the business relies on, causal maps, postmortems | `model-family`, `feature`, `causal-map`, `lesson` |
| Reference | `docs/reference/` | Code style and conventions, best practices, task recipes | `convention`, `practice`, `how-to` |
| Team | `docs/team/` | How the team works, onboarding reading paths, decision records | `how-we-work`, `onboarding-path`, `decision-record` |
| Glossary | `docs/glossary/` | Terms the team and its partners use, defined once | `glossary` |
| Apps | `docs/apps/` | Registry of companion applications, generated from `facts/apps.yaml` | `app-registry` |

Each section directory has an `index.md` of type `landing` that says what the
section holds and lists its pages.

## 4. Front matter

Every page begins with YAML front matter. The validator in
`scripts/validate_frontmatter.py` enforces this schema.

```yaml
---
title: Short page title            # required, string
type: kpi                          # required, one of the page types in section 5
owner: role-or-person              # required, who answers for this page
audience: [ds, mle]                # required, one or more of: ds, mle, de, analyst, product, leadership, all
status: active                     # required, one of: draft, active, deprecated
last_reviewed: 2026-01-15          # required, ISO date the content was last confirmed correct
review_cadence: 90d                # required, one of: 30d, 90d, 180d, 365d
tags: [retention, promo]           # optional, lowercase kebab-case strings
sources:                           # optional, where the facts on this page came from
  - "Finance monthly pack, Jan 2026"
---
```

Rules:

- `last_reviewed` is bumped only when a person has confirmed the page is
  correct, not when the file is edited for formatting.
- `status: deprecated` pages keep their content and gain an admonition at the
  top pointing to the replacement.
- `owner` is a role where possible (`ds-lead`, `platform-owner`) so pages
  survive staff changes.

## 5. Page types

Each type lists its purpose and its required sections, in order. Optional
sections are marked. Templates for each type are in `templates/`.

### landing
Purpose: orient the reader to a section. Required: one paragraph on what the
section holds; a list of pages with one line each. No facts, no numbers.

### economics (Business)
Purpose: explain how the company or a product makes money. Required:
**Revenue mechanics** (who pays, for what, when); **Cost structure** (the main
costs and which ones the team's work touches); **Unit economics** (the margin
logic in one paragraph, numbers from facts); **Where models act** (the
decisions in this flow that models or analytics influence); **Sources**.

### strategy (Business)
Purpose: record a corporate or product strategy the team must understand.
Required: **Objective**; **Horizon**; **What success looks like** (the KPIs,
linked); **How this team contributes**; **What it changes about our priorities**;
**Sources**. Optional: **Risks**.

### kpi (Business)
Purpose: define one business metric. One page per KPI. Required: **Definition**
(plain words); **Formula** (exact, with the source tables or systems);
**Current level** (rendered from `facts/kpis.yaml`, never typed); **Owner and
source of truth**; **What moves it**; **Common misreadings**; **Related KPIs**
(links). Optional: **History** (link to the dashboard in the app registry).

### platform (Technology)
Purpose: describe one platform component the team depends on. Required:
**What it is for**; **Architecture** (a Mermaid diagram or a linked one);
**How we use it**; **Limits and quotas** (from `facts/platform.yaml`); **Owner
and support path**; **Runbooks** (links). Optional: **Known issues**.

### setup-guide (Technology)
Purpose: get a machine or environment working. Required: **Prerequisites**;
**Steps** (numbered, each verifiable); **Verify** (how to know it worked);
**Troubleshooting**; **Verified on** (date and OS, from front matter and text).

### access (Technology)
Purpose: explain how to get access to a system or dataset. Required: **What
this grants**; **Who may have it**; **How to request** (exact steps or link);
**Approver**; **Review and revocation**.

### model-family (Modeling)
Purpose: record what the team knows about a class of model as used here.
Required: **Where we use it** (links to systems or decisions); **When it is the
right choice**; **When it is not**; **Lessons learned** (dated bullets, each
with a cause); **Reference implementations** (links). Optional: **Open
questions**.

### feature (Modeling)
Purpose: document a feature the business relies on. Required: **Business
meaning** (what it represents to a non-technical reader); **Definition and
source**; **Leakage and timing risks**; **Known failure modes**; **Models that
use it** (links).

### causal-map (Modeling)
Purpose: make the team's causal beliefs about an outcome explicit. Required:
**Outcome** (link to its KPI page); **Diagram** (Mermaid DAG); **Assumptions**
(each node and edge the team is least sure about); **Evidence** (what has been
tested, with links); **What we would need to believe to change this**.

### lesson (Modeling)
Purpose: a postmortem or lesson learned from a model, launch, or analysis.
Required: **What happened**; **Impact**; **Cause**; **What we changed**; **What
we would do differently**. Blameless by rule: no individual is named as a
cause.

### convention (Reference)
Purpose: a code style or repository convention. Required: **Rule**; **Why**;
**Example** (do and don't); **Enforcement** (linter, review, or honor system).

### practice (Reference)
Purpose: a best practice with judgment in it. Required: **When this applies**;
**The practice**; **Why**; **Anti-patterns**; **Examples** (links).

### how-to (Reference)
Purpose: a task recipe. Required: **Goal**; **Steps**; **Verify**; **See also**.

### how-we-work (Team)
Purpose: describe a ritual, role, or working agreement. Required: **What**;
**Who**; **When**; **Why**; **How to change this**.

### onboarding-path (Team)
Purpose: a curated reading order for one audience. Required: **Who this is
for**; **By end of week one**; **By end of month one**; **By end of quarter
one**; each a numbered list of links with one line on why. No new content; only
links.

### decision-record (Team)
Purpose: record a decision the team made and why. One file per decision, named
`DR-NNNN-short-slug.md`. Required: **Context**; **Decision**; **Alternatives
considered**; **Consequences**; **Status** (proposed, accepted, superseded by
DR-NNNN). Decision records are never edited after acceptance except to change
status.

### glossary
Purpose: define terms. A single page using definition lists, alphabetized. Each
term: one-sentence definition, optional link to the page that explains it.

### app-registry
Purpose: list every companion application. Generated from `facts/apps.yaml` by
a macro loop. Not hand-edited.

## 6. Allowed Markdown

Pages may use CommonMark plus the following, and nothing else:

- Tables, footnotes, definition lists, task lists.
- Admonitions (`!!! note`, `!!! warning`, `!!! tip`, `!!! danger`,
  `???` collapsible), used sparingly.
- Content tabs (`=== "Tab"`).
- Fenced code blocks with a language tag. Mermaid diagrams as `mermaid` fences.
- Snippets (`--8<-- "path"`) for shared fragments kept under `includes/`.
- Macros `{{ ... }}` and `{% ... %}` that reference variables loaded from
  `facts/*.yaml`. No arithmetic or logic beyond loops and attribute access.
- Raw HTML only for an `<iframe>` on an Apps page, and only through the
  `includes/embed.md` snippet.

Not allowed: inline HTML elsewhere, images without alt text, absolute links to
pages inside this site, emoji shortcodes in headings, any renderer-specific
syntax not listed above.

## 7. Facts

`facts/` holds YAML files whose top level is a single mapping key:

| File | Key | Holds |
|---|---|---|
| `facts/kpis.yaml` | `kpis` | `as_of` date and `items`, a mapping of KPI key to name, unit, current level, period, source of truth, owner |
| `facts/platform.yaml` | `platform` | Environments, quotas, limits, URLs for platform components |
| `facts/team.yaml` | `team` | Roles and who holds them, team channels, meeting cadence |
| `facts/apps.yaml` | `apps` | Companion application registry: key to name, url, owner, purpose, status, linked_from |

Reference a fact in a page as `{{ kpis.items.<key>.current }}` or
`{{ platform.<component>.<field> }}`. Update facts by editing the YAML and
bumping its `as_of`; the pages follow.

## 8. Review and staleness

CI runs `scripts/stale_report.py`, which lists every page whose
`last_reviewed` plus `review_cadence` is in the past, grouped by owner. The
report is informational on pull requests and should be worked down weekly. A
page that cannot be reviewed is set to `status: deprecated` rather than left
stale.

## 9. Changing this spec

Changes to page types, front matter, or allowed syntax are made here first,
with a version bump and a line in `CHANGELOG.md`, then applied to pages and
templates in the same change.
