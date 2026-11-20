# Handbook specification

**Version 0.6.0 · Draft**

This document is the contract for everything under `docs/`. People and automated
assistants follow it when they add or change a page. A page that does not fit
a strict page type defined here is a `general` page.

## 1. Purpose

The handbook is the single reference for how a data science and machine
learning team works inside its company: how the business makes money and what
it measures, the technology the team runs on, the methods it uses and what it has learned
using them, the conventions it follows, and how the team itself operates. It
serves three audiences at once: a new hire in their first month, a current team
member looking something up, and a cross-functional partner trying to
understand what the team does and why.

It is a static website generated from Markdown held in a git repository.
Interactive material (dashboards, apps, notebooks) lives elsewhere and is
linked from here through the Apps page.

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
4. **Strict where it is a lookup, free where it is judgment.** Pages that repeat
   and get looked up have a strict type with required sections, so a reader
   knows what to expect and an assistant knows what to write. Everything else is
   a `general` page and evolves to fit the business.
5. **Unverified is labeled.** A claim that has not been confirmed against a
   source is marked as such in the text, never silently presented as fact.
6. **Small pages, strong links.** One topic per page. Prefer linking to an
   existing page over repeating its content.

## 3. Sections

| Section | Directory | What lives here | Page types |
|---|---|---|---|
| Home | `docs/index.md` | What the handbook is, how to use it, where each reader starts | `general` |
| Business | `docs/business/` | How the company and its products make money, the strategies that matter, the decisions the business makes, the KPIs and how they relate | `business-overview`, `decision-inventory`, `kpi`, `general` |
| Data | `docs/data/` | The systems data comes from, how it is organized into domains, what each table holds and how far it can be trusted | `source-system`, `data-domain`, `dataset` |
| Methods | `docs/methods/` | How the team works with data: analysis methods and model families at the top level, development practices under `development/` | `method`, `how-to`, `general` |
| Technology | `docs/technology/` | What the team works with: platforms, environments, development tools, setup and access recipes | `platform`, `how-to`, `general` |
| Oversight | `docs/oversight/` | The Monitor & Govern band: what is watched on every model and who acts, the governance rules, the decision log, and under `insights/` the index of every insight and the freestanding writeups | `insight`, `general` |
| Team | `docs/team/` | How the team works with partners, the onboarding guide, decision records | `decision-record`, `general` |
| Reference | `docs/reference/` | Lookup pages: `glossary.md`, the terms the team and its partners use, defined once, on one page; and `apps.md`, the registry of companion applications, generated from `facts/apps.yaml` | `general` |

Each section directory has an `index.md` of type `general` that says what the
section holds and lists its pages. Index pages carry no facts and no numbers.
Three exceptions: a system directory under Data, whose `index.md` is that
system's `source-system` page; the Business section, whose `index.md` is
the `business-overview` page; and Reference, which has no `index.md` because
its two pages are listed in the navigation and on the home page.

### Business layout

The Business index is the overview of the company. Beside it sit the decision
inventory, three lens pages (strategy, operating environment, competitive
position), and `docs/business/kpis/`, whose `index.md` is the KPI driver tree
and whose other pages are one `kpi` page per metric. A report that applies an
analysis method to the business, such as the customer-base audit, is a
`general` page here that links to its `method` page under Methods: the method
page holds the framework, the Business page holds the findings. Fill order:
overview, decision inventory, KPI tree and KPI pages, then the lens pages
last.

### Oversight layout

Oversight is the Monitor & Govern band. Its index says how the parts relate.
`monitoring.md` is policy and register: what must be watched on every model
in production, the thresholds, and who acts. `governance.md` is the rules:
approvals, model risk, access and privacy, and the business's risk appetite
applied. `decision-log.md` is the contract for recording business decisions
so they can be audited and replayed. `insights/` holds the generated index and
freestanding insight pages. The boundary with Methods: Oversight says what
must be true and who answers for it; Methods says how the team makes it true.
A page that needs both is two pages that link.

