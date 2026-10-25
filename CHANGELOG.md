# Changelog

Changes to the handbook specification and template. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
