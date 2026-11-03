# Changelog

Changes to the handbook specification and template. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
