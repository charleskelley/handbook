# Changelog

Changes to the handbook specification and template. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
