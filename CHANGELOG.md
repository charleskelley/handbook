# Changelog

Changes to the handbook specification and template. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- Path to production opens with the environments a change passes through:
  two as the rule, each described by who acts there, what data it sees, and
  what may run there; and a comparison of one, two, three, and four or more
  environments, with the rehearsal environment as the first one a team adds.
- Path to production names roles, not products: the artifact registry, CI,
  the model registry, the tracking server. The gates table, the release
  table, and the wide flow chart are replaced by two small diagrams: the
  two rules, and a swim lane of the eight steps from a branch to a promoted
  model, with each step and its reason listed beneath.
- Development environments names roles, not products, and places every way
  of working inside dev, the environment where people act under their own
  identity.
- The five decision records, all still proposed, name roles in place of
  products. MLflow and Evidently stay named, as the tools those records
  choose. DR-0001, DR-0003, and DR-0005 have new titles.

## [0.9.0] - 2026-11-22

### Changed

- The Data section follows the chain data moves along, with one `general`
  page for each stage: `sources/index.md`, `factory.md`, `store.md`,
  `training-data.md`, and `predictions.md`. System directories and
  `source-system` pages move under `docs/data/sources/`, and the validator
  looks for a system directory's index there.
- The factory, store, training data, and predictions pages stop at the
  concept. The detail lives in the factory's and the store's own
  documentation and in each model's repository, and each page ends with a
  note saying what that documentation must carry.
- `general` is a page type of the Data section.

### Added

- Conventions gains a data contracts part: every data object read outside
  the project that builds it has a contract file, in an open standard, kept
  beside the code and checked in CI. The standard and the checking tool are
  in a new `platform.contracts` block in `facts/platform.yaml`.
- Data pages, all conceptual: the section overview rewritten around the
  chain, and overview pages for Sources, Factory, Store, Training data, and
  Predictions.

## [0.8.0] - 2026-11-21

### Changed

- A `method` page has a depth, set in a new front matter field `depth`,
  required on `method` pages and allowed on no other. **build** is the full
  contract and requires **Building the outputs**, **Checks**, **Pitfalls**,
  and **Worked examples**. **guide** is orientation and requires **Common
  approaches**, **Reading a result you did not produce**, and **Further
  reading**. The validator enforces both.
- A `method` page tagged `causal` requires **Assumptions**, after **When it
  is not**. The validator enforces it.
- A `method` page may be about a recurring problem, such as churn
  prediction, as well as a technique.
- A principle several methods rest on is a `general` page in the group it
  serves.
- A citation is checked against the publisher's or a library's record
  before it is written.
- The two existing method pages gain `depth: build`. The customer-base audit
  page links forward to funnel analysis, survival analysis, and decomposing
  a change. The RFM page's one unverified citation is resolved.

### Added

- Analysis pages on understanding the business: survival analysis and
  decomposing a change (build), funnel analysis and segmentation (guide).
- Analysis pages on experiments and causal claims: directional versus causal
  and stating uncertainty (principles, `general` pages), experiments and
  lift tests and difference-in-differences (build), causal diagrams,
  measuring impact without an experiment, matching, synthetic control, and
  marketing mix modeling (guide).
- Modeling pages: framing and evaluating a prediction, linear and logistic
  regression, churn and propensity models, customer lifetime value, and
  time-series forecasting (build), gradient-boosted trees, uplift modeling,
  anomaly detection, and recommenders (guide).
- A Modeling group in the navigation, and on the Methods index a list of
  every page with its depth and two suggested paths through them.
- `scripts/method_diagrams.py`, which generates five small figures for the
  method pages, and its line in the `just diagram` recipe.

## [0.7.0] - 2026-11-21

### Changed

- The `method` page type is laid out in four parts that follow the reader's
  questions: Decide, Understand, Build, Here. The required sections are the
  same six in a new order: **When it is the right choice** and **When it is
  not** now follow **What it is**, and **Where it applies to our data**
  moves down beside **Lessons learned** and **Reference implementations**.
  The validator checks the new order.
- New optional `method` sections with fixed headings: **Building the
  outputs**, **Checks**, **Pitfalls**, and **Sources** as the last section.
  **Assumptions** is required on a page that makes a causal claim.
- Methods has three groups, Analysis, Modeling, and Development, shown in the
  navigation and on the Methods index. A method is filed by what it
  produces. Analysis and Modeling pages stay as files directly under
  `docs/methods/`.
- The two method pages are reordered to the new layout. No wording changed.

### Added

- The first method page, `docs/methods/customer-base-audit.md`: the
  customer-base audit framework, with a five-lens diagram generated by
  `scripts/customer_base_audit_diagram.py`.
- `docs/business/customer-base-audit.md`, a wireframe for the audit's
  findings. The Business layout says how a report page and its method page
  divide: framework under Methods, findings under Business.
- A method page for RFM analysis, `docs/methods/rfm-analysis.md`, with a
  recency-by-frequency grid generated by `scripts/rfm_diagram.py`.
- The customer-base audit method page gains what is needed to build the
  analysis from it: table contracts, a definition for every component of the
  decomposition, the form of each lens's outputs, checks, pitfalls, and a
  worked example on made-up figures.
- The RFM analysis method page gains the same: a table contract, a
  definition for each measure, defaults for its choices, the form of each
  output, checks, pitfalls, and a worked example on made-up figures.

## [0.6.0] - 2026-11-18

### Changed