### Data layout

Each system with many tables gets a directory named for what people call it,
for example `docs/data/bigquery/`. Its `index.md` is the system's overview and
the map of everything below it. Subpages are domains, organized by business
concern, or dataset pages for single large tables that span domains. Special
sources that fit neither are carved out and noted in the `index.md`. A smaller
system is a single `source-system` page, `docs/data/<system>.md`.

A Data page says what a system holds and what it means. A platform page says how
the system runs and what its quotas are. A system can have both.

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
- `status` also shows in the navigation: a pencil beside a draft page, the
  renderer's own marker beside a deprecated one, nothing beside an active one.
  Hovering the marker names the status. A page loses its pencil only when an
  owner reviews it and sets `status: active`.
- `owner` is a role where possible (`ds-lead`, `platform-owner`) so pages
  survive staff changes.
- Quote `title` when it contains a colon (every decision record does), or YAML
  rejects it. The templates quote every title.

## 5. Page types

There are eleven strict types, each with a template in `templates/`, and one
free type. Each strict type lists its purpose and its required sections, in order.
The validator enforces the required sections. Optional sections are named here
and may be added after the required ones.

Two optional sections apply to pages about data:

- **Quirks** record structural, timeless properties of a system or table:
  timezones, soft deletes, re-statements, or a dropdown that defaults to one
  value. Allowed on `source-system`, `data-domain`, and `dataset` pages.