- The Glossary and Apps sections become two pages in a new Reference section,
  `docs/reference/glossary.md` and `docs/reference/apps.md`. Reference has no
  index page. Links to the old paths are updated.
- Oversight comes before Team in the navigation and in the spec's section
  table, so the five sections that map to the landscape come first.
- The home page maps those five sections to the landscape in one table and
  lists Team and Reference separately as supporting sections.
- Section overview pages appear as the first link in the sidebar; the
  `navigation.indexes` theme feature is off.

## [0.5.0] - 2026-11-15

### Added

- Two strict page types for the Business section: `business-overview`, the
  company in the shape of an annual filing's Business section, which is the
  Business index; and `decision-inventory`, the decisions the business makes
  repeatedly, each a candidate outcome loop. Templates for both.
- Business layout: overview, decision inventory, three lens pages, and
  `docs/business/kpis/` whose index is the KPI driver tree. Fill order stated.
- Wireframes: a page may be published as headings plus `*Add:*` prompts and a
  "Gather first" admonition naming its sources. The validator fails an active
  page that still has a prompt.
- `facts/business.yaml`; KPI facts gain their place in the driver tree
  (parent, edge, guardrail_for, has_loop).
- Oversight section: monitoring policy and register, governance, and the
  decision log, as wireframes.

### Changed

- The Insights section becomes `docs/oversight/insights/`, inside the new
  Oversight section, so the handbook has one section for the landscape's
  Monitor & Govern band. The `insight` page type and `facts/insights.yaml` are
  unchanged; links to the old path are updated.

## [0.4.0] - 2026-11-13

### Added

- Images with alt text under `docs/assets/`, with `#only-light` and
  `#only-dark` variants for a diagram that has a version per theme.
- The Methods overview states how the team practises applied ML, structured
  by the DPOM landscape, and carries the landscape diagram.
- Page `status` shows in the navigation: a pencil beside drafts, the
  renderer's marker beside deprecated pages, nothing beside active ones, with
  a tooltip naming the status.

### Removed

- Snippets that quote files from `examples/`, and the `examples/` directory.
  Pages describe how a thing works and link to the repository that holds the
  code; they do not quote it. Snippets remain for `includes/` fragments.

## [0.3.1] - 2026-11-11

### Added

- Snippets may quote files, or named sections of files, from `examples/`, so
  pages that show example code include it rather than copy it.

## [0.3.0] - 2026-11-02

### Changed

- Page types pared from 23 to nine strict types plus `general`, which has no
  required sections. Pages that fit no strict type are `general` rather than
  requiring a spec change.
- Removed types: economics, strategy, feature, causal-map, convention, practice,
  setup-guide, worked-example, onboarding-path, access, how-we-work, landing,
  glossary, app-registry. Useful prompts moved to optional sections on kpi,
  method, and how-to pages.
- Page type `lesson` replaced by `insight`: an endogenous or exogenous event or
  circumstance that changes how data is interpreted.
- Source-system pages gain System of record for, and What's here on a system
  directory's index. Known quirks becomes optional Quirks, also allowed on
  data-domain and dataset pages.
- Data layout: a directory per system, with domains as subpages. Tables start on
  the domain page.
- Reference section removed. Methods holds development practices under
  `development/`. Technology holds development tools. How-tos sit with their subject.
- Three onboarding paths replaced by one onboarding guide. How-we-work is one
  untemplated page.
- `pyproject.toml` version synced with the spec.

### Added

- Insights section, with an index generated from `facts/insights.yaml`.
- `system_of_record` on datasets in `facts/data.yaml`.
- Explicit heading anchors in the allowed Markdown, for inline insights.
- Validator checks required headings on strict pages and templates, checks fact
  links, and warns when a page uses an `example` fact key.

### Fixed

- KPI macros use `kpis["items"]`. The documented `kpis.items` form failed to render
  and the build still reported no issues.
- Template titles are quoted. The decision-record title `DR-NNNN: ...` contains a
  colon and failed to parse as YAML when the template was copied unchanged.

## [0.2.0] - 2026-10-25

### Changed

- Section renamed Modeling to Methods (`docs/methods/`) to avoid confusion with
  data modeling in the Data section.
- Page type `model-family` renamed `method`, widened to any analysis method or
  model family; template renamed.
- Navigation order: Business, Data, Methods, Technology, Team, Reference,
  Glossary, Apps. The home page explains the reading order.

### Added

- Page type `worked-example`: one analysis or model in practice, end to end,
  with what was measured afterward.
- Worked-examples step in all three onboarding paths.
- `AGENTS.md`: which assistant tier for which page type, and the
  missing-facts test before trusting a tier.

## [0.1.1] - 2026-10-25

### Added

- Data section with three page types: source-system, data-domain, dataset.
- `facts/data.yaml` for dataset freshness, latency, retention, and ownership.
- Data step in all three onboarding paths.

## [0.1.0] - 2026-10-24

### Added

- Specification: eight sections, nineteen page types with required headings,
  front matter schema, allowed Markdown subset, facts-in-YAML rule, review and
  staleness rule.
- Agent contract (`AGENTS.md`).
- Zensical configuration with navigation tabs for every section and an
  alternate palette block.
- Section stubs, three onboarding paths, decision record template, glossary
  and app registry pages.
- Facts files: KPIs, platform, team, apps.
- Templates for every page type.
- Scripts: front matter validator, staleness report, notebook conversion.
- CI workflow: build, lint, validator, staleness report, link check.