- **Insights** record events or circumstances that change how data is read. See
  [insight](#insight-insights). Allowed on any strict page.

The test between them: if interpretation differs before and after a date, it is
an insight. If it has always been true, it is a quirk.

### general
Purpose: anything that does not repeat often enough to need a shape, including
section indexes, the glossary, the Apps page, how-we-work, and business pages
such as how a product makes money. Front matter only, no required sections.
Organic pages may become a strict type later if a pattern emerges.

### business-overview (Business)
Purpose: the company as a new reader needs it, in the shape of the Business
section of an annual filing. One page per handbook, the Business index.
Required: **What the company does** (one paragraph a new hire repeats
correctly); **Products and segments** (what is sold, to whom, grouped the way
finance reports it); **How money is made** (per segment: who pays, for what,
when, and the pricing basis); **Customers and markets**; **Operations** (how
the product is delivered and the few processes that matter); **Regulation and
risk** (the risk factors that touch data or models, with links to Team and
Methods); **Seasonality and cycles**; **Organization** (how the business is
organized and where the data science team sits); **What this means for the
team** (the outcomes the loop is entered at). Optional: **Insights**. Segment
names and revenue mix come from `facts/business.yaml`.

### decision-inventory (Business)
Purpose: the decisions the business makes repeatedly, each a candidate outcome
loop. One page per handbook. Required: **How to read this page**;
**Decisions** (a table with the columns decision, who decides, cadence,
inputs, outcome moved, mechanism, loop, KPI; mechanism is one of judgment,
rule, or model; loop is open or closed); **Candidates for an outcome loop**
(the open rows worth closing first, and why); **How a row changes** (who adds
a row, who reviews it, and when a decision record is needed). Optional:
**Insights**.

### kpi (Business)
Purpose: define one business metric. One page per KPI. Required: **Definition**
(plain words); **Formula** (exact, with the source tables or systems);
**Current level** (rendered from `facts/kpis.yaml`, never typed); **Owner and
source of truth**; **What moves it**; **Common misreadings**; **Related KPIs**
(links). Optional: **Causal diagram** (Mermaid DAG); **What we would need to
believe to change this**; **History** (link to the dashboard on the Apps page);
**Insights**.

### source-system (Data)
Purpose: describe one system data comes from. Every system in the chain gets a
page, including the warehouse and the systems that feed it. Required: **What it
is** (the business process it runs); **System of record for** (the kinds of data
this system is authoritative for, and where analysts actually pull each one if
elsewhere); **What it emits** (events or tables, with grain and keys); **How it
lands** (pipeline, cadence, latency, from `facts/data.yaml`); **Owner and
contact**. Required on a system directory's `index.md`: **What's here** (the map
of domains, single tables, and carveouts). Optional: **Quirks**; **Insights**.

System of record is a relationship between a system and a kind of data, not a
kind of system. A warehouse may be the system of record for marketing data while
a document store is the system of record for web data that analysts pull from
the warehouse.

### data-domain (Data)
Purpose: explain one business domain within a system. Required: **Scope** (the
business area covered); **Model** (a Mermaid entity diagram or a linked one, with
the grain of each core table and the domain's semantic model); **Canonical
tables** (the tables, described on this page); **How to join** (the keys that
work and the ones that do not); **Conventions** (naming, partitioning, history
handling); **Owner**. Optional: **Quirks**; **Insights**.

Tables start on the domain page. A table gets its own `dataset` page when it
outgrows the domain page.

### dataset (Data)
Purpose: document one table or dataset that outgrew its domain page, or a large
table that spans domains. Required: **What it holds** (one paragraph, plus grain
and primary key); **Where it comes from** (the system it is pulled from, its
system of record, and the pipeline); **Freshness and retention** (from
`facts/data.yaml`, never typed); **Columns that matter** (the handful a reader
needs, with business meaning); **Quality checks** (what is tested and what is
not); **Known issues** (current defects); **Used by** (links to KPI and method
pages). Optional: **Access** (link to the how-to); **Quirks**; **Insights**.

### method (Methods)
Purpose: one page per algorithm or analysis method as used here, from gradient
boosting to uplift modeling to a difference-in-differences design. Required:
**What it is** (one paragraph for a technical reader); **Where it applies to our
data** (the business questions and datasets it suits, linked); **When it is the
right choice**; **When it is not**; **Lessons learned** (dated bullets, each with
a cause); **Reference implementations** (links). Optional: **Causal diagram**;
**Worked examples**; **What was measured afterward** (the outcome against its
counterfactual, or an honest note that it was not measured); **Open questions**;
**Insights**.

### platform (Technology)
Purpose: describe one platform component the team depends on. Required:
**What it is for**; **Architecture** (a Mermaid diagram or a linked one);
**How we use it**; **Limits and quotas** (from `facts/platform.yaml`); **Owner
and support path**; **Runbooks** (links). Optional: **Known issues**;
**Insights**.

### how-to (Methods, Technology)
Purpose: a task recipe, kept beside its subject. Tool setup and access requests
sit under Technology. Tasks such as shipping a model sit under Methods. Required:
**Goal**; **Steps** (numbered, each verifiable); **Verify**; **See also**.
Optional: **Troubleshooting**; **Verified on** (date and OS, for setup recipes);
**Insights**.

### decision-record (Team)
Purpose: record a decision the team made and why. One file per decision, named
`DR-NNNN-short-slug.md`. Required: **Context**; **Decision**; **Alternatives
considered**; **Consequences**; **Status** (proposed, accepted, superseded by
DR-NNNN). Decision records are never edited after acceptance except to change
status. A decision record says why a change was made. An insight says what the
change did to the data.

### insight (Oversight)
Purpose: a freestanding writeup of an endogenous or exogenous event or
circumstance that changes how data is interpreted, such as a record system
change or a market shock. Required: **What is true**; **When it applied**; **How
we know**; **What it affects** (links); **Does it still hold**. Blameless by
rule: no individual is named as a cause.

Small insights are inline and use the format in section 6. A large insight gets
this page, and each affected page carries an inline note linking to it. Every
insight, inline or freestanding, has an entry in `facts/insights.yaml`, and
`docs/oversight/insights/index.md` is generated from that file.

## 6. Allowed Markdown

Pages may use CommonMark plus the following, and nothing else:

- Tables, footnotes, definition lists, task lists.
- Admonitions (`!!! note`, `!!! warning`, `!!! tip`, `!!! danger`,
  `???` collapsible), used sparingly.
- Content tabs (`=== "Tab"`).
- Fenced code blocks with a language tag. Mermaid diagrams as `mermaid` fences.
- Snippets (`--8<-- "path"`) for shared fragments kept under `includes/`.
- Images (`![alt](../assets/name.svg)`) with alt text, kept under
  `docs/assets/`. A diagram with a light and a dark version uses two files,
  marked `#only-light` and `#only-dark` after the path, so each theme shows
  its own.
- Macros `{{ ... }}` and `{% ... %}` that reference variables loaded from
  `facts/*.yaml`. No arithmetic or logic beyond loops and attribute access.
- Explicit heading anchors (`{: #slug }`), used to give inline insights a stable
  link target. The colon is required, because `{#` opens a macro comment.
- Raw HTML only for an `<iframe>` on an Apps page, and only through the
  `includes/embed.md` snippet.

An inline insight is an H3 under an `## Insights` heading, with an anchor,
followed by its date, what happened, the effect on the data, and a link to the
full writeup if there is one:

```markdown
## Insights

### Short title {: #short-slug }

YYYY-MM-DD to YYYY-MM-DD. What happened, and how it changes reading the data.
[Full writeup](../oversight/insights/short-slug.md).
```

Not allowed: inline HTML elsewhere, images without alt text, absolute links to
pages inside this site, emoji shortcodes in headings, any renderer-specific
syntax not listed above.

### Wireframes

A page may be published before it is written, as a wireframe: the headings in
place and a prompt under each one saying what goes there and why. A wireframe
is `status: draft`, so it carries the pencil in the navigation, and it is
filled in place by a person or an assistant working from the sources it names.
Three conventions make that fill reliable:

- A `!!! note "Gather first"` admonition at the top lists the source documents
  the page expects, so the fill starts from sources rather than from memory.
- Each prompt has the form `*Add: what goes here.* Why: why it matters.`, the
  same form the onboarding page uses. A prompt may also say what to leave as
  `*[unverified: needs source]*` when the sources are silent.
- A page cannot be `status: active` while any `*Add:` prompt remains. The
  validator enforces this. Removing the last prompt is not a review; the owner
  still confirms the content and bumps `last_reviewed`.

## 7. Facts

`facts/` holds YAML files whose top level is a single mapping key:

| File | Key | Holds |
|---|---|---|
| `facts/business.yaml` | `business` | `as_of`, `segments` (key to name, what it sells, revenue share), `priorities` (the stated priorities for the current period, each with an owner), `competitors` (key to name and where they compete) |
| `facts/kpis.yaml` | `kpis` | `as_of` date and `items`, a mapping of KPI key to name, unit, current level, period, source of truth, owner, and its place in the driver tree: parent, edge (sum, product, ratio, causal), guardrail_for, has_loop |
| `facts/data.yaml` | `data` | `as_of` and `datasets`, a mapping of dataset key to name, location, grain, freshness, latency, retention, owner, source system (where it is pulled from), system of record |
| `facts/platform.yaml` | `platform` | Environments, quotas, limits, URLs for platform components |
| `facts/team.yaml` | `team` | Roles and who holds them, team channels, meeting cadence |
| `facts/apps.yaml` | `apps` | Companion application registry: key to name, url, owner, purpose, status, linked_from |
| `facts/insights.yaml` | `insights` | `as_of` and `categories`, a mapping of category to name and `items`. Each item has title, kind (endogenous or exogenous), start, optional end, and link (a path under `docs/`, with an anchor for inline insights) |

Mappings named `items` need the bracket form, `kpis["items"]`, because
`kpis.items` resolves to a built-in method.

Entries whose key starts with `example` are placeholders. They are exempt from
the link checks, and a warning is printed if a page under `docs/` uses one.

Reference a fact in a page as `{{ kpis["items"].<key>.current }}` or
`{{ platform.<component>.<field> }}` or `{{ data.datasets.<key>.freshness }}`. Update facts by editing the YAML and
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
